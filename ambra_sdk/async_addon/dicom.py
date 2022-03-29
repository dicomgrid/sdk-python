"""Dicom addon namespace."""
import os
from enum import Enum, auto
from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO, Dict, NamedTuple, Optional, cast

import pydicom
from pydicom.dataset import FileDataset


class UploadedImageParams(NamedTuple):
    """Image object."""

    study_uid: str
    image_uid: str
    image_version: str
    namespace: str
    attr: Any


class DicomUploadType(Enum):
    """Image upload methods."""

    Auto = auto()  # Auto select of the best algorithm for upload
    DefaultUpload = auto()  # Upload using one call of upload endpoint, best for small files
    MultipartUpload = auto()  # Upload of objects in parts, best for large files


class Dicom:
    """Dicom addon namespace."""

    DICOM_UPLOAD_TYPE = DicomUploadType.Auto
    CHUNK_SIZE = 2 * 1024 * 1024  # 2 Mb chunks
    UPLOAD_RETRY_DELAY = 5000  # if chunk upload fails, wait 5s before trying again
    CHUNK_UPLOAD_THRESHOLD = 10 * CHUNK_SIZE  # file must be at least this size to use multipart
    COMPRESSION_THRESHOLD = 25 * 1024  # 25 Kb
    RETRY_LIMIT = 120

    def __init__(self, api):
        """Init.

        :param api: base api
        """
        self._api = api

    async def get(
        self,
        *,
        namespace_id: str,
        study_uid: str,
        image_uid: str,
        image_version: str = '*',
        engine_fqdn: Optional[str] = None,
        pretranscode: Optional[bool] = None,
    ) -> FileDataset:
        """Get dicom.

        :param namespace_id: uploading to namespace
        :param study_uid: study_uid
        :param image_uid: image_uid
        :param image_version: image_version

        :param engine_fqdn: fqdn (if None gets namespace fqdn)
        :param pretranscode: get pretranscoded

        :return: pydicom object
        """
        if engine_fqdn is None:
            engine_fqdn = await self._namespace_fqdn(namespace_id)

        dicom_payload_resp = await self._api. \
            Storage. \
            Image. \
            dicom_payload(
                engine_fqdn=engine_fqdn,
                namespace=namespace_id,
                study_uid=study_uid,
                image_uid=image_uid,
                image_version=image_version,
                pretranscode=pretranscode,
            )
        return pydicom.read_file(
            fp=BytesIO(await dicom_payload_resp.content.read()),
            force=True,
        )

    async def upload(
        self,
        *,
        dicom_file: BinaryIO,
        namespace_id: str,
        engine_fqdn: Optional[str] = None,
        study_uid: Optional[str] = None,
    ) -> UploadedImageParams:
        """Upload dicom file to namespace.

        :param dicom_file: dicom file
        :param namespace_id: uploading to namespace
        :param engine_fqdn: fqdn (if None gets namespace fqdn)
        :param study_uid: UID of the study (if None taken from file)

        :raises ValueError: Unknown DICOM_UPLOAD_TYPE

        :return: uploaded image params. Note: if image is larger than 20 Mb, multipart upload used. Multipart upload
            is asynchronous, image params are not available after upload. You can disable this behaviour
            by DICOM_UPLOAD_TYPE setting in the Dicom module.
        """
        if engine_fqdn is None:
            engine_fqdn = await self._namespace_fqdn(namespace_id)

        if not study_uid:
            ds = pydicom.dcmread(fp=dicom_file, stop_before_pixels=True)
            study_uid = cast(str, ds.StudyInstanceUID)
        upload_type = self.DICOM_UPLOAD_TYPE
        if upload_type == DicomUploadType.Auto:
            dicom_file.seek(0, os.SEEK_END)
            file_size = dicom_file.tell()
            dicom_file.seek(0)
            if file_size > self.CHUNK_UPLOAD_THRESHOLD:
                upload_type = DicomUploadType.MultipartUpload
            else:
                upload_type = DicomUploadType.DefaultUpload

        if upload_type == DicomUploadType.DefaultUpload:
            return await self._default_upload(
                dicom_file=dicom_file,
                namespace_id=namespace_id,
                engine_fqdn=engine_fqdn,
                study_uid=study_uid,
            )
        elif upload_type == DicomUploadType.MultipartUpload:
            return await self._multipart_upload(
                dicom_file=dicom_file,
                namespace_id=namespace_id,
                engine_fqdn=engine_fqdn,
                study_uid=study_uid,
            )

        raise ValueError(f'Unknown upload type {upload_type}')

    async def upload_from_path(
        self,
        *,
        dicom_path: Path,
        namespace_id: str,
        engine_fqdn: Optional[str] = None,
        study_uid: Optional[str] = None,
    ) -> UploadedImageParams:
        """Upload dicom to namespace from path.

        :param dicom_path: path to dicom
        :param namespace_id: uploading to namespace
        :param engine_fqdn: fqdn (if None gets namespace fqdn)
        :param study_uid: UID of the study (if None taken from file)

        :return: uploaded image params
        """
        with open(dicom_path, 'rb') as dicom_file:
            return await self.upload(
                dicom_file=dicom_file,
                namespace_id=namespace_id,
                engine_fqdn=engine_fqdn,
                study_uid=study_uid,
            )

    async def _multipart_upload(
        self,
        *,
        dicom_file: BinaryIO,
        namespace_id: str,
        engine_fqdn: str,
        study_uid: str,
    ) -> UploadedImageParams:
        initiate_response = await self._api.Storage.Image.multipart_initiate(engine_fqdn)
        upload_uuid = initiate_response['upload_uuid']
        chunk_number = 0
        file_size = 0
        while True:
            part = dicom_file.read(self.CHUNK_SIZE)
            if not part:
                break
            file_size += len(part)
            await self._api.Storage.Image.multipart_chunk_upload(
                engine_fqdn=engine_fqdn,
                upload_uuid=upload_uuid,
                bytes_part=part,
                chunk_number=chunk_number,
            )
            chunk_number += 1
        dicom_file.seek(0)
        await self._api.Storage.Image.multipart_complete(
            engine_fqdn=engine_fqdn,
            namespace=namespace_id,
            upload_uuid=upload_uuid,
            study_uid=study_uid,
            file_size=file_size,
        )
        return UploadedImageParams(
            study_uid=study_uid,
            image_uid='',
            image_version='',
            namespace=namespace_id,
            attr=None,
        )

    async def _default_upload(
        self,
        dicom_file: BinaryIO,
        namespace_id: str,
        engine_fqdn: str,
        study_uid: str,
    ) -> UploadedImageParams:
        response = await self._api.Storage.Image.upload(
            engine_fqdn=engine_fqdn,
            namespace=namespace_id,
            opened_file=dicom_file,
            study_uid=study_uid,
        )
        return UploadedImageParams(
            study_uid=response.study_uid,
            image_uid=response.image_uid,
            image_version=response.image_version,
            namespace=response.namespace,
            attr=response.attr,
        )

    async def _namespace_fqdn(self, namespace_id: str) -> str:
        """Get cached fqdn for namespace.

        :param namespace_id: namespace id
        :return: fqdn
        """
        if not getattr(self, '_cached_fqdns', None):
            self._cached_fqdns: Dict[str, str] = {}
        engine_fqdn = self._cached_fqdns.get(namespace_id)
        if engine_fqdn is None:
            engine_fqdn_obj = await self._api \
                .Namespace \
                .engine_fqdn(namespace_id=namespace_id) \
                .get()
            engine_fqdn = engine_fqdn_obj.engine_fqdn
            self._cached_fqdns[namespace_id] = engine_fqdn
        return engine_fqdn

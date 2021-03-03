"""Dicom addon namespace."""

from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO, Dict, NamedTuple, Optional

import pydicom
from pydicom.dataset import FileDataset


class UploadedImageParams(NamedTuple):
    """Image object."""

    study_uid: str
    image_uid: str
    image_version: str
    namespace: str
    attr: Any


class Dicom:
    """Dicom addon namespace."""

    def __init__(self, api):
        """Init.

        :param api: base api
        """
        self._api = api

    def get(
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
            engine_fqdn = self._namespace_fqdn(namespace_id)

        dicom_payload_resp = self._api. \
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
            fp=BytesIO(dicom_payload_resp.content),
            force=True,
        )

    def upload(
        self,
        *,
        dicom_file: BinaryIO,
        namespace_id: str,
        engine_fqdn: Optional[str] = None,
    ) -> UploadedImageParams:
        """Upload dicom file to namespace.

        :param dicom_file: dicom file
        :param namespace_id: uploading to namespace
        :param engine_fqdn: fqdn (if None gets namespace fqdn)

        :return: uploaded image params
        """
        if engine_fqdn is None:
            engine_fqdn = self._namespace_fqdn(namespace_id)

        response = self._api.Storage.Image.upload(
            engine_fqdn=engine_fqdn,
            namespace=namespace_id,
            opened_file=dicom_file,
        )
        return UploadedImageParams(
            study_uid=response.study_uid,
            image_uid=response.image_uid,
            image_version=response.image_version,
            namespace=response.namespace,
            attr=response.attr,
        )

    def upload_from_path(
        self,
        *,
        dicom_path: Path,
        namespace_id: str,
        engine_fqdn: Optional[str] = None,
    ) -> UploadedImageParams:
        """Upload dicom to namespace from path.

        :param dicom_path: path to dicom
        :param namespace_id: uploading to namespace
        :param engine_fqdn: fqdn (if None gets namespace fqdn)

        :return: uploaded image params
        """
        with open(dicom_path, 'rb') as dicom_file:
            return self.upload(
                dicom_file=dicom_file,
                namespace_id=namespace_id,
                engine_fqdn=engine_fqdn,
            )

    def _namespace_fqdn(self, namespace_id: str) -> str:
        """Get cached fqdn for namespace.

        :param namespace_id: namespace id
        :return: fqdn
        """
        if not getattr(self, '_cached_fqdns', None):
            self._cached_fqdns: Dict[str, str] = {}
        engine_fqdn = self._cached_fqdns.get(namespace_id)
        if engine_fqdn is None:
            engine_fqdn = self._api \
                .Namespace \
                .engine_fqdn(namespace_id=namespace_id) \
                .get() \
                .engine_fqdn
            self._cached_fqdns[namespace_id] = engine_fqdn
        return engine_fqdn

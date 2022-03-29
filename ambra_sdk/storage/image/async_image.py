"""Async storage image namespace."""

from typing import Optional, Union

from aiohttp import ClientResponse
from box import Box

from ambra_sdk.storage.image.base_image import BaseImage
from ambra_sdk.storage.request import PreparedRequest
from ambra_sdk.types import RequestsFileType


class AsyncImage(BaseImage):
    """Asyn storage Image commands."""

    async def upload(
        self,
        engine_fqdn: str,
        namespace: str,
        opened_file: RequestsFileType,
        study_uid: Optional[str] = None,
        use_box: bool = True,
        x_ambrahealth_job_id: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Box, ClientResponse, PreparedRequest]:
        """Upload image to a namespace.

        URL: /namespace/{namespace}/image?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param opened_file: Opened file (like in requests) (Required).
            File object, or may be 2-tuples (filename, fileobj),
            3-tuples (filename, fileobj, contentype) or
            4-tuples (filename, fileobj, contentype, custom_headers).
        :param study_uid: study uid
        :param use_box: Use box for response.
        :param x_ambrahealth_job_id: X-AmbraHealth-Job-Id headers argument
        :param only_prepare: Get prepared request.

        :returns: image object attributes
        """
        prepared_request = self._upload(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            opened_file=opened_file,
            study_uid=study_uid,
            x_ambrahealth_job_id=x_ambrahealth_job_id,
        )
        if only_prepare is True:
            return prepared_request
        response = await prepared_request.async_execute()
        if use_box is True:
            return Box(await response.json())
        return response

    async def wrap(
        self,
        engine_fqdn: str,
        namespace: str,
        opened_file: RequestsFileType,
        tags: Optional[str] = None,
        render_wrapped_pdf: Optional[bool] = None,
        x_ambrahealth_job_id: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[ClientResponse, PreparedRequest]:
        """Upload a non DICOM image.

        URL: /namespace/{namespace}/wrap?sid={sid}&render_wrapped_pdf={0,1}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param tags: Any DICOM tags to be overwrite or added should be provided as a form-data field.
        :param opened_file: The multipart file to be uploaded should be
            provided as a form-data field.
            File object, or may be 2-tuples (filename, fileobj),
            3-tuples (filename, fileobj, contentype) or
            4-tuples (filename, fileobj, contentype, custom_headers).

        :param render_wrapped_pdf: An integer value of either 0 or 1.
        :param x_ambrahealth_job_id: X-AmbraHealth-Job-Id headers argument
        :param only_prepare: Get prepared request.

        :returns: image object attributes
        """
        prepared_request = self._wrap(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            opened_file=opened_file,
            tags=tags,
            render_wrapped_pdf=render_wrapped_pdf,
            x_ambrahealth_job_id=x_ambrahealth_job_id,
        )
        if only_prepare is True:
            return prepared_request
        return await prepared_request.async_execute()

    async def cadsr(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        phi_namespace: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[ClientResponse, PreparedRequest]:
        """Gets graphical annotations according to vendor definitions for CAD SR object.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/cadsr?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: image version (Required).
        :param phi_namespace: A string, set to the UUID
            of the namespace where the file was attached
            if it was attached to a shared instance of the study
            outside of the original storage namespace
        :param only_prepare: Get prepared request.

        :returns: the vendor-specified graphical \
            annotations, empty if not implemented for the vendor or generating device.
        """
        prepared_request = self._cadsr(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        return await prepared_request.async_execute()

    async def dicom_payload(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        # In external api this is a hash parameter
        image_version: str,
        phi_namespace: Optional[str] = None,
        pretranscode: Optional[bool] = None,
        transfer_syntax: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[ClientResponse, PreparedRequest]:
        """Gets dicom payload.

        URL: {namespace}/{studyUid}/image/{imageUid}/version/{hash}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: image version (Required).
        :param phi_namespace: A string, set to the UUID
            If set, specifies the phi namespace from which to pull PHI.
            Will overlay the values onto the phiSource.
        :param pretranscode: Get pretranscoded dicom.
        :param transfer_syntax: Transfer syntax.
        :param only_prepare: Get prepared request.

        :returns: dicom.
        """
        prepared_request = self._dicom_payload(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
            phi_namespace=phi_namespace,
            pretranscode=pretranscode,
            transfer_syntax=transfer_syntax,
        )
        if only_prepare is True:
            return prepared_request
        return await prepared_request.async_execute()

    async def multipart_initiate(
        self,
        engine_fqdn: str,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[Box, ClientResponse, PreparedRequest]:
        """Initiate the multipart upload.

        URL: /multipart/initiate?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: uuid of multipart upload
        """
        prepared_request = self._multipart_initiate(
            engine_fqdn=engine_fqdn,
        )
        if only_prepare is True:
            return prepared_request
        response = await prepared_request.async_execute()
        if use_box is True:
            return Box(await response.json())
        return response

    async def multipart_chunk_upload(
        self,
        engine_fqdn: str,
        upload_uuid: str,
        bytes_part: bytes,
        chunk_number: int,
        only_prepare: bool = False,
    ) -> Union[ClientResponse, PreparedRequest]:
        """Upload a part of image.

        URL: multipart/{upload_uuid}

        :param engine_fqdn: Engine FQDN (Required).
        :param upload_uuid: UUID of the initiated multipart upload (Required).
        :param bytes_part: part of image (Required).
        :param chunk_number: sequence number, first part has number 0 (Required).
        :param only_prepare: Get prepared request.

        :returns: status code
        """
        prepared_request = self._multipart_chunk_upload(
            engine_fqdn=engine_fqdn,
            upload_uuid=upload_uuid,
            bytes_part=bytes_part,
            chunk_number=chunk_number,
        )
        if only_prepare is True:
            return prepared_request
        return await prepared_request.async_execute()

    async def multipart_complete(
        self,
        engine_fqdn: str,
        namespace: str,
        upload_uuid: str,
        file_size: int,
        endpoint: str = 'image',
        tags='',
        study_uid: Optional[str] = None,
        render_wrapped_pdf='',
        only_prepare: bool = False,
    ) -> Union[Box, ClientResponse, PreparedRequest]:
        """Finish the multipart upload process.

        URL: multipart/{upload_uuid}/complete

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param upload_uuid: UUID of the initiated multipart upload (Required).
        :param file_size: size of whole file (Required).
        :param endpoint: the endpoint to which the reconstructed file needs to be submitted. Only the image and wrap endpoint are supported at the moment.
        :param tags: the tags to be used to submit reconstructed file.
        :param study_uid: study uid.
        :param render_wrapped_pdf: if the file to be submitted should be treated as wrapped pdf.
        :param only_prepare: Get prepared request.

        :returns: status code
        """
        prepared_request = self._multipart_complete(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            upload_uuid=upload_uuid,
            file_size=file_size,
            endpoint=endpoint,
            tags=tags,
            study_uid=study_uid,
            render_wrapped_pdf=render_wrapped_pdf,
        )
        if only_prepare is True:
            return prepared_request
        return await prepared_request.async_execute()

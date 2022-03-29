"""Storage image namespace."""

import os
import zlib
from typing import Optional, Set

from aiohttp import FormData

from ambra_sdk.storage.bool_to_int import bool_to_int
from ambra_sdk.storage.request import PreparedRequest, StorageMethod
from ambra_sdk.types import RequestsFileType


class BaseImage:
    """Base storage Image commands."""

    def __init__(self, storage):
        """init.

        :param storage: storage api
        """
        self._storage = storage

    def _upload(
        self,
        engine_fqdn: str,
        namespace: str,
        opened_file: RequestsFileType,
        study_uid: Optional[str] = None,
        x_ambrahealth_job_id: Optional[str] = None,
    ) -> PreparedRequest:
        """Upload image to a namespace.

        URL: /namespace/{namespace}/image?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param opened_file: Opened file (like in requests) (Required).
            File object, or may be 2-tuples (filename, fileobj),
            3-tuples (filename, fileobj, contentype) or
            4-tuples (filename, fileobj, contentype, custom_headers).
        :param study_uid: study uid
        :param x_ambrahealth_job_id: X-AmbraHealth-Job-Id headers argument

        :returns: image object attributes
        """
        url_template = '/namespace/{namespace}/image'
        url_arg_names = {'engine_fqdn', 'namespace'}
        request_arg_names = {
            'study_uid',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        headers = {}
        if x_ambrahealth_job_id is not None:
            headers['X-AmbraHealth-Job-Id'] = x_ambrahealth_job_id
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
            headers=headers,
            data=opened_file,
        )

    def _wrap(
        self,
        engine_fqdn: str,
        namespace: str,
        opened_file: RequestsFileType,
        tags: Optional[str] = None,
        render_wrapped_pdf: Optional[bool] = None,
        x_ambrahealth_job_id: Optional[str] = None,
    ) -> PreparedRequest:
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

        :raises ValueError: Multifiles uploading for wrap
        :returns: image object attributes
        """
        render_wrapped_pdf: int = bool_to_int(  # type: ignore
            render_wrapped_pdf,
        )
        url_template = '/namespace/{namespace}/wrap'
        url_arg_names = {'engine_fqdn', 'namespace'}
        request_arg_names = {
            'tags',
            'render_wrapped_pdf',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        if isinstance(opened_file, tuple):
            fp = opened_file[1]
        elif isinstance(opened_file, FormData):
            form_data_fields = opened_file._fields  # NOQA:WPS437
            if len(form_data_fields) != 1:
                raise ValueError('Multifiles uploading for wrap.')
            files_info = form_data_fields[0]
            fp = files_info[2]
        else:
            fp = opened_file
        file_size = os.fstat(fp.fileno()).st_size
        if isinstance(opened_file, FormData):
            files = opened_file
            data_name = files._fields[0][0]['name']  # NOQA:WPS437
            if data_name != 'file':
                # In this case we have 404 error from storage
                raise ValueError(
                    'For FormData use "file" field name. '
                    'Example f = fd.add_field("file", ...)',
                )
        else:
            files = {
                'file': opened_file,
            }
        headers = {'X-File-Size': str(file_size)}

        if x_ambrahealth_job_id is not None:
            headers['X-AmbraHealth-Job-Id'] = x_ambrahealth_job_id

        if tags is not None:
            post_data = {
                'tags': tags,
            }
            prepared_request = PreparedRequest(
                storage=self._storage,
                method=StorageMethod.post,
                url=url,
                params=request_data,
                files=files,
                headers=headers,
                data=post_data,
            )
        else:
            prepared_request = PreparedRequest(
                storage=self._storage,
                method=StorageMethod.post,
                url=url,
                params=request_data,
                files=files,
                headers=headers,
            )
        return prepared_request

    def _cadsr(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
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

        :returns: the vendor-specified graphical \
            annotations, empty if not implemented for the vendor or generating device.
        """
        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}/cadsr'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'image_uid',
            'image_version',
        }
        request_arg_names = {'phi_namespace'}
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
        )

    def _dicom_payload(
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
    ) -> PreparedRequest:
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

        :returns: dicom.
        """
        pretranscode: int = bool_to_int(  # type: ignore
            pretranscode,
        )
        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}'

        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'image_uid',
            'image_version',
        }
        request_arg_names = {
            'phi_namespace',
            'pretranscode',
            'transfer_syntax',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
            stream=True,
        )

    def _multipart_initiate(
        self,
        engine_fqdn: str,
    ) -> PreparedRequest:
        """Initiate the multipart upload.

        URL: multipart/initiate?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).

        :returns: uuid of multipart upload
        """
        url_template = '/multipart/initiate'
        url_arg_names = {'engine_fqdn'}
        request_arg_names: Set[str] = set()
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
        )

    def _multipart_chunk_upload(
        self,
        engine_fqdn: str,
        upload_uuid: str,
        bytes_part: bytes,
        chunk_number: int,
    ) -> PreparedRequest:
        """Upload a part of image.

        URL: multipart/{upload_uuid}

        :param engine_fqdn: Engine FQDN (Required).
        :param upload_uuid: UUID of the initiated multipart upload (Required).
        :param bytes_part: part of image (Required).
        :param chunk_number: sequence number, first part has number 0 (Required).

        :returns: status code
        """
        url_template = '/multipart/{upload_uuid}'
        url_arg_names = {'engine_fqdn', 'upload_uuid'}
        request_arg_names: Set[str] = set()
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        headers = {
            'X-AmbraHealth-part-checksum': str(zlib.crc32(bytes_part)),
            'X-File-Size': str(len(bytes_part)),
            'X-File-Name': f'{chunk_number:05d}',
        }
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
            headers=headers,
            data=bytes_part,
        )

    def _multipart_complete(
        self,
        engine_fqdn: str,
        namespace: str,
        upload_uuid: str,
        file_size: int,
        endpoint: str = 'image',
        tags='',
        study_uid: Optional[str] = None,
        render_wrapped_pdf='',
    ) -> PreparedRequest:
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

        :returns: status code
        """
        url_template = '/multipart/{upload_uuid}/complete'
        url_arg_names = {
            'engine_fqdn',
            'upload_uuid',
        }

        request_arg_names = {
            'namespace',
            'endpoint',
            'study_uid',
            'tags',
            'render_wrapped_pdf',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        headers = {
            'X-File-Size': str(file_size),
            'X-File-Name': 'name',
        }
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
            headers=headers,
        )

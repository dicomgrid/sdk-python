"""Storage image namespace."""

import os
from typing import Optional, Union

from box import Box
from requests import Response

from ambra_sdk.exceptions.storage import (
    EntityTooLarge,
    PermissionDenied,
    PreconditionFailed,
)
from ambra_sdk.storage.bool_to_int import bool_to_int
from ambra_sdk.storage.request import PreparedRequest, StorageMethod
from ambra_sdk.types import RequestsFileType


class Image:
    """Storage Image commands."""

    def __init__(self, storage):
        """init.

        :param storage: storage api
        """
        self._storage = storage

    def upload(
        self,
        engine_fqdn: str,
        namespace: str,
        opened_file: RequestsFileType,
        study_uid: Optional[str] = None,
        use_box: bool = True,
        x_ambrahealth_job_id: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Box, Response, PreparedRequest]:
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
        prepared_request = PreparedRequest(
            storage_=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
            headers=headers,
            data=opened_file,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()
        if use_box is True:
            return Box(response.json())
        return response

    # TODO: What to do with tags?
    def wrap(
        self,
        engine_fqdn: str,
        namespace: str,
        opened_file: RequestsFileType,
        tags: Optional[str] = None,
        render_wrapped_pdf: Optional[bool] = None,
        x_ambrahealth_job_id: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        else:
            fp = opened_file
        file_size = os.fstat(fp.fileno()).st_size
        files = {
            'file': opened_file,
        }
        headers = {'X-File-Size': str(file_size)}

        if x_ambrahealth_job_id is not None:
            headers['X-AmbraHealth-Job-Id'] = x_ambrahealth_job_id

        errors_mapping = {
            403:
            PermissionDenied(
                'The sid is not valid or the user does '
                'not have permission to upload a non DICOM '
                'file from a study specified by the namespace.',
            ),
            412:
            PreconditionFailed(
                'X-File-Size header is not provided or has an '
                'invalid value.',
            ),
            413:
            EntityTooLarge(
                'The file to be DICOM-wrapped is larger than '
                '2GiB (2^31 - 1 bytes).',
            ),
        }

        if tags is not None:
            post_data = {
                'tags': tags,
            }
            prepared_request = PreparedRequest(
                storage_=self._storage,
                method=StorageMethod.post,
                url=url,
                errors_mapping=errors_mapping,
                params=request_data,
                files=files,
                headers=headers,
                data=post_data,
            )
        else:
            prepared_request = PreparedRequest(
                storage_=self._storage,
                method=StorageMethod.post,
                url=url,
                errors_mapping=errors_mapping,
                params=request_data,
                files=files,
                headers=headers,
            )

        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def cadsr(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        phi_namespace: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        prepared_request = PreparedRequest(
            storage_=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def dicom_payload(
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
    ) -> Union[Response, PreparedRequest]:
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
        prepared_request = PreparedRequest(
            storage_=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
            stream=True,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

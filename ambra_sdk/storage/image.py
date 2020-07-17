"""Storage image namespace."""

import os
from io import BufferedReader
from typing import Optional, Set, Union

from box import Box
from requests import Response

from ambra_sdk.exceptions.storage import (
    EntityTooLarge,
    PermissionDenied,
    PreconditionFailed,
)
from ambra_sdk.storage.bool_to_int import bool_to_int
from ambra_sdk.storage.request import PreparedRequest, StorageMethod


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
        opened_file: BufferedReader,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[Box, Response, PreparedRequest]:
        """Upload image to a namespace.

        URL: /namespace/{namespace}/image?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param opened_file: Opened file (Required).
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: image object attributes
        """
        url_template = '/namespace/{namespace}/image'
        url_arg_names = {'engine_fqdn', 'namespace'}
        request_arg_names: Set[str] = set()
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        prepared_request = PreparedRequest(
            storage_=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
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
        opened_file: BufferedReader,
        tags: Optional[str] = None,
        render_wrapped_pdf: Optional[bool] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
        """Upload a non DICOM image.

        URL: /namespace/{namespace}/wrap?sid={sid}&render_wrapped_pdf={0,1}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param tags: Any DICOM tags to be overwrite or added should be provided as a form-data field.
        :param opened_file: The multipart file to be uploaded should be provided as a form-data field.
        :param render_wrapped_pdf: An integer value of either 0 or 1.
        :param only_prepare: Get prepared request.

        :returns: image object attributes
        """
        render_wrapped_pdf: int = bool_to_int(  # type: ignore
            render_wrapped_pdf,
        )
        url_template = '/namespace/{namespace}/wrap'
        url_arg_names = {'engine_fqdn', 'namespace'}
        request_arg_names: Set[str] = set()
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        file_size = os.fstat(opened_file.fileno()).st_size
        files = {
            'file': opened_file,
        }
        headers = {'X-File-Size': str(file_size)}

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

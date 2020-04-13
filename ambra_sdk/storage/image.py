"""Storage image namespace."""

from io import BufferedReader
from typing import Optional, Set

from box import Box

from ambra_sdk.storage.bool_to_int import bool_to_int
from ambra_sdk.storage.response import check_response


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
    ) -> Box:
        """Upload image to a namespace.

        URL: /namespace/{namespace}/image?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param opened_file: Opened file (Required).

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
        response = self._storage.post(
            url,
            params=request_data,
            data=opened_file,
        )
        response = check_response(response, url_arg_names=url_arg_names)
        return Box(response.json())

    # TODO: What to do with tags?
    def wrap(
        self,
        engine_fqdn: str,
        namespace: str,
        opened_file: BufferedReader,
        tags: Optional[str] = None,
        render_wrapped_pdf: Optional[bool] = None,
    ) -> Box:
        """Upload a non DICOM image.

        URL: /namespace/{namespace}/wrap?sid={sid}&render_wrapped_pdf={0,1}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param tags: Any DICOM tags to be overwrite or added should be provided as a form-data field.
        :param opened_file: The multipart file to be uploaded should be provided as a form-data field.
        :param render_wrapped_pdf: An integer value of either 0 or 1.

        :returns: image object attributes
        """
        render_wrapped_pdf: int = bool_to_int(render_wrapped_pdf)  # type: ignore
        url_template = '/namespace/{namespace}/wrap'
        url_arg_names = {'engine_fqdn', 'namespace'}
        request_arg_names: Set[str] = set()
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        files = {
            'file': opened_file,
        }
        if tags is not None:
            post_data = {
                'tags': tags,
            }
            response = self._storage.post(
                url,
                params=request_data,
                files=files,
                data=post_data,
            )
        else:
            response = self._storage.post(
                url,
                params=request_data,
                files=files,
            )
        response = check_response(response, url_arg_names=url_arg_names)
        return Box(response.json())

    def cadsr(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        phi_namespace: Optional[str] = None,
    ) -> Box:
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
        response = self._storage.get(url, params=request_data)
        response = check_response(response, url_arg_names=url_arg_names)
        return Box(response.json())

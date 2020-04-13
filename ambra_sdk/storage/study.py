"""Storage study namespace."""

import json
from io import BufferedReader
from typing import Any, Dict, Optional, Set

from box import Box
from requests import Response

from ambra_sdk.exceptions.storage import (
    PermissionDenied,
    PreconditionFailed,
    UnsupportedMediaType,
)
from ambra_sdk.storage.bool_to_int import bool_to_int
from ambra_sdk.storage.response import check_response


def validate_size_x_string(size_str: str):
    """Validate size x string.

    :param size_str: size str in WxH format

    :raises ValueError: Wrong size value
    """
    try:
        width, height = size_str.split('x')
    except ValueError:
        raise ValueError('Wrong size format')

    try:
        int(width)
    except ValueError:
        raise ValueError('Wrong width value')
    try:
        int(height)
    except ValueError:
        raise ValueError('Wrong height value')


def validate_size(size_str: Optional[str]):
    """Validate size.

    :param size_str: size
    """
    if size_str is None:
        return
    try:  # NOQA:WPS229
        int(size_str)
    except ValueError:
        validate_size_x_string(size_str)


class Study:
    """Storage Study."""

    def __init__(self, storage):
        """Init.

        :param storage: storage api
        """
        self._storage = storage

    def schema(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        extended: Optional[bool] = None,
        attachments_only: Optional[bool] = None,
        phi_namespace: Optional[str] = None,
    ) -> Box:
        """Get the schema of study.

        URL: /study/{namespace}/{studyUid}/schema?sid={sid}&phi_namespace={phi_namespace}&extended={1,0}&attachments_only={0,1}  # NOQA E501

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param extended: is an bool, when set to 1 will include
            the optional phi_version and transfer_attributes
            name/value pairs in the response.
        :param attachments_only: is an bool, when set to 1
            will only include a list of
            the attachments in the study.
        :param phi_namespace: A string, set to the UUID of the
            namespace where the file was attached if it was
            attached to a shared instance of the study
            outside of the original storage namespace

        :returns: study schema
        """
        extended: int = bool_to_int(extended)  # type: ignore
        attachemtns_onlynt: int = bool_to_int(attachments_only)  # type: ignore
        url_template = '/study/{namespace}/{study_uid}/schema'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }
        request_arg_names = {'phi_namespace', 'extended', 'attachments_only'}
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.get(url, params=request_data)
        response = check_response(response, url_arg_names=url_arg_names)
        return Box(response.json())

    def delete(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        keep_attachments: Optional[bool] = None,
    ):
        """Deletes a study.

        URL: /study/{namespace}/{study_uid}?sid={sid}&keep_attachments={1,0}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param keep_attachments: An integer value of 1 or 0.

        If the optional parameter keep_attachments is set to 1, then:
            all DICOM images will be deleted.
            reports and attachments related to the study will be kept.
        """
        keep_attachments: int = bool_to_int(keep_attachments)  # type: ignore

        url_template = '/study/{namespace}/{study_uid}'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }
        request_arg_names = {'keep_attachments'}
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.delete(url, params=request_data)
        check_response(response, url_arg_names=url_arg_names)

    def delete_image(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        version: Optional[str] = None,
    ):
        """Deletes a study image.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}?sid={sid}&version={image version hash}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param version: The image version hash
        """
        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'image_uid',
        }
        request_arg_names = {'version'}
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.delete(url, params=request_data)
        check_response(response, url_arg_names=url_arg_names)

    def count(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        images_only: Optional[bool] = None,
        attachments_only: Optional[bool] = None,
        count_files: Optional[bool] = None,
    ) -> Box:
        """Gets study file count.

        URL: /study/{namespace}/{studyUid}/count?sid={sid}&images_only={1,0}&attachments_only={1,0}&count_files={1,0}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param images_only: an integer, zero or 1, returns the number
            of images in the study with superseded images by way of study update not counted.
        :param attachments_only: an integer, zero or 1, returns
            the number of attachments which have been added to this study.
        :param count_files: if present and set to 1 will count files stored
            on-disk for images and/or attachments,
            instead of counting from (possibly cached) meta data.

        :returns: count obj
        """
        images_only: int = bool_to_int(images_only)  # type: ignore
        attachments_only: int = bool_to_int(attachments_only)  # type: ignore
        count_files: int = bool_to_int(count_files)  # type: ignore
        url_template = '/study/{namespace}/{study_uid}/count'
        url_arg_names = {'engine_fqdn', 'namespace', 'study_uid'}
        request_arg_names = {'images_only', 'attachments_only', 'count_files'}
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.get(url, params=request_data)
        response = check_response(response, url_arg_names=url_arg_names)
        return Box(response.json())

    def tag(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: str,
    ) -> Box:
        """Gets study tags.

        URL: /study/{namespace}/{studyUid}/tag?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param phi_namespace: A string, set to the UUID of the
            namespace where the file was attached if
            it was attached to a shared instance of
            the study outside of the original storage namespace

        :returns: study tag object
        """
        url_template = '/study/{namespace}/{study_uid}/tag'
        url_arg_names = {'engine_fqdn', 'namespace', 'study_uid'}
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

    def attribute(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_version: str,
        phi_namespace: Optional[str] = None,
    ) -> Box:
        """Gets study image attributes.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/attribute?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_version: Image version (Required).
        :param phi_namespace: A string, set to the UUID of the namespace
            where the file was attached if it was attached to a
            shared instance of the study outside of the original storage namespace

        :returns: study attributes
        """
        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}/attribute'
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

    def image_phi(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_version: str,
        phi_namespace: Optional[str] = None,
    ) -> Box:
        """Gets study image PHI.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/phi?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_version: Image version (Required).
        :param phi_namespace: A string, set to the UUID of the namespace where the file was attached if it was attached to a shared instance of the study outside of the original storage namespace

        :returns: image PHI object
        """
        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}/phi'
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

    def phi(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
    ) -> Box:
        """Gets study PHI data.

        URL: /study/{namespace}/{studyUid}/phi?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param phi_namespace: A string, set to the UUID of the namespace where the file was attached if it was attached to a shared instance of the study outside of the original storage namespace

        :returns: study PHI data object
        """
        url_template = '/study/{namespace}/{study_uid}/phi'
        url_arg_names = {'engine_fqdn', 'namespace', 'study_uid'}
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

    def thumbnail(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        frame_number: int,
        depth: int = 8,
        phi_namespace: Optional[str] = None,
    ) -> Box:
        """Gets study image thumbnail.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/frame/{frameNumber}/thumbnail?sid={sid}&depth={8,16}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).
        :param frame_number: Frame number (Required).
        :param depth: Set the bit depth of the JPEG output (8 or 16).
        :param phi_namespace: A string, set to the UUID of the
            namespace where the file was attached if it was
            attached to a shared instance of the study
            outside of the original storage namespace

        :raises ValueError: Wrong value of depth

        :returns: Thumbnail object
        """
        if depth not in {8, 16}:
            raise ValueError('Depth must be in (8, 16)')

        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}/frame/{frame_number}/thumbnail'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'image_uid',
            'frame_number',
        }
        request_arg_names = {'depth', 'phi_namespace'}
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.get(url, params=request_data)
        response = check_response(response, url_arg_names=url_arg_names)
        return Box(response.json())

    def diagnostic(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        frame_number: int,
        phi_namespace: Optional[str] = None,
        depth: int = 8,
        size: Optional[str] = None,
    ) -> Box:
        """Gets study diagnostic image.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/frame/{frameNumber}/diagnostic?sid={sid}&phi_namespace={phi_namespace}&depth={8,16}&size=[max-edge-length|{width}x{height}]

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param frame_number: Frame number (Required).
        :param phi_namespace: A string, set to the UUID of the namespace
            where the file was attached if it was attached to a shared
            instance of the study outside of the original storage namespace
        :param depth: Set the bit depth of the JPEG output (8 or 16).
        :param size: Specify size of output. Omitted or 0 indicates no
            change; one number sets the maximum edge length in pixels;
            wxh sets maximum width and height

        :raises ValueError: Wrongh depth or size param

        :returns: Diagnostic image object
        """
        if depth not in {8, 16}:
            raise ValueError('Depth must be in (8, 16)')

        validate_size(size)

        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}/frame/{frame_number}/diagnostic'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'image_uid',
            'image_version',
            'frame_number',
        }
        request_arg_names = {'phi_namespace', 'depth', 'size'}
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.get(url, params=request_data)
        response = check_response(response, url_arg_names=url_arg_names)
        return Box(response.json())

    def frame(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        # TODO: frame number format
        frame_number: str,
        phi_namespace: Optional[str] = None,
        depth: int = 8,
        quality: float = 0.9,
        size: Optional[str] = None,
    ) -> Response:
        """Gets study image frame.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/frame/{frameNumber:[0-9][0-9]*|[0-9][0-9]*}?sid={sid}&phi_namespace={phi_namespace}&depth={8,16}&quality={0.0-1.0}&size=[max-edge-length|{width}x{height}]

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).
        :param frame_number: Frame number (Required).
        :param phi_namespace: A string, set to the UUID of the namespace where the file was attached if it was attached to a shared instance of the study outside of the original storage namespace
        :param depth: Set the bit depth of the JPEG output (8 or 16).
        :param quality: Set the JPEG compression quality 0 < q ≤ 1.0 (default 0.9)
        :param size: Specify size of output. Omitted or 0 indicates no change; one number sets the maximum edge length in pixels; wxh sets maximum width and height

        :raises ValueError: Wrongh depth or size param

        :returns: study image frame response
        """
        if depth not in {8, 16}:
            raise ValueError('Depth must be in (8, 16)')
        validate_size(size)

        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}/frame/{frame_number}'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'image_uid',
            'image_version',
            'frame_number',
        }
        request_arg_names = {
            'phi_namespace',
            'depth',
            'quality',
            'size',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.get(url, params=request_data, stream=True)
        return check_response(response, url_arg_names=url_arg_names)

    def pdf(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
    ) -> Response:
        """Gets a study encapsulated pdf file.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/pdf?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).

        :returns: Pdf response object
        """
        url_template = '/study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/pdf'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'image_uid',
            'image_version',
        }
        request_arg_names: Set[str] = set()
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response: Response = self._storage.get(
            url,
            params=request_data,
            stream=True,
        )
        response = check_response(response, url_arg_names=url_arg_names)
        return response

    def image_json(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        phi_namespace: Optional[str] = None,
        exclude_unnamed: Optional[str] = None,
        all_dicom_values: Optional[str] = None,
    ) -> Box:
        r"""Gets all DICOM attributes for an individual image.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/json?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).
        :param phi_namespace: A string, set to the UUID of
            the namespace where the file was attached if it
            was attached to a shared instance of the study
            outside of the original storage namespace
        :param exclude_unnamed: A string containing "1"
            or "0" (default 0). When "1", private tags
            (with "name": "?") are not included
        :param all_dicom_values: A string containing "1"
            or "0" (default 0). When "1", all values from
            a multi-value DICOM tag will be returned, separated
            by "\". Otherwise, only the first value is returned

        :returns: DICOM attributes object
        """
        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}/json'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'image_uid',
            'image_version',
        }
        request_arg_names = {
            'phi_namespace',
            'exclude_unnamed',
            'all_dicom_values',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.get(url, params=request_data)
        response = check_response(response, url_arg_names=url_arg_names)
        return Box(response.json())

    def json(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
        groups: Optional[str] = None,
        include_tags: Optional[str] = None,
        exclude_unnamed: Optional[str] = None,
        all_dicom_values: Optional[str] = None,
        series_uid: Optional[str] = None,
    ) -> Box:
        r"""Gets DICOM attributes for all images in a study.

        URL: /study/{namespace}/{studyUid}/json?sid={sid}&phi_namespace={phi_namespace}&groups={group ids}&include_tags={tags}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param phi_namespace: A string, set to the UUID of
            the namespace where the file was attached if it
            was attached to a shared instance of the study
            outside of the original storage namespace
        :param groups: The groups parameter will allow the
            client to filter tags to only those in a certain
            set of DICOM groups. Comma-separated list of decimal values.
        :param include_tags: Comma-separated list of DICOM tags
            to include. Format: 00080018,00080020
        :param exclude_unnamed: A string containing "1" or "0"
            (default 0). When "1", private tags (with "name": "?")
            are not included
        :param all_dicom_values: A string containing "1" or "0"
            (default 0). When "1", all values from a multi-value
            DICOM tag will be returned, separated by "\".
            Otherwise, only the first value is returned
        :param series_uid: A string containing a Series Instance UID.
            If specified, the results will only include DICOM tags
            from images from the specified series

        :returns: DICOM attributes object
        """
        url_template = '/study/{namespace}/{study_uid}/json'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }

        request_arg_names = {
            'phi_namespace',
            'groups',
            'include_tags',
            'exclude_unnamed',
            'all_dicom_values',
            'series_uid',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.get(url, params=request_data)
        response = check_response(response, url_arg_names=url_arg_names)
        return Box(response.json())

    def attachment(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        attachment_id: str,
        version: str,
        phi_namespace: Optional[str] = None,
    ) -> Response:
        """Gets the selected attachment.

        URL: /study/{namespace}/{studyUid}/attachment/{attachmentId}/version/{version}?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param attachment_id: Attachment uid (Required).
        :param version: version (Required).
        :param phi_namespace: A string, set to the UUID of
            the namespace where the file was attached if it
            was attached to a shared instance of the study
            outside of the original storage namespace

        :returns: attachments response
        """
        url_template = '/study/{namespace}/{study_uid}/attachment/{attachment_id}/version/{version}'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'attachment_id',
            'version',
        }
        request_arg_names = {'phi_namespace'}
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response: Response = self._storage.get(
            url,
            params=request_data,
            stream=True,
        )
        response = check_response(response, url_arg_names=url_arg_names)
        return response

    def latest(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        file_name: str,
        phi_namespace: Optional[str] = None,
    ) -> Response:
        """Gets the latest attachment for a study.

        URL: /study/{namespace}/{studyUid}/attachment/{filename:latest|latest}?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param file_name: filename or latest (Required).
        :param phi_namespace: A string, set to the UUID of
            the namespace where the file was attached if it
            was attached to a shared instance of the study
            outside of the original storage namespace

        :returns: latest attachment response
        """
        url_template = '/study/{namespace}/{study_uid}/attachment/{file_name}'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'file_name',
        }
        request_arg_names = {'phi_namespace'}
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response: Response = self._storage.get(
            url,
            params=request_data,
            stream=True,
        )
        response = check_response(response, url_arg_names=url_arg_names)
        return response

    def post_attachment(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        opened_file: BufferedReader,
        phi_namespace: Optional[str] = None,
        wrap_images: Optional[bool] = None,
        return_html: Optional[bool] = None,
        synchronous_wrap: Optional[bool] = None,
        static_ids: Optional[bool] = None,
    ) -> Box:
        """Posts an attachment to a study.

        URL: /study/{namespace}/{studyUid}/attachment?sid={sid}&phi_namespace={phi_namespace}&wrap_images={0,1}&return_html={0,1}&synchronous_wrap={0,1}&static_ids={0,1}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param opened_file: Opened file (Required).
        :param phi_namespace: A string, set to the UUID of
            the namespace where the file was attached if it
            was attached to a shared instance of the study
            outside of the original storage namespace
        :param wrap_images: An integer of value 1 or 0.
            For attachments that are images, or can be rendered
            to an image, generate a new DICOM image in the study
            containing (a rendered image of) the attachment
            (also controlled by namespace setting auto_wrap_images).
        :param synchronous_wrap: An integer of value 1 or 0.
            If 1, do all processing for image wrapping before returning,
            including Services notifications.
        :param static_ids: An integer of value 1 or 0. If 1,
            the attachment, series and any images rendered from PDF
            are assigned (u)uids based on a hash of the attachment,
            which will be the same if the attachment is re-uploaded.
            The attachment is also allowed to be re-uploaded when set to 1.
        :param return_html: An integer of value 1 or 0. Return results as
            Content Type text html, instead of
            application json (required for certain browsers)

        :returns: posts attachments response

        The request entity must contain
        a single multipart/form-data element named
        data containing the content to be attached.

        If the optional parameter wrap_images or synchronous_wrap
        is set to 1, or the uploading account has the setting
        auto_wrap_images set to 1, then:
        attachments of type image/jpeg or image/bmp are, asynchronously
        (unless synchronous_wrap=1) to the Store Attachment request,
        posted to the Wrap Attachment service, to be stored as a single
        DICOM image in a new series within the specified study.
        attachments of type application/pdf are, asynchronously
        (unless synchronous_wrap=1) to the Store Attachment request,
        rendered to DICOM images at a resolution of 200 ppi,
        one image per page of the original PDF. The resulting are
        stored in a new series within the specified study.
        UIDs assigned to the series and images will be random unless static_ids=1
        """
        wrap_images: int = bool_to_int(wrap_images)  # type: ignore
        synchronous_wrap: int = bool_to_int(synchronous_wrap)  # type: ignore
        static_ids: int = bool_to_int(static_ids)  # type: ignore
        return_html: int = bool_to_int(return_html)  # type: ignore

        files = {'data': opened_file}

        url_template = '/study/{namespace}/{study_uid}/attachment'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }
        request_arg_names = {
            'phi_namespace',
            'wrap_images',
            'return_html',
            'synchronous_wrap',
            'static_ids',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.post(url, params=request_data, files=files)
        check_response(response, url_arg_names=url_arg_names)
        return Box(response.json())

    def download(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        bundle: str,
        phi_namespace: Optional[str] = None,
        series_uid: Optional[str] = None,
        image_uid: Optional[str] = None,
        include_wrapped_dicoms: Optional[bool] = None,
        stop_on_failure: Optional[bool] = None,
        exclude_viewer: Optional[bool] = None,
    ) -> Response:
        """Downloads a study ZIP file.

        URL: /study/{namespace}/{studyUid}/download?sid={sid}&phi_namespace={phi_namespace}&bundle={iso,dicom,osx,win}&include_wrapped_dicoms={0,1}&series_uid={series_uid[,series_uid...]}&image_uid={image_uid[,image_uid...]}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param bundle: A string with value "dicom", "iso", "osx" or "win" (Required).

        :param phi_namespace: The shared-to namespace UUID
            of a shared instance of a study (Optional)
        :param include_wrapped_dicoms: When "1", will also
            include the DICOM file of a wrapped DICOM.
            Default is to only include the unwrapped file.
        :param series_uid: One or more Series Instance UIDs,
            comma-separated. Download will only include images
            from these series.
        :param image_uid: One or more SOP Instance UIDs,
            comma-separated. Download will only include these images.
        :param stop_on_failure: If "1", will not include the viewer
            app if there are any errors generating the download.
        :param exclude_viewer: If "1", viewer app will not be
            included in the "iso", "osx", and "win" bundle.
            The viewer app can be retrieved separately via /download/viewer

        :raises ValueError: Wrong bundle value

        :returns: study zip file response
        """
        if bundle not in {'dicom', 'iso', 'osx', 'win'}:
            raise ValueError('Boundle not in ("dicom", "iso", "osx", "win")')

        include_wrapped_dicoms: int = bool_to_int(include_wrapped_dicoms)  # type: ignore
        stop_on_failure: int = bool_to_int(stop_on_failure)  # type: ignore
        exclude_viewer: int = bool_to_int(exclude_viewer)  # type: ignore

        url_template = '/study/{namespace}/{study_uid}/download'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }

        request_arg_names = {
            'bundle',
            'phi_namespace',
            'series_uid',
            'image_uid',
            'include_wrapped_dicoms',
            'stop_on_failure',
            'exclude_viewer',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response: Response = self._storage.get(
            url,
            params=request_data,
            stream=True,
        )
        response = check_response(response, url_arg_names=url_arg_names)
        return response

    def delete_attachment(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        attachment_id: str,
        hash_arg: str,
        phi_namespace: Optional[str] = None,
    ):
        """Deletes a study attachment.

        URL: /study/{namespace}/{studyUid}/attachment/{attachmentId}/version/{hash}?sid={sid}?phi_namespace={phi_namespace}

        Note: Instead of hash in storage api this method accept hash_arg argument.

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param attachment_id: attachment id (Required).
        :param hash_arg: hash (Required).
        :param phi_namespace: A string, set to the UUID of the
            namespace where the file was attached if it was
            attached to a shared instance of the study outside of the original storage namespace
        """
        url_template = '/study/{namespace}/{studyUid}/attachment/{attachmentId}/version/{hash_arg}'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'attachment_id',
            'hash',
        }
        request_arg_names = {'phi_namespace'}
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )

        response = self._storage.delete(url, params=request_data)
        check_response(response, url_arg_names=url_arg_names)

    def video(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        reencode_video: Optional[bool] = None,
    ) -> Response:
        """Gets a study encapsulated video.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/video?sid={sid}&reencode_video={0,1}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).
        :param reencode_video: An integer of value 1 or 0.

        :returns: Video response
        """
        reencode_video: int = bool_to_int(reencode_video)  # type: ignore

        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}/video'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'image_uid',
            'image_version',
        }
        request_arg_names = {'reencode_video'}
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )

        errors_mapping = {
            415: UnsupportedMediaType('Video was not found encapsulated in the DICOM file.')  # NOQA: 997
        }
        response: Response = self._storage.get(
            url,
            params=request_data,
            stream=True,
        )
        response = check_response(response, url_arg_names=url_arg_names)
        return response

    def split(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
        to_namespace: Optional[str] = None,
        series_uid: Optional[str] = None,
        delete_series_from_original: Optional[str] = None,
    ) -> Response:
        """Split a study.

        URL: /study/{namespace}/{studyUid}/split?sid={sid}&phi_namespace={namespace}&to_namespace={namespace}&series_uid={series_uid,series_uid...series_uid}&delete_series_from_original={0,1}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param phi_namespace: An optional namespace UUID
            to burn-in PHI overrides to split study (defaults to no overrides)
        :param to_namespace: An optional namespace UUID to create
            the split study (defaults to current namespace)
        :param series_uid: An optional series instance uids list
            delimited by comas, only specified series will be split
            (defaults to split all image instances)
        :param delete_series_from_original: An integer value of either
            0 or 1. If 1 the series specified in the series_uid list will
            be deleted from the original study

        :returns: Split study response
        """
        url_template = '/study/{namespace}/{study_uid}/split'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }

        request_arg_names = {
            'phi_namespace',
            'to_namespace',
            'series_uid',
            'delete_series_from_original',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response: Response = self._storage.post(url, params=request_data)
        response = check_response(response, url_arg_names=url_arg_names)
        # new study uid
        return response

    def merge(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        secondary_study_uid: str,
        delete_secondary_study: Optional[bool] = None,
        series_uids: Optional[str] = None,
    ):
        """Merge studies.

        URL: /study/{namespace}/{studyUid}/merge?sid={sid}&secondary_study_uid={secondary_study_uid}&delete_secondary_study={0,1}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param secondary_study_uid: The secondary study uid to be
            merged into the studyUid(Required).
        :param delete_secondary_study: An integer, when set to 1
            the process will check that the sid provided has the
            required permission to delete the secondary study.
        :param series_uids: A list of one or more comma-separated
            Series Instance UIDs, used to filter images merged
            from secondary study.
        """
        url_template = '/study/{namespace}/{study_uid}/merge'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }
        request_arg_names = {
            'secondary_study_uid',
            'delete_secondary_study',
            'series_uids',
        }

        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )

        errors_mapping = {
            500: PermissionDenied(
                'the SID provided does not have the proper '
                'permission to delete the secondary study if '
                'the optional parameter delete_secondary_study '
                'is set to 1.'  # NOQA: 1106
            ),
        }
        response = self._storage.get(url, params=request_data)
        check_response(
            response,
            url_arg_names=url_arg_names,
            errors_mapping=errors_mapping,
        )

    def anonymize(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        region: Dict[str, Any],
        to_namespace: Optional[str] = None,
        new_study_uid: Optional[str] = None,
        keep_image_uids: Optional[str] = None,
        color: Optional[str] = None,
    ):
        """Produce a new study that is a copy of the old, with specified pixel regions obscured.

        URL: /study/{namespace}/{studyUid}/anonymize

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param region: Region (Required).
        :param to_namespace: The storage namespace
            into which the new study should be
            placed (default same as original).
        :param new_study_uid: The Study Instance UID of
            the new study (default is randomly generated).
        :param keep_image_uids: Should SOP Instance UIDs
            of modified copies be same as originals? (default is false)
        :param color: HTML-formatted color (rrggbb) of
            obscured regions (default is black-and-white checkerboard)

        The request entity is a JSON object specifying the regions
        to be obscured. Regions may be specified at study, series,
        or instance level; but only the highest matching level
        containing a regions field will be used.
        """
        url_template = '/study/{namespace}/{study_uid}/anonymize'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }

        request_arg_names = {
            'to_namespace',
            'new_study_uid',
            'keep_image_uids',
            'color',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.post(
            url,
            params=request_data,
            data=json.dumps(region),
        )
        errors_mapping = {
            412: PreconditionFailed('phi_namespace or to_namespace is not provided.'),
        }
        check_response(
            response,
            url_arg_names=url_arg_names,
            errors_mapping=errors_mapping,
        )

    def crop(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        region: Dict[str, Any],
        to_namespace: Optional[str] = None,
        new_study_uid: Optional[str] = None,
        keep_image_uids: Optional[str] = None,
    ):
        """Produce a new study that is a copy of the old, cropped to specified pixel region.

        URL: /study/{namespace}/{studyUid}/crop

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param region: Region (Required).
        :param to_namespace: The storage namespace into
            which the new study should be placed
            (default: same as original).
        :param new_study_uid: The Study Instance UID
            of the new study (default: randomly generated).
        :param keep_image_uids: Should SOP Instance UIDs
            of modified copies be same as originals? 1/0
            (default: 0/false)

        The request entity is a JSON object specifying the
        region to be cropped. Region may be specified at study,
        series, or instance level; but only the highest matching
        level containing a region field will be used.
        Example:
        { "series":{ "1.2.3.4.5":
        {"region":{"x":10,"y":10, "width":30, "height":40}},
        "1.3.5.7.9":{ "instances":{ "1.3.5.7.9.101":{"region":
        {"x":20,"y":20, "width":30, "height":20} } } } }
        """
        url_template = '/study/{namespace}/{study_uid}/crop'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }

        request_arg_names = {
            'to_namespace',
            'new_study_uid',
            'keep_image_uids',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.post(
            url,
            params=request_data,
            data=json.dumps(region),
        )
        errors_mapping = {
            412: PreconditionFailed('phi_namespace or to_namespace is not provided.'),
        }
        check_response(
            response,
            url_arg_names=url_arg_names,
            errors_mapping=errors_mapping,
        )

    def cache(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
    ):
        """Clears the image and metadata cache for the indicated study.

        URL: /study/{namespace}/{studyUid}/cache

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        """
        url_template = '/study/{namespace}/{study_uid}/cache'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }
        request_arg_names: Set[str] = set()
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        response = self._storage.delete(url, params=request_data)
        check_response(response, url_arg_names=url_arg_names)

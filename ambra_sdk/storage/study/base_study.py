"""Storage study namespace."""

import json
from typing import Any, Dict, Optional, Set

from box import Box, BoxList

from ambra_sdk.storage.bool_to_int import bool_to_int
from ambra_sdk.storage.request import PreparedRequest, StorageMethod
from ambra_sdk.types import RequestsFileType


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


class ImageJsonBox(Box):
    """Image json box.

    Response object for image_json method
    """

    def get_tags(self, filter_dict: Dict[str, Any]):
        """Get tags by filter.

        :param filter_dict: dict for filtering
        :yields: tag
        """
        tags = self['tags']
        for tag in tags:
            if all(
                tag.get(filter_key) == filter_value
                for filter_key, filter_value in filter_dict.items()
            ):
                yield tag

    def tag_by_name(self, name: str):
        """Get tag by name.

        :param name: name of tag
        :returns: tag
        """
        return next(
            self.get_tags(filter_dict={'name': name}),
            None,
        )


class JsonBox(BoxList):
    """Json box.

    Response object for json method.
    """

    def __init__(self, *args, **kwargs):
        """Init.

        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(
            *args,
            box_class=ImageJsonBox,
            **kwargs,
        )


class BaseStudy:
    """Base Storage Study."""

    def __init__(self, storage):
        """Init.

        :param storage: storage api
        """
        self._storage = storage

    def _schema(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        extended: Optional[bool] = None,
        attachments_only: Optional[bool] = None,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
        )

    def _delete(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        keep_attachments: Optional[bool] = None,
    ) -> PreparedRequest:
        """Deletes a study.

        URL: /study/{namespace}/{study_uid}?sid={sid}&keep_attachments={1,0}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param keep_attachments: An integer value of 1 or 0.

        :returns: Delete response

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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.delete,
            url=url,
            params=request_data,
        )

    def _delete_image(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        x_ambrahealth_job_id: Optional[str] = None,
    ) -> PreparedRequest:
        """Deletes a single image from a study.

        To delete multiple images, study/delete/images/.

        The HTTP method must be DELETE
        This method sends a STUDY_DELETE notification to Services after the image is deleted
        This method is synchronous - it doesn't return until the image is deleted and Services notification is sent

        URL: /study/{namespace}/{studyUid}/image/{imageUid}?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param x_ambrahealth_job_id: X-AmbraHealth-Job-Id headers argument

        :returns: Delete image response
        """
        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'image_uid',
        }
        request_arg_names: Set[str] = set()
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
            method=StorageMethod.delete,
            url=url,
            params=request_data,
            headers=headers,
        )

    def _delete_images(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        request_body: str,
    ) -> PreparedRequest:
        """Delete multiple images from a study.

        The HTTP method must be DELETE
        This method sends one STUDY_DELETE notification to Services after the images are deleted
        This method is synchronous - it doesn't return until all images are deleted and Services notification is sent

        URL: /study/{namespace}/{studyUid}/images?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param request_body: Comma-separated list of
            multiple image UIDs (Required).

        :returns: Delete images response
        """
        url_template = '/study/{namespace}/{study_uid}/images'
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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.delete,
            url=url,
            params=request_data,
            data=request_body,
        )

    def _count(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        images_only: Optional[bool] = None,
        attachments_only: Optional[bool] = None,
        count_files: Optional[bool] = None,
    ) -> PreparedRequest:
        """Gets study file count.

        URL: /study/{namespace}/{studyUid}/count?sid={sid}&images_only={1,0}&attachments_only={1,0}&count_files={1,0}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
        )

    def _tag(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
        )

    def _attribute(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        phi_namespace: Optional[str] = None,
        groups: Optional[str] = None,
        include_tags: Optional[str] = None,
        exclude_unnamed: Optional[str] = None,
    ) -> PreparedRequest:
        """Gets study image attributes.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/attribute?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).
        :param phi_namespace: A string, set to the UUID of the namespace
            where the file was attached if it was attached to a
            shared instance of the study outside of the original storage namespace
        :param groups: The groups parameter will allow the client to
            filter tags to only those in a certain set of top-level
            DICOM groups. Comma-separated list of decimal values, or
            hex values preceeded with "0x".
        :param include_tags: Comma-separated list of top-level DICOM tags
            to include. Format: 00080018,00080020 Nested tags
            (00081111:00080550) only filter at the top level,
            everything is included within the sequence
        :param exclude_unnamed: A string containing "1" or "0" (default 0).
            When "1", private tags (with "name": "?") are not included

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
        request_arg_names = {
            'phi_namespace',
            'groups',
            'include_tags',
            'exclude_unnamed',
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
        )

    def _image_phi(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
        """Gets study image PHI.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/phi?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
        )

    def _phi(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
        )

    def _thumbnail(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        frame_number: int,
        depth: Optional[int] = None,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
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
        if depth is not None and depth not in {8, 16}:
            raise ValueError('Depth must be in (8, 16)')

        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}/frame/{frame_number}/thumbnail'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'image_uid',
            'image_version',
            'frame_number',
        }
        request_arg_names = {'depth', 'phi_namespace'}
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

    def _diagnostic(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        frame_number: int,
        phi_namespace: Optional[str] = None,
        depth: Optional[int] = None,
        size: Optional[str] = None,
    ) -> PreparedRequest:
        """Gets study diagnostic image.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/frame/{frameNumber}/diagnostic?sid={sid}&phi_namespace={phi_namespace}&depth={8,16}&size=[max-edge-length|{width}x{height}]

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).
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
        if depth is not None and depth not in {8, 16}:
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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
        )

    def _frame(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        frame_number: str,
        phi_namespace: Optional[str] = None,
        depth: Optional[int] = None,
        quality: Optional[float] = None,
        size: Optional[str] = None,
    ) -> PreparedRequest:
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
        if depth is not None and depth not in {8, 16}:
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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
            stream=True,
        )

    def _frame_tiff(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        frame_number: str,
        phi_namespace: Optional[str] = None,
        depth: Optional[int] = None,
        size: Optional[str] = None,
    ) -> PreparedRequest:
        """Gets study image frame as TIFF.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/frame/{frameNumber:[0-9]*}/tiff?sid={sid}&phi_namespace={phi_namespace}&depth={8,16}&size=[max-edge-length|{width}x{height}]

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).
        :param frame_number: Frame number (Required).
        :param phi_namespace: A string, set to the UUID of the namespace where the file was attached if it was attached to a shared instance of the study outside of the original storage namespace
        :param depth: Set the bit depth of the JPEG output (8 or 16).
        :param size: Specify size of output. Omitted or 0 indicates no change; one number sets the maximum edge length in pixels; wxh sets maximum width and height

        :raises ValueError: Wrongh depth or size param

        :returns: study image frame response
        """
        if depth is not None and depth not in {8, 16}:
            raise ValueError('Depth must be in (8, 16)')
        validate_size(size)

        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}/frame/{frame_number}/tiff'
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
            'size',
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

    def _pdf(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
    ) -> PreparedRequest:
        """Gets a study encapsulated pdf file.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/pdf?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).

        :returns: Pdf response object
        """
        url_template = '/study/{namespace}/{study_uid}/image/{image_uid}/version/{image_version}/pdf'
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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
            stream=True,
        )

    def _image_json(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        phi_namespace: Optional[str] = None,
        exclude_unnamed: Optional[bool] = None,
        all_dicom_values: Optional[bool] = None,
        groups: Optional[str] = None,
        include_tags: Optional[str] = None,
    ) -> PreparedRequest:
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
        :param exclude_unnamed: When True, private tags
            (with "name": "?") are not included
        :param all_dicom_values: When True all values from
            a multi-value DICOM tag will be returned, separated
            by "\". Otherwise, only the first value is returned
        :param groups: groups
        :param include_tags: include_tags

        :returns: DICOM attributes object
        """
        all_dicom_values: int = bool_to_int(all_dicom_values)  # type: ignore
        exclude_unnamed: int = bool_to_int(exclude_unnamed)  # type: ignore
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
            'groups',
            'include_tags',
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
        )

    def _json(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
        groups: Optional[str] = None,
        all_dicom_values: Optional[bool] = None,
        include_tags: Optional[str] = None,
        exclude_unnamed: Optional[bool] = None,
        series_uid: Optional[str] = None,
    ) -> PreparedRequest:
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
            set of top-level DICOM groups. Comma-separated list
            of decimal values, or hex values preceeded with "0x".
        :param all_dicom_values: A string containing "1" or "0"
            (default 0). When "1", all values from a multi-value
            DICOM tag will be returned, separated by "\".
            Otherwise, only the first value is returned
        :param include_tags: Comma-separated list of top-level DICOM tags
            to include. Format: 00080018,00080020 Nested tags
            (00081111:00080550) only filter at the top level, everything
            is included within the sequence
        :param exclude_unnamed: If True private tags (with "name": "?")
            are not included
        :param series_uid: A string containing a Series Instance UID.
            If specified, the results will only include DICOM tags
            from images from the specified series

        :returns: DICOM attributes object
        """
        all_dicom_values: int = bool_to_int(all_dicom_values)  # type: ignore
        exclude_unnamed: int = bool_to_int(exclude_unnamed)  # type: ignore
        url_template = '/study/{namespace}/{study_uid}/json'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }

        request_arg_names = {
            'phi_namespace',
            'groups',
            'all_dicom_values',
            'include_tags',
            'exclude_unnamed',
            'series_uid',
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
        )

    def _attachment(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        attachment_id: str,
        version: str,
        phi_namespace: Optional[str] = None,
        file_name: Optional[str] = None,
    ) -> PreparedRequest:
        """Gets the selected attachment.

        URL: /study/{namespace}/{studyUid}/attachment/{attachmentId}/version/{version}?sid={sid}&phi_namespace={phi_namespace}
        URL: /study/{namespace}/{studyUid}/attachment/{attachmentId}/version/{version}/{filename}?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param attachment_id: Attachment uid (Required).
        :param version: version (Required).
        :param phi_namespace: A string, set to the UUID of
            the namespace where the file was attached if it
            was attached to a shared instance of the study
            outside of the original storage namespace
        :param file_name: filename

        :returns: attachments response
        """
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'attachment_id',
            'version',
        }
        if file_name is not None:
            url_template = '/study/{namespace}/{study_uid}/attachment/{attachment_id}/version/{version}/{file_name}'
            url_arg_names.add('file_name')
        else:
            url_template = '/study/{namespace}/{study_uid}/attachment/{attachment_id}/version/{version}'
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
            stream=True,
        )

    def _latest(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        file_name: Optional[str] = None,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
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
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }
        if file_name is not None:
            url_template = '/study/{namespace}/{study_uid}/attachment/latest/{file_name}'
            url_arg_names.add('file_name')
        else:
            url_template = '/study/{namespace}/{study_uid}/attachment/latest'

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
            stream=True,
        )

    def _post_attachment(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        opened_file: RequestsFileType,
        phi_namespace: Optional[str] = None,
        wrap_images: Optional[bool] = None,
        wrap_html_as_pdf: Optional[bool] = None,
        return_html: Optional[bool] = None,
        synchronous_wrap: Optional[bool] = None,
        static_ids: Optional[bool] = None,
        x_ambrahealth_job_id: Optional[str] = None,
    ) -> PreparedRequest:
        """Posts an attachment to a study.

        URL: /study/{namespace}/{studyUid}/attachment?sid={sid}&phi_namespace={phi_namespace}&wrap_images={0,1}&return_html={0,1}&synchronous_wrap={0,1}&static_ids={0,1}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param opened_file: Opened file (like in requests) (Required).
            File object, or may be 2-tuples (filename, fileobj),
            3-tuples (filename, fileobj, contentype) or
            4-tuples (filename, fileobj, contentype, custom_headers).
        :param phi_namespace: A string, set to the UUID of
             the namespace where the file was attached if it
             was attached to a shared instance of the study
             outside of the original storage namespace
        :param wrap_images: An integer of value 1 or 0. If 1,
             for attachments that are images, or can be rendered
             to an image, generate a new DICOM image in the study
             containing (a rendered image of) the attachment
             (also controlled by namespace setting auto_wrap_images).
        :param wrap_html_as_pdf: An integer of value 1 or 0.
             If 1, for attachments that are html, generate a
             new pdf and attach that (instead of the original html).
        :param synchronous_wrap: An integer of value 1 or 0.
             If 1, do all processing for image wrapping before
             returning, including Services notifications.
             Additionally triggers wrap_images functionality.
        :param static_ids: An integer of value 1 or 0. If 1,
            the attachment, series and any images rendered from PDF
            are assigned (u)uids based on a hash of the attachment,
            which will be the same if the attachment is re-uploaded.
            The attachment is also allowed to be re-uploaded when set to 1.
        :param return_html: An integer of value 1 or 0. Return results as
            Content Type text html, instead of
            application json (required for certain browsers)
        :param x_ambrahealth_job_id: X-AmbraHealth-Job-Id headers argument

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
        # Attachment must be an image
        wrap_images: int = bool_to_int(wrap_images)  # type: ignore
        wrap_html_as_pdf: int = bool_to_int(wrap_html_as_pdf)  # type: ignore
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
            'wrap_html_as_pdf',
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
        headers = {}
        if x_ambrahealth_job_id is not None:
            headers['X-AmbraHealth-Job-Id'] = x_ambrahealth_job_id
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
            headers=headers,
            files=files,
        )

    def _attachment_image(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        attachment_uid: str,
        version: str,
        static_ids: Optional[bool] = None,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
        """Attachment image.

        Adds a render of an attachment to a study.

        URL: /study/{namespace}/{studyUid}/attachment/{attachmentUid}/version/{version}/image?sid={sid}&

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param attachment_uid: Attachment uid (Required).
        :param version: version (Required)
        :param static_ids: An integer of value 1 or 0. If 1, series
            and images rendered from PDF are assigned (u)uids based
            on a hash of the attachment; repeated requests to render the
            same PDF will not result in more images.
        :param phi_namespace: A string, set to the UUID of the namespace
            where the file was attached if it was attached to a shared
            instance of the study outside of the original storage namespace

        :returns: 202 Attachment succesfully rendered as an image and added to study.
            500 (SERVER ERROR) if server error persisted.
        """
        static_ids: int = bool_to_int(static_ids)  # type: ignore

        url_template = '/study/{namespace}/{study_uid}/attachment/{attachment_uid}/version/{version}/image'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'attachment_uid',
            'version',
        }
        request_arg_names = {
            'phi_namespace',
            'static_ids',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
        )

    def _download(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        # In external api it is optional. But this call drops with 500 error
        # if bundle is None.
        bundle: str,
        phi_namespace: Optional[str] = None,
        series_uid: Optional[str] = None,
        image_uid: Optional[str] = None,
        include_wrapped_dicoms: Optional[bool] = None,
        stop_on_failure: Optional[bool] = None,
        exclude_viewer: Optional[bool] = None,
        v3: Optional[bool] = None,
        roche_directory: Optional[bool] = None,
        flat_directory: Optional[bool] = None,
        transfer_syntax: Optional[bool] = None,
        anonymize_tags: Optional[str] = None,
    ) -> PreparedRequest:
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
        :param v3: If "1", viewer app will be pro viewer, and format/content
            will support pro viewer.
        :param roche_directory: If "1", .dcm files will be organized into
            StudyDate-ClinicalTrialTimePointID/Modality/SeriesTime-SeriesDescription/ folders (instead of SER000X/ folders).
        :param flat_directory: If "1", .dcm files will be flatly named
            IMG0001-IMG{image count}, and not be organized into SER folder.
        :param transfer_syntax: transfer syntax
        :param anonymize_tags: The list of tag ids with overridden values
            separated by comma (,) that should be overridden.
            Example:
            anonymize_tags={{tag_id_int_1}}={{tag_value_1}},{{tag_id_int_2}}={{tag_value_2}}.
            To omit tag, provide special keyword that is being used in services overrides as value: __DELETE__

        :raises ValueError: Wrong bundle value

        :returns: study zip file response
        """
        if bundle not in {'dicom', 'iso', 'osx', 'win'}:
            raise ValueError('Boundle not in ("dicom", "iso", "osx", "win")')

        include_wrapped_dicoms: int = bool_to_int(  # type: ignore
            include_wrapped_dicoms,
        )
        stop_on_failure: int = bool_to_int(stop_on_failure)  # type: ignore
        exclude_viewer: int = bool_to_int(exclude_viewer)  # type: ignore
        v3: int = bool_to_int(v3)  # type: ignore
        roche_directory: int = bool_to_int(roche_directory)  # type: ignore
        flat_directory: int = bool_to_int(flat_directory)  # type: ignore

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
            'v3',
            'roche_directory',
            'flat_directory',
            'transfer_syntax',
            'anonymize_tags',
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

    def _delete_attachment(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        attachment_id: str,
        hash_arg: str,
        phi_namespace: Optional[str] = None,
        x_ambrahealth_job_id: Optional[str] = None,
    ) -> PreparedRequest:
        """Deletes a study attachment.

        URL: /study/{namespace}/{studyUid}/attachment/{attachmentId}/version/{hash}?sid={sid}?phi_namespace={phi_namespace}

        Note: Instead of hash in storage api this method accept hash_arg argument.
        Actually, hash_args is attachment version...

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param attachment_id: attachment id (Required).
        :param hash_arg: hash (Required).
        :param phi_namespace: A string, set to the UUID of the
            namespace where the file was attached if it was
            attached to a shared instance of the study outside of the original storage namespace
        :param x_ambrahealth_job_id: X-AmbraHealth-Job-Id headers argument

        :returns: Delete attachemnt response
        """
        url_template = '/study/{namespace}/{study_uid}/attachment/{attachment_id}/version/{hash_arg}'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'attachment_id',
            'hash_arg',
        }
        request_arg_names = {'phi_namespace'}
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
            method=StorageMethod.delete,
            url=url,
            params=request_data,
            headers=headers,
        )

    def _video(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        reencode_video: Optional[bool] = None,
    ) -> PreparedRequest:
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

        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
            stream=True,
        )

    def _split(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
        to_namespace: Optional[str] = None,
        series_uid: Optional[str] = None,
        delete_series_from_original: Optional[str] = None,
    ) -> PreparedRequest:
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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
        )

    def _merge(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        # In external api it is optional. But this call drops with 400 error if
        # secondary_study_uid is None.
        secondary_study_uid: str,
        delete_secondary_study: Optional[bool] = None,
        series_uids: Optional[str] = None,
        x_ambrahealth_job_id: Optional[str] = None,
    ) -> PreparedRequest:
        """Merge studies.

        URL: /study/{namespace}/{studyUid}/merge?sid={sid}&secondary_study_uid={secondary_study_uid}&delete_secondary_study={0,1}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param secondary_study_uid: A list of one or more
            comma-separated secondary Study UIDs to be merged
            into the studyUid(Required).
        :param delete_secondary_study: An integer, when set to 1
            the process will check that the sid provided has the
            required permission to delete the secondary study.
        :param series_uids: A list of one or more comma-separated
            Series Instance UIDs, used to filter images merged
            from secondary study.
        :param x_ambrahealth_job_id: X-AmbraHealth-Job-Id headers argument

        :returns: Actually empty response
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
        headers = {}
        if x_ambrahealth_job_id is not None:
            headers['X-AmbraHealth-Job-Id'] = x_ambrahealth_job_id
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.get,
            url=url,
            params=request_data,
            headers=headers,
        )

    # Nicholas Byers dg1572443133:
    # with is_ai=true, you should expect the tag (0012,0063)
    # De-Identification Method to then read "SYSTEM" (instead of "MANUAL")
    def _anonymize(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        region: Dict[str, Any],
        phi_namespace: Optional[str] = None,
        to_namespace: Optional[str] = None,
        new_study_uid: Optional[str] = None,
        keep_image_uids: Optional[str] = None,
        color: Optional[str] = None,
        x_ambrahealth_job_id: Optional[str] = None,
        is_ai: bool = False,
    ) -> PreparedRequest:
        """Produce a new study that is a copy of the old, with specified pixel regions obscured.

        URL: /study/{namespace}/{studyUid}/anonymize

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param region: Region (Required).
        :param phi_namespace: phi namespace
        :param to_namespace: The storage namespace
            into which the new study should be
            placed (default same as original).
        :param new_study_uid: The Study Instance UID of
            the new study (default is randomly generated).
        :param keep_image_uids: Should SOP Instance UIDs
            of modified copies be same as originals? (default is false)
        :param color: HTML-formatted color (rrggbb) of
            obscured regions (default is black-and-white checkerboard)
        :param x_ambrahealth_job_id: X-AmbraHealth-Job-Id headers argument
        :param is_ai: This is request from ai stack flag

        :returns: Anonymize study response

        The request entity is a JSON object specifying the regions
        to be obscured. Regions may be specified at study, series,
        or instance level; but only the highest matching level
        containing a regions field will be used.
        """
        is_ai: Optional[str] = 'true' if is_ai else None  # type: ignore
        url_template = '/study/{namespace}/{study_uid}/anonymize'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }

        request_arg_names = {
            'phi_namespace',
            'to_namespace',
            'new_study_uid',
            'keep_image_uids',
            'color',
            'is_ai',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        if x_ambrahealth_job_id is not None:
            headers['X-AmbraHealth-Job-Id'] = x_ambrahealth_job_id
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
            headers=headers,
            data=json.dumps(region),
        )

    def _crop(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        region: Dict[str, Any],
        phi_namespace: Optional[str] = None,
        to_namespace: Optional[str] = None,
        new_study_uid: Optional[str] = None,
        keep_image_uids: Optional[str] = None,
    ) -> PreparedRequest:
        """Produce a new study that is a copy of the old, cropped to specified pixel region.

        URL: /study/{namespace}/{studyUid}/crop

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param region: Region (Required).
        :param phi_namespace: phi namespace
        :param to_namespace: The storage namespace into
            which the new study should be placed
            (default: same as original).
        :param new_study_uid: The Study Instance UID
            of the new study (default: randomly generated).
        :param keep_image_uids: Should SOP Instance UIDs
            of modified copies be same as originals? 1/0
            (default: 0/false)

        :returns: Crop study response

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
            'phi_namespace',
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
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
            headers=headers,
            data=json.dumps(region),
        )

    def _cache(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
    ) -> PreparedRequest:
        """Clears the image and metadata cache for the indicated study.

        URL: /study/{namespace}/{studyUid}/cache

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).

        :returns: Cache study response
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
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.delete,
            url=url,
            params=request_data,
        )

    def _hl7_to_sr(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        hl7uuid: str,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
        """Hl7 to sr.

        Gets the HL7 report from services, converts to the DICOM SR
        and uploads to the storage.

        URL: /study/{namespace}/{studyUid}/hl7/{hl7Uuid}/sr?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param hl7uuid: hl7 report UUID from services to convert to DICOM SR.
        :param phi_namespace: A string, set to the UUID of the namespace
            where the file was attached if it was attached to a shared
            instance of the study outside of the original storage namespace


        :returns: hl7_to_sr result
        """
        url_template = '/study/{namespace}/{study_uid}/hl7/{hl7uuid}/sr'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'hl7uuid',
        }
        request_arg_names = {
            'phi_namespace',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
        )

    def _clone(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
        new_image_uids: Optional[bool] = None,
        new_series_uids: Optional[bool] = None,
        x_ambrahealth_job_id: Optional[str] = None,
    ) -> PreparedRequest:
        """Clone.

        Clones the specified study into new study_uid into the same namespace
        and generates new series uid and image uids if it's requested.

        URL: /study/{namespace}/{studyUid}/clone?sid={sid}&phi_namespace={phi_namespace}&new_image_uids={true/false}&new_series_uids={true/false}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param phi_namespace: A string, set to the UUID of the namespace
            where the file was attached if it was attached to a shared
            instance of the study outside of the original storage namespace
        :param new_image_uids: true/false, whether to generate for study new image uids.
        :param new_series_uids: true/false, whether to generate for study new series uids.
        :param x_ambrahealth_job_id: X-AmbraHealth-Job-Id headers argument

        :return: new study uid
        """
        if new_image_uids is not None:
            new_image_uids: str = 'true' if new_image_uids else 'false'  # type: ignore

        if new_series_uids is not None:
            new_series_uids: str = 'true' if new_series_uids else 'false'  # type: ignore

        url_template = '/study/{namespace}/{study_uid}/clone'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }
        request_arg_names = {
            'phi_namespace',
            'new_image_uids',
            'new_series_uids',
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
            # This method is POST !
            method=StorageMethod.post,
            url=url,
            params=request_data,
            headers=headers,
        )

    def _create_rt(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        body: str,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
        """Create RT.

        Generates RTSTRUCT DICOM file from the content sent by client

        URL: /study/{namespace}/{studyUid}/rt?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param phi_namespace: A string, set to the UUID of the namespace
            where the file was attached if it was attached to a shared
            instance of the study outside of the original storage namespace

        :param body: Body that represents fields of the RTSTRUCT DICOM
        :return: Image attributes
        """
        url_template = '/study/{namespace}/{study_uid}/rt'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }
        request_arg_names = {
            'phi_namespace',
        }
        url, request_data = self._storage.get_url_and_request(
            url_template,
            url_arg_names,
            request_arg_names,
            locals(),
        )
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }

        return PreparedRequest(
            storage=self._storage,
            method=StorageMethod.post,
            url=url,
            params=request_data,
            data=body,
            headers=headers,
        )

    def _image_dicomweb(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        series_uid: str,
        image_uid: str,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
        """Returns JSON representation of a single DICOM as defined by the DICOMWeb WADO-RS Metadata standard \
            http://dicom.nema.org/medical/dicom/current/output/html/part18.html#table_10.4.1-2.

        URL: dicomweb/{namespace}/studies/{studyUid}/series/{seriesUid}/instances/{imageUid}/metadata?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param series_uid: Series uid (Required).
        :param image_uid: Image uid (Required).
        :param phi_namespace: A string, set to the UUID of the
            namespace where the file was attached if it was
            attached to a shared instance of the study
            outside of the original storage namespace

        :returns: A JSON representation of a DICOM according to the DICOMWeb standard,
            omitting any bulkdata, pixeldata, or other binary fields.
        """
        url_template = '/dicomweb/{namespace}/studies/{study_uid}/series/{series_uid}/instances/{image_uid}/metadata'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'series_uid',
            'image_uid',
        }
        request_arg_names = {
            'phi_namespace',
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
        )

    def _series_dicomweb(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        series_uid: str,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
        """Returns JSON representation of a series of DICOM(s) as defined by the DICOMWeb WADO-RS Metadata standard \
            http://dicom.nema.org/medical/dicom/current/output/html/part18.html#table_10.4.1-2.

        URL: dicomweb/{namespace}/studies/{studyUid}/series/{seriesUid}/metadata?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param series_uid: Series uid (Required).
        :param phi_namespace: A string, set to the UUID of the
            namespace where the file was attached if it was
            attached to a shared instance of the study
            outside of the original storage namespace

        :returns: A JSON representation of a series of DICOM(s) according to the DICOMWeb standard,
            omitting any bulkdata, pixeldata, or other binary fields.
        """
        url_template = '/dicomweb/{namespace}/studies/{study_uid}/series/{series_uid}/metadata'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
            'series_uid',
        }
        request_arg_names = {
            'phi_namespace',
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
        )

    def _study_dicomweb(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
    ) -> PreparedRequest:
        """Returns JSON representation of an entire study of DICOMs as defined by the DICOMWeb WADO-RS Metadata standard \
            http://dicom.nema.org/medical/dicom/current/output/html/part18.html#table_10.4.1-2.

        URL: dicomweb/{namespace}/studies/{studyUid}/metadata?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param phi_namespace: A string, set to the UUID of the
            namespace where the file was attached if it was
            attached to a shared instance of the study
            outside of the original storage namespace

        :returns: A JSON representation of an entire study of DICOM(s) according to the DICOMWeb standard,
            omitting any bulkdata, pixeldata, or other binary fields.
        """
        url_template = '/dicomweb/{namespace}/studies/{study_uid}/metadata'
        url_arg_names = {
            'engine_fqdn',
            'namespace',
            'study_uid',
        }
        request_arg_names = {
            'phi_namespace',
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
        )

"""Storage study namespace."""

from typing import Any, Dict, Optional, Union

from box import Box, BoxList
from requests import Response

from ambra_sdk.storage.request import PreparedRequest
from ambra_sdk.storage.study.base_study import BaseStudy, ImageJsonBox, JsonBox
from ambra_sdk.types import RequestsFileType


class Study(BaseStudy):
    """Storage Study."""

    def schema(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        extended: Optional[bool] = None,
        attachments_only: Optional[bool] = None,
        phi_namespace: Optional[str] = None,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[Box, Response, PreparedRequest]:
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
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: study schema
        """
        prepared_request = self._schema(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            extended=extended,
            attachments_only=attachments_only,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()

        if use_box is True:
            return Box(response.json())
        return response

    def delete(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        keep_attachments: Optional[bool] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
        """Deletes a study.

        URL: /study/{namespace}/{study_uid}?sid={sid}&keep_attachments={1,0}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param keep_attachments: An integer value of 1 or 0.
        :param only_prepare: Get prepared request.

        :returns: Delete response

        If the optional parameter keep_attachments is set to 1, then:
            all DICOM images will be deleted.
            reports and attachments related to the study will be kept.
        """
        prepared_request = self._delete(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            keep_attachments=keep_attachments,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def delete_image(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        x_ambrahealth_job_id: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: Delete image response
        """
        prepared_request = self._delete_image(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            x_ambrahealth_job_id=x_ambrahealth_job_id,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def delete_images(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        request_body: str,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: Delete images response
        """
        prepared_request = self._delete_images(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            request_body=request_body,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def count(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        images_only: Optional[bool] = None,
        attachments_only: Optional[bool] = None,
        count_files: Optional[bool] = None,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[Box, Response, PreparedRequest]:
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
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: count obj
        """
        prepared_request = self._count(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            images_only=images_only,
            attachments_only=attachments_only,
            count_files=count_files,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()
        if use_box is True:
            return Box(response.json())
        return response

    def tag(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[Box, Response, PreparedRequest]:
        """Gets study tags.

        URL: /study/{namespace}/{studyUid}/tag?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param phi_namespace: A string, set to the UUID of the
            namespace where the file was attached if
            it was attached to a shared instance of
            the study outside of the original storage namespace
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: study tag object
        """
        prepared_request = self._tag(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()
        if use_box is True:
            return Box(response.json())
        return response

    def attribute(
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
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[Box, Response, PreparedRequest]:
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
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: study attributes
        """
        prepared_request = self._attribute(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
            phi_namespace=phi_namespace,
            groups=groups,
            include_tags=include_tags,
            exclude_unnamed=exclude_unnamed,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()
        if use_box is True:
            return Box(response.json())
        return response

    def image_phi(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        phi_namespace: Optional[str] = None,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[Box, Response, PreparedRequest]:
        """Gets study image PHI.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/phi?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).
        :param phi_namespace: A string, set to the UUID of the namespace where the file was attached if it was attached to a shared instance of the study outside of the original storage namespace
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: image PHI object
        """
        prepared_request = self._image_phi(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()
        if use_box is True:
            return Box(response.json())
        return response

    def phi(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[Box, Response, PreparedRequest]:
        """Gets study PHI data.

        URL: /study/{namespace}/{studyUid}/phi?sid={sid}&phi_namespace={phi_namespace}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param phi_namespace: A string, set to the UUID of the namespace where the file was attached if it was attached to a shared instance of the study outside of the original storage namespace
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: study PHI data object
        """
        prepared_request = self._phi(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()
        if use_box is True:
            return Box(response.json())
        return response

    def thumbnail(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        frame_number: int,
        depth: Optional[int] = None,
        phi_namespace: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: Thumbnail object
        """
        prepared_request = self._thumbnail(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
            frame_number=frame_number,
            depth=depth,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def diagnostic(
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
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: Diagnostic image object
        """
        prepared_request = self._diagnostic(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
            frame_number=frame_number,
            phi_namespace=phi_namespace,
            depth=depth,
            size=size,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def frame(
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
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: study image frame response
        """
        prepared_request = self._frame(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
            frame_number=frame_number,
            phi_namespace=phi_namespace,
            depth=depth,
            quality=quality,
            size=size,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def frame_tiff(
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
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: study image frame response
        """
        prepared_request = self._frame_tiff(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
            frame_number=frame_number,
            phi_namespace=phi_namespace,
            depth=depth,
            size=size,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def pdf(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
        """Gets a study encapsulated pdf file.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/pdf?sid={sid}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).
        :param only_prepare: Get prepared request.

        :returns: Pdf response object
        """
        prepared_request = self._pdf(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def image_json(
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
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[ImageJsonBox, Response, PreparedRequest]:
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
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: DICOM attributes object
        """
        prepared_request = self._image_json(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
            phi_namespace=phi_namespace,
            exclude_unnamed=exclude_unnamed,
            all_dicom_values=all_dicom_values,
            groups=groups,
            include_tags=include_tags,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()
        if use_box is True:
            return ImageJsonBox(response.json())
        return response

    def json(
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
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[JsonBox, Response, PreparedRequest]:
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
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: DICOM attributes object
        """
        prepared_request = self._json(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            phi_namespace=phi_namespace,
            groups=groups,
            all_dicom_values=all_dicom_values,
            include_tags=include_tags,
            exclude_unnamed=exclude_unnamed,
            series_uid=series_uid,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()
        if use_box is True:
            return JsonBox(response.json())
        return response

    def attachment(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        attachment_id: str,
        version: str,
        phi_namespace: Optional[str] = None,
        file_name: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: attachments response
        """
        prepared_request = self._attachment(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            attachment_id=attachment_id,
            version=version,
            phi_namespace=phi_namespace,
            file_name=file_name,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def latest(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        file_name: Optional[str] = None,
        phi_namespace: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: latest attachment response
        """
        prepared_request = self._latest(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            file_name=file_name,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def post_attachment(
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
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

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
        prepared_request = self._post_attachment(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            opened_file=opened_file,
            phi_namespace=phi_namespace,
            wrap_images=wrap_images,
            wrap_html_as_pdf=wrap_html_as_pdf,
            return_html=return_html,
            synchronous_wrap=synchronous_wrap,
            static_ids=static_ids,
            x_ambrahealth_job_id=x_ambrahealth_job_id,
        )
        if only_prepare is True:
            return prepared_request
        # Method can return Html (depends on params)...
        return prepared_request.execute()

    def attachment_image(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        attachment_uid: str,
        version: str,
        static_ids: Optional[bool] = None,
        phi_namespace: Optional[str] = None,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[Box, Response, PreparedRequest]:
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
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: 202 Attachment succesfully rendered as an image and added to study.
            500 (SERVER ERROR) if server error persisted.
        """
        prepared_request = self._attachment_image(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            attachment_uid=attachment_uid,
            version=version,
            static_ids=static_ids,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()

        if use_box is True:
            return Box(response.json())
        return response

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
        v3: Optional[bool] = None,
        roche_directory: Optional[bool] = None,
        flat_directory: Optional[bool] = None,
        transfer_syntax: Optional[bool] = None,
        anonymize_tags: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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

        :param only_prepare: Get prepared request.

        :returns: study zip file response
        """
        prepared_request = self._download(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            bundle=bundle,
            phi_namespace=phi_namespace,
            series_uid=series_uid,
            image_uid=image_uid,
            include_wrapped_dicoms=include_wrapped_dicoms,
            stop_on_failure=stop_on_failure,
            exclude_viewer=exclude_viewer,
            v3=v3,
            roche_directory=roche_directory,
            flat_directory=flat_directory,
            transfer_syntax=transfer_syntax,
            anonymize_tags=anonymize_tags,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def delete_attachment(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        attachment_id: str,
        hash_arg: str,
        phi_namespace: Optional[str] = None,
        x_ambrahealth_job_id: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: Delete attachemnt response
        """
        prepared_request = self._delete_attachment(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            attachment_id=attachment_id,
            hash_arg=hash_arg,
            phi_namespace=phi_namespace,
            x_ambrahealth_job_id=x_ambrahealth_job_id,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def video(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        image_uid: str,
        image_version: str,
        reencode_video: Optional[bool] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
        """Gets a study encapsulated video.

        URL: /study/{namespace}/{studyUid}/image/{imageUid}/version/{imageVersion}/video?sid={sid}&reencode_video={0,1}

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param image_uid: Image uid (Required).
        :param image_version: Image version (Required).
        :param reencode_video: An integer of value 1 or 0.
        :param only_prepare: Get prepared request.

        :returns: Video response
        """
        prepared_request = self._video(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
            reencode_video=reencode_video,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def split(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
        to_namespace: Optional[str] = None,
        series_uid: Optional[str] = None,
        delete_series_from_original: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: Split study response
        """
        prepared_request = self._split(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            phi_namespace=phi_namespace,
            to_namespace=to_namespace,
            series_uid=series_uid,
            delete_series_from_original=delete_series_from_original,
        )
        if only_prepare is True:
            return prepared_request
        # new study uid
        return prepared_request.execute()

    def merge(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        secondary_study_uid: str,
        delete_secondary_study: Optional[bool] = None,
        series_uids: Optional[str] = None,
        x_ambrahealth_job_id: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: Actually empty response
        """
        prepared_request = self._merge(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            secondary_study_uid=secondary_study_uid,
            delete_secondary_study=delete_secondary_study,
            series_uids=series_uids,
            x_ambrahealth_job_id=x_ambrahealth_job_id,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    # Nicholas Byers dg1572443133:
    # with is_ai=true, you should expect the tag (0012,0063)
    # De-Identification Method to then read "SYSTEM" (instead of "MANUAL")
    def anonymize(
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
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :returns: Anonymize study response

        The request entity is a JSON object specifying the regions
        to be obscured. Regions may be specified at study, series,
        or instance level; but only the highest matching level
        containing a regions field will be used.
        """
        prepared_request = self._anonymize(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            region=region,
            phi_namespace=phi_namespace,
            to_namespace=to_namespace,
            new_study_uid=new_study_uid,
            keep_image_uids=keep_image_uids,
            color=color,
            x_ambrahealth_job_id=x_ambrahealth_job_id,
            is_ai=is_ai,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def crop(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        region: Dict[str, Any],
        phi_namespace: Optional[str] = None,
        to_namespace: Optional[str] = None,
        new_study_uid: Optional[str] = None,
        keep_image_uids: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

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
        prepared_request = self._crop(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            region=region,
            phi_namespace=phi_namespace,
            to_namespace=to_namespace,
            new_study_uid=new_study_uid,
            keep_image_uids=keep_image_uids,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def cache(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
        """Clears the image and metadata cache for the indicated study.

        URL: /study/{namespace}/{studyUid}/cache

        :param engine_fqdn: Engine FQDN (Required).
        :param namespace: Namespace (Required).
        :param study_uid: Study uid (Required).
        :param only_prepare: Get prepared request.

        :returns: Cache study response
        """
        prepared_request = self._cache(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def hl7_to_sr(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        hl7uuid: str,
        phi_namespace: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.


        :returns: hl7_to_sr result
        """
        prepared_request = self._hl7_to_sr(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            hl7uuid=hl7uuid,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def clone(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
        new_image_uids: Optional[bool] = None,
        new_series_uids: Optional[bool] = None,
        x_ambrahealth_job_id: Optional[str] = None,
        only_prepare: bool = False,
    ) -> Union[Response, PreparedRequest]:
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
        :param only_prepare: Get prepared request.

        :return: new study uid
        """
        prepared_request = self._clone(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            phi_namespace=phi_namespace,
            new_image_uids=new_image_uids,
            new_series_uids=new_series_uids,
            x_ambrahealth_job_id=x_ambrahealth_job_id,
        )
        if only_prepare is True:
            return prepared_request
        return prepared_request.execute()

    def create_rt(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        body: str,
        phi_namespace: Optional[str] = None,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[Box, Response, PreparedRequest]:
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
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :return: Image attributes
        """
        prepared_request = self._create_rt(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            phi_namespace=phi_namespace,
            body=body,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()

        if use_box is True:
            return Box(response.json())
        return response

    def image_dicomweb(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        series_uid: str,
        image_uid: str,
        phi_namespace: Optional[str] = None,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[Box, Response, PreparedRequest]:
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
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: A JSON representation of a DICOM according to the DICOMWeb standard,
            omitting any bulkdata, pixeldata, or other binary fields.
        """
        prepared_request = self._image_dicomweb(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            series_uid=series_uid,
            image_uid=image_uid,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()

        if use_box is True:
            return Box(response.json())
        return response

    def series_dicomweb(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        series_uid: str,
        phi_namespace: Optional[str] = None,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[BoxList, Response, PreparedRequest]:
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
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: A JSON representation of a series of DICOM(s) according to the DICOMWeb standard,
            omitting any bulkdata, pixeldata, or other binary fields.
        """
        prepared_request = self._series_dicomweb(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            series_uid=series_uid,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()

        if use_box is True:
            return BoxList(response.json())
        return response

    def study_dicomweb(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        phi_namespace: Optional[str] = None,
        use_box: bool = True,
        only_prepare: bool = False,
    ) -> Union[BoxList, Response, PreparedRequest]:
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
        :param use_box: Use box for response.
        :param only_prepare: Get prepared request.

        :returns: A JSON representation of an entire study of DICOM(s) according to the DICOMWeb standard,
            omitting any bulkdata, pixeldata, or other binary fields.
        """
        prepared_request = self._study_dicomweb(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            phi_namespace=phi_namespace,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()

        if use_box is True:
            return BoxList(response.json())
        return response

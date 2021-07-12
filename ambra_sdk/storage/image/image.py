"""Storage image namespace."""

from typing import Optional, Union

from box import Box
from requests import Response

from ambra_sdk.storage.image.base_image import BaseImage
from ambra_sdk.storage.request import PreparedRequest
from ambra_sdk.types import RequestsFileType


class Image(BaseImage):
    """Storage Image commands."""

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
        prepared_request = self._upload(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            opened_file=opened_file,
            study_uid=study_uid,
            x_ambrahealth_job_id=x_ambrahealth_job_id,
        )
        if only_prepare is True:
            return prepared_request
        response = prepared_request.execute()
        if use_box is True:
            return Box(response.json())
        return response

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
        return prepared_request.execute()

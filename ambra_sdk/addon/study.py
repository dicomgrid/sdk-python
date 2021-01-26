"""Study addon namespace."""

import uuid as uuid_lib
from contextlib import suppress
from io import BytesIO
from pathlib import Path
from time import monotonic
from typing import Any, Dict, List, Mapping, NamedTuple, Optional, Tuple, Union

import pydicom
from box import Box

from ambra_sdk.exceptions.service import (
    NotFound,
    NotPermitted,
    PreconditionFailed,
)
from ambra_sdk.models import Study as StudyModel
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.ws import WSManager


class UploadedImageParams(NamedTuple):
    """Image object."""

    study_uid: str
    image_uid: str
    image_version: str
    namespace: str
    attr: Any


class Study:  # NOQA:WPS214
    """Study addon namespace."""

    def __init__(self, api):
        """Init.

        :param api: base api
        """
        self._api = api

    def upload_dicom(
        self,
        dicom_path: Path,
        namespace_id: str,
        engine_fqdn: Optional[str] = None,
    ) -> UploadedImageParams:
        """Upload dicom to namespace.

        :param dicom_path: path to dicom
        :param namespace_id: uploading to namespace
        :param engine_fqdn: fqdn (if None gets namespace fqdn)

        :return: uploaded image params
        """
        if engine_fqdn is None:
            engine_fqdn = self._namespace_fqdn(namespace_id)

        with open(dicom_path, 'rb') as dicom_file:
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

    def upload(
        self,
        study_dir: Path,
        namespace_id: str,
    ) -> Tuple[str, List[UploadedImageParams]]:
        """Upload study to namespace.

        :param study_dir: path to study dir
        :param namespace_id: uploading to namespace

        :raises ValueError: Study dir is not directory
        :return: list of image params
        """
        if not study_dir.is_dir():
            raise ValueError('study_dir is not directory')

        images_params = []

        first_dicom = next(study_dir.glob('**/*.dcm'), None)
        if first_dicom is None:
            raise ValueError('study_dir is empty')

        ds = pydicom.dcmread(str(first_dicom))
        patient_name = ds.PatientName
        study_uid = ds.StudyInstanceUID
        study_time = ds.StudyTime
        study_date = ds.StudyDate

        # create new study
        response_data = self._api.Study.add(
            study_uid=study_uid,
            study_date=study_date,
            study_time=study_time,
            patient_name=patient_name,
            storage_namespace=namespace_id,
            phi_namespace=namespace_id,
            thin=None,
        ).get()
        engine_fqdn = response_data.engine_fqdn
        uuid: str = response_data.uuid

        # upload images
        for dicom_path in study_dir.glob('**/*.dcm'):
            images_params.append(
                self.upload_dicom(
                    dicom_path,
                    namespace_id,
                    engine_fqdn,
                ),
            )
        # then sync data
        # In api.html sync method have not uuid param...
        # So we use this hardcode:
        request = self._api.Study.sync(image_count=1)
        request.request_data['uuid'] = uuid  # NOQA:WPS437
        request.get()

        return uuid, images_params

    def wait(
        self,
        study_uid: str,
        namespace_id: str,
        timeout: float,
        ws_timeout: int,
    ) -> Box:
        """Wait study in namespace.

        :param study_uid: study_uid
        :param namespace_id: namespace
        :param timeout: time for waiting new study
        :param ws_timeout: time for waiting in socket
        :raises TimeoutError: if study not ready by timeout
        :return: Study box object
        """
        ws_url = self._api.ws_url
        ws_manager = WSManager(ws_url)
        study = None
        start = monotonic()

        channel_name = 'study.{namespace_id}'.format(namespace_id=namespace_id)
        sid = self._api.sid

        with ws_manager.channel(sid, channel_name) as ws:
            while True:
                if monotonic() - start >= timeout:
                    break
                with suppress(NotFound):
                    study = self._api.Study.get(
                        study_uid=study_uid,
                        storage_namespace=namespace_id,
                    ).get()

                if study and study.phantom == 0:
                    break

                with suppress(TimeoutError):
                    ws.wait_for_event(
                        channel_name,
                        sid,
                        'READY',
                        timeout=ws_timeout,
                    )
        if not study:
            raise TimeoutError
        return study

    def wait_job(
        self,
        job_id: str,
        namespace_id: str,
        timeout: float,
        ws_timeout: int,
    ):
        """Wait job.

        :param job_id: job id
        :param namespace_id: job namespace_id
        :param timeout: time for waiting new study
        :param ws_timeout: time for waiting in socket

        :raises TimeoutError: if job not ready by timeout
        :raises RuntimeError: Bad answer from ws
        """
        errors_mapping: Mapping[  # NOQA:WPS234
            Union[Tuple[str, Optional[str]], str],
            PreconditionFailed,
        ] = {
            ('NOT_FOUND', None): NotFound('The job can not be found'),
            ('NOT_PERMITTED', None): NotPermitted(
                'The user is not permitted to access this job',
            ),
        }
        request_data = {
            'id': job_id,
        }
        get_job_query = QueryO(
            api=self._api,
            url='/job/get',
            request_data=request_data,
            errors_mapping=errors_mapping,
            required_sid=True,
        )

        ws_url = self._api.ws_url
        ws_manager = WSManager(ws_url)
        start = monotonic()

        # K. Pustovalov: job channel have form job.namespace
        channel_name = 'job.{namespace_id}'.format(namespace_id=namespace_id)
        sid = self._api.sid

        job_is_ready = False
        with ws_manager.channel(sid, channel_name) as ws:
            while True:
                if monotonic() - start >= timeout:
                    break
                with suppress(NotFound):
                    job_status = get_job_query.get()
                    if job_status['state'] != 'DONE':
                        raise RuntimeError(  # NOQA:WPS220
                            'Unknown job status {job_status}'.format(
                                job_status=job_status['state'],
                            ),
                        )
                    job_is_ready = True
                    break
                with suppress(TimeoutError):
                    ws.wait_for_event(
                        channel_name,
                        sid,
                        'DONE',
                        timeout=ws_timeout,
                    )
        if job_is_ready is False:
            raise TimeoutError

    def upload_and_get(
        self,
        study_dir: Path,
        namespace_id: str,
        timeout: float = 200.0,
        ws_timeout: int = 5,
    ) -> Box:
        """Upload study to namespace.

        :param study_dir: path to study dir
        :param namespace_id: uploading to namespace
        :param timeout: time for waiting new study
        :param ws_timeout: time for waiting in socket
        :return: Study box object
        """
        uuid, images_params = self.upload(
            study_dir,
            namespace_id,
        )
        study_uid = images_params[0].study_uid
        return self.wait(
            study_uid=study_uid,
            namespace_id=namespace_id,
            timeout=timeout,
            ws_timeout=ws_timeout,
        )

    def duplicate_and_get(
        self,
        uuid: str,
        namespace_id: str,
        include_attachments: bool = False,
        timeout: float = 200.0,
        ws_timeout: int = 5,
    ) -> Box:
        """Duplicate study to namespace.

        :param uuid: study_uuid
        :param namespace_id: to namespace_id
        :param include_attachments: include attachments
        :param timeout: waiting timeout
        :param ws_timeout: waiting from ws timeout

        :return: duplicated study
        """
        include_attachments_int = int(include_attachments)

        from_study_uid = self._api.Study \
            .get(uuid=uuid) \
            .only(StudyModel.study_uid) \
            .get() \
            .study_uid

        self._api.Study.duplicate(
            uuid=uuid,
            namespace_id=namespace_id,
            include_attachments=include_attachments_int,
        ).get()
        return self.wait(
            study_uid=from_study_uid,
            namespace_id=namespace_id,
            timeout=timeout,
            ws_timeout=ws_timeout,
        )

    def dicom(
        self,
        namespace_id: str,
        study_uid: str,
        image_uid: str,
        image_version: str = '*',
        engine_fqdn: Optional[str] = None,
        pretranscode: Optional[bool] = None,
    ):
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

    def anonymize_and_wait(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        region: Dict[str, Any],
        to_namespace: Optional[str] = None,
        new_study_uid: Optional[str] = None,
        keep_image_uids: Optional[str] = None,
        color: Optional[str] = None,
        only_prepare: bool = False,
        x_ambrahealth_job_id: Optional[str] = None,
        timeout: float = 200.0,
        ws_timeout: int = 5,
    ) -> str:
        """Start anonymization and wait when it completed.

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
        :param only_prepare: Get prepared request.
        :param x_ambrahealth_job_id: X-AmbraHealth-Job-Id headers argument
        :param timeout: waiting timeout
        :param ws_timeout: waiting from ws timeout

        :returns: new study uid
        """
        if x_ambrahealth_job_id is None:
            x_ambrahealth_job_id = str(uuid_lib.uuid4())
        anonymize = self._api.Storage.Study.anonymize(
            engine_fqdn,
            namespace,
            study_uid,
            region,
            to_namespace,
            new_study_uid,
            keep_image_uids,
            color,
            only_prepare,
            x_ambrahealth_job_id,
        )
        anonymized_study_uid: str = anonymize.text

        # A. Matveev: job namespace is initial namespace
        self.wait_job(
            job_id=x_ambrahealth_job_id,
            namespace_id=namespace,
            timeout=timeout,
            ws_timeout=ws_timeout,
        )
        return anonymized_study_uid

    def anonymize_and_get(
        self,
        engine_fqdn: str,
        namespace: str,
        study_uid: str,
        region: Dict[str, Any],
        to_namespace: Optional[str] = None,
        new_study_uid: Optional[str] = None,
        keep_image_uids: Optional[str] = None,
        color: Optional[str] = None,
        only_prepare: bool = False,
        x_ambrahealth_job_id: Optional[str] = None,
        timeout: float = 200.0,
        ws_timeout: int = 5,
    ) -> Box:
        """Start anonymization wait and get anonymized study.

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
        :param only_prepare: Get prepared request.
        :param x_ambrahealth_job_id: X-AmbraHealth-Job-Id headers argument
        :param timeout: waiting timeout
        :param ws_timeout: waiting from ws timeout

        :raises TimeoutError: if job or study not ready by timeout
        :returns: new study
        """
        start = monotonic()
        new_study_uid = self.anonymize_and_wait(
            engine_fqdn,
            namespace,
            study_uid,
            region,
            to_namespace,
            new_study_uid,
            keep_image_uids,
            color,
            only_prepare,
            x_ambrahealth_job_id,
            timeout,
            ws_timeout,
        )
        spend_time = monotonic() - start
        rest_timeout = timeout - spend_time

        if rest_timeout <= 0:
            raise TimeoutError
        new_namespace = to_namespace if to_namespace is not None else namespace
        return self.wait(
            study_uid=new_study_uid,
            namespace_id=new_namespace,
            timeout=rest_timeout,
            ws_timeout=ws_timeout,
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

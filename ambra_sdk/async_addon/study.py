"""Study addon namespace."""

from contextlib import suppress
from itertools import chain
from pathlib import Path
from time import monotonic
from typing import Any, Dict, Iterator, List, Optional, Tuple

import pydicom
from box import Box

from ambra_sdk.addon.dicom import UploadedImageParams
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.models import Study as StudyModel
from ambra_sdk.service.ws import AsyncWSManager


class Study:  # NOQA:WPS214
    """Study addon namespace."""

    def __init__(self, api):
        """Init.

        :param api: base api
        """
        self._api = api

    async def upload_dir(
        self,
        *,
        study_dir: Path,
        namespace_id: str,
    ) -> Tuple[str, List[UploadedImageParams]]:
        """Upload study to namespace from path.

        :param study_dir: path to study dir
        :param namespace_id: uploading to namespace

        :raises ValueError: Study dir is not directory
        :return: list of image params
        """
        if not study_dir.is_dir():
            raise ValueError('study_dir is not directory')

        return await self.upload_paths(
            dicom_paths=study_dir.glob('**/*.dcm'),
            namespace_id=namespace_id,
        )

    async def upload_paths(
        self,
        *,
        dicom_paths: Iterator[Path],
        namespace_id: str,
    ) -> Tuple[str, List[UploadedImageParams]]:
        """Upload study to namespace from dicoms iterator.

        :param dicom_paths: iterator of dicom paths
        :param namespace_id: uploading to namespace

        :raises ValueError: Study dir is not directory
        :return: list of image params
        """
        images_params = []

        first_dicom_path = next(dicom_paths, None)
        if first_dicom_path is None:
            raise ValueError('Dicoms iterator is empty')

        # In pydicom we can pass file path object
        # But in AI we use old version of pydicom.
        # For this version we can pass only fp or str.
        ds = pydicom.dcmread(fp=str(first_dicom_path), stop_before_pixels=True)
        patient_name = ds.PatientName
        study_uid = ds.StudyInstanceUID
        study_time = ds.StudyTime
        study_date = ds.StudyDate

        # create new study
        response_data = await self._api.Study.add(
            study_uid=study_uid,
            study_date=study_date,
            study_time=study_time,
            patient_name=patient_name,
            storage_namespace=namespace_id,
            phi_namespace=namespace_id,
        ).get()
        engine_fqdn = response_data.engine_fqdn
        uuid: str = response_data.uuid

        # upload images
        for dicom_path in chain((first_dicom_path, ), dicom_paths):
            with dicom_path.open(mode='rb') as dicom:
                images_params.append(
                    await self._api.Addon.Dicom.upload(
                        dicom_file=dicom,
                        namespace_id=namespace_id,
                        engine_fqdn=engine_fqdn,
                    ),
                )

        # then sync data
        # In api.html sync method have not uuid param...
        # So we use this hardcode:
        request = self._api.Study.sync(image_count=1)
        request_data = request.request_args.data or {}
        request_data['uuid'] = uuid  # NOQA:WPS437
        request.request_args.data = request_data  # NOQA:WPS110
        await request.get()

        return uuid, images_params

    async def wait(
        self,
        *,
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
        ws_manager = AsyncWSManager(ws_url)
        study = None
        start = monotonic()

        channel_name = 'study.{namespace_id}'.format(namespace_id=namespace_id)
        sid = await self._api.get_sid()

        async with ws_manager.channel(sid, channel_name) as ws:
            while True:
                if monotonic() - start >= timeout:
                    break
                with suppress(NotFound):
                    study = await self._api.Study.get(
                        study_uid=study_uid,
                        storage_namespace=namespace_id,
                    ).get()

                if study and study.phantom == 0:
                    break

                with suppress(TimeoutError):
                    await ws.wait_for_event(
                        channel_name,
                        sid,
                        'READY',
                        timeout=ws_timeout,
                    )
        if not study:
            raise TimeoutError
        return study

    async def upload_dir_and_get(
        self,
        *,
        study_dir: Path,
        namespace_id: str,
        timeout: float = 200.0,
        ws_timeout: int = 5,
    ) -> Box:
        """Upload study from dir and get.

        :param study_dir: path to study dir
        :param namespace_id: uploading to namespace
        :param timeout: time for waiting new study
        :param ws_timeout: time for waiting in socket
        :return: Study box object
        """
        uuid, images_params = await self.upload_dir(
            study_dir=study_dir,
            namespace_id=namespace_id,
        )

        study_uid = images_params[0].study_uid
        return await self.wait(
            study_uid=study_uid,
            namespace_id=namespace_id,
            timeout=timeout,
            ws_timeout=ws_timeout,
        )

    async def upload_paths_and_get(
        self,
        *,
        dicom_paths: Iterator[Path],
        namespace_id: str,
        timeout: float = 200.0,
        ws_timeout: int = 5,
    ) -> Box:
        """Upload study from dir and get.

        :param dicom_paths: iterator of dicom paths
        :param namespace_id: uploading to namespace
        :param timeout: time for waiting new study
        :param ws_timeout: time for waiting in socket
        :return: Study box object
        """
        uuid, images_params = await self.upload_paths(
            dicom_paths=dicom_paths,
            namespace_id=namespace_id,
        )

        study_uid = images_params[0].study_uid
        return await self.wait(
            study_uid=study_uid,
            namespace_id=namespace_id,
            timeout=timeout,
            ws_timeout=ws_timeout,
        )

    async def duplicate_and_get(
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

        from_study_obj = await self._api.Study \
            .get(uuid=uuid) \
            .only(StudyModel.study_uid) \
            .get()

        from_study_uid = from_study_obj.study_uid

        await self._api.Study.duplicate(
            uuid=uuid,
            namespace_id=namespace_id,
            include_attachments=include_attachments_int,
        ).get()
        return await self.wait(
            study_uid=from_study_uid,
            namespace_id=namespace_id,
            timeout=timeout,
            ws_timeout=ws_timeout,
        )

    async def anonymize_and_wait(
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
        timeout: float = 200.0,
        ws_timeout: int = 5,
    ) -> str:
        """Start anonymization and wait when it completed.

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
        :param timeout: waiting timeout
        :param ws_timeout: waiting from ws timeout

        :returns: new study uid
        """
        anonymize = await self._api.Addon.Job.wait_completion(
            self._api.Storage.Study.anonymize,
            timeout=timeout,
            ws_timeout=ws_timeout,
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            region=region,
            phi_namespace=phi_namespace,
            to_namespace=to_namespace,
            new_study_uid=new_study_uid,
            keep_image_uids=keep_image_uids,
            color=color,
            only_prepare=only_prepare,
            x_ambrahealth_job_id=x_ambrahealth_job_id,
            is_ai=is_ai,
        )
        anonymized_study_uid: str = await anonymize.text()
        return anonymized_study_uid  # NOQA:WPS331

    async def anonymize_and_get(
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
        timeout: float = 200.0,
        ws_timeout: int = 5,
    ) -> Box:
        """Start anonymization wait and get anonymized study.

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
        :param timeout: waiting timeout
        :param ws_timeout: waiting from ws timeout

        :raises TimeoutError: if job or study not ready by timeout
        :returns: new study
        """
        start = monotonic()
        anonymize = await self._api.Addon.Job.wait_completion(
            self._api.Storage.Study.anonymize,
            timeout=timeout,
            ws_timeout=ws_timeout,
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
            region=region,
            phi_namespace=phi_namespace,
            to_namespace=to_namespace,
            new_study_uid=new_study_uid,
            keep_image_uids=keep_image_uids,
            color=color,
            only_prepare=only_prepare,
            x_ambrahealth_job_id=x_ambrahealth_job_id,
            is_ai=is_ai,
        )
        anonymized_study_uid: str = await anonymize.text()
        spend_time = monotonic() - start
        rest_timeout = timeout - spend_time

        if rest_timeout <= 0:
            raise TimeoutError
        new_namespace = to_namespace if to_namespace is not None else namespace
        return await self.wait(
            study_uid=anonymized_study_uid,
            namespace_id=new_namespace,
            timeout=rest_timeout,
            ws_timeout=ws_timeout,
        )

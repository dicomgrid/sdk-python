import inspect
from pathlib import Path

import pytest
from dynaconf import settings


@pytest.mark.asyncio
class TestAsyncAddonStudy:
    """Test addon study namespace."""

    async def test_upload_dir(
        self,
        async_api,
        async_account,
        async_auto_remove,
    ):
        """Test study upload from path method."""
        study_dir = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only')

        namespace_id = async_account.account.namespace_id
        _, images_params = await async_api.Addon.Study.upload_dir(
            study_dir=study_dir,
            namespace_id=namespace_id,
        )
        image_params = images_params[0]
        new_study = await async_api.Addon.Study.wait(
            study_uid=image_params.study_uid,
            namespace_id=namespace_id,
            timeout=settings.API.upload_study_timeout,
            ws_timeout=settings.API.upload_study_timeout,
        )
        assert new_study
        async_auto_remove(new_study)

    async def test_upload_paths(
        self,
        async_api,
        async_account,
        async_auto_remove,
    ):
        """Test study upload dicoms method."""
        study_dir = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only')

        namespace_id = async_account.account.namespace_id
        _, images_params = await async_api.Addon.Study.upload_paths(
            dicom_paths=study_dir.glob('**/*.dcm'),
            namespace_id=namespace_id,
        )
        image_params = images_params[0]
        new_study = await async_api.Addon.Study.wait(
            study_uid=image_params.study_uid,
            namespace_id=namespace_id,
            timeout=settings.API.upload_study_timeout,
            ws_timeout=settings.API.upload_study_timeout,
        )
        assert new_study
        async_auto_remove(new_study)

    async def test_upload_dir_and_get(
        self,
        async_api,
        async_account,
        async_auto_remove,
    ):
        """Test study upload dir and get method."""
        study_dir = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only')

        namespace_id = async_account.account.namespace_id

        new_study = await async_api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir,
            namespace_id=namespace_id,
            timeout=settings.API.upload_study_timeout,
            ws_timeout=settings.API.upload_study_timeout,
        )
        assert new_study
        async_auto_remove(new_study)

    async def test_upload_paths_and_get(
        self,
        async_api,
        async_account,
        async_auto_remove,
    ):
        """Test study upload paths and get method."""
        study_dir = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only')

        namespace_id = async_account.account.namespace_id

        new_study = await async_api.Addon.Study.upload_paths_and_get(
            dicom_paths=study_dir.glob('**/*.dcm'),
            namespace_id=namespace_id,
            timeout=settings.API.upload_study_timeout,
            ws_timeout=settings.API.upload_study_timeout,
        )
        assert new_study
        async_auto_remove(new_study)

    async def test_duplicate_and_get(
        self,
        async_api,
        async_account,
        async_readonly_study,
        async_create_group,
    ):
        """Test duplicate study and get."""
        group = await async_create_group()
        duplicated_study = await async_api.Addon.Study.duplicate_and_get(
            uuid=async_readonly_study.uuid,
            namespace_id=group.namespace_id,
            include_attachments=False,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )

        assert duplicated_study.uuid != async_readonly_study.uuid
        assert duplicated_study.study_uid == async_readonly_study.study_uid
        assert duplicated_study.phi_namespace == group.namespace_id
        await async_api.Study.delete(uuid=duplicated_study.uuid).get()

    async def test_duplicate_fixture(
        self,
        async_api,
        async_readonly_study,
        async_duplicate,
    ):
        """Test duplicate study fixture."""
        duplicated_study = await async_duplicate(async_readonly_study.uuid)

        assert duplicated_study.uuid != async_readonly_study.uuid
        assert duplicated_study.study_uid == async_readonly_study.study_uid

    def test_anonymize_and_wait_signature(self, async_api):
        """Test anonymize_and_wait signature."""
        anonymize_and_wait_s = inspect.signature(
            async_api.Addon.Study.anonymize_and_wait,
        )
        anonymize_s = inspect.signature(async_api.Storage.Study.anonymize)
        assert set(anonymize_and_wait_s.parameters) - \
            {'timeout', 'ws_timeout'} == set(anonymize_s.parameters)

    async def test_anonymize_and_wait(
        self,
        async_api,
        async_readonly_study,
        async_auto_remove,
        async_storage_auto_remove,
    ):
        """Test anonymize_and_wait."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid
        series_uid = '1.2.840.113619.2.278.3.2831165743.908.1345078604.948'

        region = {
            'series': {
                series_uid: {
                    'regions': [
                        {
                            'x': 10,
                            'y': 10,
                            'width': 30,
                            'height': 40,
                        },
                    ],
                },
            },
        }
        new_study_uid = await async_api.Addon.Study.anonymize_and_wait(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            to_namespace=storage_namespace,
            study_uid=study_uid,
            region=region,
            color='121197149',
        )
        assert new_study_uid != study_uid

        async_storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            new_study_uid,
        )

        new_study = await async_api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        async_auto_remove(new_study)

    def test_anonymize_and_get_signature(self, async_api):
        """Test anonymize_and_get signature."""
        anonymize_and_get_s = inspect.signature(
            async_api.Addon.Study.anonymize_and_get,
        )
        anonymize_s = inspect.signature(async_api.Storage.Study.anonymize)
        assert set(anonymize_and_get_s.parameters) - \
            {'timeout', 'ws_timeout'} == set(anonymize_s.parameters)

    async def test_anonymize_and_get(
        self,
        async_api,
        async_readonly_study,
        async_auto_remove,
        async_storage_auto_remove,
    ):
        """Test anonymize_and_get."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid
        series_uid = '1.2.840.113619.2.278.3.2831165743.908.1345078604.948'

        region = {
            'series': {
                series_uid: {
                    'regions': [
                        {
                            'x': 10,
                            'y': 10,
                            'width': 30,
                            'height': 40,
                        },
                    ],
                },
            },
        }
        new_study = await async_api.Addon.Study.anonymize_and_get(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            to_namespace=storage_namespace,
            study_uid=study_uid,
            region=region,
            color='121197149',
        )
        assert new_study.study_uid != study_uid

        async_storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            new_study.study_uid,
        )
        async_auto_remove(new_study)

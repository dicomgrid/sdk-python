import inspect
import tempfile
import zipfile
from pathlib import Path

import pytest
from dynaconf import settings


class TestAddonStudy:
    """Test addon study namespace."""

    def test_upload_dir(
        self,
        api,
        account,
        auto_remove,
    ):
        """Test study upload from path method."""
        study_dir = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only')

        namespace_id = account.account.namespace_id
        _, images_params = api.Addon.Study.upload_dir(
            study_dir=study_dir,
            namespace_id=namespace_id,
        )
        image_params = images_params[0]
        new_study = api.Addon.Study.wait(
            study_uid=image_params.study_uid,
            namespace_id=namespace_id,
            timeout=settings.API.upload_study_timeout,
            ws_timeout=settings.API.upload_study_timeout,
        )
        assert new_study
        auto_remove(new_study)

    def test_upload_paths(
        self,
        api,
        account,
        auto_remove,
    ):
        """Test study upload dicoms method."""
        study_dir = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only')

        namespace_id = account.account.namespace_id
        _, images_params = api.Addon.Study.upload_paths(
            dicom_paths=study_dir.glob('**/*.dcm'),
            namespace_id=namespace_id,
        )
        image_params = images_params[0]
        new_study = api.Addon.Study.wait(
            study_uid=image_params.study_uid,
            namespace_id=namespace_id,
            timeout=settings.API.upload_study_timeout,
            ws_timeout=settings.API.upload_study_timeout,
        )
        assert new_study
        auto_remove(new_study)

    def test_upload_dir_and_get(
        self,
        api,
        account,
        auto_remove,
    ):
        """Test study upload dir and get method."""
        study_dir = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only')

        namespace_id = account.account.namespace_id

        new_study = api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir,
            namespace_id=namespace_id,
            timeout=settings.API.upload_study_timeout,
            ws_timeout=settings.API.upload_study_timeout,
        )
        assert new_study
        auto_remove(new_study)

    def test_upload_paths_and_get(
        self,
        api,
        account,
        auto_remove,
    ):
        """Test study upload paths and get method."""
        study_dir = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only')

        namespace_id = account.account.namespace_id

        new_study = api.Addon.Study.upload_paths_and_get(
            dicom_paths=study_dir.glob('**/*.dcm'),
            namespace_id=namespace_id,
            timeout=settings.API.upload_study_timeout,
            ws_timeout=settings.API.upload_study_timeout,
        )
        assert new_study
        auto_remove(new_study)

    def test_duplicate_and_get(
        self,
        api,
        account,
        readonly_study,
        create_group,
    ):
        """Test duplicate study and get."""
        group = create_group()
        duplicated_study = api.Addon.Study.duplicate_and_get(
            uuid=readonly_study.uuid,
            namespace_id=group.namespace_id,
            include_attachments=False,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )

        assert duplicated_study.uuid != readonly_study.uuid
        assert duplicated_study.study_uid == readonly_study.study_uid
        assert duplicated_study.phi_namespace == group.namespace_id
        api.Study.delete(uuid=duplicated_study.uuid).get()

    def test_duplicate_fixture(
        self,
        api,
        readonly_study,
        duplicate,
    ):
        """Test duplicate study fixture."""
        duplicated_study = duplicate(readonly_study.uuid)

        assert duplicated_study.uuid != readonly_study.uuid
        assert duplicated_study.study_uid == readonly_study.study_uid

    def test_anonymize_and_wait_signature(self, api):
        """Test anonymize_and_wait signature."""
        anonymize_and_wait_s = inspect.signature(
            api.Addon.Study.anonymize_and_wait,
        )
        anonymize_s = inspect.signature(api.Storage.Study.anonymize)
        assert set(anonymize_and_wait_s.parameters) - \
            {'timeout', 'ws_timeout'} == set(anonymize_s.parameters)

    def test_anonymize_and_wait(
        self,
        api,
        readonly_study,
        auto_remove,
        storage_auto_remove,
    ):
        """Test anonymize_and_wait."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid
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
        new_study_uid = api.Addon.Study.anonymize_and_wait(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            to_namespace=storage_namespace,
            phi_namespace=readonly_study.phi_namespace,
            study_uid=study_uid,
            region=region,
            color='121197149',
        )
        assert new_study_uid != study_uid

        storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            new_study_uid,
        )

        new_study = api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        auto_remove(new_study)

    def test_anonymize_and_get_signature(self, api):
        """Test anonymize_and_get signature."""
        anonymize_and_get_s = inspect.signature(
            api.Addon.Study.anonymize_and_get,
        )
        anonymize_s = inspect.signature(api.Storage.Study.anonymize)
        assert set(anonymize_and_get_s.parameters) - \
            {'timeout', 'ws_timeout'} == set(anonymize_s.parameters)

    def test_anonymize_and_get(
        self,
        api,
        readonly_study,
        auto_remove,
        storage_auto_remove,
    ):
        """Test anonymize_and_get."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid
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
        new_study = api.Addon.Study.anonymize_and_get(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            to_namespace=storage_namespace,
            phi_namespace=readonly_study.phi_namespace,
            study_uid=study_uid,
            region=region,
            color='121197149',
        )
        assert new_study.study_uid != study_uid

        storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            new_study.study_uid,
        )
        auto_remove(new_study)

    def test_upload_dir_with_big_file(
        self,
        api,
        account,
        auto_remove,
    ):
        """Test study upload using multipart algorithm."""
        study_zip = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'big_one.zip')

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            with zipfile.ZipFile(study_zip, 'r') as zip_ref:
                zip_ref.extractall(tmp_dir_name)
            namespace_id = account.account.namespace_id
            _, images_params = api.Addon.Study.upload_dir(
                study_dir=Path(tmp_dir_name),
                namespace_id=namespace_id,
            )
            image_params = images_params[0]
            new_study = api.Addon.Study.wait(
                study_uid=image_params.study_uid,
                namespace_id=namespace_id,
                timeout=settings.API.upload_study_timeout,
                ws_timeout=settings.API.upload_study_timeout,
            )
            assert new_study
            auto_remove(new_study)


class TestAddonStudyDeprecated:
    """Test addon study namespace deprecated methods."""

    @pytest.mark.deprecated
    def test_upload_dicom(
        self,
        api,
        account,
    ):
        """Test study upload image method."""
        dicom_path = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only', 'series_1', 'IMG00001.dcm')

        namespace_id = account.account.namespace_id
        engine_fqdn = api \
            .Namespace \
            .engine_fqdn(namespace_id=namespace_id) \
            .get() \
            .engine_fqdn

        image_params = api.Addon.Study.upload_dicom(
            dicom_path,
            namespace_id,
            engine_fqdn,
        )
        study_uid = '1.2.840.10008.1.142353.149743743.367518058.1111111111'  # NOQA:E501
        image_uid = '1.2.840.113619.2.278.3.2831165743.908.1345078604.949.1'
        assert image_params.study_uid == study_uid
        assert image_params.image_uid == image_uid
        assert image_params.image_version
        assert image_params.namespace == namespace_id
        assert image_params.attr

    @pytest.mark.deprecated
    def test_upload_dicom_without_fqdn(
        self,
        api,
        account,
    ):
        """Test study upload image method.

        Case: engine_fqdn is None
        """
        dicom_path = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only', 'series_1', 'IMG00001.dcm')
        namespace_id = account.account.namespace_id
        image_params = api.Addon.Study.upload_dicom(dicom_path, namespace_id)
        study_uid = '1.2.840.10008.1.142353.149743743.367518058.1111111111'  # NOQA:E501

        image_uid = '1.2.840.113619.2.278.3.2831165743.908.1345078604.949.1'
        assert image_params.study_uid == study_uid
        assert image_params.image_uid == image_uid
        assert image_params.image_version
        assert image_params.namespace == namespace_id
        assert image_params.attr

    @pytest.mark.deprecated
    def test_upload(
        self,
        api,
        account,
        auto_remove,
    ):
        """Test study upload image method."""
        study_dir = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only')

        namespace_id = account.account.namespace_id
        _, images_params = api.Addon.Study.upload(
            study_dir=study_dir,
            namespace_id=namespace_id,
        )
        image_params = images_params[0]
        new_study = api.Addon.Study.wait(
            study_uid=image_params.study_uid,
            namespace_id=namespace_id,
            timeout=settings.API.upload_study_timeout,
            ws_timeout=settings.API.upload_study_timeout,
        )
        assert new_study
        auto_remove(new_study)

    @pytest.mark.deprecated
    def test_upload_and_get(
        self,
        api,
        account,
        auto_remove,
    ):
        """Test study upload and get method."""
        study_dir = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only')

        namespace_id = account.account.namespace_id

        new_study = api.Addon.Study.upload_and_get(
            study_dir=study_dir,
            namespace_id=namespace_id,
            timeout=settings.API.upload_study_timeout,
            ws_timeout=settings.API.upload_study_timeout,
        )
        assert new_study
        auto_remove(new_study)

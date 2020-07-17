from pathlib import Path

from dynaconf import settings


class TestAddonStudy:
    """Test addon study namespace."""

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

        assert namespace_id in api.Addon.Study._cached_fqdns

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

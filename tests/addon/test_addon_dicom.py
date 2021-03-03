from pathlib import Path

from pydicom.dataset import FileDataset


class TestAddonDicom:
    """Test addon dicom namespace."""

    def test_get(
        self,
        api,
        readonly_study,
    ):
        """Test get."""
        schema = api.Storage.Study.schema(
            engine_fqdn=readonly_study.engine_fqdn,
            study_uid=readonly_study.study_uid,
            namespace=readonly_study.storage_namespace,
        )
        image = schema['series'][0]['images'][0]
        image_uid = image['id']
        dicom = api.Addon.Dicom.get(
            namespace_id=readonly_study.storage_namespace,
            study_uid=readonly_study.study_uid,
            image_uid=image_uid,
        )
        assert isinstance(dicom, FileDataset)

    def test_upload(
        self,
        api,
        account,
    ):
        """Test upload."""
        dicom_path = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only', 'series_1', 'IMG00001.dcm')

        namespace_id = account.account.namespace_id
        engine_fqdn = api \
            .Namespace \
            .engine_fqdn(namespace_id=namespace_id) \
            .get() \
            .engine_fqdn

        with open(dicom_path, 'rb') as dicom_file:
            image_params = api.Addon.Dicom.upload(
                dicom_file=dicom_file,
                namespace_id=namespace_id,
                engine_fqdn=engine_fqdn,
            )
        study_uid = '1.2.840.10008.1.142353.149743743.367518058.1111111111'  # NOQA:E501
        image_uid = '1.2.840.113619.2.278.3.2831165743.908.1345078604.949.1'
        assert image_params.study_uid == study_uid
        assert image_params.image_uid == image_uid
        assert image_params.image_version
        assert image_params.namespace == namespace_id
        assert image_params.attr

    def test_upload_from_path(
        self,
        api,
        account,
    ):
        """Test upload from path."""
        dicom_path = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only', 'series_1', 'IMG00001.dcm')

        namespace_id = account.account.namespace_id
        engine_fqdn = api \
            .Namespace \
            .engine_fqdn(namespace_id=namespace_id) \
            .get() \
            .engine_fqdn

        image_params = api.Addon.Dicom.upload_from_path(
            dicom_path=dicom_path,
            namespace_id=namespace_id,
            engine_fqdn=engine_fqdn,
        )
        study_uid = '1.2.840.10008.1.142353.149743743.367518058.1111111111'  # NOQA:E501
        image_uid = '1.2.840.113619.2.278.3.2831165743.908.1345078604.949.1'
        assert image_params.study_uid == study_uid
        assert image_params.image_uid == image_uid
        assert image_params.image_version
        assert image_params.namespace == namespace_id
        assert image_params.attr

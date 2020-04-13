from pathlib import Path

from ambra_sdk.service.filtering import Filter, FilterCondition


class TestStorageImage:
    """Test storage image namespace."""

    def test_upload_study(self, upload_study):
        """Test uploading study path."""
        dicom_path = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'anonymize')
        study = upload_study(dicom_path)
        study_uid = '1.2.840.10008.1.142353.149743743.367518058.1727281618'  # NOQA:E501
        assert study.image_count == 6
        assert study.study_uid == study_uid

    def test_readonly_study_fixture(self, api, account, readonly_study):
        """Test readonly fixture."""
        study_uid = '1.2.840.10008.1.142353.149743743.367518058.1111111111'  # NOQA:E501
        assert readonly_study.image_count == 3
        assert readonly_study.study_uid == study_uid
        studies = api \
            .Study \
            .list() \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    account.account.namespace_id,
                ),
            ).all()
        assert len(list(studies)) == 1

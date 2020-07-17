from pathlib import Path

import pytest

from ambra_sdk.service.filtering import Filter, FilterCondition


class TestStorageImage:
    """Test storage image namespace."""

    @pytest.fixture(scope='class')
    def image(self, api, readonly_study):
        """First study image."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        schema = api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        return schema.series[0]['images'][0]

    def test_all_methods_prepared(self, api):
        """Test all methods have only prepare argument."""
        study = api.Storage.Image
        for attribute_name in dir(study):  # NOQA:WPS421
            if not attribute_name.startswith('_'):
                attribute = getattr(study, attribute_name)
                if callable(attribute):
                    assert 'only_prepare' in \
                        attribute.__func__.__code__.co_varnames  # NOQA:WPS609

    def test_cadsr(self, api, image, readonly_study):
        """Test cadsr method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid
        image_uid = image['id']
        image_version = image['version']
        cadsr = api.Storage.Image.cadsr(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
        )

        assert cadsr.status_code == 200

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


# This is modify readonly study so this test in external class.
class TestStorageImageWrap:
    """Test storage image namespace wrap."""

    def test_wrap(self, api, readonly_study):
        """Test wrap method."""
        image_path = Path(__file__) \
            .parents[1] \
            .joinpath('images', 'logo.png')
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace

        with open(image_path, 'rb') as opened_file:
            wrap = api.Storage.Image.wrap(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                opened_file=opened_file,
            )

            assert wrap.status_code == 202

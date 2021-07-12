from pathlib import Path

import pytest
from aiohttp import FormData

from ambra_sdk.service.filtering import Filter, FilterCondition


@pytest.mark.asyncio
class TestAsyncStorageImage:
    """Test storage image namespace."""

    @pytest.fixture(scope='class')
    async def async_image(self, async_api, async_readonly_study):
        """First study image."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        schema = await async_api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        return schema.series[0]['images'][0]

    def test_all_methods_prepared(self, async_api):
        """Test all methods have only prepare argument."""
        study = async_api.Storage.Image
        for attribute_name in dir(study):  # NOQA:WPS421
            if not attribute_name.startswith('_'):
                attribute = getattr(study, attribute_name)
                if callable(attribute):
                    assert 'only_prepare' in \
                        attribute.__func__.__code__.co_varnames  # NOQA:WPS609

    async def test_cadsr(self, async_api, async_image, async_readonly_study):
        """Test cadsr method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid
        image_uid = async_image['id']
        image_version = async_image['version']
        cadsr = await async_api.Storage.Image.cadsr(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=image_uid,
            image_version=image_version,
        )

        assert cadsr.status == 200

    async def test_upload_study(self, async_upload_study):
        """Test uploading study path."""
        dicom_path = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'anonymize')
        study = await async_upload_study(dicom_path)
        study_uid = '1.2.840.10008.1.142353.149743743.367518058.1727281618'  # NOQA:E501
        assert study.image_count == 6
        assert study.study_uid == study_uid

    async def test_async_readonly_study_fixture(
        self,
        async_api,
        async_account,
        async_readonly_study,
    ):
        """Test readonly fixture."""
        study_uid = '1.2.840.10008.1.142353.149743743.367518058.1111111111'  # NOQA:E501
        assert async_readonly_study.image_count == 3
        assert async_readonly_study.study_uid == study_uid
        studies_generator = async_api \
            .Study \
            .list() \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    async_account.account.namespace_id,
                ),
            ).all()
        studies = []
        async for study in studies_generator:
            studies.append(study)
        assert len(studies) == 1

    async def test_dicom_payload(
        self,
        async_api,
        async_readonly_study,
        async_image,
    ):
        """Test dicom payload."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        dicom_payload = await async_api.Storage.Image.dicom_payload(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=async_image['id'],
            image_version=async_image['version'],
        )
        assert dicom_payload.status == 200
        assert dicom_payload.content

    async def test_dicom_payload_pretranscoded(
        self,
        async_api,
        async_readonly_study,
        async_image,
    ):
        """Test pretranscoded dicom payload."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        dicom_payload = await async_api.Storage.Image.dicom_payload(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=async_image['id'],
            image_version=async_image['version'],
            pretranscode=True,
        )
        assert dicom_payload.status == 200
        assert dicom_payload.content


# This is modify readonly study so this test in external class.
@pytest.mark.asyncio
class TestStorageImageWrap:
    """Test storage image namespace wrap."""

    async def test_wrap(self, async_api, async_readonly_study):
        """Test wrap method."""
        image_path = Path(__file__) \
            .parents[2] \
            .joinpath('images', 'logo.png')
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace

        with open(image_path, 'rb') as opened_file:
            wrap = await async_api.Storage.Image.wrap(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                opened_file=opened_file,
            )

            assert wrap.status == 202

    async def test_wrap_with_filename(self, async_api, async_readonly_study):
        """Test wrap method.

        Upload file with filename
        """
        image_path = Path(__file__) \
            .parents[2] \
            .joinpath('images', 'logo.png')
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace

        with open(image_path, 'rb') as opened_file:
            wrap = await async_api.Storage.Image.wrap(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                opened_file=opened_file,
            )

            assert wrap.status == 202

    async def test_wrap_with_filename_and_content_type(
        self,
        async_api,
        async_readonly_study,
    ):
        """Test wrap method.

        Upload file with filename and contenttype
        """
        image_path = Path(__file__) \
            .parents[2] \
            .joinpath('images', 'logo.png')
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace

        with open(image_path, 'rb') as opened_file:
            form_data = FormData()
            form_data.add_field(
                'file',
                opened_file,
                filename='filename',
                content_type='application/json',
            )
            wrap = await async_api.Storage.Image.wrap(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                opened_file=form_data,
            )
            assert wrap.status == 202

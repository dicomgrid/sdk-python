from pathlib import Path

import pytest
from pydicom.dataset import FileDataset


@pytest.mark.asyncio
class TestAsyncAddonDicom:
    """Test addon dicom namespace."""

    async def test_get(
        self,
        async_api,
        async_readonly_study,
    ):
        """Test get."""
        schema = await async_api.Storage.Study.schema(
            engine_fqdn=async_readonly_study.engine_fqdn,
            study_uid=async_readonly_study.study_uid,
            namespace=async_readonly_study.storage_namespace,
        )
        image = schema['series'][0]['images'][0]
        image_uid = image['id']
        dicom = await async_api.Addon.Dicom.get(
            namespace_id=async_readonly_study.storage_namespace,
            study_uid=async_readonly_study.study_uid,
            image_uid=image_uid,
        )
        assert isinstance(dicom, FileDataset)

    async def test_upload(
        self,
        async_api,
        async_account,
    ):
        """Test upload."""
        dicom_path = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only', 'series_1', 'IMG00001.dcm')

        namespace_id = async_account.account.namespace_id
        engine_fqdn = (
            await async_api
            .Namespace
            .engine_fqdn(namespace_id=namespace_id)
            .get()
        ).engine_fqdn

        with open(dicom_path, 'rb') as dicom_file:
            image_params = await async_api.Addon.Dicom.upload(
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

    async def test_upload_from_path(
        self,
        async_api,
        async_account,
    ):
        """Test upload from path."""
        dicom_path = Path(__file__) \
            .parents[1] \
            .joinpath('dicoms', 'read_only', 'series_1', 'IMG00001.dcm')

        namespace_id = async_account.account.namespace_id
        engine_fqdn = (
            await async_api
            .Namespace
            .engine_fqdn(namespace_id=namespace_id)
            .get()
        ).engine_fqdn

        image_params = await async_api.Addon.Dicom.upload_from_path(
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

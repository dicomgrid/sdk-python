import logging
from pathlib import Path

import pytest
from dynaconf import settings

from ambra_sdk.exceptions.storage import (
    AccessDenied,
    AmbraResponseException,
    StudyNotFound,
)
from ambra_sdk.service.ws import AsyncWSManager

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
class TestAsyncStorageStudy:
    """Test Study namespace of Storage api."""

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

    @pytest.fixture(scope='class')
    async def async_logo_attachment(self, async_api, async_readonly_study):
        """Ambra logo attachment."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid
        logo = Path(__file__) \
            .parents[2] \
            .joinpath('images', 'logo.png')
        with open(logo, 'rb') as f:
            await async_api.Storage.Study.post_attachment(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
                opened_file=f,
            )
        schema = await async_api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        attachment = schema.attachments[0]
        yield attachment
        await async_api.Storage.Study.delete_attachment(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            attachment_id=attachment['id'],
            hash_arg=attachment['version'],
        )

    async def test_all_methods_prepared(self, async_api):
        """Test all methods have only prepare argument."""
        study = async_api.Storage.Study
        for attribute_name in dir(study):  # NOQA:WPS421
            if not attribute_name.startswith('_'):
                attribute = getattr(study, attribute_name)
                if callable(attribute):
                    assert 'only_prepare' in \
                        attribute.__func__.__code__.co_varnames  # NOQA:WPS609

    async def test_schema_prepared(self, async_api, async_readonly_study):
        """Test schema prepared method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        prepared = await async_api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            only_prepare=True,
        )
        assert prepared.url

    async def test_schema_bad_request(self, async_api, async_readonly_study):
        """Test schema bad request."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = 'bad'

        with pytest.raises(StudyNotFound) as exc:
            await async_api.Storage.Study.schema(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
            )
        exc_v = exc.value
        assert exc_v.code == 404
        assert exc_v.exception_data['study_uid'] == 'bad'
        assert exc_v.storage_code == 18
        assert exc_v.description == "Study wasn't found by provided ids"
        assert exc_v.http_status_code == 404
        assert exc_v.readable_status == 'STUDY_NOT_FOUND'
        assert exc_v.created
        assert exc_v.extended is None
        assert str(exc_v) == "404. Study wasn't found by provided ids"

    @pytest.mark.skip('NULL pointer exception in storage')
    async def test_schema_bad_request_with_trace(
        self,
        async_api,
        async_readonly_study,
    ):
        """Test schema bad r request with trace."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = 'bad'

        with pytest.raises(StudyNotFound) as exc:
            q = async_api.Storage.Study.schema(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
                only_prepare=True,
            )
            q.headers = {'X-AmbraHealth-Verbose-Errors': '1'}
            q.execute()
        exc_v = exc.value
        assert exc_v.code == 404
        assert exc_v.exception_data['study_uid'] == 'bad'
        assert exc_v.storage_code == 18
        assert exc_v.description == "Study wasn't found by provided ids"
        assert exc_v.http_status_code == 404
        assert exc_v.readable_status == 'STUDY_NOT_FOUND'
        assert exc_v.created
        assert exc_v.extended is not None
        assert str(exc_v) == "404. Study wasn't found by provided ids"

    async def test_schema(self, async_api, async_readonly_study):
        """Test schema method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        schema = await async_api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert schema

    async def test_delete(self, async_api, async_account, async_auto_remove):
        """Test delete method."""
        study_dir = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'anonymize')
        study = await async_api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir,
            namespace_id=async_account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study.uuid)
        async_auto_remove(study)

        engine_fqdn = study.engine_fqdn
        storage_namespace = study.storage_namespace
        study_uid = study.study_uid

        delete = await async_api.Storage.Study.delete(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert delete.status in {200, 202}

    async def test_delete_image(
        self,
        async_api,
        async_account,
        async_auto_remove,
        async_storage_auto_remove,
    ):
        """Test delete_image method."""
        study_dir = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'anonymize')
        study = await async_api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir,
            namespace_id=async_account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study.uuid)
        async_auto_remove(study)

        engine_fqdn = study.engine_fqdn
        storage_namespace = study.storage_namespace
        study_uid = study.study_uid
        async_storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            study_uid,
        )

        schema = await async_api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        image = schema.series[0]['images'][0]

        delete_image = await async_api.Storage.Study.delete_image(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=image['id'],
        )
        assert delete_image.status in {200, 202}

    async def test_delete_images(
        self,
        async_api,
        async_account,
        async_auto_remove,
        async_storage_auto_remove,
    ):
        """Test delete_images method."""
        study_dir = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'anonymize')
        study = await async_api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir,
            namespace_id=async_account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study.uuid)
        async_auto_remove(study)

        engine_fqdn = study.engine_fqdn
        storage_namespace = study.storage_namespace
        study_uid = study.study_uid
        async_storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            study_uid,
        )
        schema = await async_api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        request_body = ','.join(
            [i['id'] for i in schema.series[0]['images']],
        )

        delete_images = await async_api.Storage.Study.delete_images(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            request_body=request_body,
        )
        assert delete_images.status in {200, 202}

        with pytest.raises(StudyNotFound):
            delete_images = await async_api.Storage.Study.delete_images(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid='unknownstudy',
                request_body=request_body,
            )

    @pytest.mark.skip('Now in storage this is not a general exception')
    async def test_delete_images_unprocessable_entity(
        self,
        async_api,
        async_account,
        async_auto_remove,
        async_storage_auto_remove,
    ):
        """Test delete_images method unprocessable entity."""
        study_dir = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'anonymize')
        study = await async_api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir,
            namespace_id=async_account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study.uuid)
        await async_auto_remove(study)

        engine_fqdn = study.engine_fqdn
        storage_namespace = study.storage_namespace
        study_uid = study.study_uid
        await async_storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            study_uid,
        )
        await async_api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )

        # TODO unprocessable entity?
        await async_api.Storage.Study.delete_images(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            request_body='',
        )

    async def test_count(self, async_api, async_readonly_study):
        """Test count method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        count = await async_api.Storage.Study.count(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert count

    async def test_tag(self, async_api, async_readonly_study):
        """Test tag method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        tag = await async_api.Storage.Study.tag(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert tag

    async def test_attribute(
        self,
        async_api,
        async_readonly_study,
        async_image,
    ):
        """Test attribute method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        attribute = await async_api.Storage.Study.attribute(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=async_image['id'],
            image_version=async_image['version'],
        )
        assert attribute

    async def test_image_phi(
        self,
        async_api,
        async_readonly_study,
        async_image,
    ):
        """Test image_phi method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        image_phi = await async_api.Storage.Study.image_phi(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=async_image['id'],
            image_version=async_image['version'],
        )
        assert image_phi

    async def test_phi(self, async_api, async_readonly_study):
        """Test phi method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        phi = await async_api.Storage.Study.phi(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert phi

    async def test_thumbnail(
        self,
        async_api,
        async_readonly_study,
        async_image,
    ):
        """Test thumbnail method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        thumbnail = await async_api.Storage.Study.thumbnail(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=async_image['id'],
            image_version=async_image['version'],
            frame_number=0,
        )
        assert thumbnail.status == 200

    async def test_diagnostic(
        self,
        async_api,
        async_readonly_study,
        async_image,
    ):
        """Test diagnostic method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        diagnostic = await async_api.Storage.Study.diagnostic(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=async_image['id'],
            image_version=async_image['version'],
            frame_number=0,
        )
        assert diagnostic.status == 200

    async def test_frame(
        self,
        async_api,
        async_readonly_study,
        async_image,
    ):
        """Test frame method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        frame = await async_api.Storage.Study.frame(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=async_image['id'],
            image_version=async_image['version'],
            frame_number=0,
        )
        assert frame.status == 200

    async def test_frame_tiff(
        self,
        async_api,
        async_readonly_study,
        async_image,
    ):
        """Test frame tiff method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        frame_tiff = await async_api.Storage.Study.frame_tiff(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=async_image['id'],
            image_version=async_image['version'],
            frame_number=0,
        )
        assert frame_tiff.status == 200

    @pytest.mark.skip('Now in storage this is not a general exception')
    async def test_pdf(
        self,
        async_api,
        async_readonly_study,
        async_image,
    ):
        """Test pdf method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        # TODO: Check with pdf dicoms
        # TODO Unsupported Media type exception
        await async_api.Storage.Study.pdf(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=async_image['id'],
            image_version=async_image['version'],
        )

    async def test_image_json(
        self,
        async_api,
        async_readonly_study,
        async_image,
    ):
        """Test image_json method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        image_json = await async_api.Storage.Study.image_json(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=async_image['id'],
            image_version=async_image['version'],
        )
        assert image_json

        assert len(list(image_json.get_tags(filter_dict={'group': 2}))) == 7
        tag = image_json.tag_by_name('Manufacturer')
        assert tag.group == 8
        assert tag.element == 112
        assert tag.vr == 'LO'
        assert tag.vl == 18
        assert tag.value == 'GE MEDICAL SYSTEMS'

    async def test_json(self, async_api, async_readonly_study):
        """Test json method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        json = await async_api.Storage.Study.json(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert json
        assert len(list(json[0].get_tags(filter_dict={'group': 2}))) == 7
        tag = json[0].tag_by_name('Manufacturer')
        assert tag.group == 8
        assert tag.element == 112
        assert tag.vr == 'LO'
        assert tag.vl == 18
        assert tag.value == 'GE MEDICAL SYSTEMS'

    async def test_post_attachment(self, async_logo_attachment):
        """Test post_attachment method."""
        # This is tested by logo_attachemnt fixture
        assert async_logo_attachment

    async def test_delete_attachment(self, async_logo_attachment):
        """Test post_attachment method."""
        # This is tested by logo_attachemnt fixture
        assert async_logo_attachment

    async def test_attachment(
        self,
        async_api,
        async_readonly_study,
        async_logo_attachment,
    ):
        """Test attachment method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        attachment = await async_api.Storage.Study.attachment(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            attachment_id=async_logo_attachment['id'],
            version=async_logo_attachment['version'],
        )
        assert attachment.status == 200

    async def test_latest(
        self,
        async_api,
        async_readonly_study,
        async_logo_attachment,
    ):
        """Test latest method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        latest = await async_api.Storage.Study.latest(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert latest.status == 200

    async def test_download(self, async_api, async_readonly_study):
        """Test download method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        download = await async_api.Storage.Study.download(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            bundle='dicom',
        )
        assert download.status == 200

    @pytest.mark.skip('Now in storage this is not a general exception')
    async def test_video(
        self,
        async_api,
        async_readonly_study,
        async_image,
    ):
        """Test video method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        # TODO: Check with video dicoms
        # TODO Unsupported Media type exception
        await async_api.Storage.Study.video(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=async_image['id'],
            image_version=async_image['version'],
        )

    async def test_split_one_series(
        self,
        async_api,
        async_account,
        async_readonly_study,
        async_auto_remove,
    ):
        """Test split method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        split = await async_api.Storage.Study.split(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert split.status in {200, 202}
        new_study_uid = await split.text()
        logger.info('New splitted study %s', new_study_uid)

        new_study = await async_api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        async_auto_remove(new_study)
        assert new_study

    async def test_split_multi_series(
        self,
        async_api,
        async_account,
        multi_series_study,
        async_auto_remove,
    ):
        """Test split method."""
        engine_fqdn = multi_series_study.engine_fqdn
        storage_namespace = multi_series_study.storage_namespace
        study_uid = multi_series_study.study_uid

        split = await async_api.Storage.Study.split(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            series_uid='1.2.840.113619.2.278.3.2831165743.908.1345078604.111',
        )

        new_study_uid = await split.text()
        logger.info('New splitted study %s', new_study_uid)
        assert split.status in {200, 202}

        new_study = await async_api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        async_auto_remove(new_study)
        assert new_study

    async def test_merge(
        self,
        async_api,
        async_account,
        async_auto_remove,
    ):
        """Test merge method.

        Merge is async operation.
        This method append images from one study to another.
        """
        study_dir1 = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'splitted', '1')

        study1 = await async_api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir1,
            namespace_id=async_account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study1.uuid)
        async_auto_remove(study1)

        study_dir2 = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'splitted', '2')

        study2 = await async_api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir2,
            namespace_id=async_account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study2.uuid)
        async_auto_remove(study2)

        engine_fqdn = study1.engine_fqdn
        storage_namespace = study1.storage_namespace

        # Merge is async operation...
        # So we need to wait EDIT event in websocket
        ws_url = '{url}/channel/websocket'.format(url=async_api._api_url)

        channel_name = 'study.{namespace_id}'.format(
            namespace_id=storage_namespace,
        )
        sid = await async_api.get_sid()
        ws_manager = AsyncWSManager(ws_url)

        async with ws_manager.channel(sid, channel_name) as ws:
            await async_api.Storage.Study.merge(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study1.study_uid,
                secondary_study_uid=study2.study_uid,
            )
            await ws.wait_for_event(
                channel_name,
                sid,
                'EDIT',
                timeout=settings.API['merge_timeout'],
            )

        schema = await async_api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study1.study_uid,
        )
        # Actually, merge method merge only images,
        # but in  test fixtures each images have own series.
        # Old study1 have only 2 images.
        assert len(schema.series) == 4

    async def test_anonymize(
        self,
        async_api,
        async_account,
        async_readonly_study,
        async_auto_remove,
        async_storage_auto_remove,
    ):
        """Test anonymize method."""
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

        anonymize = await async_api.Storage.Study.anonymize(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            to_namespace=storage_namespace,
            study_uid=study_uid,
            region=region,
            color='121197149',
        )
        assert anonymize.status in {200, 202}

        new_study_uid = await anonymize.text()
        async_storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            new_study_uid,
        )

        # wait for ready new study
        new_study = await async_api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('New anonymized study %s', new_study.uuid)
        async_auto_remove(new_study)
        assert new_study

    async def test_crop(
        self,
        async_api,
        async_account,
        async_readonly_study,
        async_auto_remove,
        async_storage_auto_remove,
    ):
        """Test crop method."""
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

        crop = await async_api.Storage.Study.crop(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            to_namespace=storage_namespace,
            study_uid=study_uid,
            region=region,
        )
        assert crop.status in {200, 202}

        new_study_uid = await crop.text()
        async_storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            new_study_uid,
        )

        # wait for ready new study
        new_study = await async_api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('New cropped study %s', new_study.uuid)
        async_auto_remove(new_study)
        assert new_study

    async def test_cache(self, async_api, async_readonly_study):
        """Test cache method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        cache = await async_api.Storage.Study.cache(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert cache.status in {200, 202}

    async def test_hl7_to_sr(self, async_api, async_readonly_study):
        """Test hl7 to sr.

        We test only exceution (we have no hl7)
        Also this method return 500 at some reasons..
        """
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        with pytest.raises(AmbraResponseException):
            await async_api.Storage.Study.hl7_to_sr(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
                hl7uuid='123',
            )

    async def test_retry_storage_with_new_sid(
        self,
        async_api,
        async_readonly_study,
    ):
        """Test retry storage request with new sid.

        In storage PermissionDenied means two things:

        1. Wrong sid
        2. User have not access to some stoudy
        """
        async_api._sid = 'Wrong sid'
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid
        try:
            await async_api.Storage.Study.schema(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
            )
        except Exception:
            pytest.fail('Something goes wrong with retrying with new sid')

        # But access denied still works:
        with pytest.raises(AccessDenied):
            await async_api.Storage.Study.schema(
                engine_fqdn=engine_fqdn,
                namespace='abra',
                study_uid='kadabra',
            )

    async def test_clone(
        self,
        async_api,
        async_readonly_study,
        async_auto_remove,
    ):
        """Test clone method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        clone = await async_api.Storage.Study.clone(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert clone.status in {200, 202}
        new_study_uid = await clone.text()
        new_study = await async_api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        assert new_study
        async_auto_remove(new_study)

    async def test_attachment_image(
        self,
        async_api,
        async_readonly_study,
        async_logo_attachment,
    ):
        """Test attachment image method."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid
        attachment = await async_api.Storage.Study.attachment_image(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            attachment_uid=async_logo_attachment['id'],
            version=async_logo_attachment['version'],
        )
        assert attachment.study_uid

    async def test_create_rt(
        self,
        async_api,
        async_readonly_study,
    ):
        """Test create rt."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        body = """{
          "structureSetLabel": "1",
          "structureSetName": "1",
          "structureSetDescription": "1",
          "instanceNumber": "1",
          "structureSetDate": 1625486773319,
          "structureSetTime": 1625486773319,
          "referencedFrameOfReferenceList": [
              {
                  "frameOfReferenceUID": "1",
                  "rtReferencedStudies": [
                      {
                          "referencedSOPClassUID": "1",
                          "referencedSOPInstanceUID": "1",
                          "rtReferencedSeries": [
                              {
                                  "seriesInstanceUID": "series",
                                  "contourImageSequences": [
                                      {
                                          "referencedFrameNumber": "10",
                                          "referencedSegmentNumber": "3"
                                      }
                                  ]
                              }
                          ]
                      }
                  ]
              }
          ],
          "structureSetROISequences": [
              {
                  "roiNumber": "1",
                  "referencedFrameOfReferenceUID": "1",
                  "roiName": "1",
                  "roiDescription": "1",
                  "roiVolume": "1",
                  "roiGenerationAlgorithm": "MANUAL",
                  "roiGenerationDescription": "1",
                  "derivationCodeSequences": [
                      {
                          "codeValue": "1",
                          "codingSchemeDesignator": "1",
                          "codingSchemeVersion": "1",
                          "codeMeaning": "1"
                      }
                  ]
              }
          ],
          "predecessorStructureSet": [
              {
                  "referencedSOPClassUID": "sop class uid",
                  "referencedSOPInstanceUID": "instance uid"
              }
          ],
          "roiContours": [
              {
                  "referencedROINumber": "12",
                  "roiDisplayColor": "333",
                  "contourSequences": [
                      {
                          "contourNumber": "3",
                          "attachedContours": "3",
                          "contourGeometricType": "OPEN_PLANAR",
                          "contourSlabThickness": "3",
                          "contourOffsetVector": "3",
                          "numberOfContourPoints": "3",
                          "contourImageSequence": [
                              {
                                  "referencedFrameNumber": "21",
                                  "referencedSegmentNumber": "18"
                              }
                          ],
                          "contourData": [
                              {
                                  "x": 5.6,
                                  "y": 123.9,
                                  "z": 43.2
                              }
                          ]
                      }
                  ]
              }
          ],
          "rtROIObservations": [
              {
                  "observationNumber": "11",
                  "referencedROINumber": "11",
                  "roiObservationLabel": "11",
                  "roiObservationDescription": "11",
                  "rtROIInterpretedType": "EXTERNAL",
                  "roiInterpreter": "11",
                  "materialId": "11",
                  "relatedROISequences": [
                      {
                          "referencedROINumber": "22",
                          "rtROIRelationship": "22"
                      }
                  ],
                  "codeSequenceMacroAttributes": [
                      {
                          "codeValue": "88",
                          "codingSchemeDesignator": "88",
                          "codingSchemeVersion": "88",
                          "codeMeaning": "88"
                      }
                  ],
                  "relatedRtRoiObservationsSequence": [
                      "33"
                  ],
                  "physicalProperties": [
                      {
                          "roiPhysicalProperty": "EFFECTIVE_Z",
                          "roiElementalCompositeSequences": [
                              {
                                  "roiAtomicNumber": "5",
                                  "roiAtomicMassFraction": "5",
                                  "physicalPropertyValue": "5"
                              }
                          ]
                      }
                  ]
              }
          ]
      }"""
        create_rt = await async_api.Storage.Study.create_rt(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            body=body,
        )
        assert create_rt.namespace
        assert create_rt.study_uid

    async def test_dicomweb(self, async_api, async_readonly_study):
        """Test dicomweb methods."""
        engine_fqdn = async_readonly_study.engine_fqdn
        storage_namespace = async_readonly_study.storage_namespace
        study_uid = async_readonly_study.study_uid

        schema = await async_api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert schema

        series_uid = schema['series'][0]['series_uid']
        image_uid = schema['series'][0]['images'][0]['id']

        image_dicomweb = await async_api.Storage.Study.image_dicomweb(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            series_uid=series_uid,
            image_uid=image_uid,
        )
        assert image_dicomweb
        assert image_dicomweb['00080018']['Value'][0] == image_uid

        series_dicomweb = await async_api.Storage.Study.series_dicomweb(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            series_uid=series_uid,
        )
        assert series_dicomweb
        assert series_dicomweb[0]['0020000E']['Value'][0] == series_uid

        study_dicomweb = await async_api.Storage.Study.study_dicomweb(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert study_dicomweb
        assert study_dicomweb[0]['0020000D']['Value'][0] == study_uid

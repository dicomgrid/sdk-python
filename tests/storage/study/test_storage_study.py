import logging
from pathlib import Path

import pytest
from dynaconf import settings

from ambra_sdk.exceptions.storage import (
    AccessDenied,
    AmbraResponseException,
    BadRequest,
    ImageNotFound,
    NotPdfFile,
    NotVideoInImage,
    StudyNotFound,
)
from ambra_sdk.service.ws import WSManager

logger = logging.getLogger(__name__)


class TestStorageStudy:
    """Test Study namespace of Storage api."""

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

    @pytest.fixture(scope='class')
    def logo_attachment(self, api, readonly_study):
        """Ambra logo attachment."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid
        logo = Path(__file__) \
            .parents[2] \
            .joinpath('images', 'logo.png')
        with open(logo, 'rb') as f:
            api.Storage.Study.post_attachment(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
                opened_file=f,
            )
        schema = api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        attachment = schema.attachments[0]
        yield attachment
        api.Storage.Study.delete_attachment(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            attachment_id=attachment['id'],
            hash_arg=attachment['version'],
        )

    def test_all_methods_prepared(self, api):
        """Test all methods have only prepare argument."""
        study = api.Storage.Study
        for attribute_name in dir(study):  # NOQA:WPS421
            if not attribute_name.startswith('_'):
                attribute = getattr(study, attribute_name)
                if callable(attribute):
                    assert 'only_prepare' in \
                        attribute.__func__.__code__.co_varnames  # NOQA:WPS609

    def test_schema_prepared(self, api, readonly_study):
        """Test schema prepared method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        prepared = api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            only_prepare=True,
        )
        assert prepared.url

    def test_schema_bad_request(self, api, readonly_study):
        """Test schema bad request."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = 'bad'

        with pytest.raises(StudyNotFound) as exc:
            api.Storage.Study.schema(
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

    def test_schema_bad_request_with_trace(self, api, readonly_study):
        """Test schema bad r request with trace."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = 'bad'

        with pytest.raises(StudyNotFound) as exc:
            q = api.Storage.Study.schema(
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

    def test_schema(self, api, readonly_study):
        """Test schema method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        schema = api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert schema

    def test_delete(self, api, account, auto_remove):
        """Test delete method."""
        study_dir = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'anonymize')
        study = api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir,
            namespace_id=account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study.uuid)
        auto_remove(study)

        engine_fqdn = study.engine_fqdn
        storage_namespace = study.storage_namespace
        study_uid = study.study_uid

        delete = api.Storage.Study.delete(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert delete.status_code in {200, 202}

    def test_delete_image(
        self,
        api,
        account,
        auto_remove,
        storage_auto_remove,
    ):
        """Test delete_image method."""
        study_dir = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'anonymize')
        study = api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir,
            namespace_id=account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study.uuid)
        auto_remove(study)

        engine_fqdn = study.engine_fqdn
        storage_namespace = study.storage_namespace
        study_uid = study.study_uid
        storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            study_uid,
        )

        schema = api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        image = schema.series[0]['images'][0]

        delete_image = api.Storage.Study.delete_image(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=image['id'],
        )
        assert delete_image.status_code in {200, 202}

        with pytest.raises(ImageNotFound):
            delete_image = api.Storage.Study.delete_image(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
                image_uid=image['id'],
            )

    def test_delete_images(
        self,
        api,
        account,
        auto_remove,
        storage_auto_remove,
    ):
        """Test delete_images method."""
        study_dir = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'anonymize')
        study = api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir,
            namespace_id=account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study.uuid)
        auto_remove(study)

        engine_fqdn = study.engine_fqdn
        storage_namespace = study.storage_namespace
        study_uid = study.study_uid
        storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            study_uid,
        )
        schema = api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        request_body = ','.join(
            [i['id'] for i in schema.series[0]['images']],
        )

        delete_images = api.Storage.Study.delete_images(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            request_body=request_body,
        )
        assert delete_images.status_code in {200, 202}

        with pytest.raises(StudyNotFound):
            delete_images = api.Storage.Study.delete_images(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid='unknownstudy',
                request_body=request_body,
            )

    def test_delete_images_unprocessable_entity(
        self,
        api,
        account,
        auto_remove,
        storage_auto_remove,
    ):
        """Test delete_images method unprocessable entity."""
        study_dir = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'anonymize')
        study = api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir,
            namespace_id=account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study.uuid)
        auto_remove(study)

        engine_fqdn = study.engine_fqdn
        storage_namespace = study.storage_namespace
        study_uid = study.study_uid
        storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            study_uid,
        )
        with pytest.raises(BadRequest):
            api.Storage.Study.delete_images(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
                request_body='',
            )

    def test_count(self, api, readonly_study):
        """Test count method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        count = api.Storage.Study.count(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert count

    def test_tag(self, api, readonly_study):
        """Test tag method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        tag = api.Storage.Study.tag(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert tag

    def test_attribute(self, api, readonly_study, image):
        """Test attribute method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        attribute = api.Storage.Study.attribute(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=image['id'],
            image_version=image['version'],
        )
        assert attribute

    def test_image_phi(self, api, readonly_study, image):
        """Test image_phi method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        image_phi = api.Storage.Study.image_phi(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=image['id'],
            image_version=image['version'],
        )
        assert image_phi

    def test_phi(self, api, readonly_study):
        """Test phi method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        phi = api.Storage.Study.phi(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert phi

    def test_thumbnail(self, api, readonly_study, image):
        """Test thumbnail method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        thumbnail = api.Storage.Study.thumbnail(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=image['id'],
            image_version=image['version'],
            frame_number=0,
        )
        assert thumbnail.status_code == 200

    def test_diagnostic(self, api, readonly_study, image):
        """Test diagnostic method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        diagnostic = api.Storage.Study.diagnostic(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=image['id'],
            image_version=image['version'],
            frame_number=0,
        )
        assert diagnostic.status_code == 200

    def test_frame(self, api, readonly_study, image):
        """Test frame method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        frame = api.Storage.Study.frame(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=image['id'],
            image_version=image['version'],
            frame_number=0,
        )
        assert frame.status_code == 200

    def test_frame_tiff(self, api, readonly_study, image):
        """Test frame tiff method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        frame_tiff = api.Storage.Study.frame_tiff(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=image['id'],
            image_version=image['version'],
            frame_number=0,
        )
        assert frame_tiff.status_code == 200

    def test_pdf(self, api, readonly_study, image):
        """Test pdf method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        # TODO: Check with pdf dicoms
        with pytest.raises(NotPdfFile):
            api.Storage.Study.pdf(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
                image_uid=image['id'],
                image_version=image['version'],
            )

    def test_image_json(self, api, readonly_study, image):
        """Test image_json method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        image_json = api.Storage.Study.image_json(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            image_uid=image['id'],
            image_version=image['version'],
        )
        assert image_json

        assert len(list(image_json.get_tags(filter_dict={'group': 2}))) == 7
        tag = image_json.tag_by_name('Manufacturer')
        assert tag.group == 8
        assert tag.element == 112
        assert tag.vr == 'LO'
        assert tag.vl == 18
        assert tag.value == 'GE MEDICAL SYSTEMS'

    def test_json(self, api, readonly_study):
        """Test json method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        json = api.Storage.Study.json(
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

    def test_post_attachment(self, logo_attachment):
        """Test post_attachment method."""
        # This is tested by logo_attachemnt fixture
        assert logo_attachment

    def test_delete_attachment(self, logo_attachment):
        """Test post_attachment method."""
        # This is tested by logo_attachemnt fixture
        assert logo_attachment

    def test_attachment(
        self,
        api,
        readonly_study,
        logo_attachment,
    ):
        """Test attachment method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        attachment = api.Storage.Study.attachment(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            attachment_id=logo_attachment['id'],
            version=logo_attachment['version'],
        )
        assert attachment.status_code == 200

    def test_latest(self, api, readonly_study, logo_attachment):
        """Test latest method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        latest = api.Storage.Study.latest(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert latest.status_code == 200

    def test_download(self, api, readonly_study):
        """Test download method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        download = api.Storage.Study.download(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            bundle='dicom',
        )
        assert download.status_code == 200

    def test_video(self, api, readonly_study, image):
        """Test video method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        # TODO: Check with video dicoms
        with pytest.raises(NotVideoInImage):
            api.Storage.Study.video(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
                image_uid=image['id'],
                image_version=image['version'],
            )

    def test_split_one_series(
        self,
        api,
        account,
        readonly_study,
        auto_remove,
    ):
        """Test split method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        split = api.Storage.Study.split(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert split.status_code in {200, 202}
        new_study_uid = split.text
        logger.info('New splitted study %s', new_study_uid)

        new_study = api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        auto_remove(new_study)
        assert new_study

    def test_split_multi_series(
        self,
        api,
        account,
        multi_series_study,
        auto_remove,
    ):
        """Test split method."""
        engine_fqdn = multi_series_study.engine_fqdn
        storage_namespace = multi_series_study.storage_namespace
        study_uid = multi_series_study.study_uid

        split = api.Storage.Study.split(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            series_uid='1.2.840.113619.2.278.3.2831165743.908.1345078604.111',
        )

        new_study_uid = split.text
        logger.info('New splitted study %s', new_study_uid)
        assert split.status_code in {200, 202}

        new_study = api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        auto_remove(new_study)
        assert new_study

    def test_merge(
        self,
        api,
        account,
        auto_remove,
    ):
        """Test merge method.

        Merge is async operation.
        This method append images from one study to another.
        """
        study_dir1 = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'splitted', '1')

        study1 = api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir1,
            namespace_id=account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study1.uuid)
        auto_remove(study1)

        study_dir2 = Path(__file__) \
            .parents[2] \
            .joinpath('dicoms', 'splitted', '2')

        study2 = api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir2,
            namespace_id=account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', study2.uuid)
        auto_remove(study2)

        engine_fqdn = study1.engine_fqdn
        storage_namespace = study1.storage_namespace

        # Merge is async operation...
        # So we need to wait EDIT event in websocket
        ws_url = '{url}/channel/websocket'.format(url=api._api_url)

        channel_name = 'study.{namespace_id}'.format(
            namespace_id=storage_namespace,
        )
        sid = api.sid
        ws_manager = WSManager(ws_url)

        with ws_manager.channel(sid, channel_name) as ws:
            api.Storage.Study.merge(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study1.study_uid,
                secondary_study_uid=study2.study_uid,
            )
            ws.wait_for_event(
                channel_name,
                sid,
                'EDIT',
                timeout=settings.API['merge_timeout'],
            )

        schema = api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study1.study_uid,
        )
        # Actually, merge method merge only images,
        # but in  test fixtures each images have own series.
        # Old study1 have only 2 images.
        assert len(schema.series) == 4

    def test_anonymize(
        self,
        api,
        account,
        readonly_study,
        auto_remove,
        storage_auto_remove,
    ):
        """Test anonymize method."""
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

        anonymize = api.Storage.Study.anonymize(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            to_namespace=storage_namespace,
            study_uid=study_uid,
            region=region,
            color='121197149',
        )
        assert anonymize.status_code in {200, 202}

        new_study_uid = anonymize.text
        storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            new_study_uid,
        )

        # wait for ready new study
        new_study = api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('New anonymized study %s', new_study.uuid)
        auto_remove(new_study)
        assert new_study

    def test_crop(
        self,
        api,
        account,
        readonly_study,
        auto_remove,
        storage_auto_remove,
    ):
        """Test crop method."""
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

        crop = api.Storage.Study.crop(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            to_namespace=storage_namespace,
            study_uid=study_uid,
            region=region,
        )
        assert crop.status_code in {200, 202}

        new_study_uid = crop.text
        storage_auto_remove(
            engine_fqdn,
            storage_namespace,
            new_study_uid,
        )

        # wait for ready new study
        new_study = api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('New cropped study %s', new_study.uuid)
        auto_remove(new_study)
        assert new_study

    def test_cache(self, api, readonly_study):
        """Test cache method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        cache = api.Storage.Study.cache(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert cache.status_code in {200, 202}

    def test_hl7_to_sr(self, api, readonly_study):
        """Test hl7 to sr.

        We test only exceution (we have no hl7)
        Also this method return 500 at some reasons..
        """
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        with pytest.raises(AmbraResponseException):
            api.Storage.Study.hl7_to_sr(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
                hl7uuid='123',
            )

    def test_retry_storage_with_new_sid(self, api, readonly_study):
        """Test retry storage request with new sid.

        In storage PermissionDenied means two things:

        1. Wrong sid
        2. User have not access to some stoudy
        """
        api._sid = 'Wrong sid'
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid
        try:
            api.Storage.Study.schema(
                engine_fqdn=engine_fqdn,
                namespace=storage_namespace,
                study_uid=study_uid,
            )
        except Exception:
            pytest.fail('Something goes wrong with retrying with new sid')

        # But access denied still works:
        with pytest.raises(AccessDenied):
            api.Storage.Study.schema(
                engine_fqdn=engine_fqdn,
                namespace='abra',
                study_uid='kadabra',
            )

    def test_clone(self, api, readonly_study, auto_remove):
        """Test clone method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        clone = api.Storage.Study.clone(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert clone.status_code in {200, 202}
        new_study_uid = clone.text
        new_study = api.Addon.Study.wait(
            study_uid=new_study_uid,
            namespace_id=storage_namespace,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        assert new_study
        auto_remove(new_study)

    def test_attachment_image(
        self,
        api,
        readonly_study,
        logo_attachment,
    ):
        """Test attachment image method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid
        attachment = api.Storage.Study.attachment_image(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            attachment_uid=logo_attachment['id'],
            version=logo_attachment['version'],
        )
        assert attachment.study_uid

    def test_create_rt(
        self,
        api,
        readonly_study,
    ):
        """Test create rt."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

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
        create_rt = api.Storage.Study.create_rt(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            body=body,
        )
        assert create_rt.namespace
        assert create_rt.study_uid

    def test_dicomweb(self, api, readonly_study):
        """Test dicomweb methods."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        schema = api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert schema

        series_uid = schema['series'][0]['series_uid']
        image_uid = schema['series'][0]['images'][0]['id']

        image_dicomweb = api.Storage.Study.image_dicomweb(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            series_uid=series_uid,
            image_uid=image_uid,
        )
        assert image_dicomweb
        assert image_dicomweb['00080018']['Value'][0] == image_uid

        series_dicomweb = api.Storage.Study.series_dicomweb(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
            series_uid=series_uid,
        )
        assert series_dicomweb
        assert series_dicomweb[0]['0020000E']['Value'][0] == series_uid

        study_dicomweb = api.Storage.Study.study_dicomweb(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert study_dicomweb
        assert study_dicomweb[0]['0020000D']['Value'][0] == study_uid

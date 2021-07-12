"""Async study fixtures."""

import logging
from contextlib import contextmanager, suppress
from pathlib import Path
from time import monotonic
from typing import Optional

import pytest
from dynaconf import settings

from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.service.filtering import Filter, FilterCondition

logger = logging.getLogger(__name__)

# This fixtures depends of storage cluster in order to
# prevent pytest use studies from one class between different
# storages. (account depends on storage cluster, so without this
# demand we cant delete account fixture).


@pytest.fixture
async def async_storage_auto_remove(async_api):
    """Storage auto remove.

    In some tests we manually create a new studies in storage.
    If such test is failed, study can not be removed.
    This fixture remove study in any cases.

    :param async_api: api
    :yields: add to auto remove fn
    """
    studies = []

    def add_to_autoremove(engine_fqdn, namespace, study_uid):
        studies.append((engine_fqdn, namespace, study_uid))

    yield add_to_autoremove

    for engine_fqdn, namespace, study_uid in studies:
        await async_api.Storage.Study.delete(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
        )
        logger.info('Storage auto removed study %s', study_uid)


@pytest.fixture
async def async_auto_remove(async_api):
    """Auto remove.

    In some tests we manually create a new studies in.
    If such test is failed, study can not be removed.
    This fixture remove study in any cases.

    :param async_api: async_api
    :yields: add to auto remove fn
    """
    studies = []

    def add_to_autoremove(study):
        studies.append(study)

    yield add_to_autoremove

    for study in studies:
        logger.info('Auto removed study %s', study.uuid)
        await async_api.Study.delete(uuid=study.uuid).get()


@pytest.fixture
async def async_upload_study(
    async_api,
    async_account,
):
    """Upload study.

    :param async_api: api fixture
    :param async_account: account fixture

    :yields: upload study by path function
    """
    uploaded_studies = []

    async def _upload_study(study_dir):
        new_study = await async_api.Addon.Study.upload_dir_and_get(
            study_dir=study_dir,
            namespace_id=async_account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', new_study.uuid)
        uploaded_studies.append(new_study)
        return new_study
    yield _upload_study
    for study in uploaded_studies:
        await async_api.Study.delete(uuid=study.uuid).get()
        logger.info('Deleted study %s', study.uuid)


@pytest.fixture(scope='class')
async def async_readonly_study(
    async_api,
    async_account,
):
    """Read only study.

    This is usefull for creating study one time per class.

    Dont use this study path manually
    Dont modify this study (use duplicate mechanism)

    :param async_api: api fixture
    :param async_account: account fixture

    :yields: uploaded study
    """
    study_dir = Path(__file__) \
        .parents[1] \
        .joinpath('dicoms', 'read_only')

    study = await async_api.Addon.Study.upload_dir_and_get(
        study_dir=study_dir,
        namespace_id=async_account.account.namespace_id,
        timeout=settings.API['upload_study_timeout'],
        ws_timeout=settings.API['ws_timeout'],
    )
    logger.info('Uploaded study %s', study.uuid)
    yield study
    await async_api.Study.delete(uuid=study.uuid).get()
    logger.info('Deleted study %s', study.uuid)


@pytest.fixture(scope='class')
async def async_readonly_study2(
    async_api,
    async_account,
):
    """Read only study.

    This is usefull for creating study one time per class.

    Dont use this study path manually
    Dont modify this study (use duplicate mechanism)

    :param async_api: api fixture
    :param async_account: account fixture

    :yields: uploaded study
    """
    study_dir = Path(__file__) \
        .parents[1] \
        .joinpath('dicoms', 'read_only2')

    study = await async_api.Addon.Study.upload_dir_and_get(
        study_dir=study_dir,
        namespace_id=async_account.account.namespace_id,
        timeout=settings.API['upload_study_timeout'],
        ws_timeout=settings.API['ws_timeout'],
    )
    logger.info('Uploaded study %s', study.uuid)
    yield study
    await async_api.Study.delete(uuid=study.uuid).get()
    logger.info('Deleted study %s', study.uuid)


@pytest.fixture(scope='class')
async def async_multi_series_study(
    async_api,
    async_account,
):
    """Read only multi  series study.

    This is usefull for creating study one time per class.

    Dont use this study path manually
    Dont modify this study (use duplicate mechanism)

    :param async_api: async_api fixture
    :param async_account: account fixture

    :yields: uploaded study
    """
    study_dir = Path(__file__) \
        .parents[1] \
        .joinpath('dicoms', 'multi_series')

    study = await async_api.Addon.Study.upload_dir_and_get(
        study_dir=study_dir,
        namespace_id=async_account.account.namespace_id,
        timeout=settings.API['upload_study_timeout'],
        ws_timeout=settings.API['ws_timeout'],
    )

    yield study
    await async_api.Study.delete(uuid=study.uuid).get()


@pytest.fixture
async def async_duplicate(async_api, async_create_group):
    """Duplicate study to group namespace.

    :param async_api: async_api fixture
    :param async_create_group: create_group fixture

    :yields: duplicate study function
    """
    studies = []

    async def _duplicate(
        from_study_uuid: str,
        to_namespace_id: Optional[str] = None,
        include_attachments: bool = False,
    ):
        if to_namespace_id is None:
            new_group = await async_create_group()
            to_namespace_id = new_group.namespace_id

        duplicated_study = await async_api.Addon.Study.duplicate_and_get(
            uuid=from_study_uuid,
            namespace_id=to_namespace_id,
            include_attachments=include_attachments,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Duplicated study %s', duplicated_study.uuid)
        studies.append(duplicated_study)
        return duplicated_study
    yield _duplicate
    logger.info('Start delete %s studies', str(len(studies)))
    for study in studies:
        await async_api.Study.delete(uuid=study.uuid).get()
        logger.info('Deleted study %s', study.uuid)

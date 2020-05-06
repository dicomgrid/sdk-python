"""Study fixtures."""

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
def storage_auto_remove(api):
    """Storage auto remove.

    In some tests we manually create a new studies in storage.
    If such test is failed, study can not be removed.
    This fixture remove study in any cases.

    :param api: api
    :yields: add to auto remove fn
    """
    studies = []

    def add_to_autoremove(engine_fqdn, namespace, study_uid):
        studies.append((engine_fqdn, namespace, study_uid))

    yield add_to_autoremove

    for engine_fqdn, namespace, study_uid in studies:
        api.Storage.Study.delete(
            engine_fqdn=engine_fqdn,
            namespace=namespace,
            study_uid=study_uid,
        )
        logger.info('Storage auto removed study %s', study_uid)


@pytest.fixture
def auto_remove(api):
    """Auto remove.

    In some tests we manually create a new studies in.
    If such test is failed, study can not be removed.
    This fixture remove study in any cases.

    :param api: api
    :yields: add to auto remove fn
    """
    studies = []

    def add_to_autoremove(study):
        studies.append(study)

    yield add_to_autoremove

    for study in studies:

        logger.info('Auto removed study %s', study.uuid)
        api.Study.delete(uuid=study.uuid).get()


@pytest.fixture
def upload_study(
    api,
    account,
    storage_cluster,
):
    """Upload study.

    :param api: api fixture
    :param account: account fixture
    :param storage_cluster: storage cluster

    :yields: upload study by path function
    """
    uploaded_studies = []

    def _upload_study(study_dir):
        new_study = api.Addon.Study.upload_and_get(
            study_dir=study_dir,
            namespace_id=account.account.namespace_id,
            timeout=settings.API['upload_study_timeout'],
            ws_timeout=settings.API['ws_timeout'],
        )
        logger.info('Uploaded study %s', new_study.uuid)
        uploaded_studies.append(new_study)
        return new_study
    yield _upload_study
    for study in uploaded_studies:
        api.Study.delete(uuid=study.uuid).get()
        logger.info('Deleted study %s', study.uuid)


@pytest.fixture(scope='class')
def readonly_study(
    api,
    account,
    storage_cluster,
):
    """Read only study.

    This is usefull for creating study one time per class.

    Dont use this study path manually
    Dont modify this study (use duplicate mechanism)

    :param api: api fixture
    :param account: account fixture
    :param storage_cluster: storage cluster

    :yields: uploaded study
    """
    study_dir = Path(__file__) \
        .parents[1] \
        .joinpath('dicoms', 'read_only')

    study = api.Addon.Study.upload_and_get(
        study_dir=study_dir,
        namespace_id=account.account.namespace_id,
        timeout=settings.API['upload_study_timeout'],
        ws_timeout=settings.API['ws_timeout'],
    )
    logger.info('Uploaded study %s', study.uuid)
    yield study
    api.Study.delete(uuid=study.uuid).get()
    logger.info('Deleted study %s', study.uuid)


@pytest.fixture(scope='class')
def readonly_study2(
    api,
    account,
    storage_cluster,
):
    """Read only study.

    This is usefull for creating study one time per class.

    Dont use this study path manually
    Dont modify this study (use duplicate mechanism)

    :param api: api fixture
    :param account: account fixture
    :param storage_cluster: storage cluster

    :yields: uploaded study
    """
    study_dir = Path(__file__) \
        .parents[1] \
        .joinpath('dicoms', 'read_only2')

    study = api.Addon.Study.upload_and_get(
        study_dir=study_dir,
        namespace_id=account.account.namespace_id,
        timeout=settings.API['upload_study_timeout'],
        ws_timeout=settings.API['ws_timeout'],
    )
    logger.info('Uploaded study %s', study.uuid)
    yield study
    api.Study.delete(uuid=study.uuid).get()
    logger.info('Deleted study %s', study.uuid)


@pytest.fixture(scope='class')
def multi_series_study(
    api,
    account,
):
    """Read only multi  series study.

    This is usefull for creating study one time per class.

    Dont use this study path manually
    Dont modify this study (use duplicate mechanism)

    :param api: api fixture
    :param account: account fixture

    :yields: uploaded study
    """
    study_dir = Path(__file__) \
        .parents[1] \
        .joinpath('dicoms', 'multi_series')

    study = api.Addon.Study.upload_and_get(
        study_dir=study_dir,
        namespace_id=account.account.namespace_id,
        timeout=settings.API['upload_study_timeout'],
        ws_timeout=settings.API['ws_timeout'],
    )

    yield study
    api.Study.delete(uuid=study.uuid).get()


@pytest.fixture
def duplicate(api, create_group, storage_cluster):
    """Duplicate study to group namespace.

    :param api: api fixture
    :param create_group: create_group fixture
    :param storage_cluster: storage cluster

    :yields: duplicate study function
    """
    studies = []

    def _duplicate(
        from_study_uuid: str,
        to_namespace_id: Optional[str] = None,
        include_attachments: bool = False,
    ):
        if to_namespace_id is None:
            new_group = create_group()
            to_namespace_id = new_group.namespace_id

        duplicated_study = api.Addon.Study.duplicate_and_get(
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
        api.Study.delete(uuid=study.uuid).get()
        logger.info('Deleted study %s', study.uuid)

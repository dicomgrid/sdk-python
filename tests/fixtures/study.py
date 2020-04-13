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


@pytest.fixture
def upload_study(
    api,
    account,
):
    """Upload study.

    :param api: api fixture
    :param account: account fixture

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
        uploaded_studies.append(new_study)
        return new_study
    yield _upload_study
    for study in uploaded_studies:
        api.Study.delete(uuid=study.uuid).get()


@pytest.fixture(scope='class')
def readonly_study(
    api,
    account,
):
    """Read only study.

    This is usefull for creating study one time per class.

    Dont use this study path manually
    Dont modify this study (use duplicate mechanism)

    :param api: api fixture
    :param account: account fixture

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

    yield study
    api.Study.delete(uuid=study.uuid).get()


@pytest.fixture(scope='class')
def readonly_study2(
    api,
    account,
):
    """Read only study.

    This is usefull for creating study one time per class.

    Dont use this study path manually
    Dont modify this study (use duplicate mechanism)

    :param api: api fixture
    :param account: account fixture

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

    yield study
    api.Study.delete(uuid=study.uuid).get()


@pytest.fixture
def duplicate(api, create_group):
    """Duplicate study to group namespace.

    :param api: api fixture
    :param create_group: create_group fixture

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
        studies.append(duplicated_study)
        return duplicated_study
    yield _duplicate
    for study in studies:
        api.Study.delete(uuid=study.uuid).get()

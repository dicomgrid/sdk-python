import json
import logging
from asyncio import sleep
from time import monotonic
from typing import List, NamedTuple, Optional, Tuple

import pytest
from box import Box
from dynaconf import settings

from ambra_sdk.exceptions.service import DuplicateName, NotEmpty
from ambra_sdk.models import Group
from ambra_sdk.service.filtering import Filter, FilterCondition
from ambra_sdk.service.query import AsyncQueryO, AsyncQueryOPF

logger = logging.getLogger(__name__)


class UserParams(NamedTuple):
    """User params."""

    account: Box
    user: Box


class GroupParams(NamedTuple):
    """Group params."""

    uuid: str
    namespace_id: str
    name: str


async def async_create_account(
    async_api,
    account_name: str,
) -> Tuple[Box, Box]:
    """Create new account.

    :param async_api: async_api
    :param account_name: account name
    :raises RuntimeError: Cant find account
    :return: user params
    """
    # If account exists - raise DuplicateName error
    await AsyncQueryO(
        api=async_api,
        url='/account/add',
        request_data={
            'name': account_name,
        },
        errors_mapping={
            'DUPLICATE_NAME': DuplicateName(),
        },
        required_sid=True,
    ).get()

    account = await async_api \
        .Account \
        .list() \
        .filter_by(
            Filter(
                'name',
                FilterCondition.equals,
                account_name,
            ),
        ).first()
    if account is None:
        raise RuntimeError('Cant find test account')

    # set role permissions
    admin_role = await async_api \
        .Role \
        .list(account_id=account.uuid) \
        .filter_by(
            Filter(
                'name',
                FilterCondition.equals,
                'Administrator',
            ),
        ).first()

    if admin_role is None:
        raise RuntimeError('Cant find admin role')

    await async_api.Role.set(
        uuid=admin_role.uuid,
        permissions=json.dumps(
            {
                'study_delete': 1,
                'study_duplicate': 1,
                'study_split': 1,
                'study_merge': 1,
                'study_delete_image': 1,
                'customcode_view': 1,
                'customcode_edit': 1,
                'customcode_deploy': 1,
            },
        ),
    ).get()

    user = await async_api.User.get(account_id=account.uuid).get()
    logger.info('Created account %s', account.name)
    return (account, user)


async def async_account_studies(async_api, account) -> List[Box]:
    """List of  account studies.

    :param async_api: async_api
    :param account: account
    :return: list of studies
    """
    account_namespaces = [account.namespace_id]
    group_namespaces = []
    query = async_api \
        .Group \
        .list(account_id=account.uuid) \
        .only(Group.namespace_id).all()
    async for group in query:
        group_namespaces.append(group.namespace_id)
    account_namespaces.extend(group_namespaces)

    # Method study list does not support in_condition filtering for namespace !
    acc_studies = []
    for account_namespace in account_namespaces:
        query = async_api \
            .Study \
            .list() \
            .filter_by(
                Filter(
                    field_name='phi_namespace',
                    condition=FilterCondition.equals,
                    value=account_namespace,
                ),
            ).all()
        async for study in query:
            acc_studies.append(study)
    return acc_studies


async def async_delete_account(async_api, account) -> Box:
    """Delete account.

    :param async_api: async_api
    :param account: account
    :raises RuntimeError: if account have undeleted studies
    """
    try:
        await AsyncQueryO(
            api=async_api,
            url='/account/delete/',
            request_data={
                'uuid': account.uuid,
            },
            errors_mapping={
                'NOT_EMPTY': NotEmpty(),
            },
            required_sid=True,
        ).get()
    except NotEmpty:
        acc_studies = await async_account_studies(async_api, account)
        raise RuntimeError(
            'Account have undeleted studies:\n{studies}'.format(
                studies='\n'.join(
                    [
                        str((study.uuid, study.study_uid))
                        for study in acc_studies
                    ],
                ),
            ),
        )


async def async_clear_studies(async_api, account):
    """Delete account studies.

    :param async_api: async_api
    :param account: account
    """
    account_namespaces = [account.namespace_id]
    group_namespaces = []
    query = async_api \
        .Group \
        .list(account_id=account.uuid) \
        .only(Group.namespace_id) \
        .all()
    async for group in query:
        group_namespaces.append(group.namespace_id)
    account_namespaces.extend(group_namespaces)

    # Method study list does not support in_condition filtering for namespace !
    # So delete studies in loop
    for account_namespace in account_namespaces:
        query = async_api \
            .Study \
            .list() \
            .filter_by(
                Filter(
                    field_name='phi_namespace',
                    condition=FilterCondition.equals,
                    value=account_namespace,
                ),
            ).all()
        async for study in query:
            study_uid = study.uuid
            logger.error('Remove undeleted study %s', study_uid)
            await async_api.Study.delete(uuid=study_uid).get()


@pytest.fixture(scope='module')  # NOQA:WPS210,WPS231
async def async_account(async_api):
    """Get account.

    :param async_api: ambra async_api

    :yields: test account

    :raises RuntimeError: On deleted account with existing studies
    :raises TimeoutError: Time for waiting account deletion is out
    """
    account_name = settings.ASYNC_TEST_ACCOUNT_NAME
    try:
        account, user = await async_create_account(async_api, account_name)
    except DuplicateName:
        logger.error('Duplicated account: %s', account_name)
        account = await async_api \
            .Account \
            .list() \
            .filter_by(
                Filter(
                    'name',
                    FilterCondition.equals,
                    account_name,
                ),
            ).first()
        if account is None:
            raise RuntimeError('Account duplicated but not exists')
        await async_clear_studies(async_api, account)
        await async_delete_account(async_api, account)
        account, user = await async_create_account(async_api, account_name)

    yield UserParams(
        account=account,
        user=user,
    )
    await async_delete_account(async_api, account)
    start = monotonic()
    while True:
        if monotonic() - start >= settings.API['account_deletion_timeout']:
            raise TimeoutError('Account still exists')
        account = await async_api \
            .Account \
            .list() \
            .filter_by(
                Filter(
                    'name',
                    FilterCondition.equals,
                    account_name,
                ),
            ).first()
        if account is None:
            return
        await sleep(settings.API['account_deletion_check_interval'])


@pytest.fixture
async def async_create_group(async_api, account):
    """Create new group in account.

    :param async_api: async_api fixture
    :param account: account fixture
    :yields: create_group function
    """
    groups = []
    group_counter = 0

    async def _create_group(name: Optional[str] = None):
        nonlocal group_counter
        group_counter += 1
        if name is None:
            name = 'SDK_TEST_GROUP_{gnum}'.format(gnum=group_counter)

        account_id = account.account.uuid
        response = await async_api.Group.add(
            account_id=account_id,
            name=name,
        ).get()
        group = GroupParams(
            uuid=response.uuid,
            namespace_id=response.namespace_id,
            name=name,
        )
        groups.append(group)
        # add account user to the group
        await async_api.Group.user_add(
            uuid=group.uuid,
            user_id=account.user.uuid,
        ).get()

        return group

    yield _create_group
    for group in groups:
        await async_api.Group.delete(uuid=group.uuid).get()

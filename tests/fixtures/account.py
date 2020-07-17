"""Account, user fixtures."""

import json
import logging
from time import monotonic, sleep
from typing import List, NamedTuple, Optional, Tuple

import pytest
from box import Box
from dynaconf import settings

from ambra_sdk.exceptions.service import DuplicateName, NotEmpty
from ambra_sdk.models import Group
from ambra_sdk.service.filtering import Filter, FilterCondition
from ambra_sdk.service.query import QueryO, QueryOPF

logger = logging.getLogger(__name__)


@pytest.fixture(scope='module')
def storage_cluster(api, request):
    """Specific storage cluster.

    :param api: api
    :param request: pytest request

    :raises RuntimeError: Unknown cluster name
    :return: cluster box
    """
    cluster_name = request.param
    cluster = None
    if cluster_name != 'DEFAULT':
        cluster = QueryOPF(
            api=api,
            url='/cluster/list',
            request_data={},
            errors_mapping={},
            paginated_field='clusters',
            required_sid=True,
        ).filter_by(Filter(
            'name',
            FilterCondition.equals,
            cluster_name,
        )).first()
        if cluster is None:
            raise RuntimeError(
                'Unknown cluster name {name}'.format(name=cluster_name),
            )
    return cluster


class UserParams(NamedTuple):
    """User params."""

    account: Box
    user: Box


class GroupParams(NamedTuple):
    """Group params."""

    uuid: str
    namespace_id: str
    name: str


def create_account(api, account_name: str) -> Tuple[Box, Box]:
    """Create new account.

    :param api: api
    :param account_name: account name
    :raises RuntimeError: Cant find account
    :return: user params
    """
    # If account exists - raise DuplicateName error
    QueryO(
        api=api,
        url='/account/add',
        request_data={
            'name': account_name,
        },
        errors_mapping={
            'DUPLICATE_NAME': DuplicateName(),
        },
        required_sid=True,
    ).get()

    account = api \
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
    admin_role = api \
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

    api.Role.set(
        uuid=admin_role.uuid,
        permissions=json.dumps(
            {
                'study_delete': 1,
                'study_duplicate': 1,
                'study_split': 1,
                'study_merge': 1,
                'study_delete_image': 1,
            },
        ),
    ).get()

    user = api.User.get(account_id=account.uuid).get()
    logger.info('Created account %s', account.name)
    return (account, user)


def account_studies(api, account) -> List[Box]:
    """List of  account studies.

    :param api: api
    :param account: account
    :return: list of studies
    """
    account_namespaces = [account.namespace_id]
    group_namespaces = [
        group.namespace_id for group in
        api.Group.list(account_id=account.uuid).only(Group.namespace_id).all()
    ]
    account_namespaces.extend(group_namespaces)

    # Method study list does not support in_condition filtering for namespace !
    acc_studies = []
    for account_namespace in account_namespaces:
        studies = api \
            .Study \
            .list() \
            .filter_by(
                Filter(
                    field_name='phi_namespace',
                    condition=FilterCondition.equals,
                    value=account_namespace,
                ),
            ).all()
        acc_studies.extend(list(studies))
    return acc_studies


def delete_account(api, account) -> Box:
    """Delete account.

    :param api: api
    :param account: account
    :raises RuntimeError: if account have undeleted studies
    """
    try:
        QueryO(
            api=api,
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
        acc_studies = account_studies(api, account)
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


def clear_studies(api, account):
    """Delete account studies.

    :param api: api
    :param account: account
    """
    account_namespaces = [account.namespace_id]
    group_namespaces = [
        group.namespace_id for group in
        api.Group.list(account_id=account.uuid).only(Group.namespace_id).all()
    ]
    account_namespaces.extend(group_namespaces)

    # Method study list does not support in_condition filtering for namespace !
    # So delete studies in loop
    for account_namespace in account_namespaces:
        studies = api \
            .Study \
            .list() \
            .filter_by(
                Filter(
                    field_name='phi_namespace',
                    condition=FilterCondition.equals,
                    value=account_namespace,
                ),
            ).all()
        for study in studies:
            study_uid = study.uuid
            logger.error('Remove undeleted study %s', study_uid)
            api.Study.delete(uuid=study_uid).get()


@pytest.fixture(scope='module')  # NOQA:WPS210,WPS231
def account(api, storage_cluster):
    """Get account.

    :param api: ambra api
    :param storage_cluster: storage cluster

    :yields: test account

    :raises RuntimeError: On deleted account with existing studies
    :raises TimeoutError: Time for waiting account deletion is out
    """
    account_name = settings.TEST_ACCOUNT_NAME
    if storage_cluster:
        account_name = '{account}_{cluster}'.format(
            account=account_name,
            cluster=storage_cluster.name,
        )

    try:
        account, user = create_account(api, account_name)
    except DuplicateName:
        logger.error('Duplicated account: %s', account_name)
        account = api \
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
        clear_studies(api, account)
        delete_account(api, account)
        account, user = create_account(api, account_name)

    if storage_cluster is not None:
        QueryO(
            api=api,
            url='/cluster/account/bind',
            request_data={
                'account_id': account.uuid,
                'cluster_id': storage_cluster.uuid,
            },
            errors_mapping={},
            required_sid=True,
        ).get()
        logger.info(
            'Bind account to storage cluster {name}'.format(
                name=storage_cluster.name,
            ),
        )

    yield UserParams(
        account=account,
        user=user,
    )
    delete_account(api, account)
    start = monotonic()
    while True:
        if monotonic() - start >= settings.API['account_deletion_timeout']:
            raise TimeoutError('Account still exists')
        account = api \
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
        sleep(settings.API['account_deletion_check_interval'])


@pytest.fixture
def create_group(api, account):
    """Create new group in account.

    :param api: api fixture
    :param account: account fixture
    :yields: create_group function
    """
    groups = []
    group_counter = 0

    def _create_group(name: Optional[str] = None):
        nonlocal group_counter
        group_counter += 1
        if name is None:
            name = 'SDK_TEST_GROUP_{gnum}'.format(gnum=group_counter)

        account_id = account.account.uuid
        response = api.Group.add(
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
        api.Group.user_add(
            uuid=group.uuid,
            user_id=account.user.uuid,
        ).get()

        return group

    yield _create_group
    for group in groups:
        api.Group.delete(uuid=group.uuid).get()

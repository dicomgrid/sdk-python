"""Account, user fixtures."""

import json
import logging
from typing import NamedTuple, Optional

import pytest
from box import Box
from dynaconf import settings

from ambra_sdk.models import Group
from ambra_sdk.service.filtering import Filter, FilterCondition

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


@pytest.fixture(scope='module')  # NOQA:WPS210,WPS231
def account(api):
    """Get account.

    :param api: ambra api

    :yields: test account

    :raises RuntimeError: On deleted account with existing studies
    """
    test_account_name = settings.TEST_ACCOUNT_NAME

    # Create new account
    # Private api
    account_data = {
        'name': test_account_name,
    }
    response = api.service_post(
        '/account/add',
        required_sid=True,
        data=account_data,
    )
    response_json = response.json()
    # Account created (it can be if some testes in
    if response.status_code == 412:
        error = response_json['error_type']
        if error == 'NOT_SYSADMIN_OR_SUPPORT':
            raise RuntimeError('Not permissions for create new account')
        elif error == 'DUPLICATE_NAME':
            # Need delete?
            pass  # NOQA:WPS420

    account_response = api \
        .Account \
        .list() \
        .filter_by(
            Filter(
                'name',
                FilterCondition.equals,
                test_account_name,
            ),
        ).first()
    if account_response is None:
        raise RuntimeError('Cant find test account')

    # Clear undeleted studies

    account_namespaces = [account_response.namespace_id]
    group_namespaces = [
        group.namespace_id for group in api.Group
        .list(account_id=account_response.uuid)
        .only(Group.namespace_id).all()
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

    # set role permissions
    admin_role = api \
        .Role \
        .list(account_id=account_response.uuid) \
        .filter_by(
            Filter(
                'name',
                FilterCondition.equals,
                'Administrator',
            ),
        ).first()

    if admin_role is None:
        raise RuntimeError('Cant find admin role')

    response = api.Role.set(
        uuid=admin_role.uuid,
        permissions=json.dumps(
            {
                'webhook_view': 1,
                'webhook_edit': 1,
                'study_delete': 1,
                'study_duplicate': 1,
                'study_delete_image': 1,
                'study_manual_route': 1,
                'customcode_view': 1,
                'customcode_edit': 1,
                'customcode_deploy': 1,
            },
        )).get()

    user_response = api.User.get(account_id=account_response.uuid).get()
    yield UserParams(
        account=account_response,
        user=user_response,
    )

    # Delete account
    # Private api
    response = api.service_post(
        '/account/delete',
        required_sid=True,
        data={
            'uuid': account_response.uuid,
        },
    )
    # TODO : mb delete studies?
    if response.status_code == 412 and \
       response.json()['error_type'] == 'NOT_EMPTY':
        raise RuntimeError('Test account have undeleted studies')


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

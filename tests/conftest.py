import asyncio

import pytest
from dynaconf import settings

from ambra_sdk.api import Api, AsyncApi


@pytest.fixture(scope='session', autouse=True)
def set_test_settings():
    """Set dynaconf env for testing."""
    settings.configure(ENV_FOR_DYNACONF='testing')


@pytest.fixture(scope='module')
def api():
    """Get api.

    :yields: valid  ambra api
    """
    url = settings.API['url']
    username = settings.API['username']
    password = settings.API['password']
    api = Api.with_creds(
        url,
        username,
        password,
        'SDK testing',
    )
    yield api
    api.logout()


@pytest.fixture(scope='module')
def event_loop():
    """Event loop module scoped.

    :return: event loop for module scope
    """
    return asyncio.get_event_loop()


@pytest.fixture(scope='module')
async def async_api(event_loop):
    """Get api.

    :param event_loop: event loop for modules scope
    :yields: valid  ambra api
    """
    url = settings.API['url']
    username = settings.API['username']
    password = settings.API['password']
    api = AsyncApi.with_creds(
        url,
        username,
        password,
        'SDK testing',
    )
    yield api
    await api.logout()


pytest_plugins = [
    'tests.fixtures.account',
    'tests.fixtures.async_account',
    'tests.fixtures.study',
    'tests.fixtures.async_study',
    'tests.fixtures.ws',
    'tests.fixtures.customfield',
]


def pytest_generate_tests(metafunc):
    """Gen tests.

    :param metafunc: metafunc
    """
    if 'storage_cluster' in metafunc.fixturenames:
        cluster_names = settings \
            .from_env('testing') \
            .get('CLUSTER_STORAGE_NAMES', ['DEFAULT'])
        metafunc.parametrize(
            'storage_cluster',
            cluster_names,
            indirect=True,
        )

import pytest
from dynaconf import settings

from ambra_sdk.api import Api


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
    )
    yield api
    api.logout()


pytest_plugins = [
    'tests.fixtures.account',
    'tests.fixtures.study',
    'tests.fixtures.ws',
]

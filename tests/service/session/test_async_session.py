import pytest
from dynaconf import settings

from ambra_sdk.api import AsyncApi
from ambra_sdk.exceptions.service import InvalidCredentials, Lockout
from ambra_sdk.service.entrypoints import AsyncSession


@pytest.mark.asyncio
class TestAsyncSessionEntrypoint:
    """Test Session entrypoint."""

    async def test_get_sid_success(self, async_api):
        """Test success get sid from session."""
        session = AsyncSession(api=async_api)
        username = settings.API['username']
        password = settings.API['password']
        sid = await session.get_sid(username, password)
        assert sid

    async def test_get_sid_bad_creds(self):
        """Test unsuccess get sid from session.

        Case: bad creds
        """
        url = settings.API['url']
        api = AsyncApi.with_creds(url, 'bad_us', 'bad_pass')
        session = AsyncSession(api=api)

        # If try auth with bad creds. Server can answer:
        # Lockout(Too many failed attemps)
        with pytest.raises((InvalidCredentials, Lockout)):
            await session.get_sid('bad_us', 'bad_pass')
        await api.logout()


@pytest.mark.asyncio
class TestSession:
    """Test Session."""

    async def test_user(self, async_api):
        """Test user method."""
        user = await async_api.Session.user().get()
        assert user.namespace_id

    async def test_permissions(self, async_api):
        """Test permissions method."""
        resp = await async_api.Session.user().get()
        namespace_id = resp.namespace_id
        resp = await async_api.Session \
            .permissions(namespace_id=namespace_id) \
            .only(['study_download', 'study_upload']) \
            .get()
        assert len(resp) == 2

import pytest


@pytest.mark.asyncio
class TestAsyncUser:
    """Test async user."""

    async def test_get(self, async_api):
        """Test user get."""
        user = await async_api.User.get().get()
        assert user

    async def test_get_with_only(self, async_api):
        """Test user get."""
        user = await async_api.User.get().only('email').get()
        assert 'email' in user
        # + response dict
        assert len(user) == 1

        user = await async_api.User.get().only(['email', 'name']).get()
        assert 'email' in user
        assert 'name' in user
        # + response dict
        assert len(user) == 2

    async def test_namespace_list(self, async_api):
        """Test namespace get."""
        namespaces = await async_api.User.namespace_list().get()
        assert namespaces.namespaces

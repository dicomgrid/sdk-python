import pytest
from dynaconf import settings


@pytest.mark.asyncio
class TestAsyncAccount:
    """Test async account."""

    async def test_account_list(self, async_api):
        """Test account list."""
        accounts = []
        async for account in async_api.Account.list().all():
            accounts.append(account)
        assert list(accounts)

    async def test_account(self, async_account):
        """Test account list."""
        test_account_name = settings.ASYNC_TEST_ACCOUNT_NAME
        assert async_account.account.name == test_account_name

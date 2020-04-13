from dynaconf import settings


class TestAccount:
    """Test Account."""

    def test_account_list(self, api):
        """Test account list."""
        accounts = api.Account.list().all()
        assert list(accounts)

    def test_account(self, account):
        """Test account list."""
        assert account.account.name == settings.TEST_ACCOUNT_NAME

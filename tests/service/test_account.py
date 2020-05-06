from dynaconf import settings


class TestAccount:
    """Test Account."""

    def test_account_list(self, api):
        """Test account list."""
        accounts = api.Account.list().all()
        assert list(accounts)

    def test_account(self, account, storage_cluster):
        """Test account list."""
        test_account_name = settings.TEST_ACCOUNT_NAME
        if storage_cluster:
            test_account_name = '{account}_{cluster}'.format(
                account=test_account_name,
                cluster=storage_cluster.name,
            )

        assert account.account.name == test_account_name

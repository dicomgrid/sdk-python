import pytest

from ambra_sdk.exceptions.service import InvalidJson


class TestServiceErrors:
    """Test service errors."""

    def test_list_in_error_type(self, api, account):
        """Test list in error type."""
        # this call is return list in errors:
        with pytest.raises(InvalidJson) as exc_info:
            api.Role.add(
                account_id=account.account.uuid,
                name='some_name',
                settings='bad_json',
            ).get()
        assert exc_info.value.error_type == ['INVALID_JSON', 'settings']

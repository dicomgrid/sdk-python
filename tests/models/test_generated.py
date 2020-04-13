"""This is test python syntax of generated models."""

import pytest

from ambra_sdk.models.generated import *  # NOQA
from ambra_sdk.models.generated import Account, Role


def test_generated_models():
    """Do nothing.

    This fn test syntax errors by importing modules.
    """
    pass  # NOQA


class TestGeneratedModels:
    """Test generated models."""

    def test_base_model_parent(self):
        """Test model parent."""
        assert Account.billing._parent == Account

    def test_field_name(self):
        """Test field name."""
        assert Account.billing._name == 'billing'

    def test_full_name(self):
        """Test full name."""
        assert Account.role.permissions._full_name  \
            == 'Account.role.permissions'

    def test_base_model_descriptor(self):
        """Test full name."""
        instance = Account(uuid='123')
        assert instance.uuid == '123'
        instance.uuid = '1234'
        assert instance.uuid == '1234'
        assert instance.updated is None
        with pytest.raises(ValueError):
            # updated is datetime field
            instance.updated = 3

    def test_fk(self):
        """Test fk."""
        assert Account.role._parent == Account
        # New instance of model
        assert Account.role.permissions._parent != Role
        assert Account.role.permissions._parent.__name__ == 'Role'

    def test_fk_descriptor_validate(self):
        """Test fk descriptor validation."""
        role = Role(permissions='123')
        account = Account(role=role)
        assert account.role.permissions == '123'
        account.role.permissions = '1234'
        assert account.role.permissions == '1234'

        with pytest.raises(ValueError):
            account.role.account_id = 'abc'

        with pytest.raises(ValueError):
            account.role = 'abc'

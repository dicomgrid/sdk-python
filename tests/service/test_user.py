
class TestUser:
    """Test User."""

    def test_get(self, api):
        """Test user get."""
        user = api.User.get().get()
        assert user

    def test_get_with_only(self, api):
        """Test user get."""
        user = api.User.get().only('email').get()
        assert 'email' in user
        # + response dict
        assert len(user) == 1

        user = api.User.get().only(['email', 'name']).get()
        assert 'email' in user
        assert 'name' in user
        # + response dict
        assert len(user) == 2

    def test_namespace_list(self, api):
        """Test user get."""
        namespaces = api.User.namespace_list().get()
        assert namespaces.namespaces

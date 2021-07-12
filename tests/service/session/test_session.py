import pytest
from dynaconf import settings

from ambra_sdk.api import Api
from ambra_sdk.exceptions.service import InvalidCredentials, Lockout
from ambra_sdk.service.entrypoints import Session


class TestSessionEntrypoint:
    """Test Session entrypoint."""

    def test_get_sid_success(self, api):
        """Test success get sid from session."""
        session = Session(api=api)
        username = settings.API['username']
        password = settings.API['password']
        sid = session.get_sid(username, password)
        assert sid

    def test_get_sid_bad_creds(self):
        """Test unsuccess get sid from session.

        Case: bad creds
        """
        url = settings.API['url']
        api = Api.with_creds(url, 'bad_us', 'bad_pass')
        session = Session(api=api)

        # If try auth with bad creds. Server can answer:
        # Lockout(Too many failed attemps)
        with pytest.raises((InvalidCredentials, Lockout)):
            session.get_sid('bad_us', 'bad_pass')


class TestSession:
    """Test Session."""

    def test_user(self, api):
        """Test user method."""
        user = api.Session.user().get()
        assert user.namespace_id

    def test_permissions(self, api):
        """Test permissions method."""
        resp = api.Session.user().get()
        namespace_id = resp.namespace_id
        resp = api.Session \
            .permissions(namespace_id=namespace_id) \
            .only(['study_download', 'study_upload']) \
            .get()
        assert len(resp) == 2

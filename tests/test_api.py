import pytest
import requests
from dynaconf import settings

from ambra_sdk.api import Api
from ambra_sdk.exceptions.service import InvalidCredentials


class TestApi:
    """Test API."""

    def test_with_sid(self):
        """Test API initialization from sid."""
        url = 'url'
        sid = 'sid'
        api = Api.with_sid(url, sid)
        assert api._creds is None
        assert api._sid == sid
        assert api._api_url == url
        assert api._service_session is None
        assert api._storage_session is None
        assert api.service_retry_params
        assert api.storage_retry_params

    def test_post(self, api, requests_mock):
        """Test post method."""
        api_url = settings.API['url']
        url = 'some_url'
        requests_mock.register_uri(
            'POST',
            '{api_url}{url}'.format(api_url=api_url, url=url),
            text='test',
        )
        resp = api.service_post(url, {'a': 1})
        assert resp.status_code == 200
        assert resp.text == 'test'

    def test_get_new_sid(self, api):
        """Test get new sid."""
        assert api._sid is None
        api.get_new_sid()
        assert api._sid is not None

    def test_get_new_sid_bad_creds(self):
        """Test fail get new sid.

        Case: bad credentials.
        """
        url = settings.API['url']
        username = settings.API['username']
        password = 'bad pass'
        api = Api.with_creds(url, username, password)
        with pytest.raises(InvalidCredentials):
            api.get_new_sid()

    def test_logout(self, api):
        """Test logout."""
        api.get_new_sid()
        assert api._sid is not None
        api.logout()
        assert api._sid is None

    def test_retry_get_with_new_sid(self, api):
        """Test retry get with new sid."""
        api._sid = 'Wrong sid'
        try:
            api.Session.user().get()
        except Exception:
            pytest.fail('Something goes wrong with retrying with new sid')

    def test_retry_first_with_new_sid(self, api):
        """Test retry first with new sid.

        This test also test all method
        (first run all method and return first result)
        """
        api._sid = 'Wrong sid'
        try:
            api.Study.list().first()
        except Exception:
            pytest.fail('Something goes wrong with retrying with new sid')

    def test_headers(self, requests_mock):
        """Test post method."""
        client_name = 'client name'

        def matcher(request):  # NOQA: WPS430
            r = request._request
            assert 'SDK-VERSION' in r.headers
            assert r.headers['SDK-CLIENT-NAME'] == client_name
            return requests.Response()

        api = Api(url='http://127.0.0.1', client_name=client_name)
        url = '/some_url'
        requests_mock.add_matcher(matcher)
        api.service_post(url, {'a': 1})

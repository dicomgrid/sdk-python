import asyncio
from time import monotonic

import pytest
from aiohttp import ClientSession
from aioresponses import CallbackResult, aioresponses
from dynaconf import settings

from ambra_sdk.api import AsyncApi
from ambra_sdk.api.base_api import RateLimit, RateLimits
from ambra_sdk.exceptions.service import InvalidCredentials


class FixedAioresponses(aioresponses):
    """Fixed Aioresponses.

    Actually in ClientSession._request
    aiohttp update headers with default headers.
    This hack support this operation for aioresponses.
    """

    async def _request_mock(
        self,
        orig_self: ClientSession,
        *args,
        **kwargs,
    ):
        headers = kwargs.get('headers', {})
        kwargs['headers'] = orig_self._prepare_headers(headers)
        return await super()._request_mock(orig_self, *args, **kwargs)


class TestAsyncApi:
    """Test async API."""

    def test_with_sid(self):
        """Test API initialization from sid."""
        url = 'url'
        sid = 'sid'
        api = AsyncApi.with_sid(url, sid)
        assert api._creds is None
        assert api._sid == sid
        assert api._api_url == url
        assert api._service_session is None
        assert api._storage_session is None

    @pytest.mark.asyncio
    async def test_post(self, async_api):
        """Test post method."""
        api_url = settings.API['url']
        url = 'some_url'
        with aioresponses() as mocked:
            mocked.post(
                '{api_url}{url}'.format(api_url=api_url, url=url),
                status=200,
                body='test',
            )
            resp = await async_api.service_post(url, {'a': 1})
            assert resp.status == 200
            assert await resp.text() == 'test'

    @pytest.mark.asyncio
    async def test_get_new_sid(self, async_api):
        """Test get new sid."""
        assert async_api._sid is None
        await async_api.get_new_sid()
        assert async_api._sid is not None

    @pytest.mark.asyncio
    async def test_get_new_sid_bad_creds(self):
        """Test fail get new sid.

        Case: bad credentials.
        """
        url = settings.API['url']
        username = settings.API['username']
        password = 'bad pass'
        api = AsyncApi.with_creds(url, username, password)
        with pytest.raises(InvalidCredentials):
            await api.get_new_sid()
        await api.logout()

    @pytest.mark.asyncio
    async def test_logout(self):
        """Test logout."""
        url = settings.API['url']
        username = settings.API['username']
        password = settings.API['password']
        api = AsyncApi.with_creds(
            url,
            username,
            password,
            'SDK testing',
        )
        await api.get_new_sid()
        assert api._sid is not None
        await api.logout()
        assert api._sid is None

    @pytest.mark.asyncio
    async def test_retry_get_with_new_sid(self, async_api):
        """Test retry get with new sid."""
        async_api._sid = 'Wrong sid'
        try:
            await async_api.Session.user().get()
        except Exception:
            pytest.fail('Something goes wrong with retrying with new sid')

    @pytest.mark.asyncio
    async def test_retry_first_with_new_sid(self, async_api):
        """Test retry first with new sid.

        This test also test all method
        (first run all method and return first result)
        """
        async_api._sid = 'Wrong sid'
        try:
            await async_api.Study.list().first()
        except Exception:
            pytest.fail('Something goes wrong with retrying with new sid')

    @pytest.mark.asyncio
    async def test_service_headers(self):
        """Test service headers."""
        client_name = 'client name'

        def matcher(url, **kwargs):  # NOQA: WPS430
            headers = kwargs['headers']
            assert 'SDK-VERSION' in headers
            assert headers['SDK-CLIENT-NAME'] == client_name

            assert 'default' in headers
            assert headers['default'] == 'default'

            assert 'storage_default' not in headers

            assert 'service_default' in headers
            assert headers['service_default'] == 'default'

            return CallbackResult(status=200)

        api = AsyncApi(url='http://127.0.0.1', client_name=client_name)
        api.default_headers['default'] = 'default'
        api.storage_default_headers['storage_default'] = 'default'
        api.service_default_headers['service_default'] = 'default'
        url = '/some_url'

        with FixedAioresponses() as mocked:
            mocked.post(
                '{api_url}{url}'.format(
                    api_url=api._api_url,
                    url=url,
                ),
                callback=matcher,
            )
            await api.service_post(url, {'a': 1})
        await api.logout()

    @pytest.mark.asyncio
    async def test_storage_headers(self):
        """Test storage headers."""
        client_name = 'client name'

        def matcher(url, **kwargs):  # NOQA: WPS430
            headers = kwargs['headers']
            assert 'SDK-VERSION' in headers
            assert headers['SDK-CLIENT-NAME'] == client_name

            assert 'default' in headers
            assert headers['default'] == 'default'

            assert 'service_default' not in headers

            assert 'storage_default' in headers
            assert headers['storage_default'] == 'default'

            return CallbackResult(status=200)

        api = AsyncApi(url='http://127.0.0.1', client_name=client_name)
        api.default_headers['default'] = 'default'
        api.storage_default_headers['storage_default'] = 'default'
        api.service_default_headers['service_default'] = 'default'
        url = '/some_url'

        with FixedAioresponses() as mocked:
            mocked.post(
                url=url,
                callback=matcher,
            )
            await api.storage_post(
                url,
                required_sid=False,
                params={},
            )
        await api.logout()

    @pytest.mark.asyncio
    async def test__wait_for_service_request(self):
        """Test wait for service request."""
        api = AsyncApi.with_creds(  # NOQA:S106
            username='username',
            url='http://127.0.0.1',
            password='pass',
        )
        assert api._rate_limits
        assert api._rate_limits_lock
        await api._wait_for_service_request('')
        assert api._last_request_time
        assert api._last_call_period

        now = monotonic()
        api._last_request_time = now
        api._last_call_period = 2.0  # 2 seconds
        await api._wait_for_service_request('')
        assert monotonic() - now > 2.0

    @pytest.mark.asyncio
    async def test__wait_for_service_request_in_multiple_tasks(self):
        """Test wait for service request in multiple tasks."""
        api = AsyncApi.with_creds(  # NOQA:S106
            username='username',
            url='http://127.0.0.1',
            password='pass',
            rate_limits=RateLimits(
                default=RateLimit(1, 1),
                get_limit=RateLimit(2, 1),
                special=None,
            ),
        )
        now = monotonic()
        concurrent_tasks = 3

        await asyncio.wait(
            [
                asyncio.Task(api._wait_for_service_request('some_url'))
                for _ in range(concurrent_tasks)
            ],
        )
        spent_time = monotonic() - now
        assert spent_time > (concurrent_tasks - 1) * 1  # NOQA:WPS345
        assert spent_time < (concurrent_tasks + 1) * 1  # NOQA:WPS345

        now = monotonic()
        concurrent_tasks = 3

        await asyncio.wait(
            [
                asyncio.Task(api._wait_for_service_request('some_url/get'))
                for _ in range(concurrent_tasks)
            ],
        )
        spent_time = monotonic() - now
        assert spent_time > (concurrent_tasks - 1) * 0.5
        assert spent_time < (concurrent_tasks + 1) * 1  # NOQA:WPS345

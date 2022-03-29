"""Ambra async api."""

import logging
from asyncio import Lock, sleep
from time import monotonic
from typing import Awaitable, Callable, Optional, TypeVar

import aiohttp

from ambra_sdk.api.base_api import BaseApi
from ambra_sdk.async_addon.addon import Addon
from ambra_sdk.clear_params import clear_params
from ambra_sdk.exceptions.service import AuthorizationRequired
from ambra_sdk.exceptions.storage import AccessDenied
from ambra_sdk.request_args import AioHTTPRequestArgs
from ambra_sdk.service.entrypoints import (
    AsyncAccount,
    AsyncActivity,
    AsyncAnalytics,
    AsyncAnnotation,
    AsyncAnonymization,
    AsyncAppointment,
    AsyncAudit,
    AsyncCase,
    AsyncCustomcode,
    AsyncCustomfield,
    AsyncDestination,
    AsyncDicomdata,
    AsyncDictionary,
    AsyncFilter,
    AsyncGroup,
    AsyncHelp,
    AsyncHl7,
    AsyncKeyimage,
    AsyncLink,
    AsyncLocation,
    AsyncMeeting,
    AsyncMessage,
    AsyncNamespace,
    AsyncNode,
    AsyncNpi,
    AsyncOrder,
    AsyncPatient,
    AsyncPurge,
    AsyncQctask,
    AsyncQuery,
    AsyncRadreport,
    AsyncRadreportmacro,
    AsyncReport,
    AsyncRole,
    AsyncRoute,
    AsyncRsna,
    AsyncScanner,
    AsyncSession,
    AsyncSetting,
    AsyncSite,
    AsyncStudy,
    AsyncTag,
    AsyncTerminology,
    AsyncTraining,
    AsyncUser,
    AsyncValidate,
    AsyncWebhook,
)
from ambra_sdk.storage.storage import AsyncStorage

logger = logging.getLogger(__name__)


class AsyncApi(BaseApi):
    """Ambra Async API.

    Example:
    >>> from ambra_sdk.api import AsyncApi
    >>>
    >>> api = AsyncApi.with_creds(
    ...     url='https://ambrahealth_host/api/v3',
    ...     username='username',
    ...     password='password',
    ...     client_name='Some name (ex: Hospital-ABC)',
    ... )

    Using some special parameters (In most cases you don't need this!):

    >>> from ambra_sdk.api import AsyncApi
    >>> from ambra_sdk.api.base_api import RateLimit, RateLimits
    >>>
    >>> MY_RLS = RateLimits(
    ...        default=RateLimit(3, 2),
    ...        get_limit=RateLimit(4, 2),
    ...        special={'special_url': RateLimit(5, 2)},
    ... )
    >>>
    >>> api = AsyncApi.with_creds(
    ...     url='https://ambrahealth_host/api/v3',
    ...     username='username',
    ...     password='password',
    ...     client_name='Some name (ex: Hospital-ABC)',
    ...     special_headers_for_login={'Special-H': 'ABC'},
    ...     rate_limits=MY_RLS,
    ...     autocast_arguments=False,
    ... )
    """

    backend = 'AIOHTTP'

    def __init__(self, *args, **kwargs):
        """Init api.

        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(*args, **kwargs)
        self._service_session: Optional[aiohttp.ClientSession] = None
        self._storage_session: Optional[aiohttp.ClientSession] = None

        # For rate limits
        self._rate_limits_lock = Lock()
        self._last_request_time = None
        self._last_call_period = None

        # Init services api
        self._init_service_entrypoints()

        # Init storage api namespace
        self.Storage = AsyncStorage(self)

        # Init addon namespace
        self.Addon = Addon(self)

    @property
    def service_session(self) -> aiohttp.ClientSession:
        """Service session.

        :return: service session
        """
        headers = self._default_headers.copy()
        headers.update(self._service_default_headers)
        if self._service_session is None:
            self._service_session = aiohttp.ClientSession(headers=headers)
        return self._service_session

    @property
    def storage_session(self) -> aiohttp.ClientSession:
        """Storage session.

        :return: storage session
        """
        headers = self._default_headers.copy()
        headers.update(self._storage_default_headers)
        if self._storage_session is None:
            self._storage_session = aiohttp.ClientSession(headers=headers)
        return self._storage_session

    async def storage_get(
        self,
        url: str,
        required_sid: bool,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        """Get from storage.

        :param url: url
        :param required_sid: is this method required sid
        :param kwargs: request arguments
        :return: response obj
        """
        kwargs = await self._prepare_storage_request_args(
            required_sid=required_sid,
            **kwargs,
        )
        logger.info(
            'Storage get: %s. Params: %s',
            url,
            str(clear_params(kwargs.get('params', {}))),
        )
        return await self.storage_session.get(url=url, **kwargs)

    async def storage_delete(
        self,
        url: str,
        required_sid: bool,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        """Delete from storage.

        :param url: url
        :param required_sid: is this method required sid
        :param kwargs: request arguments
        :return: response obj
        """
        kwargs = await self._prepare_storage_request_args(
            required_sid=required_sid,
            **kwargs,
        )
        logger.info(
            'Storage delete: %s. Params: %s',
            url,
            str(clear_params(kwargs.get('params', {}))),
        )
        return await self.storage_session.delete(url=url, **kwargs)

    async def storage_post(
        self,
        url: str,
        required_sid: bool,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        """Post to storage.

        :param url: url
        :param required_sid: is this method required sid
        :param kwargs: request arguments
        :return: response obj
        """
        kwargs = await self._prepare_storage_request_args(
            required_sid=required_sid,
            **kwargs,
        )
        logger.info(
            'Storage post: %s. Params: %s',
            url,
            str(clear_params(kwargs.get('params', {}))),
        )

        return await self.storage_session.post(url=url, **kwargs)

    async def service_request(
        self,
        request_args: AioHTTPRequestArgs,
        required_sid: bool,
    ) -> aiohttp.ClientResponse:
        """Post data to url.

        :param request_args: request args
        :param required_sid: is this method required sid
        :return: response
        """
        await self._wait_for_service_request(request_args.url)
        return await self._service_request_without_rate_limits(
            request_args=request_args,
            required_sid=required_sid,
        )

    async def service_post(
        self,
        url: str,
        required_sid: bool,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        """Post data to url.

        :param url: method url
        :param required_sid: is this method required sid
        :param kwargs: request arguments
        :return: response
        """
        full_url = self.service_full_url(url)
        request_args = AioHTTPRequestArgs(
            method='POST',
            url=url,
            full_url=full_url,
            **kwargs,
        )
        return await self.service_request(
            request_args=request_args,
            required_sid=required_sid,
        )

    async def get_sid(self) -> str:
        """Get or create new sid.

        :return: sid
        """
        if self._sid is None:
            return await self.get_new_sid()
        return self._sid

    async def logout(self):
        """Logout."""
        if self._sid:
            await self.Session.logout().get()
            self._sid = None
        if self._storage_session:
            await self._storage_session.close()
        if self._service_session:
            await self._service_session.close()

    async def get_new_sid(self) -> str:
        """Get new sid.

        :raises RuntimeError: Missed credentials
        :return: sid
        """
        if self._creds is None:
            raise RuntimeError('Missed credentials')
        new_sid: str = await self.Session.get_sid(
            self._creds.username,
            self._creds.password,
            special_headers_for_login=self._special_headers_for_login,
        )
        self._sid = new_sid
        return new_sid

    FN_RETURN_TYPE = TypeVar('FN_RETURN_TYPE')

    async def retry_with_new_sid(
        self,
        fn: Callable[..., Awaitable[FN_RETURN_TYPE]],
    ) -> FN_RETURN_TYPE:
        """Retry with new sid.

        :param fn: callable method
        :return: fn result
        """
        try:
            return await fn()
        except (AuthorizationRequired, AccessDenied):
            await self.get_new_sid()
            return await fn()

    async def _wait_for_service_request(self, url):
        if self._rate_limits:
            async with self._rate_limits_lock:
                call_period = self._rate_limits.call_period(url)
                now = monotonic()
                if self._last_request_time is None:
                    # This is a first run
                    self._last_request_time = now
                    self._last_call_period = call_period
                    return

                wait_time = self._last_request_time \
                    + self._last_call_period - now
                if wait_time > 0:
                    logger.info('Sleep %s due to rate limits', wait_time)
                    await sleep(wait_time)
                self._last_request_time = monotonic()
                self._last_call_period = call_period

    async def _service_request_without_rate_limits(
        self,
        request_args: AioHTTPRequestArgs,
        required_sid: bool,
    ) -> aiohttp.ClientResponse:
        """Post data to url.

        :param request_args: request args
        :param required_sid: is this method required sid
        :return: response
        """
        if required_sid is True:
            request_data = request_args.data or {}
            request_data['sid'] = await self.get_sid()
            request_args.data = request_data  # NOQA:WPS110
        if request_args.data:
            request_args.data = {  # NOQA:WPS110
                key: value
                for key, value in request_args.data.items()  # NOQA:WPS110
                if value is not None
            }
        logger.info(
            'Service post: %s. Params: %s',
            request_args.full_url,
            str(clear_params(request_args.data)),
        )
        return await self.service_session.request(
            method=request_args.method,
            url=request_args.full_url,
            **request_args.dict_optional_args(
                self._autocast_arguments,
            ),
        )

    async def _prepare_storage_request_args(
        self,
        required_sid: bool,
        **kwargs,
    ):
        """Prepare storage request kwargs args.

        :param required_sid: required sid
        :param kwargs: kwargs
        :return: kwargs
        """
        if required_sid:
            # Sid passed always in url params (?sid=...)
            request_params = kwargs.pop('params')
            # Get or create new sid
            request_params['sid'] = await self.get_sid()
            kwargs['params'] = request_params
        return kwargs

    def _init_service_entrypoints(self):
        """Init service entrypoint namespaces."""
        self.Account = AsyncAccount(self)
        self.Activity = AsyncActivity(self)
        self.Analytics = AsyncAnalytics(self)
        self.Annotation = AsyncAnnotation(self)
        self.Appointment = AsyncAppointment(self)
        self.Audit = AsyncAudit(self)
        self.Case = AsyncCase(self)
        self.Customcode = AsyncCustomcode(self)
        self.Customfield = AsyncCustomfield(self)
        self.Destination = AsyncDestination(self)
        self.Dicomdata = AsyncDicomdata(self)
        self.Dictionary = AsyncDictionary(self)
        self.Filter = AsyncFilter(self)
        self.Group = AsyncGroup(self)
        self.Help = AsyncHelp(self)
        self.Hl7 = AsyncHl7(self)
        self.Keyimage = AsyncKeyimage(self)
        self.Link = AsyncLink(self)
        self.Location = AsyncLocation(self)
        self.Meeting = AsyncMeeting(self)
        self.Message = AsyncMessage(self)
        self.Namespace = AsyncNamespace(self)
        self.Node = AsyncNode(self)
        self.Npi = AsyncNpi(self)
        self.Order = AsyncOrder(self)
        self.Patient = AsyncPatient(self)
        self.Purge = AsyncPurge(self)
        self.Radreportmacro = AsyncRadreportmacro(self)
        self.Radreport = AsyncRadreport(self)
        self.Report = AsyncReport(self)
        self.Role = AsyncRole(self)
        self.Route = AsyncRoute(self)
        self.Rsna = AsyncRsna(self)
        self.Session = AsyncSession(self)
        self.Setting = AsyncSetting(self)
        self.Study = AsyncStudy(self)
        self.Tag = AsyncTag(self)
        self.Terminology = AsyncTerminology(self)
        self.Training = AsyncTraining(self)
        self.User = AsyncUser(self)
        self.Validate = AsyncValidate(self)
        self.Webhook = AsyncWebhook(self)
        self.Query = AsyncQuery(self)
        self.Scanner = AsyncScanner(self)
        self.Site = AsyncSite(self)
        self.AsyncAnonymization = AsyncAnonymization(self)
        self.AsyncQctask = AsyncQctask(self)

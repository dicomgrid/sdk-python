"""Ambra storage and service API."""

import logging
from threading import Lock
from time import monotonic, sleep
from typing import Callable, Optional, TypeVar

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry

from ambra_sdk.addon.addon import Addon
from ambra_sdk.api.base_api import BaseApi
from ambra_sdk.clear_params import clear_params
from ambra_sdk.exceptions.service import AuthorizationRequired
from ambra_sdk.exceptions.storage import AccessDenied
from ambra_sdk.request_args import RequestArgs
from ambra_sdk.service.entrypoints import (
    Account,
    Activity,
    Analytics,
    Annotation,
    Anonymization,
    Appointment,
    Audit,
    Case,
    Customcode,
    Customfield,
    Destination,
    Dicomdata,
    Dictionary,
    Filter,
    Group,
    Help,
    Hl7,
    Keyimage,
    Link,
    Location,
    Meeting,
    Message,
    Namespace,
    Node,
    Npi,
    Order,
    Patient,
    Purge,
    Qctask,
    Query,
    Radreport,
    Radreportmacro,
    Report,
    Role,
    Route,
    Rsna,
    Scanner,
    Session,
    Setting,
    Site,
    Study,
    Tag,
    Terminology,
    Training,
    User,
    Validate,
    Webhook,
)
from ambra_sdk.storage.storage import Storage

logger = logging.getLogger(__name__)


class Api(BaseApi):
    """Ambra API.

    Example:
    >>> from ambra_sdk.api import Api
    >>>
    >>> api = Api.with_creds(
    ...     url='https://ambrahealth_host/api/v3',
    ...     username='username',
    ...     password='password',
    ...     client_name='Some name (ex: Hospital-ABC)',
    ... )

    Using some special parameters (In most cases you don't need this!):

    >>> from ambra_sdk.api import Api
    >>> from ambra_sdk.api.base_api import RateLimit, RateLimits
    >>>
    >>> MY_RLS = RateLimits(
    ...        default=RateLimit(3, 2),
    ...        get_limit=RateLimit(4, 2),
    ...        special={'special_url': RateLimit(5, 2)},
    ... )
    >>>
    >>> api = Api.with_creds(
    ...     url='https://ambrahealth_host/api/v3',
    ...     username='username',
    ...     password='password',
    ...     client_name='Some name (ex: Hospital-ABC)',
    ...     special_headers_for_login={'Special-H': 'ABC'},
    ...     rate_limits=MY_RLS,
    ...     autocast_arguments=False,
    ... )
    """

    backend = 'REQUESTS'

    def __init__(self, *args, **kwargs):
        """Init api.

        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(*args, **kwargs)

        self._service_session: Optional[requests.Session] = None
        self._storage_session: Optional[requests.Session] = None
        self._init_request_params()

        # For rate limits
        self._rate_limits_lock = Lock()
        self._last_request_time = None
        self._last_call_period = None

        # Init services api
        self._init_service_entrypoints()

        # Init storage api namespace
        self.Storage = Storage(self)

        # Init addon namespace
        self.Addon = Addon(self)

    @property
    def service_session(self) -> requests.Session:
        """Service session.

        :return: service session
        """
        if self._service_session is None:
            self._service_session = requests.Session()
            retries = Retry(**self.service_retry_params)
            adapter = HTTPAdapter(max_retries=retries)
            self._service_session.mount('http://', adapter)
            self._service_session.mount('https://', adapter)
            self._service_session.headers.update(self._default_headers)
            self._service_session.headers.update(self._service_default_headers)
        return self._service_session

    @property
    def storage_session(self) -> requests.Session:
        """Storage session.

        :return: storage session
        """
        if self._storage_session is None:
            self._storage_session = requests.Session()
            retries = Retry(**self.storage_retry_params)
            adapter = HTTPAdapter(max_retries=retries)
            self._storage_session.mount('http://', adapter)
            self._storage_session.mount('https://', adapter)
            self._storage_session.headers.update(self._default_headers)
            self._storage_session.headers.update(self._storage_default_headers)
        return self._storage_session

    def storage_get(
        self,
        url: str,
        required_sid: bool,
        **kwargs,
    ) -> requests.Response:
        """Get from storage.

        :param url: url
        :param required_sid: is this method required sid
        :param kwargs: request arguments
        :return: response obj
        """
        kwargs = self._prepare_storage_request_args(
            required_sid=required_sid,
            **kwargs,
        )
        logger.info(
            'Storage get: %s. Params: %s',
            url,
            str(clear_params(kwargs.get('params', {}))),
        )
        return self.storage_session.get(url=url, **kwargs)

    def storage_delete(
        self,
        url: str,
        required_sid: bool,
        **kwargs,
    ) -> requests.Response:
        """Delete from storage.

        :param url: url
        :param required_sid: is this method required sid
        :param kwargs: request arguments
        :return: response obj
        """
        kwargs = self._prepare_storage_request_args(
            required_sid=required_sid,
            **kwargs,
        )
        logger.info(
            'Storage delete: %s. Params: %s',
            url,
            str(clear_params(kwargs.get('params', {}))),
        )
        return self.storage_session.delete(url=url, **kwargs)

    def storage_post(
        self,
        url: str,
        required_sid: bool,
        **kwargs,
    ) -> requests.Response:
        """Post to storage.

        :param url: url
        :param required_sid: is this method required sid
        :param kwargs: request arguments
        :return: response obj
        """
        kwargs = self._prepare_storage_request_args(
            required_sid=required_sid,
            **kwargs,
        )
        logger.info(
            'Storage post: %s. Params: %s',
            url,
            str(clear_params(kwargs.get('params', {}))),
        )
        return self.storage_session.post(url=url, **kwargs)

    def service_request(
        self,
        request_args: RequestArgs,
        required_sid: bool,
    ) -> requests.Response:
        """Post data to url.

        :param request_args: request args
        :param required_sid: is this method required sid
        :return: response
        """
        self._wait_for_service_request(request_args.url)
        return self._service_request_without_rate_limits(
            request_args=request_args,
            required_sid=required_sid,
        )

    def service_post(
        self,
        url: str,
        required_sid: bool,
        **kwargs,
    ) -> requests.Response:
        """Post data to url.

        :param url: method url
        :param required_sid: is this method required sid
        :param kwargs: request arguments
        :return: response
        """
        full_url = self.service_full_url(url)
        request_args = RequestArgs(
            method='POST',
            url=url,
            full_url=full_url,
            **kwargs,
        )
        return self.service_request(
            request_args=request_args,
            required_sid=required_sid,
        )

    def get_sid(self) -> str:
        """Get or create new sid.

        :return: sid
        """
        if self._sid is None:
            return self.get_new_sid()
        return self._sid

    @property
    def sid(self) -> str:
        """Get or create new sid property.

        :return: sid
        """
        return self.get_sid()

    def logout(self):
        """Logout."""
        if self._sid:
            self.Session.logout().get()
            self._sid = None
        if self._storage_session:
            self._storage_session.close()
        if self._service_session:
            self._service_session.close()

    def get_new_sid(self) -> str:
        """Get new sid.

        :raises RuntimeError: Missed credentials
        :return: sid
        """
        if self._creds is None:
            raise RuntimeError('Missed credentials')
        new_sid: str = self.Session.get_sid(
            self._creds.username,
            self._creds.password,
            special_headers_for_login=self._special_headers_for_login,
        )
        self._sid = new_sid
        return new_sid

    FN_RETURN_TYPE = TypeVar('FN_RETURN_TYPE')

    def retry_with_new_sid(
        self,
        fn: Callable[..., FN_RETURN_TYPE],
    ) -> FN_RETURN_TYPE:
        """Retry with new sid.

        :param fn: callable method
        :return: fn result
        """
        try:
            return fn()
        except (AuthorizationRequired, AccessDenied):
            self.get_new_sid()
            return fn()

    def _wait_for_service_request(self, url):
        if self._rate_limits:
            with self._rate_limits_lock:
                call_period = self._rate_limits.call_period(url)
                now = monotonic()
                if self._last_request_time is None:
                    # This is a first run
                    self._last_request_time = now
                    self._last_call_period = call_period
                    return

                wait_time = self._last_request_time + \
                    self._last_call_period - now
                if wait_time > 0:
                    logger.info('Sleep %s due to rate limits', wait_time)
                    sleep(wait_time)
                self._last_request_time = monotonic()
                self._last_call_period = call_period

    def _service_request_without_rate_limits(
        self,
        request_args: RequestArgs,
        required_sid: bool,
    ) -> requests.Response:
        """Post data to url.

        :param request_args: request args
        :param required_sid: is this method required sid
        :return: response
        """
        if required_sid is True:
            request_data = request_args.data or {}
            request_data['sid'] = self.sid
            request_args.data = request_data  # NOQA:WPS110
        logger.info(
            'Service post: %s. Params: %s',
            request_args.url,
            str(clear_params(request_args.data)),
        )
        return self.service_session.request(
            method=request_args.method,
            url=request_args.full_url,
            **request_args.dict_optional_args(
                self._autocast_arguments,
            ),
        )

    def _prepare_storage_request_args(
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
            request_params['sid'] = self.get_sid()
            kwargs['params'] = request_params
        return kwargs

    def _init_request_params(self):
        method_whitelist = [
            'HEAD',
            'TRACE',
            'GET',
            'PUT',
            'OPTIONS',
            'DELETE',
            'POST',
        ]
        # https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
        self.service_retry_params = {
            'total': 10,
            'connect': 5,
            'read': 5,
            'status': 5,
            'status_forcelist': [503, 504],
            'backoff_factor': 0.1,
            'method_whitelist': method_whitelist,
        }
        # Merge studies
        # /study/{namespace}/{studyUid}/merge?sid={sid}&secondary_study_uid={secondary_study_uid}&delete_secondary_study={0,1}
        # Can return 500 and its ok .....
        self.storage_retry_params = {
            'total': 10,
            'connect': 5,
            'read': 5,
            'status': 5,
            'status_forcelist': [502, 503, 504],
            'backoff_factor': 0.1,
            'method_whitelist': method_whitelist,
        }

    def _init_service_entrypoints(self):
        """Init service entrypoint namespaces."""
        self.Account = Account(self)
        self.Activity = Activity(self)
        self.Analytics = Analytics(self)
        self.Annotation = Annotation(self)
        self.Appointment = Appointment(self)
        self.Audit = Audit(self)
        self.Case = Case(self)
        self.Customcode = Customcode(self)
        self.Customfield = Customfield(self)
        self.Destination = Destination(self)
        self.Dicomdata = Dicomdata(self)
        self.Dictionary = Dictionary(self)
        self.Filter = Filter(self)
        self.Group = Group(self)
        self.Help = Help(self)
        self.Hl7 = Hl7(self)
        self.Keyimage = Keyimage(self)
        self.Link = Link(self)
        self.Location = Location(self)
        self.Meeting = Meeting(self)
        self.Message = Message(self)
        self.Namespace = Namespace(self)
        self.Node = Node(self)
        self.Npi = Npi(self)
        self.Order = Order(self)
        self.Patient = Patient(self)
        self.Purge = Purge(self)
        self.Radreportmacro = Radreportmacro(self)
        self.Radreport = Radreport(self)
        self.Report = Report(self)
        self.Role = Role(self)
        self.Route = Route(self)
        self.Rsna = Rsna(self)
        self.Session = Session(self)
        self.Setting = Setting(self)
        self.Study = Study(self)
        self.Tag = Tag(self)
        self.Terminology = Terminology(self)
        self.Training = Training(self)
        self.User = User(self)
        self.Validate = Validate(self)
        self.Webhook = Webhook(self)
        self.Query = Query(self)
        self.Scanner = Scanner(self)
        self.Site = Site(self)
        self.Anonymization = Anonymization(self)
        self.Qctask = Qctask(self)

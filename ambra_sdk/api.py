"""Ambra storage and service API."""

import logging
from typing import Callable, NamedTuple, Optional

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry

from ambra_sdk import __version__
from ambra_sdk.addon.addon import Addon
from ambra_sdk.exceptions.service import AuthorizationRequired
from ambra_sdk.exceptions.storage import PermissionDenied
from ambra_sdk.service.entrypoints import (
    Account,
    Activity,
    Analytics,
    Annotation,
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
    Radreport,
    Radreportmacro,
    Report,
    Role,
    Route,
    Rsna,
    Session,
    Setting,
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
DEFAULT_SDK_CLIENT_NAME = 'Ambra SDK default client'


class Credentials(NamedTuple):
    """Credentials."""

    username: str
    password: str


class Api:  # NOQA:WPS214,WPS230
    """Ambra API."""

    def __init__(  # NOQA:WPS211
        self,
        url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        sid: Optional[str] = None,
        client_name: str = DEFAULT_SDK_CLIENT_NAME,
    ):
        """Init api.

        :param url: api url
        :param sid: session id
        :param username: username credential
        :param password: password credential
        :param client_name: user defined client name
        """
        self._api_url: str = url
        self._creds: Optional[Credentials] = None
        self._sid: Optional[str] = sid
        self._client_name = client_name
        self._default_headers = {
            'SDK_CLIENT_NAME': client_name,
            'SDK_VERSION': __version__,
        }
        if username is not None and password is not None:
            self._creds = Credentials(username=username, password=password)
        self._service_session: Optional[requests.Session] = None
        self._storage_session: Optional[requests.Session] = None
        self._init_request_params()
        self._init_service_entrypoints()

        # Init storage api namespace
        self.Storage = Storage(self)

        # Init addon namespace
        self.Addon = Addon(self)

        # prepare ws
        self.ws_url = '{url}/channel/websocket'.format(url=url)

    @classmethod
    def with_sid(
        cls,
        url: str,
        sid: str,
        client_name: str = DEFAULT_SDK_CLIENT_NAME,
    ) -> 'Api':
        """Create Api with sid.

        :param url: api url
        :param sid: session id
        :param client_name: user defined client name

        :return: Api
        """
        return cls(
            url=url,
            sid=sid,
            client_name=client_name,
        )

    @classmethod
    def with_creds(
        cls,
        url: str,
        username: str,
        password: str,
        client_name: str = DEFAULT_SDK_CLIENT_NAME,
    ) -> 'Api':
        """Create Api with (username, password) credentials.

        :param url: api url
        :param username: username credential
        :param password: password credential
        :param client_name: user defined client name

        :return: Api
        """
        return cls(
            url=url,
            username=username,
            password=password,
            client_name=client_name,
        )

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
        if required_sid:
            # Sid passed always in url params (?sid=...)
            request_params = kwargs.pop('params')
            # Get or create new sid
            request_params['sid'] = self.sid
            kwargs['params'] = request_params
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
        if required_sid:
            # Sid passed always in url params (?sid=...)
            request_params = kwargs.pop('params')
            # Delete or create new sid
            request_params['sid'] = self.sid
            kwargs['params'] = request_params
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
        if required_sid:
            # Sid passed always in url params (?sid=...)
            request_params = kwargs.pop('params')
            # Post or create new sid
            request_params['sid'] = self.sid
            kwargs['params'] = request_params
        return self.storage_session.post(url=url, **kwargs)

    def service_full_url(self, url: str) -> str:
        """Full service method url.

        :param url: method url
        :return: full url
        """
        return '{base_url}{entrypoint_url}'.format(
            base_url=self._api_url,
            entrypoint_url=url,
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
        if required_sid is True:
            request_data = kwargs.pop('data')
            request_data['sid'] = self.sid
            kwargs['data'] = request_data
        return self.service_session.post(url=full_url, **kwargs)

    @property
    def sid(self) -> str:
        """Get or create new sid property.

        :return: sid
        """
        if self._sid is None:
            return self.get_new_sid()
        return self._sid

    def logout(self):
        """Logout."""
        self.Session.logout()
        self._sid = None

    def get_new_sid(self) -> str:
        """Get new sid.

        :raises RuntimeError: Missined credentials
        :return: sid
        """
        if self._creds is None:
            raise RuntimeError('Missed credentials')
        new_sid: str = self.Session.get_sid(
            self._creds.username,
            self._creds.password,
        )
        self._sid = new_sid
        return new_sid

    def retry_with_new_sid(
        self,
        fn: Callable,
    ):
        """Retry with new sid.

        :param fn: callable method
        :return: fn result
        """
        try:
            return fn()
        except (AuthorizationRequired, PermissionDenied):
            self.get_new_sid()
            return fn()

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

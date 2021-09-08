"""Base API."""

from typing import Dict, NamedTuple, Optional

from ambra_sdk import __version__

DEFAULT_SDK_CLIENT_NAME = 'Ambra SDK default client'


class Credentials(NamedTuple):
    """Credentials."""

    username: str
    password: str


class RateLimit(NamedTuple):
    """Rate limit."""

    calls: int
    seconds: float


class RateLimits(NamedTuple):
    """Rate limits.

    default: rate limit for default requests
    get: rate limit special for get requests
    special: rate limit for special methods
    """

    default: RateLimit
    get_limit: Optional[RateLimit]
    special: Optional[Dict[str, RateLimit]]

    def call_period(self, url: str) -> float:
        """Call period for url.

        :param url: url
        :return: call period
        """
        if self.special and url in self.special:
            rate_limit = self.special[url]
        elif self.get_limit and url.endswith('get'):
            rate_limit = self.get_limit
        else:
            rate_limit = self.default
        return float(rate_limit.seconds) / rate_limit.calls


DEFAULT_RATE_LIMITS = RateLimits(
    default=RateLimit(2, 1),
    get_limit=RateLimit(5, 1),
    special=None,
)


class BaseApi:  # NOQA:WPS214,WPS230
    """Ambra API."""

    def __init__(  # NOQA:WPS211
        self,
        url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        sid: Optional[str] = None,
        client_name: str = DEFAULT_SDK_CLIENT_NAME,
        special_headers_for_login: Optional[Dict[str, str]] = None,
        rate_limits: Optional[RateLimits] = DEFAULT_RATE_LIMITS,
        autocast_arguments: bool = True,
    ):
        """Init api.

        :param url: api url
        :param sid: session id
        :param username: username credential
        :param password: password credential
        :param client_name: user defined client name
            This is some string. Using this in ambra sdk server
            we can find your requests and can help you to
            solve some problems.
        :param special_headers_for_login: some special
            headers for logging requests.
        :param rate_limits: how many requests you can
            execute per second using this Api
        :param autocast_arguments: If is True,
            SDK tring to cast your parameters to valid
            request arguments. For example:

            some_datetime -> '%Y-%m-%d %H:%M:%S'
            ['a', 'b'] -> '["a", "b"]'

            without this argument you need to do something like this:
            >> api.Study.get(
            ..     ...,
            ..     fields=json.dumps(["field1", "field2"]),
            .. ).get()
        """
        self._api_url: str = url
        self._creds: Optional[Credentials] = None
        self._sid: Optional[str] = sid
        self._client_name = client_name
        self._special_headers_for_login = special_headers_for_login
        self._default_headers = {
            'SDK-CLIENT-NAME': client_name,
            'SDK-VERSION': __version__,
        }
        self._storage_default_headers: Dict[str, str] = {}
        self._service_default_headers: Dict[str, str] = {}
        if username is not None and password is not None:
            self._creds = Credentials(username=username, password=password)
        self._rate_limits = rate_limits
        self.ws_url = '{url}/channel/websocket'.format(url=self._api_url)
        self._autocast_arguments = autocast_arguments

    @property
    def default_headers(self):
        """Default headers."""  # NOQA:D401
        return self._default_headers  # NOQA:DAR201

    @property
    def service_default_headers(self):
        """Service default headers."""
        return self._service_default_headers  # NOQA:DAR201

    @property
    def storage_default_headers(self):
        """Storage default headers."""
        return self._storage_default_headers  # NOQA:DAR201

    @classmethod
    def with_sid(
        cls,
        url: str,
        sid: str,
        client_name: str = DEFAULT_SDK_CLIENT_NAME,
        rate_limits: RateLimits = DEFAULT_RATE_LIMITS,
        autocast_arguments: bool = True,
    ) -> 'BaseApi':
        """Create Api with sid.

        :param url: api url
        :param sid: session id
        :param client_name: user defined client name
            This is some string. Using this in ambra sdk server
            we can find your requests and can help you to
            solve some problems.
        :param rate_limits: how many requests you can
            execute per second using this Api
        :param autocast_arguments: If is True,
            SDK tring to cast your parameters to valid
            request arguments. For example:

            some_datetime -> '%Y-%m-%d %H:%M:%S'
            ['a', 'b'] -> '["a", "b"]'

            without this argument you need to do something like this:
            >> api.Study.get(
            ..     ...,
            ..     fields=json.dumps(["field1", "field2"]),
            .. ).get()

        :return: Api
        """
        return cls(
            url=url,
            sid=sid,
            client_name=client_name,
            rate_limits=rate_limits,
            autocast_arguments=autocast_arguments,
        )

    @classmethod
    def with_creds(
        cls,
        url: str,
        username: str,
        password: str,
        client_name: str = DEFAULT_SDK_CLIENT_NAME,
        special_headers_for_login: Optional[Dict[str, str]] = None,
        rate_limits: RateLimits = DEFAULT_RATE_LIMITS,
        autocast_arguments: bool = True,
    ) -> 'BaseApi':
        """Create Api with (username, password) credentials.

        :param url: api url
        :param username: username credential
        :param password: password credential
        :param client_name: user defined client name
            This is some string. Using this in ambra sdk server
            we can find your requests and can help you to
            solve some problems.
        :param special_headers_for_login: some special
            headers for logging requests.
        :param rate_limits: how many requests you can
            execute per second using this Api
        :param autocast_arguments: If is True,
            SDK tring to cast your parameters to valid
            request arguments. For example:

            some_datetime -> '%Y-%m-%d %H:%M:%S'
            ['a', 'b'] -> '["a", "b"]'

            without this argument you need to do something like this:
            >> api.Study.get(
            ..     ...,
            ..     fields=json.dumps(["field1", "field2"]),
            .. ).get()

        :return: Api
        """
        return cls(
            url=url,
            username=username,
            password=password,
            client_name=client_name,
            special_headers_for_login=special_headers_for_login,
            rate_limits=rate_limits,
            autocast_arguments=autocast_arguments,
        )

    def service_full_url(self, url: str) -> str:
        """Full service method url.

        :param url: method url
        :return: full url
        """
        return '{base_url}{entrypoint_url}'.format(
            base_url=self._api_url,
            entrypoint_url=url,
        )

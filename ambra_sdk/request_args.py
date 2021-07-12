"""Request args."""

from typing import Any, Iterable, Mapping, Optional

import aiohttp
from aiohttp.helpers import sentinel


class RequestArgs:  # NOQA:WPS230
    """Request args.

    Like in requests.request args
    """

    def __init__(  # NOQA:D107,WPS211
        self,
        method: str,
        url: str,
        full_url: str,
        params: Optional[Any] = None,  # NOQA:WPS110
        data: Optional[Any] = None,  # NOQA:WPS110
        json: Optional[Any] = None,
        headers: Optional[Any] = None,
        cookies: Optional[Any] = None,
        files: Optional[Any] = None,
        auth: Optional[Any] = None,
        timeout: Optional[Any] = None,
        allow_redirects: Optional[Any] = None,
        proxies: Optional[Any] = None,
        verify: Optional[Any] = None,
        stream: Optional[Any] = None,
        cert: Optional[Any] = None,
    ):  # NOQA: DAR101
        """Init."""
        self.method = method
        self.url = url
        self.full_url = full_url
        self.params = params  # NOQA:WPS110
        self.data = data  # NOQA:WPS110
        self.json = json
        self.headers = headers
        self.cookies = cookies
        self.files = files
        self.auth = auth
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.proxies = proxies
        self.verify = verify
        self.stream = stream
        self.cert = cert

    def to_dict(self):
        """To dict.

        :return: dict repr
        """
        return self.__dict__.copy()

    def dict_optional_args(self):
        """Get dict optional args.

        :return: dict of request optional parameters
        """
        dict_args = self.to_dict()
        dict_args.pop('method')
        dict_args.pop('url')
        dict_args.pop('full_url')
        return dict_args


class AioHTTPRequestArgs:  # NOQA:WPS230
    """AioHTTP Request args."""

    def __init__(  # NOQA:D107,WPS211
        self,
        method: str,
        url: str,
        full_url: str,
        params: Optional[Mapping[str, str]] = None,  # NOQA:WPS110
        data: Any = None,  # NOQA:WPS110
        json: Any = None,
        cookies=None,
        headers=None,
        skip_auto_headers: Optional[Iterable[str]] = None,
        auth: Optional[aiohttp.BasicAuth] = None,
        allow_redirects: bool = True,
        max_redirects: int = 10,
        compress: Optional[str] = None,
        chunked: Optional[bool] = None,
        expect100: bool = False,
        raise_for_status=None,
        read_until_eof: bool = True,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        timeout=sentinel,
        ssl=None,
        proxy_headers=None,
        trace_request_ctx=None,
    ):

        self.method = method
        self.url = url
        self.full_url = full_url
        self.params = params  # NOQA:WPS110
        self.data = data  # NOQA:WPS110
        self.json = json
        self.cookies = cookies
        self.headers = headers
        self.skip_auto_headers = skip_auto_headers
        self.auth = auth
        self.allow_redirects = allow_redirects
        self.max_redirects = max_redirects
        self.compress = compress
        self.chunked = chunked
        self.expect100 = expect100
        self.raise_for_status = raise_for_status
        self.read_until_eof = read_until_eof
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self.timeout = timeout
        self.ssl = ssl
        self.proxy_headers = proxy_headers
        self.trace_request_ctx = trace_request_ctx

    def to_dict(self):
        """To dict.

        :return: dict repr
        """
        return self.__dict__.copy()

    def dict_optional_args(self):
        """Get dict optional args.

        :return: dict of request optional parameters
        """
        dict_args = self.to_dict()
        dict_args.pop('method')
        dict_args.pop('url')
        dict_args.pop('full_url')
        return dict_args

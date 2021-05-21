"""Request args."""

from typing import Any, Optional


class RequestArgs:  # NOQA:WPS230
    """Request args.

    Like in requests.request args
    """

    def __init__(  # NOQA:D107,WPS211
        self,
        method: str,
        url: str,
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
        return dict_args

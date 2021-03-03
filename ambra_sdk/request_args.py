"""Request args."""

from dataclasses import asdict, dataclass
from typing import Any, Optional


@dataclass
class RequestArgs:
    """Request args.

    Like in requests.request args
    """

    method: str
    url: str
    params: Optional[Any] = None  # NOQA:WPS110
    data: Optional[Any] = None  # NOQA:WPS110
    json: Optional[Any] = None
    headers: Optional[Any] = None
    cookies: Optional[Any] = None
    files: Optional[Any] = None
    auth: Optional[Any] = None
    timeout: Optional[Any] = None
    allow_redirects: Optional[Any] = None
    proxies: Optional[Any] = None
    verify: Optional[Any] = None
    stream: Optional[Any] = None
    cert: Optional[Any] = None

    def to_dict(self):
        """To dict.

        :return: dict repr
        """
        return asdict(self)

    def dict_optional_args(self):
        """Get dict optional args.

        :return: dict of request optional parameters
        """
        dict_args = self.to_dict()
        dict_args.pop('method')
        dict_args.pop('url')
        return dict_args

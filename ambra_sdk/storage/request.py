from enum import Enum
from io import BufferedReader
from typing import TYPE_CHECKING, Any, Dict, Mapping, NamedTuple, Optional

from requests import Response

from ambra_sdk.exceptions.storage import AmbraResponseException
from ambra_sdk.storage.response import check_response

if TYPE_CHECKING:
    from ambra_sdk.storage.storage import Storage  # NOQA:WPS433


class StorageMethod(Enum):
    """Storage methods."""

    get = 'GET'
    post = 'POST'
    delete = 'DELETE'


class PreparedRequest(NamedTuple):
    """Prepared request."""

    # This some sort of private field.
    # User should not have dicect access to this field
    # But we can not use _name in NamedTuple attributes
    storage_: 'Storage'  # NOQA WPS1120
    url: str
    method: StorageMethod
    # Mapping type is covariant is covariant type
    errors_mapping: Optional[Mapping[int, AmbraResponseException]] = None
    params: Optional[Dict[str, Any]] = None  # NOQA:WPS110
    files: Optional[Dict[str, BufferedReader]] = None
    headers: Optional[Dict[str, str]] = None
    data: Optional[Any] = None  # NOQA:WPS110
    stream: Optional[bool] = None

    def execute(self) -> Response:
        """Execute prepared request.

        If sid problems we try to get new sid
        and retry request.

        :return: response object
        """
        response: Response = self.storage_.retry_with_new_sid(
            self.execute_once,
        )
        return response  # NOQA:WPS331

    def execute_once(self) -> Response:
        """Execute prepared request.

        :return: response object
        :raises RuntimeError: Unknown request method
        """
        request_kwargs: Dict[str, Any] = {}
        if self.params is not None:
            request_kwargs['params'] = self.params

        if self.data is not None:
            request_kwargs['data'] = self.data

        if self.headers is not None:
            request_kwargs['headers'] = self.headers

        if self.files is not None:
            request_kwargs['files'] = self.files

        if self.stream is not None:
            request_kwargs['stream'] = self.stream

        if self.method == StorageMethod.get:
            response = self.storage_.get(self.url, **request_kwargs)

        elif self.method == StorageMethod.post:
            response = self.storage_.post(self.url, **request_kwargs)

        elif self.method == StorageMethod.delete:
            response = self.storage_.delete(self.url, **request_kwargs)

        else:
            raise RuntimeError(
                'Unknown storage request method: {method}'.format(
                    method=self.method,
                ),
            )

        return check_response(
            response,
            self.url,
            errors_mapping=self.errors_mapping,
        )

from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from aiohttp import ClientResponse, FormData
from requests import Response

from ambra_sdk.storage.response import async_check_errors, check_errors
from ambra_sdk.types import RequestsFileType

if TYPE_CHECKING:
    from ambra_sdk.storage.storage.storage import Storage  # NOQA:WPS433
    from ambra_sdk.storage.storage.async_storage \
        import AsyncStorage  # NOQA:WPS433


class StorageMethod(Enum):
    """Storage methods."""

    get = 'GET'
    post = 'POST'
    delete = 'DELETE'


REQUEST_FILES_TYPE = Optional[Union[Dict[str, RequestsFileType], FormData]]


class PreparedRequest:  # NOQA:WPS230
    """Prepared request."""

    __slots__ = (
        'storage',
        'url',
        'method',
        'params',
        'files',
        'headers',
        'data',
        'stream',
    )

    def __init__(  # NOQA:WPS211,D107
        self,
        storage: Union['Storage', 'AsyncStorage'],
        url: str,
        method: StorageMethod,
        params: Optional[Dict[str, Any]] = None,  # NOQA:WPS110
        files: REQUEST_FILES_TYPE = None,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,  # NOQA:WPS110
        stream: Optional[bool] = None,
    ):
        self.storage = storage
        self.url = url
        self.method = method
        self.params = params  # NOQA:WPS110
        self.files = files
        self.headers = headers
        self.data = data  # NOQA:WPS110
        self.stream = stream

    def execute(self) -> Response:
        """Execute prepared request.

        If sid problems we try to get new sid
        and retry request.

        :return: response object
        """
        if TYPE_CHECKING:
            assert isinstance(self.storage, Storage)  # NOQA:S101

        response: Response = self.storage.retry_with_new_sid(
            self.execute_once,
        )
        return response  # NOQA:WPS331

    def execute_once(self) -> Response:
        """Execute prepared request.

        :return: response object
        :raises RuntimeError: Unknown request method
        """
        if TYPE_CHECKING:
            assert isinstance(self.storage, Storage)  # NOQA:S101

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
            response = self.storage.get(self.url, **request_kwargs)

        elif self.method == StorageMethod.post:
            response = self.storage.post(self.url, **request_kwargs)

        elif self.method == StorageMethod.delete:
            response = self.storage.delete(self.url, **request_kwargs)

        else:
            raise RuntimeError(
                'Unknown storage request method: {method}'.format(
                    method=self.method,
                ),
            )

        return check_errors(response)

    async def async_execute(self) -> ClientResponse:
        """Execute prepared request.

        If sid problems we try to get new sid
        and retry request.

        :return: response object
        """
        response: ClientResponse = await self \
            .storage.retry_with_new_sid(self.async_execute_once)
        return response  # NOQA:WPS331

    async def async_execute_once(self) -> ClientResponse:
        """Execute prepared request.

        :return: response object
        :raises RuntimeError: Unknown request method
        """
        request_kwargs: Dict[str, Any] = {}
        if self.params is not None:
            request_kwargs['params'] = self.params

        if self.data is not None and self.files is not None:
            raise RuntimeError('Use data or files in prepared request')
        if self.data is not None:
            request_kwargs['data'] = self.data

        if self.files is not None:
            request_kwargs['data'] = self.files

        if self.headers is not None:
            request_kwargs['headers'] = self.headers

        response: ClientResponse

        if TYPE_CHECKING:
            assert isinstance(self.storage, AsyncStorage)  # NOQA:S101

        if self.method == StorageMethod.get:
            response = await self.storage.get(self.url, **request_kwargs)

        elif self.method == StorageMethod.post:
            response = await self.storage.post(self.url, **request_kwargs)

        elif self.method == StorageMethod.delete:
            response = await self.storage.delete(self.url, **request_kwargs)

        else:
            raise RuntimeError(
                'Unknown storage request method: {method}'.format(
                    method=self.method,
                ),
            )

        return await async_check_errors(response)

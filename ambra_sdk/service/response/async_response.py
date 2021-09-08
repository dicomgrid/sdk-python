"""Async response objects."""

from typing import Optional, Union

import aiohttp

from ambra_sdk.exceptions.service import AmbraResponseException
from ambra_sdk.request_args import AioHTTPRequestArgs
from ambra_sdk.service.response.base_response import (
    ERROR_MAPPING,
    JSON_RETURN_TYPE,
    BaseIterableResponse,
    check_401_405,
    check_412,
)

ASYNC_RETURN_TYPE = Union[JSON_RETURN_TYPE, aiohttp.ClientResponse]


class AsyncIterableResponse(BaseIterableResponse):
    """Async iterable response."""

    def __init__(  # NOQA: WPS211
        self,
        *,
        request_args: AioHTTPRequestArgs,
        **kwargs,
    ):
        """Respone initialization.

        :param request_args: request args
        :param kwargs: kwargs
        """
        super().__init__(**kwargs)
        self._request_args = request_args

    def __aiter__(self):
        """Return iterator by rows.

        :return: async data generator
        """
        return self._data_generator()

    async def first(self) -> Optional[JSON_RETURN_TYPE]:
        """First element.

        :return: Return first element of seq.
        """
        try:

            response_obj: JSON_RETURN_TYPE = \
                await self.__aiter__().__anext__()  # NOQA:WPS609
        except StopAsyncIteration:
            return None
        return response_obj  # NOQA:WPS331

    async def _data_generator(self):  # NOQA: WPS231
        """Return iterator by rows.

        :yields: response object

        :raises RuntimeError: Max rows in page diffs from request
        """
        # Reset row pointer
        self._current_row = 0
        while True:
            self._request_args.data = self._prepare_data(  # NOQA:WPS110
                self._request_args.data,
            )
            response = await self._api.retry_with_new_sid(self._get_response)
            json = await response.json()
            more = json['page']['more']
            # maximum rows in page
            max_rows_in_page = json['page']['rows']
            if max_rows_in_page != self._rows_in_page:
                raise RuntimeError(
                    'The max_rows_in_page parameter was ignored by the server',
                )
            # TODO: What about study/list:: template field?!!
            for row in json[self._pagination_field]:
                if self._current_row < self._min_row:
                    self._current_row += 1
                    continue
                if self._max_row is not None and \
                   self._current_row >= self._max_row:
                    return
                self._current_row += 1
                yield self._return_constructor(row)
            if more == 0:
                break

    async def _get_response(self):
        response = await self._api.service_request(
            required_sid=self._required_sid,
            request_args=self._request_args,
        )
        return await async_check_response(response, self._errors_mapping)


async def async_check_response(  # NOQA:WPS231
    response: aiohttp.ClientResponse,
    errors_mapping: ERROR_MAPPING,
):
    """Check response on errors.

    :param response: response obj
    :param errors_mapping: map of error name and exception

    :return: response object

    :raises AmbraResponseException: Unknown exception
    :raises RuntimeError: Bad content type for 412
    """
    status_code = response.status
    if status_code == 200:
        return response
    check_401_405(status_code)
    if status_code == 412:
        content_type = response.headers.get('content-type')
        if content_type is None or 'application/json' not in content_type:
            raise RuntimeError(
                'Bad content type for 412: {content_type}'.format(
                    content_type=content_type,
                ),
            )
        json = await response.json()
        check_412(json, errors_mapping)

    response_text = await response.text()
    raise AmbraResponseException(
        code=status_code,
        description='Unknown error',
        response_text=response_text,
    )

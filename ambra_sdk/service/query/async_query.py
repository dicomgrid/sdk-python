"""Async query objects."""

from typing import TYPE_CHECKING, Optional

from ambra_sdk.request_args import AioHTTPRequestArgs
from ambra_sdk.service.filtering import WithFilter
from ambra_sdk.service.only import WithOnly
from ambra_sdk.service.query.base_query import BaseQuery, BaseQueryP
from ambra_sdk.service.response import (
    JSON_RETURN_TYPE,
    RETURN_TYPE,
    AsyncIterableResponse,
    async_check_response,
)
from ambra_sdk.service.sorting import WithSorting

if TYPE_CHECKING:
    from ambra_sdk.api.async_api import AsyncApi  # NOQA:WPS433


class AsyncQuery(BaseQuery):
    """Simple Query."""

    def __init__(self, api: 'AsyncApi', *args, **kwargs):
        """Init.

        :param api: api
        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(api, *args, **kwargs)
        self.request_args = AioHTTPRequestArgs(
            method='POST',
            url=self.url,
            full_url=self._api.service_full_url(self.url),
            data=self.request_data,
        )

    async def get(self) -> RETURN_TYPE:
        """Get response object.

        If sid problems we try to get new sid
        and retry request.

        :return: json box or response
        """
        return await self._api.retry_with_new_sid(self.get_once)

    async def get_once(self) -> RETURN_TYPE:
        """Get response object.

        :return: json box or response
        """
        response = await self._api.service_request(
            request_args=self.request_args,
            required_sid=self._required_sid,
        )
        response = await async_check_response(response, self._errors_mapping)
        content_type = response.headers.get('content-type')
        if content_type and 'application/json' in content_type:
            response_json = await response.json()
            if 'status' in response_json:
                response_json.pop('status')
            return self.return_constructor(response_json)
        return response


class AsyncQueryP(BaseQueryP):
    """Query with pagination."""

    def __init__(self, api: 'AsyncApi', *args, **kwargs):
        """Init.

        :param api: api
        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(api, *args, **kwargs)
        self.request_args = AioHTTPRequestArgs(
            method='POST',
            url=self.url,
            full_url=self._api.service_full_url(self.url),
            data=self.request_data,
        )

    def all(self) -> AsyncIterableResponse:  # NOQA: A003,WPS125
        """Get iterable response.

        :returns: iterable response object
        """
        return AsyncIterableResponse(
            api=self._api,
            url=self.url,
            required_sid=self._required_sid,
            request_args=self.request_args,
            errors_mapping=self._errors_mapping,
            pagination_field=self._paginated_field,
            rows_in_page=self._rows_in_page,
            return_constructor=self.return_constructor,
        )

    async def first(self) -> Optional[JSON_RETURN_TYPE]:
        """Get First element of sequence.

        :returns: Response object
        """
        return await self.all().first()

    async def get(self) -> RETURN_TYPE:
        """Get response object.

        WARNING: This method should be used only for get
          some extra fields from the first page of results.
          Use .first() or .all() methods!

        If sid problems we try to get new sid
        and retry request.

        :return: json box or response
        """
        return await self._api.retry_with_new_sid(self.get_once)

    async def get_once(self) -> RETURN_TYPE:
        """Get response object.

        WARNING: This method should be used only for get
          some extra fields from the first page of results.
          Use .first() or .all() methods!

        :return: json box or response
        """
        response = await self._api.service_request(
            request_args=self.request_args,
            required_sid=self._required_sid,
        )
        response = await async_check_response(response, self._errors_mapping)
        content_type = response.headers.get('content-type')
        if content_type and 'application/json' in content_type:
            response_json = await response.json()
            if 'status' in response_json:
                response_json.pop('status')
            return self.return_constructor(response_json)
        return response


# mypy bug https://github.com/python/mypy/issues/9031
class AsyncQueryO(AsyncQuery, WithOnly[AioHTTPRequestArgs]):  # type: ignore
    """AsyncQuery with only fields."""


class AsyncQueryOF(  # type: ignore
    AsyncQueryO,
    WithFilter[AioHTTPRequestArgs],
):
    """AsyncQuery with filtering."""


class AsyncQueryOS(  # type: ignore
    AsyncQueryO,
    WithSorting[AioHTTPRequestArgs],
):
    """AsyncQuery with sorting."""


class AsyncQueryOSF(  # type: ignore
    AsyncQueryOF,
    WithSorting[AioHTTPRequestArgs],
):
    """AsyncQuery with filtering ans sorting."""


class AsyncQueryOP(AsyncQueryP, WithOnly[AioHTTPRequestArgs]):  # type: ignore
    """AsyncQuery with pagination and only fields."""


class AsyncQueryOPF(  # type: ignore
    AsyncQueryOP,
    WithFilter[AioHTTPRequestArgs],
):
    """AsyncQuery with pagination and filtering."""


class AsyncQueryOPS(  # type: ignore
    AsyncQueryOP,
    WithSorting[AioHTTPRequestArgs],
):
    """AsyncQuery with pagination and sorting."""


class AsyncQueryOPSF(  # type: ignore
    AsyncQueryOPS,
    WithFilter[AioHTTPRequestArgs],
):
    """AsyncQuery with pagination sorting and filtering."""

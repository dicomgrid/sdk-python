"""Query objects."""

from typing import TYPE_CHECKING, Optional

from ambra_sdk.request_args import RequestArgs
from ambra_sdk.service.filtering import WithFilter
from ambra_sdk.service.only import WithOnly
from ambra_sdk.service.query.base_query import BaseQuery, BaseQueryP
from ambra_sdk.service.response import (
    JSON_RETURN_TYPE,
    RETURN_TYPE,
    IterableResponse,
    check_response,
)
from ambra_sdk.service.sorting import WithSorting

if TYPE_CHECKING:
    from ambra_sdk.api.api import Api  # NOQA:WPS433


class Query(BaseQuery):
    """Simple Query."""

    def __init__(self, api: 'Api', *args, **kwargs):
        """Init.

        :param api: api
        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(api, *args, **kwargs)
        self.request_args = RequestArgs(
            method='POST',
            url=self.url,
            full_url=self._api.service_full_url(self.url),
            data=self.request_data,
        )

    def get(self) -> RETURN_TYPE:
        """Get response object.

        If sid problems we try to get new sid
        and retry request.

        :return: json box or response
        """
        get_result = self._api.retry_with_new_sid(self.get_once)
        return get_result  # NOQA:331

    def get_once(self) -> RETURN_TYPE:
        """Get response object.

        :return: json box or response
        """
        response = self._api.service_request(
            request_args=self.request_args,
            required_sid=self._required_sid,
        )
        response = check_response(response, self._errors_mapping)
        content_type = response.headers.get('content-type')
        if content_type and 'application/json' in content_type:
            response_json = response.json()
            if 'status' in response_json:
                response_json.pop('status')
            return self.return_constructor(response_json)
        return response


class QueryP(BaseQueryP):
    """Base query with pagination."""

    def __init__(self, api: 'Api', *args, **kwargs):
        """Init.

        :param api: api
        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(api, *args, **kwargs)
        self.request_args = RequestArgs(
            method='POST',
            url=self.url,
            full_url=self._api.service_full_url(self.url),
            data=self.request_data,
        )

    def all(self) -> IterableResponse:  # NOQA: A003,WPS125
        """Get iterable response.

        :returns: iterable response object
        """
        return IterableResponse(
            api=self._api,
            url=self.url,
            required_sid=self._required_sid,
            request_args=self.request_args,
            errors_mapping=self._errors_mapping,
            pagination_field=self._paginated_field,
            rows_in_page=self._rows_in_page,
            return_constructor=self.return_constructor,
        )

    def first(self) -> Optional[JSON_RETURN_TYPE]:
        """Get First element of sequence.

        :returns: Response object
        """
        return self.all().first()

    def get(self) -> RETURN_TYPE:
        """Get response object.

        WARNING: This method should be used only for get
          some extra fields from the first page of results.
          Use .first() or .all() methods!

        If sid problems we try to get new sid
        and retry request.

        :return: json box or response
        """
        get_result = self._api.retry_with_new_sid(self.get_once)
        return get_result  # NOQA:331

    def get_once(self) -> RETURN_TYPE:
        """Get response object.

        WARNING: This method should be used only for get
          some extra fields from the first page of results.
          Use .first() or .all() methods!

        :return: json box or response
        """
        response = self._api.service_request(
            request_args=self.request_args,
            required_sid=self._required_sid,
        )
        response = check_response(response, self._errors_mapping)
        content_type = response.headers.get('content-type')
        if content_type and 'application/json' in content_type:
            response_json = response.json()
            if 'status' in response_json:
                response_json.pop('status')
            return self.return_constructor(response_json)
        return response


# mypy bug https://github.com/python/mypy/issues/9031
class QueryO(Query, WithOnly[RequestArgs]):  # type: ignore
    """Query with only fields."""


class QueryOF(QueryO, WithFilter[RequestArgs]):  # type: ignore
    """Query with filtering."""


class QueryOS(QueryO, WithSorting[RequestArgs]):  # type: ignore
    """Query with sorting."""


class QueryOSF(QueryOF, WithSorting[RequestArgs]):  # type: ignore
    """Query with filtering ans sorting."""


class QueryOP(QueryP, WithOnly[RequestArgs]):  # type: ignore
    """Query with pagination and only fields."""


class QueryOPF(QueryOP, WithFilter[RequestArgs]):  # type: ignore
    """Query with pagination and filtering."""


class QueryOPS(QueryOP, WithSorting[RequestArgs]):  # type: ignore
    """Query with pagination and sorting."""


class QueryOPSF(QueryOPS, WithFilter[RequestArgs]):  # type: ignore
    """Query with pagination sorting and filtering."""

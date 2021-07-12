"""Base query objects."""
from typing import Any, Callable, Dict, Generic

from box import Box

from ambra_sdk.service.response import ERROR_MAPPING, JSON_RETURN_TYPE

DEFAULT_ROWS_IN_PAGINATION_PAGE = 100


class BaseQuery(Generic[JSON_RETURN_TYPE]):
    """Base query."""

    def __init__(  # NOQA: WPS211
        self,
        api,
        url: str,
        request_data: Dict[str, Any],
        errors_mapping: ERROR_MAPPING,
        required_sid: bool = False,
        return_constructor: Callable[..., JSON_RETURN_TYPE] = Box,
    ):
        """Query initialization.

        :param api: Api instance
        :param url: query url
        :param request_data: data for request
        :param errors_mapping: map of error name and exception
        :param required_sid: is sid requred for this query
        :param return_constructor: constructor for return type
        """
        self._api = api
        self.url = url
        self.request_data = request_data
        self._required_sid = required_sid
        self._errors_mapping = errors_mapping
        self.return_constructor = return_constructor

    @property
    def full_url(self) -> str:
        """Full url.

        :return: full method url
        """
        full_url: str = self._api.service_full_url(self.url)
        return full_url  # NOQA:331


class BaseQueryP(BaseQuery):
    """Base query with pagination."""

    def __init__(  # NOQA: WPS211
        self,
        api,
        url: str,
        request_data: Dict[str, Any],
        errors_mapping: ERROR_MAPPING,
        paginated_field: str,
        required_sid: bool = False,
        return_constructor: Callable[..., JSON_RETURN_TYPE] = Box,
    ):
        """Query initialization.

        :param api: Api instance
        :param url: query url
        :param request_data: data for request
        :param errors_mapping: map of error name and exception
        :param required_sid: is sid requred for this query
        :param paginated_field: field for pagination
        :param return_constructor: constructor for return type
        """
        super().__init__(
            api=api,
            url=url,
            request_data=request_data,
            errors_mapping=errors_mapping,
            required_sid=required_sid,
            return_constructor=return_constructor,
        )
        self._paginated_field = paginated_field
        self._rows_in_page = DEFAULT_ROWS_IN_PAGINATION_PAGE

    def set_rows_in_page(self, rows_in_page: int):
        """Set number of rows in one page.

        :param  rows_in_page: number of rows
        :return: self object
        :raises ValueError: number of rows should be 0 < n < 5000
        """
        # From api.html:
        #
        # The default is 100 or 1000 depending on
        # the object type and the maximum is 5000
        rows_in_page = int(rows_in_page)
        if rows_in_page > 5000:
            raise ValueError('Max rows in page is 5000')
        if rows_in_page < 0:
            raise ValueError('Negative rows in page')
        self._rows_in_page = rows_in_page
        return self


def get_query_cls_name(
    with_pagination: bool,
    with_filtering: bool,
    with_sorting: bool,
) -> str:
    """Get query class name.

    :param with_pagination: have pagination
    :param with_filtering: have filtering
    :param with_sorting: have sorting
    :return: class name
    """
    cls_name = 'QueryO'
    if with_pagination:
        cls_name += 'P'  # NOQA: WPS336
    if with_sorting:
        cls_name += 'S'  # NOQA: WPS336
    if with_filtering:
        cls_name += 'F'  # NOQA: WPS336
    return cls_name

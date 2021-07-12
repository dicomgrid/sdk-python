"""Base response objects."""

from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

from box import Box

from ambra_sdk.exceptions.service import (
    AuthorizationRequired,
    MethodNotAllowed,
    PreconditionFailed,
)

JSON_RETURN_TYPE = TypeVar('JSON_RETURN_TYPE')
ERROR_MAPPING = Mapping[
    Union[Tuple[str, Optional[str]], str],
    PreconditionFailed,
]


class BaseIterableResponse(Generic[JSON_RETURN_TYPE]):
    """BaseIterable response."""

    def __init__(  # NOQA: WPS211
        self,
        *,
        api,
        url: str,
        required_sid: bool,
        errors_mapping: ERROR_MAPPING,
        pagination_field: str,
        rows_in_page: int,
        return_constructor: Callable[..., JSON_RETURN_TYPE] = Box,
    ):
        """Respone initialization.

        :param api: api
        :param url: url
        :param required_sid: require_sid
        :param errors_mapping: map of error name and exception
        :param pagination_field: field for pagination
        :param rows_in_page: number of rows in page
        :param return_constructor: constructor for return type
        """
        self._api = api
        self._url = url
        self._required_sid = required_sid
        self._errors_mapping = errors_mapping
        self._pagination_field = pagination_field
        self._rows_in_page = rows_in_page
        self._return_constructor = return_constructor

        self._min_row: int = 0
        self._max_row: Optional[int] = None
        self._current_row: Optional[int] = None

    def __getitem__(self, key: slice):
        """Set range.

        :param key: slice for get

        :return: self object

        :raises TypeError: Invalid argument type
        :raises ValueError: Slice have a step argument
        """
        if not isinstance(key, slice):
            raise TypeError('Invalid argument type')
        start = key.start
        stop = key.stop
        step = key.step
        if step:
            raise ValueError('Not implemented slice step')
        return self.set_range(start, stop)

    def set_range(self, min_row: Optional[int], max_row: Optional[int]):
        """Set range.

        :param min_row: start row number
        :param max_row: end row number

        :return: self object

        :raises ValueError: min_row or max_row is negative
        """
        if min_row is not None and min_row < 0:
            raise ValueError('Min row is negative')
        if max_row is not None and max_row < 0:
            raise ValueError('Max row is negative')
        if min_row is None:
            min_row = 0
        self._min_row = min_row
        self._max_row = max_row
        return self

    def _prepare_data(
        self,
        request_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Prepare data for request.

        :param request_data: request data
        :return: prepared data
        """
        if request_data is None:
            request_data = {}
        request_data['page.rows'] = self._rows_in_page
        if self._current_row:
            request_data['page.number'] =  \
                self._current_row // self._rows_in_page + 1
        else:
            # Page number starts from 0
            page_number = self._min_row // self._rows_in_page
            # But for request page number starts from 1
            request_data['page.number'] = page_number + 1
            self._current_row = self._rows_in_page * page_number
        return request_data


def check_401_405(status_code: int) -> None:  # NOQA:WPS114
    """Check 401 405 status codes.

    :param status_code: status code
    :raises AuthorizationRequired: Auth required
    :raises MethodNotAllowed: Method not allowed
    """
    if status_code == 401:
        raise AuthorizationRequired()
    if status_code == 405:
        raise MethodNotAllowed()


def check_412(json, errors_mapping: ERROR_MAPPING):  # NOQA:WPS114
    """Check 412.

    :param json: json
    :param errors_mapping: errors mapping

    :raises RuntimeError: 412 with no error status
    :raises exception: Some Ambra respose exception
    :raises PreconditionFailed: Some unknow exception with 412
    """
    if json['status'] != 'ERROR':
        raise RuntimeError('412 response have no error status field')
    error_type: str = json.get('error_type')
    error_subtype: Optional[Any] = json.get('error_subtype', None)
    error_data = json.get('error_data')

    # Error type can be a list.
    # we should get only frist value of this list
    # but in Exception we pass all type
    if isinstance(error_type, list):
        error_type_value = error_type[0]
    else:
        error_type_value = error_type

    # Error subtype can be a list.
    # We should use only hashable types for dict keys
    error_subtype_str: Optional[str] = str(error_subtype) \
        if error_subtype is not None else None
    exception = errors_mapping.get((error_type_value, error_subtype_str))

    # If we have not special exc for subtype - get default
    if exception is None:
        exception = errors_mapping.get((error_type_value, None))

    # For backward compatibility
    # In previous version we have errors_mapping:
    # error_type => exception
    # Now we have:
    # (error_type, error_subtype) => exception
    if not exception and error_subtype is None:
        exception = errors_mapping.get(error_type_value)
    if exception:
        exception.set_additional_info(
            error_type,
            error_subtype,
            error_data,
        )
        raise exception
    raise PreconditionFailed(
        error_type=error_type,
        error_subtype=error_subtype,
        error_data=error_data,
    )

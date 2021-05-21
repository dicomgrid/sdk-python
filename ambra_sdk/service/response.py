"""Response objects."""

from typing import (
    Any,
    Callable,
    Generic,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

from box import Box
from requests import Response

from ambra_sdk.exceptions.service import (
    AmbraResponseException,
    AuthorizationRequired,
    MethodNotAllowed,
    PreconditionFailed,
)
from ambra_sdk.request_args import RequestArgs

RETURN_TYPE = TypeVar('RETURN_TYPE')
ERROR_MAPPING = Mapping[
    Union[Tuple[str, Optional[str]], str],
    PreconditionFailed,
]


class IterableResponse(Generic[RETURN_TYPE]):
    """Iterable response."""

    def __init__(  # NOQA: WPS211
        self,
        api,
        url: str,
        required_sid: bool,
        request_args: RequestArgs,
        errors_mapping: ERROR_MAPPING,
        pagination_field: str,
        rows_in_page: int,
        return_constructor: Callable[..., RETURN_TYPE] = Box,
    ):
        """Respone initialization.

        :param api: api
        :param url: url
        :param required_sid: require_sid
        :param request_args: request args
        :param errors_mapping: map of error name and exception
        :param pagination_field: field for pagination
        :param rows_in_page: number of rows in page
        :param return_constructor: constructor for return type
        """
        self._api = api
        self._url = url
        self._required_sid = required_sid
        self._request_args = request_args
        self._errors_mapping = errors_mapping
        self._pagination_field = pagination_field
        self._rows_in_page = rows_in_page
        self._return_constructor = return_constructor

        self._min_row: int = 0
        self._max_row: Optional[int] = None
        self._current_row = None

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

    def __iter__(self):  # NOQA: WPS231
        """Return iterator by rows.

        :yields: response object

        :raises RuntimeError: Max rows in page diffs from request
        """
        # Reset row pointer
        self._current_row = 0
        while True:
            self._prepare_data()
            response = self._api.retry_with_new_sid(self._get_response)
            json = response.json()
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

    def first(self) -> Optional[RETURN_TYPE]:
        """First element.

        :return: Return first element of seq.
        """
        try:
            response_obj: RETURN_TYPE = next(iter(self))
        except StopIteration:
            return None
        return response_obj  # NOQA:WPS331

    def _prepare_data(self):
        """Prepare data for request."""
        request_data = self._request_args.data or {}
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
        self._request_args.data = request_data  # NOQA:WPS110

    def _get_response(self):
        response = self._api.service_request(
            required_sid=self._required_sid,
            request_args=self._request_args,
        )
        return check_response(response, self._errors_mapping)


def check_response(  # NOQA:WPS231
    response: Response,
    errors_mapping: ERROR_MAPPING,
):
    """Check response on errors.

    :param response: response obj
    :param errors_mapping: map of error name and exception

    :return: response object

    :raises RuntimeError: 412 with no error status
    :raises exception: Some Ambra respose exception
    :raises PreconditionFailed: Some unknow exception with 412
    :raises AuthorizationRequired: Auth required
    :raises MethodNotAllowed: Method not allowed
    :raises AmbraResponseException: Unknown exception
    """
    if response.status_code == 200:
        return response
    elif response.status_code == 412:
        json = response.json()
        if json['status'] != 'ERROR':
            raise RuntimeError('Wrong respone')
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
    elif response.status_code == 401:
        raise AuthorizationRequired()
    elif response.status_code == 405:
        raise MethodNotAllowed()
    raise AmbraResponseException(code=response.status_code)

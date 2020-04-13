"""Response objects."""

from typing import Any, Callable, Dict, Optional

from box import Box
from requests import Response

from ambra_sdk.exceptions.service import (
    AmbraResponseException,
    AuthorizationRequired,
    MethodNotAllowed,
    PreconditionFailed,
)


class IterableResponse:
    """Iterable response."""

    def __init__(  # NOQA: WPS211
        self,
        post_method: Callable[[str, Dict[str, Any]], Response],
        url: str,
        required_sid: bool,
        request_data: Dict[str, Any],
        errors_mapping: Dict[str, PreconditionFailed],
        pagination_field: str,
        rows_in_page: int,
    ):
        """Respone initialization.

        :param post_method: post method
        :param url: url
        :param required_sid: require_sid
        :param request_data: data for request
        :param errors_mapping: map of error name and exception
        :param pagination_field: field for pagination
        :param rows_in_page: number of rows in page
        """
        self._post_method = post_method
        self._url = url
        self._required_sid = required_sid
        self._request_data = request_data
        self._errors_mapping = errors_mapping
        self._pagination_field = pagination_field

        self._rows_in_page = rows_in_page

        self._min_row: int = 0
        self._max_row: Optional[int] = None
        self._current_row = None

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
            response = self._post_method(
                url=self._url,
                required_sid=self._required_sid,
                data=self._request_data,
            )
            response = check_response(response, self._errors_mapping)

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
                yield Box(row)
            if more == 0:
                break

    def first(self) -> Optional[Box]:
        """First element.

        :return: Return first element of seq.
        """
        try:
            response_obj: Box = next(iter(self))
        except StopIteration:
            return None
        return response_obj  # NOQA:WPS331

    def _prepare_data(self):
        """Prepare data for request."""
        self._request_data['page.rows'] = self._rows_in_page
        if self._current_row:
            self._request_data['page.number'] =  \
                self._current_row // self._rows_in_page + 1
        else:
            # Page number starts from 0
            page_number = self._min_row // self._rows_in_page
            # But for request page number starts from 1
            self._request_data['page.number'] = page_number + 1
            self._current_row = self._rows_in_page * page_number


def check_response(  # NOQA:WPS231
    response: Response,
    errors_mapping: Dict[str, PreconditionFailed],
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
        error_type = json.get('error_type')
        error_subtype = json.get('error_subtype')
        error_data = json.get('error_data')

        exception = errors_mapping.get(error_type)
        if exception:
            exception.set_additional_info(error_subtype, error_data)
            raise exception
        raise PreconditionFailed()
    elif response.status_code == 401:
        raise AuthorizationRequired()
    elif response.status_code == 405:
        raise MethodNotAllowed()
    raise AmbraResponseException(code=response.status_code)

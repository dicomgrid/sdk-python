"""Response objects."""

from typing import Optional, Union

from requests import Response

from ambra_sdk.exceptions.service import AmbraResponseException
from ambra_sdk.request_args import RequestArgs
from ambra_sdk.service.response.base_response import (
    ERROR_MAPPING,
    JSON_RETURN_TYPE,
    BaseIterableResponse,
    check_401_405,
    check_412,
)

RETURN_TYPE = Union[JSON_RETURN_TYPE, Response]


class IterableResponse(BaseIterableResponse):
    """Iterable response."""

    def __init__(  # NOQA: WPS211
        self,
        *,
        request_args: RequestArgs,
        **kwargs,
    ):
        """Respone initialization.

        :param request_args: request args
        :param kwargs: kwargs
        """
        super().__init__(**kwargs)
        self._request_args = request_args

    def __iter__(self):  # NOQA: WPS231
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

    def first(self) -> Optional[JSON_RETURN_TYPE]:
        """First element.

        :return: Return first element of seq.
        """
        try:
            response_obj: JSON_RETURN_TYPE = next(iter(self))
        except StopIteration:
            return None
        return response_obj  # NOQA:WPS331

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

    :raises AmbraResponseException: Unknown exception
    :raises RuntimeError: Bad content type for 412
    """
    status_code = response.status_code
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
        json = response.json()
        check_412(json, errors_mapping)
    raise AmbraResponseException(code=status_code)

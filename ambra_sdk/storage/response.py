"""Storage respone objects."""

from typing import Any, Mapping, Optional

from requests import Response

from ambra_sdk.exceptions.storage import (
    AmbraResponseException,
    NotFound,
    PermissionDenied,
)


def check_response(
    response: Response,
    url: str,
    errors_mapping: Optional[Mapping[int, Any]] = None,
) -> Response:
    """Check response on errors.

    :param response: response obj
    :param url: full url str
    :param errors_mapping: map of error name and exception

    :return: response object

    :raises AmbraResponseException: Unknown exception
    :raises PermissionDenied: Permission denied
    :raises NotFound: Url or args is wrong
    :raises exception: Some ambra storage response exception

    """
    status_code = response.status_code
    if status_code == 200:
        return response
    # 202 - Accepted
    if status_code == 202:
        return response

    if errors_mapping is not None and status_code in errors_mapping:
        exception = errors_mapping[status_code]
        raise exception
    elif status_code == 404:
        description = 'Url is wrong: {url}' \
            .format(url=url)
        raise NotFound(description)
    elif status_code == 403:
        description = 'Access denied or wrong sid'
        raise PermissionDenied(description)
    raise AmbraResponseException(
        code=status_code,
        description='Unknown status code',
    )

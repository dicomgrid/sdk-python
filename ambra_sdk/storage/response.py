"""Storage respone objects."""

from typing import Any, Dict, Optional, Set

from requests import Response

from ambra_sdk.exceptions.storage import (
    AmbraResponseException,
    NotFound,
    PermissionDenied,
)


def check_response(
    response: Response,
    url_arg_names: Set[str],
    errors_mapping: Optional[Dict[int, Any]] = None,
) -> Response:
    """Check response on errors.

    :param response: response obj
    :param url_arg_names: set of arguments in url
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
        description = 'Url or some of {url_arg_names} is wrong' \
            .format(url_arg_names=url_arg_names)
        raise NotFound(description)
    elif status_code == 403:
        description = 'Access denied. Wrong sid'
        raise PermissionDenied(description)
    raise AmbraResponseException(
        code=status_code,
        description='Unknown status code',
    )

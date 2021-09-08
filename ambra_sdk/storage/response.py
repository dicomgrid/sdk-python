"""Storage respone objects."""

from json import JSONDecodeError
from json import loads as json_loads
from typing import NoReturn

from aiohttp import ClientResponse
from requests import Response

from ambra_sdk.exceptions.storage import (
    STORAGE_ERROR_CODES,
    STORAGE_ERRORS,
    AmbraResponseException,
)


def raise_storage_error(status_code, json) -> NoReturn:
    """Raise storage error.

    :param status_code: status code
    :param json: json

    :raises AmbraResponseException: Unknown error
    :raises error: knowon storage error
    """
    kind = json.get('kind')
    if not kind:
        raise AmbraResponseException(
            code=status_code,
            description='Unknown kind',
        )
    readable_status = kind.get('readable_status')
    if not readable_status:
        raise AmbraResponseException(
            code=status_code,
            description='Unknown storage status',
        )

    error = STORAGE_ERRORS.get(readable_status)
    if not error:
        raise AmbraResponseException(
            code=status_code,
            description='Unknown storage error',
        )

    raise error(
        http_status_code=status_code,
        exception_data=json.get('exception_data'),
        storage_code=kind.get('code'),
        description=json.get('message'),
        readable_status=readable_status,
        created=json.get('created'),
        extended=json.get('extended'),
    )


def check_errors(response: Response) -> Response:
    """Check errors.

    :param response: response
    :raises AmbraResponseException: Unknown error

    :return: resonse
    """
    status_code = response.status_code
    if status_code in {200, 202}:
        return response
    if status_code not in STORAGE_ERROR_CODES:
        raise AmbraResponseException(
            code=status_code,
            description='Unknown status code',
        )

    try:
        json = response.json()
    except JSONDecodeError:
        raise AmbraResponseException(
            code=status_code,
            description='Unknown status code',
            response_text=response.text,
        )
    raise_storage_error(status_code, json)


async def async_check_errors(response: ClientResponse) -> ClientResponse:
    """Check errors.

    :param response: response
    :raises AmbraResponseException: Unknown error

    :return: resonse
    """
    status_code = response.status
    if status_code in {200, 202}:
        return response
    if status_code not in STORAGE_ERROR_CODES:
        raise AmbraResponseException(
            code=status_code,
            description='Unknown status code',
        )

    text = await response.text()
    try:
        json = json_loads(text)
    except JSONDecodeError:
        raise AmbraResponseException(
            code=status_code,
            description='Unknown status code',
            response_text=text,
        )
    raise_storage_error(status_code, json)

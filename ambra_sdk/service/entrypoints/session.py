from typing import Dict, Optional

from ambra_sdk.service.entrypoints.generated.session import \
    AsyncSession as GAsyncSession
from ambra_sdk.service.entrypoints.generated.session import Session as GSession


class Session(GSession):
    """Session."""

    def get_sid(
        self,
        username: str,
        password: str,
        special_headers_for_login: Optional[Dict[str, str]] = None,
    ) -> 'str':
        """Get sid from credentials.

        :param username: user name
        :param password: user password
        :param special_headers_for_login: special headers for login
        :return: sid
        """
        query = self.login(login=username, password=password)
        query.request_args.headers = special_headers_for_login
        response = query.get_once()
        sid: str = response.sid
        return sid  # NOQA: WPS331


class AsyncSession(GAsyncSession):
    """AsyncSession."""

    async def get_sid(
        self,
        username: str,
        password: str,
        special_headers_for_login: Optional[Dict[str, str]] = None,
    ) -> 'str':
        """Get sid from credentials.

        :param username: user name
        :param password: user password
        :param special_headers_for_login: special headers for login
        :return: sid
        """
        query = self.login(login=username, password=password)
        query.request_args.headers = special_headers_for_login
        response = await query.get_once()
        sid: str = response.sid
        return sid  # NOQA: WPS331

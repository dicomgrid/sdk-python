from ambra_sdk.service.entrypoints.generated.session import Session as GSession


class Session(GSession):
    """Session."""

    def get_sid(self, username, password) -> 'str':
        """Get sid from credentials.

        :param username: user name
        :param password: user password
        :return: sid
        """
        response = self.login(login=username, password=password).get_once()
        sid: str = response.sid
        return sid  # NOQA: WPS331

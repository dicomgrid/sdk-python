"""Ambra exceptions."""


class AmbraException(Exception):
    """Base ambra exception."""


class AmbraResponseException(AmbraException):
    """Ambra response exception."""

    def __init__(self, code, description=None):
        """Init.

        :param code: response code
        :param description: error description
        """
        message = '{code}. {description}'.format(
            code=code,
            description=description,
        )
        super().__init__(message)
        self.code = code
        self.description = description

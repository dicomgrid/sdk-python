"""Ambra exceptions."""


class AmbraException(Exception):
    """Base ambra exception."""


class AmbraResponseException(AmbraException):
    """Ambra response exception."""

    def __init__(self, code, description=None, response_text=None):
        """Init.

        :param code: response code
        :param description: error description
        :param response_text: response text
        """
        message = '{code}. {description}'.format(
            code=code,
            description=description,
        )
        if response_text:
            message = '{base_message}\n{text}'.format(
                base_message=message,
                text=response_text,
            )
        super().__init__(message)
        self.code = code
        self.description = description
        self.response_text = response_text

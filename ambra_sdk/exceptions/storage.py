"""Ambra storage exceptions."""

from ambra_sdk.exceptions.base import AmbraResponseException


class PermissionDenied(AmbraResponseException):
    """Permission denied."""

    def __init__(self, description=None):
        """Init.

        :param description: response description
        """
        code = 403
        if description is None:
            description = 'Access denied. Wrong sid'
        super().__init__(code, description)


class NotFound(AmbraResponseException):
    """Not found."""

    def __init__(self, description=None):
        """Init.

        :param description: response description
        """
        code = 404
        if description is None:
            description = 'Not found'
        super().__init__(code, description)


class UnsupportedMediaType(AmbraResponseException):
    """Unsupported media type."""

    def __init__(self, description=None):
        """Init.

        :param description: response description
        """
        code = 415
        if description is None:
            description = 'Video was not found encapsulated in the DICOM file.'
        super().__init__(code, description)


class PreconditionFailed(AmbraResponseException):
    """Unsupported media type."""

    def __init__(self, description=None):
        """Init.

        :param description: response description
        """
        code = 412
        if description is None:
            description = 'Precondition failed.'
        super().__init__(code, description)


class InconsistencyConflict(AmbraResponseException):
    """Inconsistency conflict."""

    def __init__(self, description=None):
        """Init.

        :param description: response description
        """
        code = 409
        if description is None:
            description = 'Inconsistency conflict.'
        super().__init__(code, description)


class EntityTooLarge(AmbraResponseException):
    """EntityTooLarge."""

    def __init__(self, description=None):
        """Init.

        :param description: response description
        """
        code = 413
        if description is None:
            description = 'Entity too large.'
        super().__init__(code, description)


class UnprocessableEntity(AmbraResponseException):
    """UnprocessableEntity."""

    def __init__(self, description=None):
        """Init.

        :param description: response description
        """
        code = 422
        if description is None:
            description = 'Request body is empty.'
        super().__init__(code, description)

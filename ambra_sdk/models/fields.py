
from datetime import date, datetime

from ambra_sdk.models.base import FK, BaseField  # NOQA F401


class String(BaseField):
    """String field."""

    _python_type = str

    def validate(self, value):  # NOQA WPS110
        """Validate.

        :param value: value
        :return: value
        """
        return self._python_type(value)


class Boolean(BaseField):
    """Boolean field."""

    _python_type = bool

    def validate(self, value):  # NOQA WPS110
        """Validate.

        :param value: value
        :return: value
        """
        return self._python_type(value)

    def for_request(self, value):  # NOQA WPS110
        """Get value for request.

        :param value: value for request
        :returns: value for requesting
        """
        validated_value = self.validate(value)
        return '1' if validated_value is True else '0'


class Integer(BaseField):
    """Int field."""

    _python_type = int

    def validate(self, value):  # NOQA WPS110
        """Validate.

        :param value: value
        :return: value
        """
        return self._python_type(value)


class Float(BaseField):
    """Float field."""

    _python_type = float

    def validate(self, value):  # NOQA WPS110
        """Validate.

        :param value: value
        :return: value
        """
        return self._python_type(value)


class JsonB(BaseField):
    """JsonB field."""

    _python_type = bytes

    def validate(self, value):  # NOQA WPS110
        """Validate.

        :param value: value
        :return: value
        """
        return self._python_type(value)


class Date(BaseField):
    """Date field."""

    _python_type = date

    def validate(self, value):  # NOQA WPS110
        """Validate.

        :param value: value
        :return: value
        :raises ValueError: wrong value type
        """
        if not isinstance(
            value,
            self._python_type,
        ):
            raise ValueError
        return value


class DateTime(BaseField):
    """Date time field."""

    _python_type = datetime

    def validate(self, value):  # NOQA WPS110
        """Validate.

        :param value: value
        :return: value
        :raises ValueError: wrong value type
        """
        if not isinstance(
            value,
            self._python_type,
        ):
            raise ValueError
        return value


class DictField(BaseField):
    """Dict field.

    In pg this type is hstore
    """

    _python_type = dict

    def validate(self, value):  # NOQA WPS110
        """Validate.

        :param value: value
        :return: value
        """
        return self._python_type(value)

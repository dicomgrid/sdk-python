"""Help functions."""

from typing import Optional


def bool_to_int(bool_value: Optional[bool]) -> Optional[int]:
    """Cast bool to int value.

    :param bool_value: some bool value
    :return: int represenation
    """
    if bool_value is None:
        return bool_value
    return int(bool_value)

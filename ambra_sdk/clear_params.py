from typing import Any, Dict

PROTECTED_KEYS = frozenset((
    'sid',
    'username',
    'login',
    'password',
))


def clear_params(dict_params: Dict[str, Any]) -> Dict[str, Any]:
    """Clear PHI parameters.

    :param dict_params: params
    :return: cleared params
    """
    return {
        key: p_value for key, p_value in dict_params.items()
        if key not in PROTECTED_KEYS
    }

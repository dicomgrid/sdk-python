"""Parse errors."""

from typing import List, Optional


class ErrorSubtype:

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class ErrorParameter:

    def __init__(
        self,
        name: str,
        description: str,
        error_code: int = 412,
        subtypes: Optional[List[ErrorSubtype]] = None,
    ):
        # 412 - precondition failed
        self.name = name
        self.description = description
        self.error_code = error_code
        if subtypes is None:
            self.subtypes = [
                None,
            ]
        else:
            self.subtypes = subtypes
        self.subtypes = sorted(self.subtypes, key=lambda x: str(x))

    def exception_name(self):
        return ''.join(part.capitalize() for part in self.name.split('_'))

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, rh):
        return self.__repr__() == rh.__repr__()

    def __repr__(self):
        return '{name}: {description}'.format(
            name=self.name,
            description=self.description,
        )


ERROR_PARAMETERS_STRING_MAP = {
    '404 not found':
    ErrorParameter('NOT_FOUND', 'Not found', 404),
    'Returns a 404 HTTP error if the report can not be found or is not available for download':
    ErrorParameter('NOT_FOUND', 'Not found', 404),
    'SHARE_FAILED • The share failed. The error_subtype holds one of the following conditions.':
    ErrorParameter(
        'SHARE_FAILED',
        'The share failed. The error_subtype holds one of the following conditions.',
        subtypes=[
            ErrorSubtype(
                'SAME', 'The study can\'t be shared into the same namespace',
            ),

            ErrorSubtype(
                'NO_DESTINATION', 'The study can\'t be shared with a deleted object',
            ),
            ErrorSubtype('DECLINED', 'The charge card was declined'),
            ErrorSubtype('NO_CARD', 'The user does not have a card on file'),
            ErrorSubtype(
                'NO_CHARGE_MODALITY',
                'The charge modality is required if charge_authorized is set and the charging is by modality'
            ),
            ErrorSubtype(
                'NO_DUP_SHARE',
                'The destination namespace has the no_dup_share flag turned on and this study is a duplicate of an existing study in the namespace'
            ),
        ]
    ),
    'ROLE_NAMESPACE_MISMATCH, subtype INCOMPATIBLE_ROLE, data contains role_id and namespace_id • The role cannot be used for the account':
    ErrorParameter(
        'ROLE_NAMESPACE_MISMATCH',
        'Role namespace mismatch',
        subtypes=[
            ErrorSubtype(
                'INCOMPATIBLE_ROLE',
                'The role cannot be used for the account',
            ),
        ],
    ),
    'ROLE_NAMESPACE_MISMATCH, subtype GLOBAL_USER_WITH_RESTRICTED_ROLE, data contains role_id, namespace_id and user_id • They are making the user global with a role restricted to group/location and there is a group/location in the account':
    ErrorParameter(
        'ROLE_NAMESPACE_MISMATCH',
        'Role namespace mismatch',
        subtypes=[
            ErrorSubtype(
                'GLOBAL_USER_WITH_RESTRICTED_ROLE',
                'They are adding a global user with a role restricted to group/location and there is a group/location in the account',
            ),
        ],
    ),
    'ROLE_NAMESPACE_MISMATCH, subtype GLOBAL_USER_WITH_RESTRICTED_ROLE, data contains role_id, namespace_id and user_id • They are adding a global user with a role restricted to group/location and there is a group/location in the account':
    ErrorParameter(
        'ROLE_NAMESPACE_MISMATCH',
        'Role namespace mismatch',
        subtypes=[
            ErrorSubtype(
                'GLOBAL_USER_WITH_RESTRICTED_ROLE',
                'They are adding a global user with a role restricted to group/location and there is a group/location in the account',
            ),
        ],
    ),

    'ROLE_NAMESPACE_MISMATCH, subtype GLOBAL_USER_WITH_RESTRICTED_ROLE, data contains role_id and user_id • You are adding the group to the account with a global user with restricted role':
    ErrorParameter(
        'ROLE_NAMESPACE_MISMATCH',
        'Role namespace mismatch',
        subtypes=[
            ErrorSubtype(
                'GLOBAL_USER_WITH_RESTRICTED_ROLE',
                'You are adding the group to the account with a global user with restricted role',
            ),
        ],
    ),
    'ROLE_NAMESPACE_MISMATCH, subtype INCOMPATIBLE_ROLE, data contains role_id and namespace_id • The role cannot be used for a location':
    ErrorParameter(
        'ROLE_NAMESPACE_MISMATCH',
        'Role namespace mismatch',
        subtypes=[
            ErrorSubtype(
                'INCOMPATIBLE_ROLE',
                'The role cannot be used for the location',
            ),
        ],
    ),
    'ROLE_NAMESPACE_MISMATCH, subtype INCOMPATIBLE_ROLE, data contains role_id and namespace_id • The role cannot be used for locations':
    ErrorParameter(
        'ROLE_NAMESPACE_MISMATCH',
        'Role namespace mismatch',
        subtypes=[
            ErrorSubtype(
                'INCOMPATIBLE_ROLE',
                'The role cannot be used for locations',
            ),
        ],
    ),
    'ROLE_NAMESPACE_MISMATCH, subtype GLOBAL_USER_WITH_RESTRICTED_ROLE, data contains role_id and user_id • You are adding the location to the account with a global user with restricted role':
    ErrorParameter(
        'ROLE_NAMESPACE_MISMATCH',
        'Role namespace mismatch',
        subtypes=[
            ErrorSubtype(
                'GLOBAL_USER_WITH_RESTRICTED_ROLE',
                'You are adding the location to the account with a global user with restricted role',
            ),
        ],
    ),
    'ROLE_NAMESPACE_MISMATCH, subtype INCOMPATIBLE_ROLE, data contains role_id and namespace_id • The role cannot be used for a group':
    ErrorParameter(
        'ROLE_NAMESPACE_MISMATCH',
        'Role namespace mismatch',
        subtypes=[
            ErrorSubtype(
                'INCOMPATIBLE_ROLE',
                'The role cannot be used for a group',
            ),
        ],
    ),
    'ROLE_NAMESPACE_MISMATCH, subtype INCOMPATIBLE_ROLE, data contains role_id and namespace_id • The role cannot be used for groups':
    ErrorParameter(
        'ROLE_NAMESPACE_MISMATCH',
        'Role namespace mismatch',
        subtypes=[
            ErrorSubtype(
                'INCOMPATIBLE_ROLE',
                'The role cannot be used for groups',
            ),
        ],
    ),
}

BAD_ERROR_PARAMETERS_STRING = {
    'SAME - The study can\'t be shared into the same namespace',
    'NO_DESTINATION - The study can\'t be shared with a deleted object',
    'DECLINED - The charge card was declined',
    'NO_CARD - The user does not have a card on file',
    'NO_CHARGE_MODALITY - The charge modality is required if charge_authorized is set and the charging is by modality',
    'NO_DUP_SHARE - The destination namespace has the no_dup_share flag turned on and this study is a duplicate of an existing study in the namespace',
    'If the link is valid but an associated study is not found an HTML "Study not found." message is returned for display in the browser.',
    'If the link is valid but an associated study is not found this returns an HTML "Study not found." error for display in the browser.',
    'If the link is valid but more than 100 studies match it an HTML "Too many studies found." message is returned for display in the browser.',
    'If the link comes from a different vanity than the study an "Invalid vanity" message is returned for display in the browser',
    'Returns a 401 HTTP error if authentication failed',
}


def parse_error_parameter(parameter_str):
    if parameter_str in ERROR_PARAMETERS_STRING_MAP:
        return ERROR_PARAMETERS_STRING_MAP[parameter_str]
    try:
        name, description = parameter_str.split('•')
    except ValueError as exc:
        raise RuntimeError('Can not parse %s' % parameter_str) from exc
    name = name.strip()
    description = description.strip()
    return ErrorParameter(name, description)


def parse_error_parameters(parameters_str):
    error_params = []
    for parameter_str in parameters_str.split('\n'):
        parameter_str = parameter_str.strip()
        if parameter_str == '':
            continue
        if parameter_str in BAD_ERROR_PARAMETERS_STRING:
            continue
        param = parse_error_parameter(parameter_str)
        error_params.append(param)
    return error_params

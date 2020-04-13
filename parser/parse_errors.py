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
            self.subtypes = []
        else:
            self.subtypes = subtypes

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
    '404 not found': ErrorParameter('NOT_FOUND', 'Not found', 404),
    'Returns a 404 HTTP error if the report can not be found or is not available for download': ErrorParameter('NOT_FOUND', 'Not found', 404),
    'SHARE_FAILED • The share failed. The error_subtype holds one of the following conditions.': ErrorParameter(
        'SHARE_FAILED',
        'The share failed. The error_subtype holds one of the following conditions.',
        subtypes=[
            ErrorSubtype('SAME', 'The study can\'t be shared into the same namespace'),
            ErrorSubtype('DECLINED', 'The charge card was declined'),
            ErrorSubtype('NO_CARD', 'The user does not have a card on file'),
            ErrorSubtype('NO_CHARGE_MODALITY', 'The charge modality is required if charge_authorized is set and the charging is by modality'),
            ErrorSubtype('NO_DUP_SHARE', 'The destination namespace has the no_dup_share flag turned on and this study is a duplicate of an existing study in the namespace'),
        ]

    ),
}

BAD_ERROR_PARAMETERS_STRING = {
    'SAME - The study can\'t be shared into the same namespace',
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
    name, description = parameter_str.split('•')
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

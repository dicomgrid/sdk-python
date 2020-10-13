"""Parse request parameters."""

from enum import Enum, auto
from typing import List, NamedTuple, Optional
from ambra_sdk.pythonize import PARAMS


class RequestParameterType(Enum):
    Usual = auto()
    Filter = auto()
    Pagination = auto()
    Sorting = auto()

    # multiple params
    # /audit/log example
    # it is dict of params
    Multiple = auto()


class RequestParameter:

    @classmethod
    def filtrator(cls):
        return cls(RequestParameterType.Filter, None, None, None)

    @classmethod
    def paginator(cls):
        return cls(RequestParameterType.Pagination, None, None, None)

    @classmethod
    def sorter(cls):
        return cls(RequestParameterType.Sorting, None, None, None)

    def __init__(
        self,
        parameter_type: RequestParameterType,
        name: Optional[str],
        description: Optional[str],
        optional: Optional[bool],
        multiple_prefix: str = '',
    ):
        self.parameter_type = parameter_type
        self.name = name
        self.pythonic_name = PARAMS.get(name, name)
        self.description = description
        self.optional = optional
        self.multiline = False
        self.multiliple_prefix=multiple_prefix

    def __hash__(self):
        return hash((self.name, self.parameter_type))

    def __eq__(self, rh):
        return self.name == rh.name and self.parameter_type == self.parameter_type


class RequestGroupParametersDoc:

    def __init__(self, description):
        self.description = description


BAD_REQUEST_PARAMETERS_FIELDS = {
    'filter.*=>Filter field(s) as per the /study/list to specify the study(s) to construct the link for',
    'The include_priors link option value can be passed as a key',
    'Any additional fields will the saved in the study audit trail and the following fields email_address, redirect_url, integration_key and skip_email_prompt will be available in /namespace/share_code if this is an upload link',
}

REQUEST_PARAMETERS_STRING_MAP = {
    'v • A JSON hash with the following keys pairs. The JSON must be encrypted and base64 encoded':
    RequestParameter(
        RequestParameterType.Usual,
        'v',
        """
        A JSON hash with the following keys pairs. The JSON must be encrypted and base64 encoded:
        filter.*=>Filter field(s) as per the /study/list to specify the study(s) to construct the link for.
        The include_priors link option value can be passed as a key.
        Any additional fields will the saved in the study audit trail and the following fields email_address, redirect_url, integration_key and skip_email_prompt will be available in /namespace/share_code if this is an upload link .""",
        optional=True,
    ),
    # TODO: Can be fixed in new versions of api
    'dicom_tags A JSON list of the DICOM tags to return (optional)':
    RequestParameter(
        RequestParameterType.Usual,
        'dicom_tags',
        'A JSON list of the DICOM tags to return (optional)',
        optional=True,
    ),
    'key • The key to store the value under. If the key name begins with temp_ it is only available for the session.':
    RequestParameter(
        RequestParameterType.Usual,
        'key',
        'The key to store the value under. If the key name begins with temp it is only available for the session.',
        optional=False,
    ),
    'The rest of the parameters are logged to a message in the bucket':
    RequestParameter(
        RequestParameterType.Multiple,
        'logged_params',
        'Dict of parameters. They are logged to a message in the bucket',
        optional=False,
    ),
    'And all the ai_* settings':
    RequestParameter(
        RequestParameterType.Multiple,
        'ai_settings',
        'Dict of ai settings',
        optional=False,
    ),
    'All additional parameters will be logged as part of the TRAINING_DONE user audit event':
    RequestParameter(
        RequestParameterType.Multiple,
        'additional_parameters',
        'All additional parameters will be logged as part of the TRAINING_DONE user audit event',
        optional=False,
    ),
    'The rest of the fields can not be set by the case owner':
    RequestGroupParametersDoc(
        'The rest of the fields can not be set by the case owner',
    ),
    '-- The rest of the fields are used for the search --':
    RequestGroupParametersDoc(
        'The rest of the fields are used for the search',
    ),
    '------ The following account settings can be over-ridden in the namespace ------':
    RequestGroupParametersDoc(
        'The following account settings can be over-ridden in the namespace',
    ),

    # study.duplicate overwrite is actually optional
    'overwrite • Flag if you want to overwrite an existing study in the destination namespace':
    RequestParameter(
        RequestParameterType.Usual,
        'overwrite',
        'Flag if you want to overwrite an existing study in the destination namespace',
        optional=True,
    ),

}


def parse_request_parameter(parameter_str):
    parameter_str = parameter_str.strip()
    if parameter_str.startswith('filter.'):
        return RequestParameter.filtrator()
    elif parameter_str.startswith('page.'):
        return RequestParameter.paginator()
    elif parameter_str == 'sort_by • Sorting (optional)':
        return RequestParameter.sorter()
    else:
        name, description = parameter_str.split('•')
        name = name.strip()
        description = description.strip()

        optional = False
        if 'optional' in description:
            optional = True

        # multiple field line Node.set::setting_SETTING_NAME
        if any(i.isupper() for i in name):
            optional = True
            if 'customfield-' in name:
                multi_prefix = 'customfield-'
                field_name = 'customfield_param'
            else:
                prefix = name.split('_')[0]
                multi_prefix = '{prefix}_'.format(prefix=prefix)
                field_name = '{prefix}_param'.format(prefix=prefix)
            return RequestParameter(
                RequestParameterType.Multiple,
                field_name,
                description,
                optional,
                multiple_prefix=multi_prefix,
            )
        else:
            return RequestParameter(
                RequestParameterType.Usual,
                name,
                description,
                optional,
            )


def parse_combinated_request_parameter(parameter_str):
    if not ('|' in parameter_str or '&' in parameter_str):
        raise ValueError('Not combined parameter')
    params = []
    # Append documentation for group of params
    group_doc = parameter_str \
        .replace('||', ' OR ') \
        .replace('|', ' OR ') \
        .replace('&&', ' AND ') \
        .replace('&', ' AND ') \
        .replace('  ', ' ') \
        .replace('•', '-')

    params.append(RequestGroupParametersDoc(group_doc))
    if 'customfield-' in parameter_str:
        _, description = parameter_str.split('•')
        description = description.strip()
        optional = False
        if 'optional' in description:
            optional = True

        multi_prefix = 'customfield-'
        field_name = 'customfield_param'
        param = RequestParameter(
            RequestParameterType.Multiple,
            field_name,
            description,
            optional,
            multiple_prefix=multi_prefix,
        )
        params.append(param)
        return params

    parameter_str = parameter_str.split('•')[0]
    param_names = []
    # split by '&' because both usage '&' and '&&'
    for p_str in parameter_str.split(')')[0].strip('(').split('&'):
        # split by '|' because both usage '|' and '||'
        param_names.extend([i.strip() for i in p_str.split('|')])
    param_names = list(set([i for i in param_names if i != '']))
    for param_name in param_names:
        params.append(
            RequestParameter(
                RequestParameterType.Usual,
                param_name,
                param_name,
                True,
            ),
        )
    return params


def parse_request_parameters(parameters_str):
    request_params = []
    for parameter_str in parameters_str.split('\n'):
        parameter_str = parameter_str.strip()
        if parameter_str == '':
            continue
        if parameter_str in BAD_REQUEST_PARAMETERS_FIELDS:
            continue

        # Its description of array fields
        if parameter_str.startswith('*'):
            p_param = request_params.pop()
            parameter_str = parameter_str \
                .replace('*', '') \
                .replace('•', '-') \
                .strip()
            sep = ':' if p_param.multiline is False else ''
            desc = '{p_desc}{sep}\n            {n_desc}'.format(
                sep=sep,
                p_desc=p_param.description, n_desc=parameter_str
            )
            p_param.description = desc
            p_param.multiline = True
            request_params.append(p_param)
            continue

        # Special cases
        if parameter_str in REQUEST_PARAMETERS_STRING_MAP:
            param = REQUEST_PARAMETERS_STRING_MAP[parameter_str]
            request_params.append(param)
            continue

        first_part = parameter_str.split('•')[0]
        if '|' in first_part or '&' in first_part :
            request_params.extend(
                parse_combinated_request_parameter(parameter_str)
            )
            continue
        param = parse_request_parameter(parameter_str)
        request_params.append(param)
    return list(set(request_params))

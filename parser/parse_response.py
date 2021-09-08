"""Parse response parameters."""

from enum import Enum, auto
from typing import List, NamedTuple, Optional, Union


class LinkedParams:

    def __init__(self, link_url: str, deep: int = 1):
        self.link = link_url
        self.deep = deep

    def __repr__(self):
        return 'Link: {link}'.format(link=self.link)


DOC_FIELDS = {
    'The rest of the fields are not returned to the case owner',
    'STUDY_APPROVE - Notification to approve a study',
    'JOIN_REQUEST - A user has requested to join the account',
    'DESTINATION_SEARCH - Result of a destination search',
    'USER_INVITE- An invitation to join the account to user has being sent to a user',
    'NODE_CONNECT- A user has requested to connect the public node',
    'STUDY_REQUEST_INBOUND - An incoming study request',
    'STUDY_REQUEST_OUTBOUND - An outgoing study request',
    'TRIAL_QC_TASK - A pending clinical trial QC task',
    '* Epoch time of the event',
    '* LOCKOUT if the login failed due to the lockout or PRIMARY if the login failed due to invalid credentials',
    '* The vanity of the event',
    '* The client IP address',
    '* The rest of the fields hold the email and account information depending on the parameters used for /session/login',
}

LINKED_FIELDS = {
    'The rest of the fields are the same as /user/get':
    LinkedParams('user/get'),
    'The permissions for the user in this account':
    LinkedParams('permission_params'),
    '* The rest of the fields are the optional search parameters in either the /destination/search or the /destination/search/mwl call':
    LinkedParams('union[/destination/search,/destination/search/mwl]', deep=2),
    'The fields from /meeting/get':
    LinkedParams('/meeting/get'),
}

FIX_FIELDS_MAP = {
    # TODO: fixed in new api
    'comments • An array of the study comments, order from most recent too earliest. This is only returned if the user has the study_comment_view permissions. Each object has the fields in':
    'comments • An array of the study comments, order from most recent too earliest. This is only returned if the user has the study_comment_view permissions. Each object has the fields in the /study/comment/get call.',
    # TODO: fixed in new api
    'second_opinion_share Flag if this is a  second opinion workflow (optional)':
    'second_opinion_share • Flag if this is a  second opinion workflow (optional)',
    # TODO: fixed in new api
    'second_opinion_config JSON configuration for the second opinion workflow (optional)':
    'second_opinion_config • JSON configuration for the second opinion workflow (optional)',
    # TODO: fixed in new api
    'second_opinion_case The second opinion case. The fields are per /case/get (optional)':
    'second_opinion_case • The second opinion case. The fields are per /case/get (optional)',
    # TODO: fixed in new api
    'second_opinion_share Flag to enable/disable the second opinion workflow for the share':
    'second_opinion_share • Flag to enable/disable the second opinion workflow for the share',
    # TODO: fixed in new api
    'second_opinion_config JSON configuration for the second opinion workflow':
    'second_opinion_config • JSON configuration for the second opinion workflow',
    # TODO: fixed in new api
    'object The object this is applied against':
    'object • The object this is applied against',
}

BAD_FIELDS = {
    # TODO: fixed in new api
    'the /study/comment/get call.'
}

RETURN_REDIRECT = {
    'A redirect to the passed URL which sets an httponly CSFR token cookie',
    'A redirect to the brand OAuth provider',
    'This call returns a 302 redirect to either the study list or study viewer or uploader page  with the session setup in a cookie or in the URL if the link is valid',
    'This creates a link and uses the /link/redirect call to redirect the user to either the study viewer or a study list if multiple studies are found',
    'This link logs the user into a PHR account with any associated studies shared into it',
}


class Redirect:

    def __init__(self, description: str):
        self.descritpion = description


RETURN_STREAM = {
    'Streams back the PDF report':
    'pdf',
    'Streams back the zip file':
    'zip',
    'A CSS file':
    'css',
    'The data in i18next format':
    'i18next',
    'A binary stream of the zipped data with a content type of application/zip':
    'zip',
}


class Stream:

    def __init__(self, description: str, stream_format: str):
        self.descritpion = description
        self.stream_format = stream_format


class ResponseParameter:

    def __init__(
        self, name: Optional[str], description: Optional[str], deep: int = 0
    ):
        self.name = name
        self.description = description
        self.schema: List[Union['ResponseParameter', LinkedParams]] = []
        self.deep = deep

    def add_to_schema(
        self,
        parameter: Union['ResponseParameter', LinkedParams],
    ):
        self.schema.append(parameter)

    @property
    def is_array(self):
        """Is parameter array."""
        if self.description and 'array' in self.description:
            return True
        return False

    def __repr__(self):
        if self.schema:
            schema_str = '\n'.join([str(rparam) for rparam in self.schema], )
            return '''{name}: {description}\n{schema}'''.format(
                name=self.name,
                description=self.description,
                schema=schema_str,
            )
        return '{space}{name}: {description}'.format(
            space=self.deep * ' ',
            name=self.name,
            description=self.description
        )


class ResponseGroupParametersDoc:

    def __init__(self, description):
        self.description = description


def parse_response_parameter(parameter_str):
    # TODO: WTF '↳' is (DICT??)?
    if '*':
        deep = parameter_str.count('*') + 1

    if parameter_str in LINKED_FIELDS:
        return LINKED_FIELDS[parameter_str]
    try:
        name, description = parameter_str.split('•')
    except ValueError:
        raise ValueError(parameter_str)
    name = name.replace('*', '').replace('↳', '').strip()
    return ResponseParameter(name, description, deep)


def parse_response_parameters(parameters_str):

    current_deep = 0
    root = ResponseParameter('root', 'root', current_deep)

    previus = [root]

    for parameter_str in parameters_str.split('\n'):
        parameter_str = parameter_str.strip()
        if parameter_str == '':
            continue

        if parameter_str in BAD_FIELDS:
            continue

        if parameter_str in FIX_FIELDS_MAP:
            parameter_str = FIX_FIELDS_MAP[parameter_str]

        if parameter_str.startswith('--') or parameter_str in DOC_FIELDS:
            doc_parameter = ResponseGroupParametersDoc(parameter_str)
            root.add_to_schema(doc_parameter)
            continue

        if parameter_str in RETURN_REDIRECT:
            assert len(root.schema) == 0
            return Redirect(parameter_str)

        if parameter_str in RETURN_STREAM:
            assert len(root.schema) == 0
            return Stream(parameter_str, RETURN_STREAM[parameter_str])

        new_parameter = parse_response_parameter(parameter_str)
        deep = new_parameter.deep

        deep_diff = deep - current_deep

        # It  is not True for /study/timing/log
        # assert deep_diff in (-1, 0, 1)

        if deep_diff <= 0:
            previus.pop()

        previus[-1].add_to_schema(new_parameter)
        previus.append(new_parameter)
        current_deep = deep
    return root.schema

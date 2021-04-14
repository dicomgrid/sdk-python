"""Parse errors."""

from typing import List, Optional
import re


#error_regex = re.compile(r'(?: ([A-Z,0-9,_]+))?(?: \(([A-Z,_]+)\))?(?: \[([0-9]+)\])? • (.+)')

error_regex = re.compile(r'(?:([A-Z,0-9_]+) )?(?:\(([A-Z,_]+)\) )?(?:\[([A-Z,0-9,_]+)\] )?• (.+)')


class ErrorParameter:

    def __init__(
        self,
        name: str,
        description: str,
        error_code: int = 412,
        subtype: Optional[str] = None,
    ):
        # 412 - precondition failed
        self.name = name
        self.description = description
        self.error_code = error_code
        self.subtype = subtype

    def exception_name(self):
        return ''.join(part.capitalize() for part in self.name.split('_'))

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, rh):
        return self.__repr__() == rh.__repr__()

    def __repr__(self):
        return '{name} {subtype} {code}: {description}'.format(
            name=self.name,
            description=self.description,
            subtype=self.subtype,
            code=self.error_code,
        )


def parse_error_parameter(parameter_str):
    match = error_regex.match(parameter_str)
    assert match is not None
    groups = match.groups()
    name = groups[0]
    subtype = groups[1]
    error_code = groups[2]
    description = groups[3]
    # like [404] &bull; Not found<br>
    if name is None:
        assert error_code is not None
        return None
    return ErrorParameter(name, description, error_code, subtype)


def parse_error_parameters(parameters_str):
    error_params = []
    for parameter_str in parameters_str.split('\n'):
        parameter_str = parameter_str.strip()
        if parameter_str == '':
            continue
        error_param = parse_error_parameter(parameter_str)
        if error_param:
            error_params.append(error_param)
    return error_params

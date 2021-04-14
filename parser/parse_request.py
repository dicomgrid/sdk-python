"""Parse request parameters."""

from enum import Enum, auto
from typing import List, NamedTuple, Optional

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from ambra_sdk.pythonize import PARAMS
import re


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
        if description:
            description = description \
                .replace('•', '') \
                .replace('  ', ' ') \
                .strip()
        self.description = description
        self.optional = optional
        self.multiliple_prefix = multiple_prefix

    def __hash__(self):
        return hash((self.name, self.parameter_type))

    def __eq__(self, rh):
        return self.name == rh.name and self.parameter_type == self.parameter_type


class RequestGroupParametersDoc:

    def __init__(self, description):
        self.description = description


def parse_params_html(bs, html):
    prev = None
    desc = []

    first_arg = True
    name = None

    for el in html.contents:
        if el.name == 'div' and el['class'] and 'comment' in el['class']:
            continue
        if prev is None:
            prev = el
        if prev == '\n' and el.name == 'i':
            # not first arg
            if first_arg is False:
                arg_name = name.strip()
                arg_desc = ''.join(
                    i.text if isinstance(i, Tag) else str(i) for i in desc
                ).strip()
                yield arg_name, arg_desc
                desc = []

            name = el.text
            first_arg = False
        else:
            desc.append(el)
        prev = el

    # print last arg
    if name is not None:
        arg_name = name.strip()
        arg_desc = ''.join(
            i.text if isinstance(i, Tag) else str(i) for i in desc
        ).strip()
        yield arg_name, arg_desc
        desc = []


single_or_re = re.compile(r'[^\|]\|[^\|]')
single_and_re = re.compile(r'[^\&]\&[^\&]')


def param_from_name_and_desc(name, desc):
    if name == 'filter.*':
        return [RequestParameter.filtrator()]
    if name == 'page.*':
        return [RequestParameter.paginator()]
    if name == 'sort_by':
        return [RequestParameter.sorter()]

    assert '--' not in desc, 'Maybe comment'
    assert 'The follwing' not in desc, 'Maybe comment'

    if '**' in name:
        assert name[-2:] == '**'
        arg_name = name[:-2]
        optional = True
        return [
            RequestParameter(
                RequestParameterType.Multiple,
                arg_name,
                desc,
                optional,
            )
        ]


    # form like customfield-{DESC}
    if any(i.isupper() for i in name):
        assert '{' in name, name
        assert '}' in name, name

    if '{' in name or '}' in name:
        assert '{' in name
        assert '}' in name

        b_index = name.index('{')
        assert b_index != 0
        assert name[b_index - 1] != ' '
        multi_prefix = name.split('{')[0]
        field_name = '{pref}param'.format(
            pref=multi_prefix.replace('-', '_'),
        )
        optional = True
        return [
            RequestParameter(
                RequestParameterType.Multiple,
                field_name,
                desc,
                optional,
                multiple_prefix=multi_prefix,
            )
        ]

    # Special form for multiparams (sid || node.... &&)
    if '(' in name or ')' in name:
        assert '(' in name
        assert ')' in name
        assert name[0] == '('
        assert name[-1] == ')'
        assert not single_or_re.findall(name)
        assert not single_and_re.findall(name)

        params = set()
        for p_str in name[1:-1].split('&&'):
            for arg_name in p_str.split('||'):
                arg_name = arg_name.strip()
                optional = True
                params.add(
                    RequestParameter(
                        RequestParameterType.Usual,
                        arg_name,
                        arg_name,
                        optional,
                    )
                )
        return list(params)

    if not desc.startswith('•'):
        raise ValueError(name + ' ' + desc)
    if 'optional' in desc:
        optional = True
    else:
        optional = False
    return [
        RequestParameter(
            RequestParameterType.Usual,
            name,
            desc,
            optional,
        )
    ]


def parse_request_parameters(bs, html):
    request_params = []
    for name, desc in parse_params_html(bs, html):
        request_params.extend(param_from_name_and_desc(name, desc))

    return request_params

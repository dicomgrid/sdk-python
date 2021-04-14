"""Parse api.

$ wget https://local.ambrahealth.dev/api/v3/api.html
"""

from pathlib import Path
from typing import List, NamedTuple, Optional, Dict, Any

from bs4 import BeautifulSoup
from bs4.element import Tag
from jinja2 import Environment, FileSystemLoader

from ambra_sdk.pythonize import METHODS
from ambra_sdk.service.query import get_query_cls_name
from parse_errors import ErrorParameter, parse_error_parameters
from parse_request import (
    RequestGroupParametersDoc,
    RequestParameter,
    RequestParameterType,
    parse_request_parameters,
)
from parse_response import ResponseParameter, parse_response_parameters

FILTER_EXCEPTIONS = [
    ErrorParameter(
        name='INVALID_FIELD',
        description=
        'The field is not valid for this object. The error_subtype will hold the filter expression this applies to',
    ),
    ErrorParameter(
        name='INVALID_CONDITION',
        description=
        'The condition is not support. The error_subtype will hold the filter expression this applies to',
    ),
    ErrorParameter(
        name='FILTER_NOT_FOUND',
        description=
        'The filter can not be found. The error_subtype will hold the filter UUID',
    ),
]

SORTING_EXCEPTIONS = [
    ErrorParameter(
        name='INVALID_SORT_FIELD',
        description=
        'The field is not valid for this object. The error_subtype will hold the field name this applies to',
    ),
    ErrorParameter(
        name='INVALID_SORT_ORDER',
        description=
        'The sort order for the field is invalid. The error_subtype will hold the field name this applies to',
    ),
]


class Api:

    def __init__(
        self,
        description: str,
        url: str,
        request_parameters: List[RequestParameter],
        response_parameters: Optional[List[ResponseParameter]],
        errors: List[ErrorParameter],
        notes,
    ):
        self.description = description
        self.url = url
        self.request_parameters = request_parameters
        self.response_parameters = response_parameters
        self.errors = errors
        self.notes = notes

        self.request_usual_params = []
        self.request_multiple_params = []
        self.request_params = []
        self.with_pagination = False
        self.paginated_field = None
        self.with_filter = False
        self.with_sorting = False
        self.sid_required = False

        self.notes = []

        for rp in self.request_parameters:
            if isinstance(rp, RequestGroupParametersDoc):
                self.notes.append(rp)
                continue
            if rp.name == 'sid':
                self.sid_required = True
                continue
            rp_type = rp.parameter_type
            if rp_type == RequestParameterType.Filter:
                self.with_filter = True
                self.errors.extend(FILTER_EXCEPTIONS)
            elif rp_type == RequestParameterType.Pagination:
                assert response_parameters is not None
                self.with_pagination = True
                response_arrays = [
                    i for i in response_parameters
                    if getattr(i, 'is_array', False) is True
                ]
                if len(response_arrays) != 1:
                    raise RuntimeError('Cant define array for pagination')
                self.paginated_field = response_arrays[0]
            elif rp_type == RequestParameterType.Sorting:
                self.with_sorting = True
                self.errors.extend(SORTING_EXCEPTIONS)
            elif rp_type == RequestParameterType.Usual:
                self.request_params.append(rp)
                self.request_usual_params.append(rp)
            elif rp_type == RequestParameterType.Multiple:
                self.request_params.append(rp)
                self.request_multiple_params.append(rp)
            else:
                raise RuntimeError('Unknown request type')

        required = [i for i in self.request_params if i.optional is False]
        optionals = [i for i in self.request_params if i.optional]
        self.request_params = sorted(required, key=lambda x: x.name)
        self.request_params.extend(sorted(optionals, key=lambda x: x.name))

        self.request_usual_params = sorted(
            self.request_usual_params,
            key=lambda x: x.name,
        )

        self.request_multiple_params = sorted(
            self.request_multiple_params,
            key=lambda x: x.pythonic_name,
        )

        self.notes = sorted(self.notes, key=lambda x: x.description)
        assert len(self.errors) == len(set(self.errors))
        self.errors = sorted(
            set(self.errors),
            key=lambda x: str(x),
        )

    @property
    def namespace(self):
        return self.url.split('/')[1].capitalize()

    @property
    def path(self):
        return self.url.split('/')[2:]

    @property
    def func_name(self):
        fname = '_'.join(self.path)
        if fname in METHODS:
            return METHODS[fname]
        return fname

    @property
    def func_head(self):
        return ' '.join(self.path).capitalize()

    @property
    def query_class_name(self) -> str:
        qcname: str = get_query_cls_name(
            with_pagination=self.with_pagination,
            with_filtering=self.with_filter,
            with_sorting=self.with_sorting,
        )
        return qcname


def parse_api(api_html_file: Path):
    with open(api_html_file) as file_d:
        soup = BeautifulSoup(file_d.read(), 'html.parser')
        namespaces: Dict[str, Any] = {}
        for table_body in soup.select('table'):

            # TODO: Use normal mech
            # Get only endpoint tables
            table_head = table_body \
                .find_previous('h3')
            if 'commands' not in table_head.text:
                continue

            rows = table_body.find_all('tr')

            description: Optional[str] = None
            url: Optional[str] = None
            request_parameters = None
            response_parameters = None
            errors = []
            notes = None
            for row in rows:
                col_name = row.find_all('th')
                col_val = row.find_all('td')

                # All elements have a form
                # <tr>
                #     <th>URL</th>
                #     <td>/session/login</td>
                # </tr>
                if len(col_val) != 1 or len(col_name) != 1:
                    raise RuntimeError(
                        '''Api.html is totaly broken. Bad table at {source_line}'''
                        .format(source_line=row.sourceline)
                    )

                col_name = col_name[0].text

                if col_name == 'Description':
                    description = col_val[0].text
                elif col_name == 'URL':
                    url = col_val[0].text
                    print('METHOD ', url)
                elif col_name == 'Parameters':
                    request_parameters = parse_request_parameters(
                        soup, col_val[0]
                    )
                elif col_name == 'Returns':
                    response_parameters = parse_response_parameters(
                        col_val[0].text
                    )
                elif col_name == 'Notes':
                    notes = col_val[0].text.split('\n')
                elif col_name == 'Errors':
                    errors = parse_error_parameters(col_val[0].text)
                elif col_name == 'Permission':
                    # TODO: parse permissions
                    pass
                else:
                    raise RuntimeError(
                        'Unknown %s at %s' % (col_name, row.sourceline)
                    )

            assert description is not None
            assert url is not None
            assert request_parameters is not None

            api = Api(
                description,
                url,
                request_parameters,
                response_parameters,
                errors,
                notes,
            )

            namespaces.setdefault(
                api.namespace,
                {
                    'apis': [],
                    'exceptions': set(),
                    'query_class_names': set()
                },
            )
            namespaces[api.namespace]['apis'].append(api)
            namespaces[api.namespace]['query_class_names'].add(
                api.query_class_name
            )
            if api.errors:
                for error in api.errors:
                    namespaces[api.namespace]['exceptions'].add(
                        error.exception_name()
                    )
        return namespaces


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Parse ambra api.html.')
    parser.add_argument('api_path', help='api.html path')
    args = parser.parse_args()
    api_path_str = args.api_path
    api_path = Path(api_path_str)
    parse_api(api_path)

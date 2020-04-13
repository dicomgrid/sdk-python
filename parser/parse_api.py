"""Parse api.

$ wget https://local.ambrahealth.dev/api/v3/api.html
"""

from pathlib import Path
from typing import List, NamedTuple, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag
from jinja2 import Environment, FileSystemLoader

from ambra_sdk.service.query import get_query_cls_name
from parse_errors import ErrorParameter, parse_error_parameters
from parse_request import (
    RequestGroupParametersDoc,
    RequestParameter,
    RequestParameterType,
    parse_request_parameters,
)
from parse_response import ResponseParameter, parse_response_parameters
from ambra_sdk.pythonize import METHODS

FILTER_EXCEPTIONS = [
    ErrorParameter(
        name='INVALID_FIELD',
        description='The field is not valid for this object. The error_subtype will hold the filter expression this applies to',
    ),
    ErrorParameter(
        name='INVALID_CONDITION',
        description='The condition is not support. The error_subtype will hold the filter expression this applies to',
    ),
    ErrorParameter(
        name='FILTER_NOT_FOUND',
        description='The filter can not be found. The error_subtype will hold the filter UUID',
    ),
]


SORTING_EXCEPTIONS = [
    ErrorParameter(
        name='INVALID_SORT_FIELD',
        description='The field is not valid for this object. The error_subtype will hold the field name this applies to',
    ),
    ErrorParameter(
        name='INVALID_SORT_ORDER',
        description='The sort order for the field is invalid. The error_subtype will hold the field name this applies to',
    ),
]

class Api:

    def __init__(
        self, description: str, url: str,
        request_parameters: List[RequestParameter],
        response_parameters: List[ResponseParameter],
        errors: List[ErrorParameter], notes: List[str]
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
                self.with_pagination = True
                response_arrays = [i for i in response_parameters if getattr(
                    i, 'is_array', False) is True]
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

        self.errors = sorted(set(self.errors), key=lambda x: x.name)

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
        return get_query_cls_name(
            with_pagination=self.with_pagination,
            with_filtering=self.with_filter,
            with_sorting=self.with_sorting,
    )


def parse_apis(path_to_file: Path):
    with open(api_html_file) as file_d:
        soup = BeautifulSoup(file_d.read(), 'html.parser')
        namespaces = {}
        for table_body in soup.select('table'):

            # Get only endpoint tables
            table_head = table_body \
                .find_previous('h3')
            if 'commands' not in table_head.text:
                continue

            rows = table_body.find_all('tr')

            description = None
            url = None
            request_parameters = None
            response_parameters = None
            errors = []
            notes = None
            for row in rows:
                col_name = row.find_all('th')
                col_val = row.find_all('td')

                if len(col_val) != 1 or len(col_name) != 1:
                    # api.html is broken...
                    # try to fix this.... ;-(
                    #
                    # Case:
                    # <td>...<td></td>
                    col_name = [i for i in col_name if i.text.strip() != '']
                    col_val = [i for i in col_val if i.text.strip() != '']

                    # Case:
                    # <tr>th>Notes</th></td></tr>
                    if len(col_val) == 0:
                        new_tag = soup.new_tag("td")
                        col_val = [new_tag]

                # check after fixes
                if len(col_val) != 1 or len(col_name) != 1:
                    raise RuntimeError(
                        '''Api.html is totaly broken. Bad table at {source_line}'''
                        .format(source_line=row.sourceline)
                    )

                col_name = col_name[0].text
                col_val = col_val[0].text

                if col_name == 'Description':
                    description = col_val
                elif col_name == 'URL':
                    url = col_val
                elif col_name == 'Parameters':
                    request_parameters = parse_request_parameters(col_val)
                elif col_name == 'Returns':
                    response_parameters = parse_response_parameters(col_val)
                elif col_name == 'Notes':
                    notes = col_val.split('\n')
                elif col_name == 'Errors':
                    errors = parse_error_parameters(col_val)

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
                {'apis': [], 'exceptions': set(), 'query_class_names': set()},
            )
            namespaces[api.namespace]['apis'].append(api)
            namespaces[api.namespace]['query_class_names'].add(api.query_class_name)
            if api.errors:
                for error in api.errors:
                    namespaces[api.namespace]['exceptions'].add(
                        error.exception_name())
        return namespaces


def generate_namespaces(
    api_namespaces,
    templates_path,
    generated_api_dir,
):
    template = Environment(
        loader=FileSystemLoader(str(templates_path)),
        autoescape=True,
    ).get_template('namespace')
    for namespace_name, namespace in api_namespaces.items():
        apis = namespace['apis']
        exceptions = namespace['exceptions']
        query_class_names = namespace['query_class_names']
        rendered_namespace = template.render(
            namespace=namespace_name,
            apis=apis,
            exceptions=sorted(exceptions),
            query_class_names=sorted(query_class_names),
            request_type=RequestParameterType,
        )
        generated_api_dir \
            .joinpath('{namespace}.py'.format(namespace=namespace_name.lower())) \
            .write_text(rendered_namespace)


def generate_user_namespaces(
    api_namespaces,
    templates_path,
    user_api_dir,
):
    init_template = Environment(
        loader=FileSystemLoader(str(templates_path)),
        autoescape=True,
    ).get_template('namespaces_init')
    namespaces = api_namespaces.keys()
    rendered_init = init_template.render(namespaces=namespaces)
    user_api_dir.joinpath('__init__.py').write_text(rendered_init)

    template = Environment(
        loader=FileSystemLoader(str(templates_path)),
        autoescape=True,
    ).get_template('user_namespace')
    for namespace in api_namespaces.keys():
        rendered_namespace = template.render(namespace=namespace)
        user_api_dir \
            .joinpath('{namespace}.py'.format(namespace=namespace.lower())) \
            .write_text(rendered_namespace)


api_html_file = Path(__file__).parent.joinpath('api.html')
generated_api_dir = Path(__file__).parents[1].joinpath(
    'ambra_sdk',
    'service',
    'entrypoints',
    'generated',
)
user_api_dir = Path(__file__).parents[1].joinpath('ambra_sdk', 'service', 'entrypoints')
templates_path = Path(__file__).parent.joinpath('templates')
api_namespaces = parse_apis(api_html_file)

generate_namespaces(api_namespaces, templates_path, generated_api_dir)

# TODO: generate only new namespaces or do it manually
# generate_user_namespaces(api_namespaces, templates_path, user_api_dir)

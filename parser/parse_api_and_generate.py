"""Parse and generate api."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from parse_api import parse_api
from parse_request import RequestParameterType


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
# api_html_file = Path('/home/dyens/dev/v3services/htdocs/api.html')
generated_api_dir = Path(__file__).parents[1].joinpath(
    'ambra_sdk',
    'service',
    'entrypoints',
    'generated',
)
user_api_dir = Path(__file__).parents[1].joinpath(
    'ambra_sdk', 'service', 'entrypoints'
)
templates_path = Path(__file__).parent.joinpath('templates')
api_namespaces = parse_api(api_html_file)

generate_namespaces(api_namespaces, templates_path, generated_api_dir)

# TODO: generate only new namespaces or do it manually
# generate_user_namespaces(api_namespaces, templates_path, user_api_dir)

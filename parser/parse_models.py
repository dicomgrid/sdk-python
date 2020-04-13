"""Parse models.

$ ssh v3s@local.ambrahealth.dev
$ psql

COPY
(
select
sc.data_type,
sc.udt_name,
sc.column_name,
pt.tablename from information_schema.COLUMNS sc
join pg_tables pt on pt.tablename = sc.TABLE_NAME
where pt.schemaname='public'
)
TO '/home/v3s/schema.csv' DELIMITER ',' CSV HEADER;

$ scp v3s@local.ambrahealth.dev:/home/v3s/schema.csv .

Dictionary html file
$ wget https://local.ambrahealth.dev/api/v3/dictionary.html
"""

from pathlib import Path
from types import MappingProxyType
from typing import List, NamedTuple, Optional

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

from ambra_sdk.pythonize import FIELDS

TYPE_MAPPING = MappingProxyType({
    'citext': 'String',
    'char': 'String',
    'text': 'String',
    'memo': 'String',  # its bytes, but for api its simple str
    'flag': 'Boolean',
    'flag_no_default': 'Boolean',
    'primary_key': 'Integer',
    'big_primary_key': 'Integer',
    'integer': 'Integer',
    'big_integer': 'Integer',
    'integer_no_default': 'Integer',
    'double': 'Float',
    'json': 'JsonB',
    'foreign_key': 'FK',
    'datetime': 'DateTime',
    'date': 'Date',
    'kv': 'DictField',
})

DEFAULT_FOREIGN_MODELS = MappingProxyType({
    'account_id': 'Account',
    'user_id': 'User',
    'created_by': 'User',
    'updated_by': 'User',
    'asked_by': 'User',
    'namespace_id': 'Namespace',
    'role_id': 'Role',
    'study_id': 'Study',
    'patient_id': 'Patient',
    'engine_id': 'Engine',
    'cluster_id': 'Cluster',
    'brand_id': 'Brand',
    'case_id': 'Case',
    'customcode_id': 'Customcode',
    'node_id': 'Node',
    'asking_node': 'Node',
    'destination_id': 'Destination',
    'hl7_id': 'Hl7',
    'phi_namespace': 'Namespace',
    'storage_namespace': 'Namespace',
    'dictionary_id': 'Dictionary',
    'filter_id': 'Filter',
    'group_id': 'Group',
    'location_id': 'Location',
    'link_id': 'Link',
    'meeting_id': 'Meeting',
    'accelerator_id': 'Accelerator',
    'from_account_id': 'Account',
    'to_account_id': 'Account',
    'order_id': 'Order',
    'route_id': 'Route',
    'rsnaclr_subset_id': 'RsnaclrSubset',
    'rsync_id': 'Rsync',
    'deleted_by': 'User',
    'shared_from': 'StudyShare',
    'hl7_template_hl7_id': 'Hl7Template',
    'hl7_template_id': 'Hl7Template',
    'study_push_id': 'StudyPush',
    'new_study_id': 'Study',
    'from_study_id': 'Study',
    'sid_user_id': 'User',
    'webhook_id': 'Webhook',
})

FOREIGN_MODELS = MappingProxyType({
    'AccountCanShare': {
        'by_account_id': 'Account',
        'by_group_id': 'Group',
        'by_location_id': 'Location',
        'by_user_id': 'User',
        'with_account_id': 'Account',
        'with_group_id': 'Group',
        'with_location_id': 'Location',
        'with_user_id': 'User',
    },
    'ArchiveStudy': {
        'archive_vault_id': 'Archive',
    },
    'ArchiveStudyAws': {
        'archive_study_id': 'Archive',
    },
    'Audit': {
        'parent_id': 'SelfField',
        'proxy_id': 'User',
    },
    'Case': {
        'assigned_admin_id': 'User',
        'assigned_medical_id': 'User',
        'study_charge_id': 'Unknown',
    },
    'Cluster': {
        'archive_cluster_id': 'Archive',
        'backup_cluster_id': 'Archive',
    },
    'DestinationSearch': {
        'copy_to': 'Namespace',
        'push_to': 'Destination',
    },
    'NamespaceChildren': {
        'child_id': 'SelfField',
    },
    'TagObject': {
        'object_id': 'Unknown',
    },
    'Message': {
        'parent_id': 'Message',
    },
})


class Field(NamedTuple):
    """Field."""

    name: str
    field_type: str
    foreign_model: Optional[str]
    description: str

    @property
    def ambra_type(self) -> str:
        """Ambra field type str.

        :return: ambra type string
        """
        return TYPE_MAPPING[self.field_type]


class Model(NamedTuple):
    """Model."""

    name: str
    fields: List[Field]

    def ambra_fields(self):
        """Ambra fields.

        :yields: Field[name, field_abmbra_type, description]
        """
        for field in self.fields:
            if field.ambra_type == 'FK':
                # ID key
                yield Field(
                    field.name,
                    'Integer',
                    None,
                    'FK. {description}'.format(description=field.description),
                )
                f_model = self.foreign_model(field)
                if f_model == 'Unknown':
                    continue
                # Foreign field
                if '_id' in field.name:
                    f_name = field.name.replace('_id', '')
                else:
                    f_name = '{field_name}_obj'.format(field_name=field.name)
                yield Field(
                    f_name,
                    field.ambra_type,
                    f_model,
                    field.description,
                )
            else:
                yield Field(
                    field.name,
                    field.ambra_type,
                    None,
                    field.description,
                )

    def foreign_model(self, field: Field) -> str:
        """Foreign model for FK field.

        :param field: pg field
        :return: Foreign model name
        :raises KeyError: Unknown foreign model
        """
        assert field.ambra_type == 'FK'  # NOQA
        is_special = True
        try:
            return FOREIGN_MODELS[self.name][field.name]
        except KeyError:
            is_special = False
        if is_special is False:
            try:
                return DEFAULT_FOREIGN_MODELS[field.name]
            except KeyError:
                raise KeyError(
                    '{model_name}.{field_name}'.format(
                        model_name=self.name,
                        field_name=field.name,
                    ),
                )

    def depends_on(self) -> List[str]:
        deps = []
        for field in self.fields:
            if field.ambra_type == 'FK':
                deps.append(self.foreign_model(field))
        return deps


def camel_case(word: str) -> str:
    """To camel case.

    :param word: input word
    :return: camelcased word
    """
    return ''.join(word_p.capitalize() or '_' for word_p in word.split('_'))


def parse_models(path_to_file: Path) -> List[Model]:
    """Parse models from dictionary.html.

    Get dictionary
    wget https://local.ambrahealth.dev/api/v3/dictionary.html

    :param path_to_file: filename for parsing
    :return: models
    """
    with open(path_to_file) as file_d:
        soup = BeautifulSoup(file_d.read(), 'html.parser')
        models = []
        for table_body in soup.select('table'):
            table_name = table_body \
                .previous_element \
                .previous_element \
                .previous_element \
                .previous_element \
                .previous_element
            table_name = camel_case(table_name['name'])
            fields = []
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                if not cols:
                    continue  # its th: header
                # Get rid of empty values
                field_name = cols[0]
                field_name = FIELDS.get(field_name, field_name)
                field_type = cols[1]
                foreign_model = None
                description = cols[2]
                fields.append(
                    Field(
                        field_name,
                        field_type,
                        foreign_model,
                        description,
                    ),
                )
            models.append(Model(table_name, fields))
        return models

def generate_models(
    models_path: Path,
    templates_path: Path,
    models: List[Model],
):
    """Generate models file.

    :param models_path: path to models file
    :param templates_path: path to templates dir
    :param models: models for store
    """
    template = Environment(
        loader=FileSystemLoader(str(templates_path)),
        autoescape=True,
    ).get_template('models')
    rendered_model = template.render(models=models)
    with open(models_path, 'w') as file_d:
        file_d.write(rendered_model)


dictionary_html_file = Path(__file__).parent.joinpath('dictionary.html')
models_file = Path(__file__) \
    .parents[1] \
    .joinpath('ambra_sdk', 'models', 'generated.py')
templates_path = Path(__file__).parent.joinpath('templates')

models = parse_models(dictionary_html_file)

generate_models(models_file, templates_path, models)

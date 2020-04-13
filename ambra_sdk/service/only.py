"""Only fields."""

import json
from typing import Dict, List, Union

from ambra_sdk.models.base import FieldDescriptor

OnlyField = Union[
    str,
    Dict[str, List[str]],
    FieldDescriptor,
]

OnlyFields = Union[
    OnlyField,
    List[OnlyField],
]


class WithOnly:
    """With only fields mixin."""

    _request_data: Dict

    def only_top_field(self, field: str):
        """Request only one top field.

        :param field: top field name
        :return: self object
        """
        top_fields = self._request_data.get('fields._top')
        if top_fields:
            top_fields = json.loads(top_fields)
            top_fields.append(field)
        else:
            top_fields = [field]
        self._request_data['fields._top'] = json.dumps(top_fields)
        return self

    def only_top_fields(self, fields: List[str]):
        """Request only some fields on top level.

        :param fields: list of top fields
        :return: self object
        """
        top_fields = self._request_data.get('fields._top')
        if top_fields:
            top_fields = json.loads(top_fields)
            top_fields.extend(fields)
        else:
            top_fields = fields
        self._request_data['fields._top'] = json.dumps(top_fields)
        return self

    def only_struct_fields(self, fields: Dict[str, List[str]]):
        """Request only some fields of structs.

        :param fields: dict of struct fields.
                       Name of struct: list of fields
        :return: self object
        """
        for struct_name, struct_fields in fields.items():
            struct_name = 'fields.{struct_name}'.format(
                struct_name=struct_name,
            )
            struct_fields_list = self._request_data.get(struct_name)
            if struct_fields_list:
                struct_fields_list = json.loads(struct_fields_list)
                struct_fields_list.extend(struct_fields)
            else:
                struct_fields_list = struct_fields
            struct_fields_list = sorted(set(struct_fields_list))
            self._request_data[struct_name] = json.dumps(struct_fields_list)
        return self

    def only(self, fields: OnlyFields):  # NOQA:WPS231
        """Request only fields.

        :Example:

        >>> Api.Namespace.method.only('field1')
        >>> Api.Namespace.method.only(['field1', 'field2'])
        >>> Api.Namespace.method.only({'some_struct': ['field1', 'field2']})
        >>> Api.Namespace.method.only(
                [
                    {'some_struct1': ['field11', 'field12']},
                    {'some_struct2': ['field21', 'field22']},
                    'top_field1',
                    'top_field2',
                ]
            )
        >>> Api.Namespace.method.only(Model.field) # Create structed field
        >>> Api.Namespace.method.only(['field1', Model.field])
        >>> Api.Namespace.method.only(
                [
                    Model.field,
                    Model.field2
                    {'some_struct3': ['field31', 'field32']},
                    'top_field2',
                ]
            )

        :param fields: Some of the OnlyFields variant
        :return: self object

        :raises ValueError: Unknown field type
        """
        if isinstance(fields, list):
            fields_list: List[OnlyField] = fields
        else:
            fields_list = [fields]

        top_fields = []
        struct_fields: Dict[str, List[str]] = {}
        for field in fields_list:
            if isinstance(field, str):
                top_fields.append(field)
            elif isinstance(field, FieldDescriptor):
                struct_dict = field.get_only()
                struct_fields = self._add_struct(struct_fields, struct_dict)
            elif isinstance(field, dict):
                struct_fields = self._add_struct(struct_fields, fields)
            else:
                raise ValueError

        if top_fields:
            self.only_top_fields(top_fields)

        if struct_fields:
            self.only_struct_fields(struct_fields)

        return self

    def _add_struct(self, base_dict, new_dict):
        for struct_name, new_fields in new_dict.items():
            fields = base_dict.get(struct_name, [])
            fields.extend(new_fields)
            base_dict[struct_name] = sorted(set(fields))
        return base_dict

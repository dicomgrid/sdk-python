"""Base model and field."""

import json
from abc import ABC, abstractmethod
from collections.abc import Iterable
from copy import copy
from functools import partial
from importlib import import_module
from typing import Any, Dict, List, Optional, Type

from ambra_sdk.service.filtering import Filter, FilterCondition
from ambra_sdk.service.sorting import Sorter, SortingOrder


class BaseField(ABC):
    """Base Field."""

    _python_type: Optional[Type[Any]] = None

    def __init__(self, description):
        """Init.

        :param description: field description
        """
        self._description = description

    @abstractmethod
    def validate(self, value):
        """Validate value.

        :param value: value for validation
        """

    def _get_descriptor(self):
        return FieldDescriptor(
            field=self,
        )


class WithSorting:
    """With sorting field mixin."""

    _name: str
    _full_name: str

    def desc(self, full_name=False) -> Sorter:
        """Desc sorting.

        :param full_name: use full name
        :returns: sorter
        """
        field_name = self._full_name if full_name is True else self._name
        return Sorter(
            field_name=field_name,
            order=SortingOrder.descending,
        )

    def asc(self, full_name=False) -> Sorter:
        """Asc sorting.

        :param full_name: use full name
        :returns: sorter
        """
        field_name = self._full_name if full_name is True else self._name
        return Sorter(
            field_name=field_name,
            order=SortingOrder.ascending,
        )


class WithFiltering:  # NOQA:WPS214
    """With filtering field mixin."""

    _name: str
    _full_name: str
    _field: BaseField

    def like(self, value, full_name=True):
        """Get like filter.

        :param value: filtering value
        :param full_name: use full name for filtering
        :raises ValueError: value is not string
        :return: Filter
        """
        if self._field._python_type != str:
            raise ValueError('Use like for not string field')
        # check value type
        str(value)
        field_name = self._full_name if full_name is True else self._name
        return Filter(
            field_name=field_name,
            condition=FilterCondition.like,
            value=value,
        )

    def __getattr__(self, attribute):
        """Get attr.

        Redefined for automatic pick filter.

        :param attribute: attr
        :return: filtering function

        :raises AttributeError: Unknown attribute
        """
        conditions = FilterCondition.__members__  # NOQA:WPS609
        standart_filters = {
            'equals',
            'equals_or_null',
            'not_equals',
            'not_equals_or_null',
            'gt',
            'ge',
            'lt',
            'le',
        }
        filters_with_seq = {
            'in_condition',
            'in_or_null',
        }
        condition = conditions.get(attribute)
        if condition is None:
            raise AttributeError
        if attribute in standart_filters:
            return partial(self._standart_filter, condition=condition)
        elif attribute in filters_with_seq:
            return partial(self._filter_with_seq, condition=condition)
        raise AttributeError

    def __eq__(self, value):  # NOQA:D105
        return self.equals(value)

    def __ne__(self, value):  # NOQA:D105
        return self.not_equals(value)

    def __gt__(self, value):  # NOQA:D105
        return self.gt(value)

    def __ge__(self, value):  # NOQA:D105
        return self.ge(value)

    def __lt__(self, value):  # NOQA:D105
        return self.lt(value)

    def __le__(self, value):  # NOQA:D105
        return self.le(value)

    def _standart_filter(
        self,
        value,
        condition,
        full_name=False,
    ):
        value = self._field.validate(value)
        field_name = self._full_name if full_name is True else self._name
        return Filter(
            field_name=field_name,
            condition=condition,
            value=value,
        )

    def _filter_with_seq(self, values, condition, full_name=False):
        # check value type
        if not isinstance(values, Iterable):
            raise ValueError('Value is not iterable')
        field_name = self._full_name if full_name is True else self._name
        return Filter(
            field_name=field_name,
            condition=condition,
            value=json.dumps(values),
        )


class WithOnly:
    """With only field mixin."""

    _name: str
    _lower_parent_name: str

    def get_only(self) -> Dict[str, List[str]]:
        """Get dict for only method.

        :return: only dict
        """
        return {
            self._lower_parent_name: [self._name],
        }


class FieldDescriptor(  # NOQA:WPS214
    WithSorting,
    WithFiltering,
    WithOnly,
):
    """Field descriptor."""

    def __init__(self, field):
        """Init.

        :param field: field
        """
        self._field = field

        # This is init in model __new__
        self._parent = None
        self._name = None

        self.__doc__ = '{field_type}({description})'.format(
            field_type=field.__class__.__name__,
            description=field._description,
        )

    def parents(self):
        """Get parents.

        :return: List of parent
        """
        parent_list = []
        parent = self._parent
        while True:
            if parent is not None:
                parent_list.append(parent)
            else:
                break
            parent = parent._parent
        return parent_list

    def __get__(self, instance, owner):
        """Get from instance.

        :param instance: object
        :param owner: owner

        :return: field descriptor or field value (if instance exist)
        """
        if instance is None:
            return self
        return instance.__dict__[self.name]  # NOQA:WPS609

    def __set__(self, instance, value):
        """Set to instance.

        :param instance: instance
        :param value: value
        """
        if value is not None:
            value = self._field.validate(value)
        instance.__dict__[self.name] = value  # NOQA:WPS609

    def __set_name__(self, owner, name):
        """Set name.

        :param owner: owner
        :param name: name
        """
        self.name = name

    @property
    def _full_name(self):
        parents = self.parents()
        path = '.'.join(reversed([parent._name for parent in parents]))
        return '{path}.{name}'.format(path=path, name=self._name)

    @property
    def _parent_name(self):
        return self._parent._name

    @property
    def _lower_parent_name(self):
        return self._parent_name.lower()


class ModelDescriptor:
    """Model descriptor."""

    def __init__(self, model_name, field_name):
        """Init.

        :param model_name: model name
        :param field_name: filed name of this descriptor
        """
        self._model_name = model_name
        self._field_name = field_name

        self._from_model = None
        self._model = None

        self._parent = None

    @property
    def from_model(self):
        """Get base model for this descriptor.

        Lazy import model from models.generated.

        :return: from model
        """
        if self._from_model is None:
            generated_models = import_module('ambra_sdk.models.generated')
            self._from_model = getattr(generated_models, self._model_name)

        return self._from_model

    @property
    def model(self):
        """Get model for this descriptor.

        Lazy create new model type

        :return: model
        """
        if self._model is None:
            new_model = type(
                self.from_model.__name__,  # NOQA:WPS609
                self.from_model.__bases__,  # NOQA:WPS609
                dict(self.from_model.__dict__),  # NOQA:WPS609
            )
            new_model._name = self._field_name
            new_model._parent = self._parent
            self._model = new_model
        return self._model

    def __get__(self, instance, owner):
        """Get from instance.

        :param instance: object
        :param owner: owner

        :return: model or field value (if instance exist)
        """
        if instance is None:
            return self.model
        return instance.__dict__[self.name]  # NOQA:WPS609

    def __set__(self, instance, value):
        """Set to instance.

        :param instance: instance
        :param value: value

        :raises ValueError: Wronk type of value
        """
        if value is not None \
           and not isinstance(value, self.from_model):
            raise ValueError
        instance.__dict__[self.name] = value  # NOQA:WPS609

    def __set_name__(self, owner, name):
        """Set name.

        :param owner: owner
        :param name: name
        """
        self.name = name


class FK(BaseField):
    """Foreign key field."""

    def __init__(self, model, *args, **kwargs):
        """Init.

        :param model: Foreign model
        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(*args, **kwargs)
        self.model = model

    def validate(self, value):
        """Validate.

        :param value: value
        :raises RuntimeError: Dont use validate for this type of fields
        """
        raise RuntimeError('FK validated in descriptor')


class BaseMetaModel(type):
    """Ambra base meta model."""

    def __new__(cls, name, bases, attrs):  # NOQA:D102
        children = []
        for attr_name, attr in attrs.items():
            if isinstance(attr, FK):
                # Need copy class for set parent
                model_descriptor = ModelDescriptor(
                    model_name=attr.model,
                    field_name=attr_name,
                )
                attrs[attr_name] = model_descriptor
                children.append(model_descriptor)
            elif isinstance(attr, FieldDescriptor):
                # Need copy descriptor for set parent
                descriptor = copy(attr)
                attrs[attr_name] = descriptor
                children.append(descriptor)
            elif isinstance(attr, BaseField):
                descriptor = attr._get_descriptor()
                descriptor._name = attr_name
                attrs[attr_name] = descriptor
                children.append(descriptor)
        attrs['_name'] = name
        instance = super().__new__(cls, name, bases, attrs)
        for child in children:
            child._parent = instance
        return instance


class BaseModel(metaclass=BaseMetaModel):
    """Ambra base model."""

    _parent = None

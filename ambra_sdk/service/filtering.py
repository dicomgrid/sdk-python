"""Filtering."""

from enum import Enum
from typing import Dict, List, NamedTuple, Union


class FilterCondition(Enum):
    """Filter conditions."""

    equals = 'equals'
    equals_or_null = 'equals_or_null'
    not_equals = 'not_equals'
    not_equals_or_null = 'not_equals_or_null'
    like = 'like'
    gt = 'gt'
    ge = 'ge'
    lt = 'lt'
    le = 'le'
    in_condition = 'in'
    in_or_null = 'in_or_null'


class Filter(NamedTuple):
    """Filter rule."""

    field_name: str
    condition: FilterCondition
    value: Union[str, List[str]]  # NOQA:WPS110


class WithFilter:
    """With Filter mixin."""

    _request_data: Dict

    def filter_by(self, filter_obj: Filter):
        """Filter by filter.

        :param filter_obj: filter object
        :return: Self object
        """
        self._request_data['filter.{filter_name}.{filter_condition}'.format(
            filter_name=filter_obj.field_name,
            filter_condition=filter_obj.condition.value,
        )] = filter_obj.value
        return self

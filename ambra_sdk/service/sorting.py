"""Sorting."""

from enum import Enum
from typing import Dict, NamedTuple


class SortingOrder(Enum):
    """Sorting orders."""

    ascending = 'asc'
    descending = 'desc'


class Sorter(NamedTuple):
    """Sorter."""

    field_name: str
    order: SortingOrder = SortingOrder.ascending

    def __str__(self):
        """Get string represenation.

        :return: string repr
        """
        return '{field_name}-{order}'.format(
            field_name=self.field_name,
            order=self.order.value,
        )


class WithSorting:
    """With sorting mixin."""

    request_data: Dict

    def sort_by(self, sorter_obj: Sorter):
        """Sort by sorter.

        :param sorter_obj: sorter object
        :return: self object
        """
        sort_by = self.request_data.get('sort_by')
        if sort_by is None:
            sort_by = str(sorter_obj)
        else:
            sort_by = '{sort_by},{new_field}'.format(
                sort_by=sort_by,
                new_field=str(sorter_obj),
            )
        self.request_data['sort_by'] = sort_by
        return self

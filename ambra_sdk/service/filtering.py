"""Filtering."""

from datetime import datetime
from enum import Enum
from typing import Any, Generic, List, NamedTuple, TypeVar, Union

from ambra_sdk.request_args import (
    AioHTTPRequestArgs,
    RequestArgs,
    cast_argument,
)

REQUEST_ARGS_TYPE = TypeVar(
    'REQUEST_ARGS_TYPE',
    RequestArgs,
    AioHTTPRequestArgs,
)


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
    value: Union[datetime, str, List[str]]  # NOQA:WPS110


class WithFilter(Generic[REQUEST_ARGS_TYPE]):
    """With Filter mixin."""

    request_args: REQUEST_ARGS_TYPE

    def filter_by(self, filter_obj: Filter):
        """Filter by filter.

        :raise ValueError: timezones with one request
        :param filter_obj: filter obejct
        :return: Self object
        """
        if isinstance(filter_obj.value, datetime):
            self._add_dt_filter(filter_obj)
        else:
            self._add_filter(
                field_name=filter_obj.field_name,
                filter_condition=filter_obj.condition,
                value=filter_obj.value,
            )
        return self

    def _add_dt_filter(self, filter_obj: Filter):
        # 3.20.8.0 v3s does not work with microseconds
        # This is fixed in 3.21.1.0

        # A timezone offset in numeric format can be passed in the
        # filter.tz and will be applied to any dates in the
        # filter e.g. filter.tz=-4:00

        # A timezone name from Olson database can be passed in
        # the filter.tz. Deprecated timezones will apply as UTC.

        # Supported date and datetime formats are:
        # YYYY-MM-DD, YYYYMMDD, YYYY-MM-DD hh:mm:ss[.uuuuuu][(+|-)ZZ[:ZZ]].

        # Timezone offsets are ignored. Server-side timestamps are
        # truncated to seconds before comparison when a filter
        # lacks microseconds part.

        # Timezones apply in this order: current user's time
        # zone, filter.tz parameter, UTC by default.
        assert isinstance(filter_obj.value, datetime)  # NOQA:S101
        value = filter_obj.value  # NOQA:WPS110
        if value.tzinfo is not None:
            timezone_key = 'filter.tz'

            utcoffset = value.tzinfo.utcoffset(value)
            if utcoffset is None:
                raise ValueError('Unknown offset')
            # Maybe we can use tzinfo.zone or tzinfo.tzname(dt) if we have..
            mm, ss = divmod(utcoffset.total_seconds(), 60)
            hh, mm = divmod(mm, 60)

            if abs(hh) > 24:
                raise ValueError('Wrong timezone')

            offset_str = '{hh:+03}:{mm:02}'.format(hh=int(hh), mm=int(mm))
            request_data = self.request_args.data or {}
            filter_tz = request_data.get(timezone_key, None)
            if filter_tz is not None and offset_str != filter_tz:
                raise ValueError(
                    'Use one timezone for all datetimes in requtest',
                )
            request_data[timezone_key] = offset_str
            value = filter_obj.value.replace(tzinfo=None)  # NOQA:WPS110
            self.request_args.data = request_data  # NOQA:WPS110

        self._add_filter(
            field_name=filter_obj.field_name,
            filter_condition=filter_obj.condition,
            value=value,
        )

    def _add_filter(
        self,
        field_name: str,
        filter_condition: FilterCondition,
        value: Any,  # NOQA:WPS110
    ):
        request_data = self.request_args.data or {}
        request_data['filter.{filter_name}.{filter_condition}'.format(
            filter_name=field_name,
            filter_condition=filter_condition.value,
        )] = cast_argument(value)
        self.request_args.data = request_data  # NOQA:WPS110

from datetime import datetime

import pytest
import pytz

from ambra_sdk.request_args import RequestArgs
from ambra_sdk.service.filtering import Filter, FilterCondition, WithFilter


class TestWithFilter:
    """Test WithOnly mixin."""

    @pytest.fixture
    def query(self):
        """Query fixture."""

        class QueryO(WithFilter):  # NOQA WPS431

            def __init__(self):
                self.request_args = RequestArgs(
                    method='POST',
                    url='/some/url',
                )

        return QueryO()

    def test_filter_by_string_value(self, query):
        """Test filter by string value."""
        value = 'value'
        query.filter_by(Filter('field', FilterCondition.equals, value))
        assert 'filter.field.equals' in query.request_args.data
        assert query.request_args.data['filter.field.equals'] == 'value'

    def test_filter_by_dt_with_fixed_timezone_offset(self, query):
        """Test filter by dt with fixed timezone offset.

        utcoffset = timedelta
        tzname = None
        zone = None
        """
        fixed_offset_timezone = pytz.FixedOffset(60 * 3)
        value = datetime(2000, 1, 2, 3, 4, 5, tzinfo=fixed_offset_timezone)
        assert str(value) == '2000-01-02 03:04:05+03:00'
        query.filter_by(Filter('field', FilterCondition.equals, value))
        assert 'filter.field.equals' in query.request_args.data
        assert query.request_args.data['filter.field.equals'] == str(
            value.replace(
                tzinfo=None,
            ),
        )

        assert 'filter.tz' in query.request_args.data
        assert query.request_args.data['filter.tz'] == '+03:00'

    def test_filter_by_dt_with_fixed_timezone_negative_offset(self, query):
        """Test filter by dt with fixed timezone negative offset.

        utcoffset = timedelta
        tzname = None
        zone = None
        """
        fixed_offset_timezone = pytz.FixedOffset(-60 * 3)
        value = datetime(2000, 1, 2, 3, 4, 5, tzinfo=fixed_offset_timezone)
        assert str(value) == '2000-01-02 03:04:05-03:00'
        query.filter_by(Filter('field', FilterCondition.equals, value))
        assert 'filter.field.equals' in query.request_args.data
        assert query.request_args.data['filter.field.equals'] == str(
            value.replace(
                tzinfo=None,
            ),
        )
        assert 'filter.tz' in query.request_args.data
        assert query.request_args.data['filter.tz'] == '-03:00'

    def test_filter_by_dt_with_offset_from_str(self, query):
        """Test filter by dt with offset from str.

        utcoffset = timedelta
        tzname = UTC+03:00
        not zone
        """
        value = datetime.strptime(
            '2000-01-02 03:04:05+03:00', '%Y-%m-%d %H:%M:%S%z',
        )
        query.filter_by(Filter('field', FilterCondition.equals, value))
        assert 'filter.field.equals' in query.request_args.data
        assert query.request_args.data['filter.field.equals'] == str(
            value.replace(
                tzinfo=None,
            ),
        )
        assert 'filter.tz' in query.request_args.data
        assert query.request_args.data['filter.tz'] == '+03:00'

    def test_filter_by_dt_with_timezone(self, query):
        """Test filter by dt with offset from str.

        utcoffset = timedelta
        tzname = LMT
        zone = Europe/Moscow
        timezone have tzname, utcoffset, but not zone
        """
        mtz = pytz.timezone('Europe/Moscow')
        # Not value datetime(..., tzinfo=mtz)
        # https://stackoverflow.com/questions/1379740/pytz-localize-vs-datetime-replace
        value = mtz.localize(datetime(2020, 1, 2, 3, 4, 5))
        query.filter_by(Filter('field', FilterCondition.equals, value))
        assert 'filter.field.equals' in query.request_args.data
        assert query.request_args.data['filter.field.equals'] == str(
            value.replace(
                tzinfo=None,
            ),
        )
        assert 'filter.tz' in query.request_args.data
        assert query.request_args.data['filter.tz'] == '+03:00'

    def test_filter_with_different_timezones(self, query):
        """Test filter with different timezones."""
        mtz = pytz.timezone('Europe/Moscow')
        value = mtz.localize(datetime(2020, 1, 2, 3, 4, 5))
        query.filter_by(Filter('field', FilterCondition.equals, value))

        with pytest.raises(ValueError) as exc_info:
            mtz = pytz.timezone('America/Los_Angeles')
            value = mtz.localize(datetime(2020, 1, 2, 3, 4, 5))
            query.filter_by(Filter('field', FilterCondition.equals, value))
        assert str(
            exc_info.value,
        ) == 'Use one timezone for all datetimes in requtest'

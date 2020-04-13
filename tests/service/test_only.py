
import pytest

from ambra_sdk.service.only import WithOnly


class TestWithOnly:
    """Test WithOnly mixin."""

    @pytest.fixture
    def query(self):
        """Query fixture."""
        class QueryO(WithOnly):  # NOQA WPS431
            def __init__(self):
                self._request_data = {}

        return QueryO()

    def test__top_field(self, query):
        """Test only top field."""
        query.only('f1')
        assert query._request_data['fields._top'] == '["f1"]'
        query.only('f2')
        assert query._request_data['fields._top'] == \
            '["f1", "f2"]'

    def test_only_top_fields(self, query):
        """Test only top fields."""
        query.only(['f1', 'f2'])
        assert query._request_data['fields._top'] == '["f1", "f2"]'
        query.only(['f3'])
        assert query._request_data['fields._top'] == '["f1", "f2", "f3"]'

    def test_only_struct_fields(self, query):
        """Test struct fields."""
        query.only({'study': ['f1', 'f2']})
        assert query._request_data['fields.study'] == '["f1", "f2"]'
        query.only({'study': ['f1', 'f3']})
        assert query._request_data['fields.study'] == '["f1", "f2", "f3"]'

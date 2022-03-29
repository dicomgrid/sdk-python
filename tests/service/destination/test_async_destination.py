import pytest


@pytest.mark.asyncio
class TestAsyncDestination:
    """Test Destination."""

    def test_search(self, async_api):
        """Test destination search."""
        request = async_api.Destination.search(
            'non_existing_uuid',
            customfield_quoted_param={
                "customfield name with ' \n \\ escaped symbols": 'customfield value',  # NOQA:WPS342
            },
        )
        assert "customfield-'customfield name with \\' \n \\\\ escaped symbols'" in request.request_data  # NOQA:WPS342

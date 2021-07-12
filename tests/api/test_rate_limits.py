"""Test rate limits."""

from ambra_sdk.api.base_api import RateLimit, RateLimits


class TestRateLimits:
    """Test rate limits."""

    def test_default_call_period(self):
        """Test default call period."""
        rls = RateLimits(
            default=RateLimit(3, 2),
            get_limit=None,
            special=None,
        )
        assert rls.call_period('abc') == 2 / 3

    def test_get_call_period(self):
        """Test get call period."""
        rls = RateLimits(
            default=RateLimit(3, 2),
            get_limit=RateLimit(4, 2),
            special=None,
        )
        assert rls.call_period('abc') == 2 / 3
        assert rls.call_period('abc/get') == 2 / 4

    def test_special_call_period(self):
        """Test special call period."""
        rls = RateLimits(
            default=RateLimit(3, 2),
            get_limit=RateLimit(4, 2),
            special={'special': RateLimit(5, 2)},
        )
        assert rls.call_period('abc') == 2 / 3
        assert rls.call_period('abc/get') == 2 / 4
        assert rls.call_period('special') == 2 / 5

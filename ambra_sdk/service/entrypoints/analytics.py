from ambra_sdk.service.entrypoints.generated.analytics import \
    Analytics as GAnalytics
from ambra_sdk.service.entrypoints.generated.analytics import \
    AsyncAnalytics as GAsyncAnalytics


class Analytics(GAnalytics):
    """Analytics."""


class AsyncAnalytics(GAsyncAnalytics):
    """AsyncAnalytics."""

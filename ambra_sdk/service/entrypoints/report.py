from ambra_sdk.service.entrypoints.generated.report import \
    AsyncReport as GAsyncReport
from ambra_sdk.service.entrypoints.generated.report import Report as GReport


class Report(GReport):
    """Report."""


class AsyncReport(GAsyncReport):
    """AsyncReport."""

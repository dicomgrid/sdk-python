from ambra_sdk.service.entrypoints.generated.dicomdata import \
    AsyncDicomdata as GAsyncDicomdata
from ambra_sdk.service.entrypoints.generated.dicomdata import \
    Dicomdata as GDicomdata


class Dicomdata(GDicomdata):
    """Dicomdata."""


class AsyncDicomdata(GAsyncDicomdata):
    """AsyncDicomdata."""

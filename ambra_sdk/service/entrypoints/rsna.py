from ambra_sdk.service.entrypoints.generated.rsna import \
    AsyncRsna as GAsyncRsna
from ambra_sdk.service.entrypoints.generated.rsna import Rsna as GRsna


class Rsna(GRsna):
    """Rsna."""


class AsyncRsna(GAsyncRsna):
    """AsyncRsna."""

from ambra_sdk.service.entrypoints.generated.qctask import \
    AsyncQctask as GAsyncQctask
from ambra_sdk.service.entrypoints.generated.qctask import Qctask as GQctask


class Qctask(GQctask):
    """Qctask."""


class AsyncQctask(GAsyncQctask):
    """AsyncQctask."""

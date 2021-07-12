from ambra_sdk.service.entrypoints.generated.purge import \
    AsyncPurge as GAsyncPurge
from ambra_sdk.service.entrypoints.generated.purge import Purge as GPurge


class Purge(GPurge):
    """Purge."""


class AsyncPurge(GAsyncPurge):
    """AsyncPurge."""

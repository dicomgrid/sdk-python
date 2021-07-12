from ambra_sdk.service.entrypoints.generated.destination import \
    AsyncDestination as GAsyncDestination
from ambra_sdk.service.entrypoints.generated.destination import \
    Destination as GDestination


class Destination(GDestination):
    """Destination."""


class AsyncDestination(GAsyncDestination):
    """AsyncDestination."""

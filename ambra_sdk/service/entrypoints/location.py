from ambra_sdk.service.entrypoints.generated.location import \
    AsyncLocation as GAsyncLocation
from ambra_sdk.service.entrypoints.generated.location import \
    Location as GLocation


class Location(GLocation):
    """Location."""


class AsyncLocation(GAsyncLocation):
    """AsyncLocation."""

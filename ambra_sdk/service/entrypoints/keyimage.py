from ambra_sdk.service.entrypoints.generated.keyimage import \
    AsyncKeyimage as GAsyncKeyimage
from ambra_sdk.service.entrypoints.generated.keyimage import \
    Keyimage as GKeyimage


class Keyimage(GKeyimage):
    """Keyimage."""


class AsyncKeyimage(GAsyncKeyimage):
    """AsyncKeyimage."""

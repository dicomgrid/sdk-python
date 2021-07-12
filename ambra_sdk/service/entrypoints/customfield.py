from ambra_sdk.service.entrypoints.generated.customfield import \
    AsyncCustomfield as GAsyncCustomfield
from ambra_sdk.service.entrypoints.generated.customfield import \
    Customfield as GCustomfield


class Customfield(GCustomfield):
    """Customfield."""


class AsyncCustomfield(GAsyncCustomfield):
    """AsyncCustomfield."""

from ambra_sdk.service.entrypoints.generated.namespace import \
    AsyncNamespace as GAsyncNamespace
from ambra_sdk.service.entrypoints.generated.namespace import \
    Namespace as GNamespace


class Namespace(GNamespace):
    """Namespace."""


class AsyncNamespace(GAsyncNamespace):
    """AsyncNamespace."""

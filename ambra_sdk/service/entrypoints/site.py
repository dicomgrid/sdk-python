from ambra_sdk.service.entrypoints.generated.site import \
    AsyncSite as GAsyncSite
from ambra_sdk.service.entrypoints.generated.site import Site as GSite


class Site(GSite):
    """Site."""


class AsyncSite(GAsyncSite):
    """AsyncSite."""

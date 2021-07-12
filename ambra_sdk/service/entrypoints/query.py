from ambra_sdk.service.entrypoints.generated.query import \
    AsyncQuery as GAsyncQuery
from ambra_sdk.service.entrypoints.generated.query import Query as GQuery


class Query(GQuery):
    """Query."""


class AsyncQuery(GAsyncQuery):
    """AsyncQuery."""

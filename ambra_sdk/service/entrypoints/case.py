from ambra_sdk.service.entrypoints.generated.case import \
    AsyncCase as GAsyncCase
from ambra_sdk.service.entrypoints.generated.case import Case as GCase


class Case(GCase):
    """Case."""


class AsyncCase(GAsyncCase):
    """AsyncCase."""

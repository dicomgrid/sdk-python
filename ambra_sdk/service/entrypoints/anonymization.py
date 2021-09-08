from ambra_sdk.service.entrypoints.generated.anonymization import \
    Anonymization as GAnonymization
from ambra_sdk.service.entrypoints.generated.anonymization import \
    AsyncAnonymization as GAsyncAnonymization


class Anonymization(GAnonymization):
    """Anonymization."""


class AsyncAnonymization(GAsyncAnonymization):
    """AsyncAnonymization."""

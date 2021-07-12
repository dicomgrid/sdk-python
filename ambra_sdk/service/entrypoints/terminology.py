from ambra_sdk.service.entrypoints.generated.terminology import \
    AsyncTerminology as GAsyncTerminology
from ambra_sdk.service.entrypoints.generated.terminology import \
    Terminology as GTerminology


class Terminology(GTerminology):
    """Terminology."""


class AsyncTerminology(GAsyncTerminology):
    """AsyncTerminology."""

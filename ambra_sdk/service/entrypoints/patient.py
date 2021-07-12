from ambra_sdk.service.entrypoints.generated.patient import \
    AsyncPatient as GAsyncPatient
from ambra_sdk.service.entrypoints.generated.patient import Patient as GPatient


class Patient(GPatient):
    """Patient."""


class AsyncPatient(GAsyncPatient):
    """AsyncPatient."""

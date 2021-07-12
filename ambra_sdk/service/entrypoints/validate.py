from ambra_sdk.service.entrypoints.generated.validate import \
    AsyncValidate as GAsyncValidate
from ambra_sdk.service.entrypoints.generated.validate import \
    Validate as GValidate


class Validate(GValidate):
    """Validate."""


class AsyncValidate(GAsyncValidate):
    """AsyncValidate."""

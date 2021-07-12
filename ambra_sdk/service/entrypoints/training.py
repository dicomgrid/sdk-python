from ambra_sdk.service.entrypoints.generated.training import \
    AsyncTraining as GAsyncTraining
from ambra_sdk.service.entrypoints.generated.training import \
    Training as GTraining


class Training(GTraining):
    """Training."""


class AsyncTraining(GAsyncTraining):
    """AsyncTraining."""

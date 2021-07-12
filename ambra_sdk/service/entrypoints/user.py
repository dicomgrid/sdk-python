from ambra_sdk.service.entrypoints.generated.user import \
    AsyncUser as GAsyncUser
from ambra_sdk.service.entrypoints.generated.user import User as GUser


class User(GUser):
    """User."""


class AsyncUser(GAsyncUser):
    """AsyncUser."""

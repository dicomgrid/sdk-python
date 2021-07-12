from ambra_sdk.service.entrypoints.generated.account import Account as GAccount
from ambra_sdk.service.entrypoints.generated.account import \
    AsyncAccount as GAsyncAccount


class Account(GAccount):
    """Account."""


class AsyncAccount(GAsyncAccount):
    """AsyncAccount."""

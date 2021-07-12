from ambra_sdk.service.entrypoints.generated.scanner import \
    AsyncScanner as GAsyncScanner
from ambra_sdk.service.entrypoints.generated.scanner import Scanner as GScanner


class Scanner(GScanner):
    """Scanner."""


class AsyncScanner(GAsyncScanner):
    """AsyncScanner."""

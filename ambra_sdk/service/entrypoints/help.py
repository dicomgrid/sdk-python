from ambra_sdk.service.entrypoints.generated.help import \
    AsyncHelp as GAsyncHelp
from ambra_sdk.service.entrypoints.generated.help import Help as GHelp


class Help(GHelp):
    """Help."""


class AsyncHelp(GAsyncHelp):
    """AsyncHelp."""

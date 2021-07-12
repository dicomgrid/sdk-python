from ambra_sdk.service.entrypoints.generated.message import \
    AsyncMessage as GAsyncMessage
from ambra_sdk.service.entrypoints.generated.message import Message as GMessage


class Message(GMessage):
    """Message."""


class AsyncMessage(GAsyncMessage):
    """AsyncMessage."""

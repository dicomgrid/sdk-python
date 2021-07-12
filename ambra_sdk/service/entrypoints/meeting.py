from ambra_sdk.service.entrypoints.generated.meeting import \
    AsyncMeeting as GAsyncMeeting
from ambra_sdk.service.entrypoints.generated.meeting import Meeting as GMeeting


class Meeting(GMeeting):
    """Meeting."""


class AsyncMeeting(GAsyncMeeting):
    """AsyncMeeting."""

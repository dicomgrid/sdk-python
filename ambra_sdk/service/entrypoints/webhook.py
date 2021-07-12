from ambra_sdk.service.entrypoints.generated.webhook import \
    AsyncWebhook as GAsyncWebhook
from ambra_sdk.service.entrypoints.generated.webhook import Webhook as GWebhook


class Webhook(GWebhook):
    """Webhook."""


class AsyncWebhook(GAsyncWebhook):
    """AsyncWebhook."""

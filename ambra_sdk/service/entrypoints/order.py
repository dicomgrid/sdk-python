from ambra_sdk.service.entrypoints.generated.order import \
    AsyncOrder as GAsyncOrder
from ambra_sdk.service.entrypoints.generated.order import Order as GOrder


class Order(GOrder):
    """Order."""


class AsyncOrder(GAsyncOrder):
    """AsyncOrder."""

"""Async storage Api namespace."""

from typing import TYPE_CHECKING, Awaitable, Callable

from aiohttp import ClientResponse

from ambra_sdk.storage.image import AsyncImage
from ambra_sdk.storage.storage.base_storage import BaseStorage
from ambra_sdk.storage.study import AsyncStudy

if TYPE_CHECKING:
    from ambra_sdk.api.async_api import AsyncApi  # NOQA:WPS433


class AsyncStorage(BaseStorage):
    """Storage api namespace."""

    STORAGE_BASE_URL = 'https://{engine_fqdn}/api/v3/storage'

    def __init__(self, api: 'AsyncApi'):
        """Init.

        :param api: base api
        """
        self._api = api
        self._init_entrypoints()

    async def retry_with_new_sid(
        self,
        fn: Callable[..., Awaitable[ClientResponse]],
    ) -> ClientResponse:
        """Retry with new sid.

        :param fn: callable method
        :return: fn result
        """
        return await self._api.retry_with_new_sid(fn)

    async def delete(self, url, **kwargs) -> ClientResponse:
        """Delete from storage.

        :param url: url
        :param kwargs: delete kwargs
        :return: response obj
        """
        response: ClientResponse = await self._api.storage_delete(
            url,
            required_sid=True,
            **kwargs,
        )
        return response  # NOQA:WPS331

    async def get(self, url, **kwargs) -> ClientResponse:
        """Get from storage.

        :param url: url
        :param kwargs: delete kwargs
        :return: response obj
        """
        response: ClientResponse = await self._api.storage_get(
            url,
            required_sid=True,
            **kwargs,
        )
        return response  # NOQA:WPS331

    async def post(self, url, **kwargs) -> ClientResponse:
        """Post To storage.

        :param url: url
        :param kwargs: delete kwargs
        :return: response obj
        """
        response: ClientResponse = await self._api.storage_post(
            url,
            required_sid=True,
            **kwargs,
        )
        return response  # NOQA:WPS331

    def _init_entrypoints(self):
        """Init entrypoint namespaces."""
        self.Study = AsyncStudy(self)
        self.Image = AsyncImage(self)

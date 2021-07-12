"""Storage Api namespace."""

from typing import TYPE_CHECKING

from requests import Response

from ambra_sdk.storage.image import Image
from ambra_sdk.storage.storage.base_storage import BaseStorage
from ambra_sdk.storage.study import Study

if TYPE_CHECKING:
    from ambra_sdk.api.api import Api  # NOQA:WPS433


class Storage(BaseStorage):
    """Storage api namespace."""

    STORAGE_BASE_URL = 'https://{engine_fqdn}/api/v3/storage'

    def __init__(self, api: 'Api'):
        """Init.

        :param api: base api
        """
        self._api = api
        self._init_entrypoints()

    def retry_with_new_sid(self, fn):
        """Retry with new sid.

        :param fn: callable method
        :return: fn result
        """
        return self._api.retry_with_new_sid(fn)

    def delete(self, url, **kwargs) -> Response:
        """Delete from storage.

        :param url: url
        :param kwargs: delete kwargs
        :return: response obj
        """
        response: Response = self._api.storage_delete(
            url,
            required_sid=True,
            **kwargs,
        )
        return response  # NOQA:WPS331

    def get(self, url, **kwargs) -> Response:
        """Get from storage.

        :param url: url
        :param kwargs: delete kwargs
        :return: response obj
        """
        response: Response = self._api.storage_get(
            url,
            required_sid=True,
            **kwargs,
        )
        return response  # NOQA:WPS331

    def post(self, url, **kwargs) -> Response:
        """Post To storage.

        :param url: url
        :param kwargs: delete kwargs
        :return: response obj
        """
        response: Response = self._api.storage_post(
            url,
            required_sid=True,
            **kwargs,
        )
        return response  # NOQA:WPS331

    def _init_entrypoints(self):
        """Init entrypoint namespaces."""
        self.Study = Study(self)
        self.Image = Image(self)

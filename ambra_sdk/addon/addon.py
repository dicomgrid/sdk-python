"""Addon Api namespace.

Namespace for complex SDK functional.
"""

from ambra_sdk.addon.study import Study


class Addon:
    """Addon namespace."""

    def __init__(self, api):
        """Init.

        :param api: base API
        """
        self._api = api
        self._init_namespaces()

    def _init_namespaces(self):
        """Init addon namespaces."""
        self.Study = Study(self._api)

"""Async Addon Api namespace.

Namespace for complex SDK functional.
"""

from ambra_sdk.async_addon.dicom import Dicom
from ambra_sdk.async_addon.job import Job
from ambra_sdk.async_addon.study import Study


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
        self.Job = Job(self._api)
        self.Dicom = Dicom(self._api)

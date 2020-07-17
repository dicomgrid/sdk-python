"""Storage Api namespace."""

from typing import Any, Dict, Set, Tuple

from requests import Response

from ambra_sdk.storage.image import Image
from ambra_sdk.storage.study import Study

STORAGE_API_VERSION = 'LBL0038 v8.0 2019-07-17'


class Storage:
    """Storage api namespace."""

    STORAGE_BASE_URL = 'https://{engine_fqdn}/api/v3/storage'

    def __init__(self, api):
        """Init.

        :param api: base api
        """
        self._base_api = api
        self._init_entrypoints()

    def format_url(self, url_template: str, **kwargs) -> str:
        """Format url by template.

        :param url_template: url template
        :param kwargs: template arguments

        :return: formated url
        """
        engine_fqdn = kwargs.pop('engine_fqdn')
        base_url = self.STORAGE_BASE_URL.format(
            engine_fqdn=engine_fqdn,
        )
        url = url_template.format(**kwargs)
        return '{base_url}{url}'.format(base_url=base_url, url=url)

    def get_url_and_request(
        self,
        url_template: str,
        url_arg_names: Set[str],
        request_arg_names: Set[str],
        args: Dict[str, Any],
    ) -> Tuple[str, Dict[str, Any]]:
        """Get url and request arguments from template and locals.

        :param url_template: url template
        :param url_arg_names: url arg names for template
        :param request_arg_names: param arg names
        :param args: args dict
        :return: (url, request dict)
        """
        url_args = {
            arg_name: arg_value for arg_name, arg_value in args.items()
            if arg_name in url_arg_names
        }
        url = self.format_url(url_template, **url_args)

        request_data = {
            arg_name: arg_value for arg_name, arg_value in args.items()
            if arg_name in request_arg_names and arg_value is not None
        }
        return url, request_data

    def retry_with_new_sid(self, fn):
        """Retry with new sid.

        :param fn: callable method
        :return: fn result
        """
        return self._base_api.retry_with_new_sid(fn)

    def delete(self, url, **kwargs) -> Response:
        """Delete from storage.

        :param url: url
        :param kwargs: delete kwargs
        :return: response obj
        """
        response: Response = self._base_api.storage_delete(
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
        response: Response = self._base_api.storage_get(
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
        response: Response = self._base_api.storage_post(
            url,
            required_sid=True,
            **kwargs,
        )
        return response  # NOQA:WPS331

    def _init_entrypoints(self):
        """Init entrypoint namespaces."""
        self.Study = Study(self)
        self.Image = Image(self)

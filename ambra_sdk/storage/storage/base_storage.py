"""Base storage Api namespace."""

from typing import Any, Dict, Set, Tuple


class BaseStorage:
    """Base storage api namespace."""

    STORAGE_BASE_URL = 'https://{engine_fqdn}/api/v3/storage'

    def format_url(self, url_template: str, **kwargs) -> str:
        """Format url by template.

        :param url_template: url template
        :param kwargs: template arguments

        :return: formated url
        """
        engine_fqdn = kwargs.pop('engine_fqdn')
        base_url = self.STORAGE_BASE_URL.format(engine_fqdn=engine_fqdn)
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
            arg_name: arg_value
            for arg_name, arg_value in args.items()
            if arg_name in url_arg_names
        }
        url = self.format_url(url_template, **url_args)

        request_data = {
            arg_name: arg_value
            for arg_name, arg_value in args.items()
            if arg_name in request_arg_names and arg_value is not None
        }
        return url, request_data

from typing import Any, Dict

from box import Box, BoxList

from ambra_sdk.service.entrypoints.generated.study import Study as GStudy


class CustomFieldsList(BoxList):
    """Customfield box list."""

    def filter_by(self, filter_dict: Dict[str, Any]):
        """Filter custom fields.

        :param filter_dict: dict for filtering
        :yields: customfield
        """
        for customfield in self:
            if all(
                customfield.get(filter_key) == filter_value
                for filter_key, filter_value in filter_dict.items()
            ):
                yield customfield

    def get_by_name(self, name: str):
        """Get customfield by name.

        :param name: name of customfield
        :returns: customfield
        """
        return next(
            self.filter_by(filter_dict={'name': name}),
            None,
        )

    def get_by_uuid(self, uuid: str):
        """Get customfield by uuid.

        :param uuid: uuid of customfield
        :returns: customfield
        """
        return next(
            self.filter_by(filter_dict={'uuid': uuid}),
            None,
        )


class StudyBox(Box):
    """Study box."""

    def __setitem__(self, key, value):  # NOQA:WPS110
        """Set item for study box.

        :param key: key
        :param value: value
        """
        if key == 'customfields':
            value = CustomFieldsList(value)  # NOQA:WPS110
        super().__setitem__(key, value)


class Study(GStudy):
    """Study namespace."""

    def get(self, *args, **kwargs):
        """Get method.

        :param args: args
        :param kwargs: kwargs
        :return: query
        """
        query = super().get(*args, **kwargs)
        query.return_constructor = StudyBox
        return query

    def list(self, *args, **kwargs):  # NOQA:A003,WPS125
        """List method.

        :param args: args
        :param kwargs: kwargs
        :return: query
        """
        query = super().list(*args, **kwargs)
        query.return_constructor = StudyBox
        return query

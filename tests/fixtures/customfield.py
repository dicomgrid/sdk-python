"""Customfield fixtures."""

import pytest


@pytest.fixture
def add_customfield(api, account):
    """Add customfield.

    :param api: api
    :param account: account
    :yields: add customfield fn
    """
    customfields = []

    def _add_customfield(  # NOQA:WPS211
        required=None,
        capture_on_share_code=None,
        display_order=None,
        wrapped_dicom_only=None,
        dicom_only=None,
        capture_on_destination_search=None,
        **kwargs,
    ):
        customfield = api.Customfield.add(
            account_id=account.account.uuid,
            required=required,
            capture_on_share_code=capture_on_share_code,
            display_order=display_order,
            wrapped_dicom_only=wrapped_dicom_only,
            dicom_only=dicom_only,
            capture_on_destination_search=capture_on_destination_search,
            **kwargs,
        ).get()
        customfields.append(customfield)
        return customfield
    yield _add_customfield
    for customfield in customfields:
        api.Customfield.delete(
            uuid=customfield.uuid,
        ).get()

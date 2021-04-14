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
        **kwargs,
    ):
        customfield = api.Customfield.add(
            account_id=account.account.uuid,
            **kwargs,
        ).get()
        customfields.append(customfield)
        return customfield
    yield _add_customfield
    for customfield in customfields:
        api.Customfield.delete(
            uuid=customfield.uuid,
        ).get()

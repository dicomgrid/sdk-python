"""Websocket fixtures."""

import pytest
from dynaconf import settings

from ambra_sdk.service.ws import WSManager


@pytest.fixture(scope='module')
def ws(api):
    """Websocket manager.

    :param api: api fixture

    :yields: websocket manager
    """
    url = settings.API['url']
    ws_url = '{url}/channel/websocket'.format(url=url)
    ws_manager = WSManager(ws_url)
    ws_manager.run()
    yield ws_manager
    ws_manager.stop()


# Dont use ws_channel and account_ws in one test class.

@pytest.fixture
def ws_channel(api, ws):
    """Web socket channel.

    :param api: api fixture
    :param ws: websocket manager fixture

    :yields: func for create subscribed WSManager

    Don't use ws_channel and account_ws in one test class.
    """
    channels = []

    def _subscribe(channel):
        nonlocal channels
        ws.subscribe(api.sid, channel)
        channels.append(channel)
        return ws
    yield _subscribe
    for channel in channels:
        ws.unsubscribe(channel)


@pytest.fixture(scope='class')
def account_ws(api, account, ws):
    """Web socket channel for main test account.

    :param api: api fixture
    :param account: account fixture
    :param ws: websocket manager fixture

    :yields: WSManager subscribed on study channel

    Don't use ws_channel and account_ws in one test class.
    """
    namespace_id = account.account.namespace_id
    channel_name = 'study.{namespace_id}'.format(namespace_id=namespace_id)
    ws.subscribe(api.sid, channel_name)
    yield ws
    ws.unsubscribe(channel_name)

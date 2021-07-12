"""WS channels."""

import asyncio
import hashlib
import json
import logging
import sys
from time import monotonic
from typing import Callable, Dict, List

import aiohttp

if sys.version_info >= (3, 7):
    from contextlib import asynccontextmanager
else:
    # For python3.6
    from ambra_sdk.async_context_manager import asynccontextmanager

logger = logging.getLogger(__name__)

# Server inactivity timeout = 300
# https://github.com/dicomgrid/v3services/blob/master/app/websocket.pl#L40

INACTIVITY_TIMEOUT = 10


class AsyncWSManager:  # NOQA: WPS214
    """WS.

    WS.run create socket connection and ping it
    every INACTIVITY seconds. This is maintain connection.
    But sometimes server  close connection.
    In this case WS recreate connection and
    resubscribe channels

    Communication with WS through
    responses and requests queues.
    """

    def __init__(
        self,
        url: str,
    ):
        """Init.

        :param url: websocket url
        """
        self._url = url
        self._channels: Dict[str, str] = {}
        self._session = None
        self._ws = None
        self._last_ping = None
        self._ping_interval = INACTIVITY_TIMEOUT
        self._subscribe_wait_timeout = 10
        self._unsubscribe_wait_timeout = self._subscribe_wait_timeout

    @asynccontextmanager  # NOQA:WPS217,WPS213
    async def channels(
        self,
        sid: str,
        channel_names: List[str],
    ):
        """Channels ws context manager.

        :param sid: sid
        :param channel_names: list of channels
        :yields: self manager with channels subscribtions
        """
        for channel in channel_names:
            await self.subscribe(sid, channel)
            await self.wait_for_subscribe(
                channel,
                timeout=self._subscribe_wait_timeout,
            )
        try:  # NOQA: WPS501
            yield self
        finally:
            logger.debug('Stop')
            for channel_name in channel_names:
                await self.unsubscribe(channel_name)
                await self.wait_for_unsubscribe(
                    channel_name,
                    timeout=self._unsubscribe_wait_timeout,
                )
            # refresh socket and closed it
            await self._get_ws()
            assert self._ws is not None  # NOQA:S101
            await self._ws.close()
            await self._session.close()

    @asynccontextmanager
    async def channel(
        self,
        sid: str,
        channel_name: str,
    ):
        """Channel ws context manager.

        :param sid: sid
        :param channel_name: name of channel
        :yields: self manager with channel subscribtion
        """
        async with self.channels(sid, channel_names=[channel_name]) as ws:
            yield ws

    async def subscribe(self, sid, channel):
        """Subscribe.

        :param sid: sid
        :param channel: channel
        """
        logger.debug('Subscribe %s', channel)
        self._channels[channel] = sid
        sub_request = json.dumps(
            {
                'action': 'subscribe',
                'channel': channel,
                'sid': sid,
            },
        )
        ws = await self._get_ws()
        await ws.send_str(sub_request)

    async def resubscribe(self):
        """Resubscribe."""
        logger.debug('Resubscribe')
        for channel, sid in self._channels.items():
            await self._subscribe(sid, channel)

    async def unsubscribe(self, channel):
        """Unsubscribe.

        :param channel: channel
        """
        logger.debug('Unsubscribe %s', channel)
        self._channels.pop(channel)
        close_request = json.dumps(
            {
                'action': 'unsubscribe',
                'channel': channel,
                # But required! ;-)
                'sid': 'NOT NEEDED!',
            },
        )
        ws = await self._get_ws()
        await ws.send_str(close_request)

    async def wait_for(  # NOQA:WPS231
        self,
        fn: Callable[[aiohttp.WSMessage], bool],
        timeout: int = None,
    ) -> aiohttp.WSMessage:
        """Wait while fn(msg) is True.

        On TimeoutError this func dont stop ws.
        So you need to run this func in try-except block.

        :param fn: Function for find message
        :param timeout: timeout

        :raises TimeoutError: timeout error
        :raises RuntimeError: Unknown message in ws

        :returns: message
        """
        start = monotonic()
        while True:
            await self._ping()
            if timeout and (monotonic() - start) >= timeout:
                raise TimeoutError
            ws = await self._get_ws()
            try:
                msg: aiohttp.WSMessage = await asyncio.wait_for(
                    ws.receive(),
                    timeout=min(self._ping_interval, timeout),
                )
            except asyncio.TimeoutError:
                continue
            logger.debug('Recieved: %s', str(msg))
            if msg.type == aiohttp.WSMsgType.TEXT:
                if fn(msg):
                    return msg
            elif msg.type == aiohttp.WSMsgType.CLOSING:
                continue
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                logger.debug('Connection closed')
                # refresh socket
                ws = await self._get_ws()
                continue
            else:
                raise RuntimeError(
                    'Unimplemented {msg_type}'.format(
                        msg_type=str(msg.type),
                    ),
                )

    async def wait_for_event(
        self,
        channel: str,
        sid: str,
        event: str,
        timeout: int = None,
    ) -> aiohttp.WSMessage:
        """Wait for event.

        :param channel: channel name
        :param sid: sid
        :param event: event status name
        :param timeout: timeout

        :return: msg
        """
        sid_md5 = hashlib.md5(sid.encode()).hexdigest()  # NOQA:S303

        def _is_ready(msg):  # NOQA:WPS430
            if msg.type != aiohttp.WSMsgType.TEXT:
                return False
            msg_json = msg.json()
            msg_event = msg_json.get('event')
            msg_channel = msg_json.get('channel')
            msg_sid_md5 = msg_json.get('sid_md5')
            if msg_event is None \
               or msg_channel is None \
               or msg_sid_md5 is None:
                return False

            if channel == msg_channel \
               and msg_sid_md5 == sid_md5 \
               and msg_event == event:
                return True
            return False

        return await self.wait_for(_is_ready, timeout)

    async def wait_for_subscribe(
        self,
        channel: str,
        timeout: int = None,
    ) -> aiohttp.WSMessage:
        """Wait for subscribe.

        :param channel: channel name
        :param timeout: timeout

        :return: msg
        """

        def _is_subscribed(msg):  # NOQA:WPS430
            if msg.type != aiohttp.WSMsgType.TEXT:
                return False
            msg_json = msg.json()
            status = msg_json.get('status')
            msg_channel = msg_json.get('channel')
            if status is not None \
               and msg_channel is not None \
               and channel == msg_channel \
               and status == 'OK':
                return True
            return False

        return await self.wait_for(_is_subscribed, timeout)

    async def wait_for_unsubscribe(
        self,
        channel: str,
        timeout: int = None,
    ) -> aiohttp.WSMessage:
        """Wait for unsubscribe.

        :param channel: channel name
        :param timeout: timeout

        :return: msg
        """
        # actually this is same as wait for subscribe
        # Server return equal responses.
        return await self.wait_for_subscribe(channel, timeout)

    async def _get_ws(self):
        """Websocket connection.

        Get locks and refresh connection if it closed.

        :return: websocket connection
        """
        if self._session is None or self._session.closed:
            logger.debug('Create new session')
            self._session = aiohttp.ClientSession()
        if self._ws is None:
            logger.debug('Run ws connection')
            self._ws = await self._session.ws_connect(self._url)
        elif self._ws.closed:
            logger.debug('Restart ws connection')
            self._ws = await self._session.ws_connect(self._url)
            await self._resubscribe()
        return self._ws

    async def _ping(self):
        now = monotonic()
        if self._last_ping is None:
            self._last_ping = now
        if now - self._last_ping >= self._ping_interval:
            logger.debug('Ping')
            ping_request = json.dumps({'action': 'ping'})
            ws = await self._get_ws()
            await ws.send_str(ping_request)
            self._last_ping = now

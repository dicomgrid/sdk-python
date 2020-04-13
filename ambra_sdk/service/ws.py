"""WS channels."""

import asyncio
import hashlib
import json
import logging
import sys
from asyncio import events
from contextlib import contextmanager
from queue import Empty, Queue
from threading import Thread
from time import monotonic
from typing import Callable, Dict, List

import aiohttp

logger = logging.getLogger(__name__)


# Server inactivity timeout = 300
# https://github.com/dicomgrid/v3services/blob/master/app/websocket.pl#L40

INACTIVITY_TIMEOUT = 10

if sys.version_info > (3, 7):
    asyncio_get_running_loop = asyncio.get_running_loop
    asyncio_run = asyncio.run
else:
    # For python3.6
    asyncio_get_running_loop = asyncio.get_event_loop

    # This is simple implementation of asyncio_run
    # Standart implementation is more powerful and complex.
    # If u can, better use python3.7...
    def asyncio_run(future):  # NOQA:WPS440
        """Execute future in loop.

        :param future: some future
        :return: result
        """
        loop = events.new_event_loop()
        future_result = loop.run_until_complete(future)
        events.set_event_loop(None)
        loop.close()
        return future_result  # NOQA:WPS331


class WSManager:  # NOQA:WPS214
    """WS manager.

    :Example:

    >>> url = 'https://ambra.com/channel/websocket'
    >>> namespace_id = account.namespace_id
    >>> sid = api.sid
    >>> channel = 'study.{namespace_id}'.format(namespace_id=namespace_id)

    >>> ws = WSManager(url)
    >>> ws.run()
    >>> time.sleep(10)
    >>> ws.subscribe(sid, channel)

    >>> def wait_for_func(msg):
    >>>     ready = msg.json().get('event')
    >>>     if ready == 'READY':
    >>>         return True
    >>>     return False

    >>> try:
    >>>     ws.wait_for(wait_for_func, timeout=100)
    >>> except TimeoutError:
    >>>     pass

    >>> ws.unsubscribe(channel)
    >>> time.sleep(10)
    >>> ws.stop()
    """

    def __init__(self, url: str):
        """Init.

        :param url: websocket channel url
        """
        self._url = url
        self._requests: Queue = Queue()
        self._responses: Queue = Queue(maxsize=100)
        self._subscribe_wait_timeout = 10
        self._unsubscribe_wait_timeout = self._subscribe_wait_timeout

    def wait_for(
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

        :returns: message
        """
        start = monotonic()
        while True:
            try:
                msg: aiohttp.WSMessage = self._responses.get(timeout=timeout)
            except Empty:
                logger.debug('No messages in queue')
                raise TimeoutError

            if fn(msg):
                return msg
            if timeout and (monotonic() - start) >= timeout:
                raise TimeoutError

    def wait_for_event(
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
        return self.wait_for(_is_ready, timeout)

    def wait_for_subscribe(
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

        return self.wait_for(_is_subscribed, timeout)

    def wait_for_unsubscribe(
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
        return self.wait_for_subscribe(channel, timeout)

    def run(self):
        """Run manager."""
        ws = WS(
            url=self._url,
            responses=self._responses,
            requests=self._requests,
        )
        self._manager_thread = Thread(
            target=asyncio_run,
            args=(ws.run(), ),
        )
        self._manager_thread.start()
        self._runned = True

    def stop(self):
        """Stop manager."""
        self._requests.put(('STOP', {}))
        self._manager_thread.join()
        self._runned = False

    def subscribe(self, sid: str, channel: str):
        """Subscribe to channel.

        :param sid: sid
        :param channel: channel
        """
        self._requests.put(
            ('SUBSCRIBE', {'sid': sid, 'channel': channel}),
        )
        self.wait_for_subscribe(
            channel,
            self._subscribe_wait_timeout,
        )

    def unsubscribe(self, channel: str):
        """Subscribe from channel.

        :param channel: channel
        """
        self._requests.put(('UNSUBSCRIBE', {'channel': channel}))
        self.wait_for_unsubscribe(
            channel,
            self._unsubscribe_wait_timeout,
        )

    @contextmanager
    def channels(
        self,
        sid: str,
        channel_names: List[str],
    ):
        """Channels ws context manager.

        :param sid: sid
        :param channel_names: list of channels
        :yields: self manager with channels subscribtions
        """
        self.run()
        for channel in channel_names:
            self.subscribe(sid, channel)
        try:  # NOQA: WPS501
            yield self
        finally:
            for channel_name in channel_names:
                self.unsubscribe(channel_name)
            self.stop()

    @contextmanager
    def channel(
        self,
        sid: str,
        channel_name: str,
    ):
        """Channel ws context manager.

        :param sid: sid
        :param channel_name: name of channel
        :yields: self manager with channel subscribtion
        """
        with self.channels(sid, channel_names=[channel_name]) as ws:
            yield ws


class WS:  # NOQA: WPS214
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
        responses: Queue,
        requests: Queue,
    ):
        """Init.

        :param url: websocket url
        :param responses: responses queue
        :param requests: requests queue
        """
        self._url = url
        self._channels: Dict[str, str] = {}
        self._session = None
        self._ws = None
        self._last_ping = None
        self._ping_interval = INACTIVITY_TIMEOUT
        self._check_request_interval = 2
        self._manager_thread = None
        self._runned = False
        self._requests = requests
        self._responses = responses
        # In pytest gather create different loops.
        self._loop = None

    async def run(self):
        """Run websocket handlers."""
        self._runned = True
        self._loop = asyncio_get_running_loop()
        self._ws_lock = asyncio.Lock(loop=self._loop)
        self._session_lock = asyncio.Lock(loop=self._loop)
        try:  # NOQA:WPS501
            await asyncio.gather(
                self._request_handler(),
                self._response_handler(),
            )
        finally:
            await self._stop()

    async def _get_ws(self):
        """Websocket connection.

        Get locks and refresh connection if it closed.

        :return: websocket connection
        """
        if self._runned is False:
            return RuntimeError('Not runned')

        async with self._session_lock:
            if self._session is None or self._session.closed:
                logger.debug('Create new session')
                self._session = aiohttp.ClientSession()
        async with self._ws_lock:
            if self._ws is None:
                logger.debug('Run ws connection')
                self._ws = await self._session.ws_connect(self._url)
            elif self._ws.closed:
                logger.debug('Restart ws connection')
                self._ws = await self._session.ws_connect(self._url)
                await self._resubscribe()
            return self._ws

    def _get_from_requests(self):
        return self._requests.get(timeout=self._check_request_interval)

    async def _request_handler(self):
        logger.info('Start request handler')
        while True:
            try:
                # This is blocking. So run in executor
                request_type, kwargs = await self._loop.run_in_executor(
                    None, self._get_from_requests,
                )
            except Empty:
                await self._ping()
                continue

            logger.debug('Request: %s. %s', request_type, str(kwargs))
            if request_type == 'SUBSCRIBE':
                await self._subscribe(**kwargs)
            if request_type == 'UNSUBSCRIBE':
                await self._unsubscribe(**kwargs)
            if request_type == 'STOP':
                await self._stop()
                return

    async def _response_handler(self):
        logger.info('Start response handler')
        while True:
            if self._runned is False:
                break
            ws = await self._get_ws()
            msg = await ws.receive()
            logger.debug('Recieved: %s', str(msg))
            if msg.type == aiohttp.WSMsgType.TEXT:
                self._responses.put(msg)
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

    async def _subscribe(self, sid, channel):
        logger.info('Subscribe %s', channel)
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

    async def _resubscribe(self):
        logger.info('Resubscribe')
        for channel, sid in self._channels.items():
            await self._subscribe(sid, channel)

    async def _unsubscribe(self, channel):
        logger.info('Unsubscribe %s', channel)
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

    async def _ping(self):
        now = monotonic()
        if self._last_ping is None:
            self._last_ping = now
        if now - self._last_ping >= self._ping_interval:
            logger.info('Ping')
            ping_request = json.dumps({'action': 'ping'})
            ws = await self._get_ws()
            await ws.send_str(ping_request)
            self._last_ping = now

    async def _stop(self):
        if self._runned is False:
            # Already stopped
            return

        logger.info('Stop')
        # refresh socket and closed it
        self._runned = False
        await self._get_ws()
        await self._ws.close()
        await self._session.close()

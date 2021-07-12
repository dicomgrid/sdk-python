"""Async Job addon namespace."""

import uuid as uuid_lib
from contextlib import suppress
from time import monotonic
from typing import Mapping, Optional, Tuple, Union, cast

from box import Box

from ambra_sdk.exceptions.service import (
    NotFound,
    NotPermitted,
    PreconditionFailed,
)
from ambra_sdk.service.query import AsyncQueryO
from ambra_sdk.service.ws import AsyncWSManager

ERRORS_MAPPING_KEY_TYPE = Union[Tuple[str, Optional[str]], str]

ERRORS_MAPPING_TYPE = Mapping[ERRORS_MAPPING_KEY_TYPE, PreconditionFailed]


class Job:
    """Job addon namespace."""

    def __init__(self, api):
        """Init.

        :param api: base api
        """
        self._api = api

    async def wait_completion(
        self,
        method,
        *,
        timeout: float = 200.0,
        ws_timeout: int = 5,
        **kwargs,
    ):
        """Wait completion.

        Execute some storage method and wait it
        :param method: method
        :param timeout: timeout
        :param ws_timeout: websocket interval
        :param kwargs: method kwargs
        :return: method result
        """
        # Namespace is required in kwargs
        namespace = kwargs['namespace']
        x_ambrahealth_job_id = kwargs.get('x_ambrahealth_job_id', None)

        if x_ambrahealth_job_id is None:
            x_ambrahealth_job_id = str(uuid_lib.uuid4())
        kwargs['x_ambrahealth_job_id'] = x_ambrahealth_job_id
        method_result = await method(**kwargs)
        # A. Matveev: job namespace is initial namespace
        await self.wait(
            job_id=x_ambrahealth_job_id,
            namespace_id=namespace,
            timeout=timeout,
            ws_timeout=ws_timeout,
        )
        return method_result

    async def wait(
        self,
        *,
        job_id: str,
        namespace_id: str,
        timeout: float,
        ws_timeout: int,
    ):
        """Wait job.

        :param job_id: job id
        :param namespace_id: job namespace_id
        :param timeout: time for waiting new study
        :param ws_timeout: time for waiting in socket

        :raises TimeoutError: if job not ready by timeout
        :raises RuntimeError: Bad answer from ws
        """
        errors_mapping: ERRORS_MAPPING_TYPE = {
            ('NOT_FOUND', None):
            NotFound('The job can not be found'),
            ('NOT_PERMITTED', None):
            NotPermitted('The user is not permitted to access this job'),
        }
        request_data = {
            'id': job_id,
        }
        get_job_query = AsyncQueryO(
            api=self._api,
            url='/job/get',
            request_data=request_data,
            errors_mapping=errors_mapping,
            required_sid=True,
        )

        ws_url = self._api.ws_url
        ws_manager = AsyncWSManager(ws_url)
        start = monotonic()

        # K. Pustovalov: job channel have form job.namespace
        channel_name = 'job.{namespace_id}'.format(namespace_id=namespace_id)
        sid = await self._api.get_sid()

        job_is_ready = False
        async with ws_manager.channel(sid, channel_name) as ws:
            while True:
                if monotonic() - start >= timeout:
                    break
                with suppress(NotFound):
                    job_status = cast(Box, await get_job_query.get())
                    if job_status['state'] != 'DONE':
                        raise RuntimeError(  # NOQA:WPS220
                            'Unknown job status {job_status}'.format(
                                job_status=job_status['state'],
                            ),
                        )
                    job_is_ready = True
                    break
                with suppress(TimeoutError):
                    await ws.wait_for_event(
                        channel_name,
                        sid,
                        'DONE',
                        timeout=ws_timeout,
                    )
        if job_is_ready is False:
            raise TimeoutError

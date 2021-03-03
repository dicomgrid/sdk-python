"""Job addon namespace."""

from contextlib import suppress
from time import monotonic
from typing import Mapping, Optional, Tuple, Union

from ambra_sdk.exceptions.service import (
    NotFound,
    NotPermitted,
    PreconditionFailed,
)
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.ws import WSManager


class Job:
    """Job addon namespace."""

    def __init__(self, api):
        """Init.

        :param api: base api
        """
        self._api = api

    def wait(
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
        errors_mapping: Mapping[  # NOQA:WPS234
            Union[Tuple[str, Optional[str]], str],
            PreconditionFailed,
        ] = {
            ('NOT_FOUND', None): NotFound('The job can not be found'),
            ('NOT_PERMITTED', None): NotPermitted(
                'The user is not permitted to access this job',
            ),
        }
        request_data = {
            'id': job_id,
        }
        get_job_query = QueryO(
            api=self._api,
            url='/job/get',
            request_data=request_data,
            errors_mapping=errors_mapping,
            required_sid=True,
        )

        ws_url = self._api.ws_url
        ws_manager = WSManager(ws_url)
        start = monotonic()

        # K. Pustovalov: job channel have form job.namespace
        channel_name = 'job.{namespace_id}'.format(namespace_id=namespace_id)
        sid = self._api.sid

        job_is_ready = False
        with ws_manager.channel(sid, channel_name) as ws:
            while True:
                if monotonic() - start >= timeout:
                    break
                with suppress(NotFound):
                    job_status = get_job_query.get()
                    if job_status['state'] != 'DONE':
                        raise RuntimeError(  # NOQA:WPS220
                            'Unknown job status {job_status}'.format(
                                job_status=job_status['state'],
                            ),
                        )
                    job_is_ready = True
                    break
                with suppress(TimeoutError):
                    ws.wait_for_event(
                        channel_name,
                        sid,
                        'DONE',
                        timeout=ws_timeout,
                    )
        if job_is_ready is False:
            raise TimeoutError

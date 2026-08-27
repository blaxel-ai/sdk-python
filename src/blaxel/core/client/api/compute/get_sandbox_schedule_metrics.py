import datetime
from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.sandbox_schedule_metrics import SandboxScheduleMetrics
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_since: Union[Unset, str] = UNSET
    if not isinstance(since, Unset):
        json_since = since.isoformat()
    params["since"] = json_since

    json_until: Union[Unset, str] = UNSET
    if not isinstance(until, Unset):
        json_until = until.isoformat()
    params["until"] = json_until

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/schedules/metrics",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> SandboxScheduleMetrics | None:
    if response.status_code == 200:
        response_200 = SandboxScheduleMetrics.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[SandboxScheduleMetrics]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
) -> Response[SandboxScheduleMetrics]:
    """Get Sandbox Scheduling Metrics

     Returns active sandbox and scheduling metrics for a UTC minute window. since is inclusive and until
    is exclusive. The default window is the last 24 hours and the maximum is 7 days. Execution status
    describes submission acceptance, not process completion. Execution totals begin accumulating when
    metrics collection is enabled and can lag recent firings briefly.

    Args:
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SandboxScheduleMetrics]
    """

    kwargs = _get_kwargs(
        since=since,
        until=until,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
) -> SandboxScheduleMetrics | None:
    """Get Sandbox Scheduling Metrics

     Returns active sandbox and scheduling metrics for a UTC minute window. since is inclusive and until
    is exclusive. The default window is the last 24 hours and the maximum is 7 days. Execution status
    describes submission acceptance, not process completion. Execution totals begin accumulating when
    metrics collection is enabled and can lag recent firings briefly.

    Args:
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SandboxScheduleMetrics
    """

    return sync_detailed(
        client=client,
        since=since,
        until=until,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
) -> Response[SandboxScheduleMetrics]:
    """Get Sandbox Scheduling Metrics

     Returns active sandbox and scheduling metrics for a UTC minute window. since is inclusive and until
    is exclusive. The default window is the last 24 hours and the maximum is 7 days. Execution status
    describes submission acceptance, not process completion. Execution totals begin accumulating when
    metrics collection is enabled and can lag recent firings briefly.

    Args:
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SandboxScheduleMetrics]
    """

    kwargs = _get_kwargs(
        since=since,
        until=until,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
) -> SandboxScheduleMetrics | None:
    """Get Sandbox Scheduling Metrics

     Returns active sandbox and scheduling metrics for a UTC minute window. since is inclusive and until
    is exclusive. The default window is the last 24 hours and the maximum is 7 days. Execution status
    describes submission acceptance, not process completion. Execution totals begin accumulating when
    metrics collection is enabled and can lag recent firings briefly.

    Args:
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SandboxScheduleMetrics
    """

    return (
        await asyncio_detailed(
            client=client,
            since=since,
            until=until,
        )
    ).parsed

import datetime
from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.list_schedule_executions_sort import ListScheduleExecutionsSort
from ...models.list_schedule_executions_status import ListScheduleExecutionsStatus
from ...models.sandbox_schedule_execution_list import SandboxScheduleExecutionList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListScheduleExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    status: Union[Unset, ListScheduleExecutionsStatus] = UNSET,
    sandbox: Union[Unset, str] = UNSET,
    schedule: Union[Unset, str] = UNSET,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    json_status: Union[Unset, str] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params["sandbox"] = sandbox

    params["schedule"] = schedule

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
        "url": "/schedule-executions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> SandboxScheduleExecutionList | None:
    if response.status_code == 200:
        response_200 = SandboxScheduleExecutionList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[SandboxScheduleExecutionList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListScheduleExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    status: Union[Unset, ListScheduleExecutionsStatus] = UNSET,
    sandbox: Union[Unset, str] = UNSET,
    schedule: Union[Unset, str] = UNSET,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
) -> Response[SandboxScheduleExecutionList]:
    """List Workspace Schedule Executions

     Returns schedule execution submissions across the workspace, newest first by default. Status
    describes submission acceptance, not process completion. since and until are inclusive RFC 3339
    bounds on creation time.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListScheduleExecutionsSort]):
        q (Union[Unset, str]):
        status (Union[Unset, ListScheduleExecutionsStatus]):
        sandbox (Union[Unset, str]):
        schedule (Union[Unset, str]):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SandboxScheduleExecutionList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
        status=status,
        sandbox=sandbox,
        schedule=schedule,
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
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListScheduleExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    status: Union[Unset, ListScheduleExecutionsStatus] = UNSET,
    sandbox: Union[Unset, str] = UNSET,
    schedule: Union[Unset, str] = UNSET,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
) -> SandboxScheduleExecutionList | None:
    """List Workspace Schedule Executions

     Returns schedule execution submissions across the workspace, newest first by default. Status
    describes submission acceptance, not process completion. since and until are inclusive RFC 3339
    bounds on creation time.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListScheduleExecutionsSort]):
        q (Union[Unset, str]):
        status (Union[Unset, ListScheduleExecutionsStatus]):
        sandbox (Union[Unset, str]):
        schedule (Union[Unset, str]):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SandboxScheduleExecutionList
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
        status=status,
        sandbox=sandbox,
        schedule=schedule,
        since=since,
        until=until,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListScheduleExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    status: Union[Unset, ListScheduleExecutionsStatus] = UNSET,
    sandbox: Union[Unset, str] = UNSET,
    schedule: Union[Unset, str] = UNSET,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
) -> Response[SandboxScheduleExecutionList]:
    """List Workspace Schedule Executions

     Returns schedule execution submissions across the workspace, newest first by default. Status
    describes submission acceptance, not process completion. since and until are inclusive RFC 3339
    bounds on creation time.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListScheduleExecutionsSort]):
        q (Union[Unset, str]):
        status (Union[Unset, ListScheduleExecutionsStatus]):
        sandbox (Union[Unset, str]):
        schedule (Union[Unset, str]):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SandboxScheduleExecutionList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
        status=status,
        sandbox=sandbox,
        schedule=schedule,
        since=since,
        until=until,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListScheduleExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    status: Union[Unset, ListScheduleExecutionsStatus] = UNSET,
    sandbox: Union[Unset, str] = UNSET,
    schedule: Union[Unset, str] = UNSET,
    since: Union[Unset, datetime.datetime] = UNSET,
    until: Union[Unset, datetime.datetime] = UNSET,
) -> SandboxScheduleExecutionList | None:
    """List Workspace Schedule Executions

     Returns schedule execution submissions across the workspace, newest first by default. Status
    describes submission acceptance, not process completion. since and until are inclusive RFC 3339
    bounds on creation time.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListScheduleExecutionsSort]):
        q (Union[Unset, str]):
        status (Union[Unset, ListScheduleExecutionsStatus]):
        sandbox (Union[Unset, str]):
        schedule (Union[Unset, str]):
        since (Union[Unset, datetime.datetime]):
        until (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SandboxScheduleExecutionList
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            sort=sort,
            q=q,
            status=status,
            sandbox=sandbox,
            schedule=schedule,
            since=since,
            until=until,
        )
    ).parsed

import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.list_schedule_executions_sort import ListScheduleExecutionsSort
from ...models.list_schedule_executions_status import ListScheduleExecutionsStatus
from ...models.sandbox_schedule_execution_list import SandboxScheduleExecutionList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
    sort: ListScheduleExecutionsSort | Unset = UNSET,
    q: str | Unset = UNSET,
    status: ListScheduleExecutionsStatus | Unset = UNSET,
    sandbox: str | Unset = UNSET,
    schedule: str | Unset = UNSET,
    since: datetime.datetime | Unset = UNSET,
    until: datetime.datetime | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params["sandbox"] = sandbox

    params["schedule"] = schedule

    json_since: str | Unset = UNSET
    if not isinstance(since, Unset):
        json_since = since.isoformat()
    params["since"] = json_since

    json_until: str | Unset = UNSET
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
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
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
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
    sort: ListScheduleExecutionsSort | Unset = UNSET,
    q: str | Unset = UNSET,
    status: ListScheduleExecutionsStatus | Unset = UNSET,
    sandbox: str | Unset = UNSET,
    schedule: str | Unset = UNSET,
    since: datetime.datetime | Unset = UNSET,
    until: datetime.datetime | Unset = UNSET,
) -> Response[SandboxScheduleExecutionList]:
    """List Workspace Schedule Executions

     Returns schedule execution submissions across the workspace, newest first by default. Status
    describes submission acceptance, not process completion. since and until are inclusive RFC 3339
    bounds on creation time.

    Args:
        limit (int | Unset):  Default: 20.
        cursor (str | Unset):
        sort (ListScheduleExecutionsSort | Unset):
        q (str | Unset):
        status (ListScheduleExecutionsStatus | Unset):
        sandbox (str | Unset):
        schedule (str | Unset):
        since (datetime.datetime | Unset):
        until (datetime.datetime | Unset):

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
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
    sort: ListScheduleExecutionsSort | Unset = UNSET,
    q: str | Unset = UNSET,
    status: ListScheduleExecutionsStatus | Unset = UNSET,
    sandbox: str | Unset = UNSET,
    schedule: str | Unset = UNSET,
    since: datetime.datetime | Unset = UNSET,
    until: datetime.datetime | Unset = UNSET,
) -> SandboxScheduleExecutionList | None:
    """List Workspace Schedule Executions

     Returns schedule execution submissions across the workspace, newest first by default. Status
    describes submission acceptance, not process completion. since and until are inclusive RFC 3339
    bounds on creation time.

    Args:
        limit (int | Unset):  Default: 20.
        cursor (str | Unset):
        sort (ListScheduleExecutionsSort | Unset):
        q (str | Unset):
        status (ListScheduleExecutionsStatus | Unset):
        sandbox (str | Unset):
        schedule (str | Unset):
        since (datetime.datetime | Unset):
        until (datetime.datetime | Unset):

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
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
    sort: ListScheduleExecutionsSort | Unset = UNSET,
    q: str | Unset = UNSET,
    status: ListScheduleExecutionsStatus | Unset = UNSET,
    sandbox: str | Unset = UNSET,
    schedule: str | Unset = UNSET,
    since: datetime.datetime | Unset = UNSET,
    until: datetime.datetime | Unset = UNSET,
) -> Response[SandboxScheduleExecutionList]:
    """List Workspace Schedule Executions

     Returns schedule execution submissions across the workspace, newest first by default. Status
    describes submission acceptance, not process completion. since and until are inclusive RFC 3339
    bounds on creation time.

    Args:
        limit (int | Unset):  Default: 20.
        cursor (str | Unset):
        sort (ListScheduleExecutionsSort | Unset):
        q (str | Unset):
        status (ListScheduleExecutionsStatus | Unset):
        sandbox (str | Unset):
        schedule (str | Unset):
        since (datetime.datetime | Unset):
        until (datetime.datetime | Unset):

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
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
    sort: ListScheduleExecutionsSort | Unset = UNSET,
    q: str | Unset = UNSET,
    status: ListScheduleExecutionsStatus | Unset = UNSET,
    sandbox: str | Unset = UNSET,
    schedule: str | Unset = UNSET,
    since: datetime.datetime | Unset = UNSET,
    until: datetime.datetime | Unset = UNSET,
) -> SandboxScheduleExecutionList | None:
    """List Workspace Schedule Executions

     Returns schedule execution submissions across the workspace, newest first by default. Status
    describes submission acceptance, not process completion. since and until are inclusive RFC 3339
    bounds on creation time.

    Args:
        limit (int | Unset):  Default: 20.
        cursor (str | Unset):
        sort (ListScheduleExecutionsSort | Unset):
        q (str | Unset):
        status (ListScheduleExecutionsStatus | Unset):
        sandbox (str | Unset):
        schedule (str | Unset):
        since (datetime.datetime | Unset):
        until (datetime.datetime | Unset):

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

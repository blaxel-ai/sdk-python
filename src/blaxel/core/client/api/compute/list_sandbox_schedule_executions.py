from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.list_sandbox_schedule_executions_sort import ListSandboxScheduleExecutionsSort
from ...models.sandbox_schedule_execution_list import SandboxScheduleExecutionList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_name: str,
    *,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSandboxScheduleExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sandboxes/{sandbox_name}/schedule-executions",
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
        raise errors.UnexpectedStatus(response.status_code, response.content)
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
    sandbox_name: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSandboxScheduleExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> Response[SandboxScheduleExecutionList]:
    """List Sandbox Schedule Executions

     Returns the execution history of a Sandbox's schedules (across all schedules of the sandbox), newest
    first. Cursor-paginated via the `cursor` and `limit` query parameters. Each item records the HTTP
    status of submitting the scheduled command and the process name for log lookup.

    Args:
        sandbox_name (str):
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSandboxScheduleExecutionsSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SandboxScheduleExecutionList]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_name: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSandboxScheduleExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> SandboxScheduleExecutionList | None:
    """List Sandbox Schedule Executions

     Returns the execution history of a Sandbox's schedules (across all schedules of the sandbox), newest
    first. Cursor-paginated via the `cursor` and `limit` query parameters. Each item records the HTTP
    status of submitting the scheduled command and the process name for log lookup.

    Args:
        sandbox_name (str):
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSandboxScheduleExecutionsSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SandboxScheduleExecutionList
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        client=client,
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSandboxScheduleExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> Response[SandboxScheduleExecutionList]:
    """List Sandbox Schedule Executions

     Returns the execution history of a Sandbox's schedules (across all schedules of the sandbox), newest
    first. Cursor-paginated via the `cursor` and `limit` query parameters. Each item records the HTTP
    status of submitting the scheduled command and the process name for log lookup.

    Args:
        sandbox_name (str):
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSandboxScheduleExecutionsSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SandboxScheduleExecutionList]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSandboxScheduleExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> SandboxScheduleExecutionList | None:
    """List Sandbox Schedule Executions

     Returns the execution history of a Sandbox's schedules (across all schedules of the sandbox), newest
    first. Cursor-paginated via the `cursor` and `limit` query parameters. Each item records the HTTP
    status of submitting the scheduled command and the process name for log lookup.

    Args:
        sandbox_name (str):
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSandboxScheduleExecutionsSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SandboxScheduleExecutionList
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            client=client,
            limit=limit,
            cursor=cursor,
            sort=sort,
            q=q,
        )
    ).parsed

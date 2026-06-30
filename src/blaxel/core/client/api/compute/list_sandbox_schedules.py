from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.list_sandbox_schedules_sort import ListSandboxSchedulesSort
from ...models.list_sandbox_schedules_type import ListSandboxSchedulesType
from ...models.sandbox_schedule_entry_list import SandboxScheduleEntryList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_name: str,
    *,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSandboxSchedulesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    type_: Union[Unset, ListSandboxSchedulesType] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    json_type_: Union[Unset, str] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sandboxes/{sandbox_name}/schedules",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> SandboxScheduleEntryList | None:
    if response.status_code == 200:
        response_200 = SandboxScheduleEntryList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[SandboxScheduleEntryList]:
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
    sort: Union[Unset, ListSandboxSchedulesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    type_: Union[Unset, ListSandboxSchedulesType] = UNSET,
) -> Response[SandboxScheduleEntryList]:
    """List Sandbox Schedules

     Returns the schedules configured on a Sandbox. Starting with API version 2026-04-28 the response is
    wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions return a bare array.

    Args:
        sandbox_name (str):
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSandboxSchedulesSort]):
        q (Union[Unset, str]):
        type_ (Union[Unset, ListSandboxSchedulesType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SandboxScheduleEntryList]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
        type_=type_,
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
    sort: Union[Unset, ListSandboxSchedulesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    type_: Union[Unset, ListSandboxSchedulesType] = UNSET,
) -> SandboxScheduleEntryList | None:
    """List Sandbox Schedules

     Returns the schedules configured on a Sandbox. Starting with API version 2026-04-28 the response is
    wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions return a bare array.

    Args:
        sandbox_name (str):
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSandboxSchedulesSort]):
        q (Union[Unset, str]):
        type_ (Union[Unset, ListSandboxSchedulesType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SandboxScheduleEntryList
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        client=client,
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSandboxSchedulesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    type_: Union[Unset, ListSandboxSchedulesType] = UNSET,
) -> Response[SandboxScheduleEntryList]:
    """List Sandbox Schedules

     Returns the schedules configured on a Sandbox. Starting with API version 2026-04-28 the response is
    wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions return a bare array.

    Args:
        sandbox_name (str):
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSandboxSchedulesSort]):
        q (Union[Unset, str]):
        type_ (Union[Unset, ListSandboxSchedulesType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SandboxScheduleEntryList]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSandboxSchedulesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    type_: Union[Unset, ListSandboxSchedulesType] = UNSET,
) -> SandboxScheduleEntryList | None:
    """List Sandbox Schedules

     Returns the schedules configured on a Sandbox. Starting with API version 2026-04-28 the response is
    wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions return a bare array.

    Args:
        sandbox_name (str):
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSandboxSchedulesSort]):
        q (Union[Unset, str]):
        type_ (Union[Unset, ListSandboxSchedulesType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SandboxScheduleEntryList
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            client=client,
            limit=limit,
            cursor=cursor,
            sort=sort,
            q=q,
            type_=type_,
        )
    ).parsed

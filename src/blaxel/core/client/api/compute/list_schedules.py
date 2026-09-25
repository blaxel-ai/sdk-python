from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.list_schedules_sort import ListSchedulesSort
from ...models.list_schedules_type import ListSchedulesType
from ...models.sandbox_schedule_entry_list import SandboxScheduleEntryList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSchedulesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    sandbox: Union[Unset, str] = UNSET,
    type_: Union[Unset, ListSchedulesType] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    params["sandbox"] = sandbox

    json_type_: Union[Unset, str] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/schedules",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> SandboxScheduleEntryList | None:
    if response.status_code == 200:
        response_200 = SandboxScheduleEntryList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
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
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSchedulesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    sandbox: Union[Unset, str] = UNSET,
    type_: Union[Unset, ListSchedulesType] = UNSET,
) -> Response[SandboxScheduleEntryList]:
    """List Workspace Schedules

     Returns schedule definitions across the workspace, newest first by default.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSchedulesSort]):
        q (Union[Unset, str]):
        sandbox (Union[Unset, str]):
        type_ (Union[Unset, ListSchedulesType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SandboxScheduleEntryList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
        sandbox=sandbox,
        type_=type_,
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
    sort: Union[Unset, ListSchedulesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    sandbox: Union[Unset, str] = UNSET,
    type_: Union[Unset, ListSchedulesType] = UNSET,
) -> SandboxScheduleEntryList | None:
    """List Workspace Schedules

     Returns schedule definitions across the workspace, newest first by default.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSchedulesSort]):
        q (Union[Unset, str]):
        sandbox (Union[Unset, str]):
        type_ (Union[Unset, ListSchedulesType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SandboxScheduleEntryList
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
        sandbox=sandbox,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSchedulesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    sandbox: Union[Unset, str] = UNSET,
    type_: Union[Unset, ListSchedulesType] = UNSET,
) -> Response[SandboxScheduleEntryList]:
    """List Workspace Schedules

     Returns schedule definitions across the workspace, newest first by default.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSchedulesSort]):
        q (Union[Unset, str]):
        sandbox (Union[Unset, str]):
        type_ (Union[Unset, ListSchedulesType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SandboxScheduleEntryList]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        sort=sort,
        q=q,
        sandbox=sandbox,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListSchedulesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    sandbox: Union[Unset, str] = UNSET,
    type_: Union[Unset, ListSchedulesType] = UNSET,
) -> SandboxScheduleEntryList | None:
    """List Workspace Schedules

     Returns schedule definitions across the workspace, newest first by default.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListSchedulesSort]):
        q (Union[Unset, str]):
        sandbox (Union[Unset, str]):
        type_ (Union[Unset, ListSchedulesType]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SandboxScheduleEntryList
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            sort=sort,
            q=q,
            sandbox=sandbox,
            type_=type_,
        )
    ).parsed

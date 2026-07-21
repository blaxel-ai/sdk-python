from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.agent_list import AgentList
from ...models.error import Error
from ...models.list_agents_anchor import ListAgentsAnchor
from ...models.list_agents_sort import ListAgentsSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListAgentsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListAgentsAnchor] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    json_anchor: Union[Unset, str] = UNSET
    if not isinstance(anchor, Unset):
        json_anchor = anchor.value

    params["anchor"] = json_anchor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[AgentList, Error] | None:
    if response.status_code == 200:
        response_200 = AgentList.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AgentList, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListAgentsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListAgentsAnchor] = UNSET,
) -> Response[Union[AgentList, Error]]:
    """List all agents

     Returns AI agents deployed in the workspace. Each agent includes its deployment status, runtime
    configuration, and global inference endpoint URL. Starting with API version 2026-04-28 the response
    is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions keep returning a bare array with all agents.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListAgentsSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListAgentsAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentList, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListAgentsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListAgentsAnchor] = UNSET,
) -> Union[AgentList, Error] | None:
    """List all agents

     Returns AI agents deployed in the workspace. Each agent includes its deployment status, runtime
    configuration, and global inference endpoint URL. Starting with API version 2026-04-28 the response
    is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions keep returning a bare array with all agents.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListAgentsSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListAgentsAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentList, Error]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListAgentsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListAgentsAnchor] = UNSET,
) -> Response[Union[AgentList, Error]]:
    """List all agents

     Returns AI agents deployed in the workspace. Each agent includes its deployment status, runtime
    configuration, and global inference endpoint URL. Starting with API version 2026-04-28 the response
    is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions keep returning a bare array with all agents.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListAgentsSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListAgentsAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AgentList, Error]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListAgentsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListAgentsAnchor] = UNSET,
) -> Union[AgentList, Error] | None:
    """List all agents

     Returns AI agents deployed in the workspace. Each agent includes its deployment status, runtime
    configuration, and global inference endpoint URL. Starting with API version 2026-04-28 the response
    is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions keep returning a bare array with all agents.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListAgentsSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListAgentsAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AgentList, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            sort=sort,
            q=q,
            anchor=anchor,
        )
    ).parsed

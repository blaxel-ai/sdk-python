from http import HTTPStatus
from typing import Any

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
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListAgentsSort | Unset = UNSET,
    q: str | Unset = UNSET,
    anchor: ListAgentsAnchor | Unset = UNSET,
    external_id: str | Unset = UNSET,
    status: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    json_anchor: str | Unset = UNSET
    if not isinstance(anchor, Unset):
        json_anchor = anchor.value

    params["anchor"] = json_anchor

    params["externalId"] = external_id

    params["status"] = status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> AgentList | Error | None:
    if response.status_code == 200:
        response_200 = AgentList.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_401, response)
        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_403, response)
        return response_403

    if response.status_code == 500:
        response_500 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_500, response)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[AgentList | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListAgentsSort | Unset = UNSET,
    q: str | Unset = UNSET,
    anchor: ListAgentsAnchor | Unset = UNSET,
    external_id: str | Unset = UNSET,
    status: str | Unset = UNSET,
) -> Response[AgentList | Error]:
    """List all agents

     Returns AI agents deployed in the workspace. Each agent includes its deployment status, runtime
    configuration, and global inference endpoint URL. Starting with API version 2026-04-28 the response
    is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions keep returning a bare array with all agents.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListAgentsSort | Unset):
        q (str | Unset):
        anchor (ListAgentsAnchor | Unset):
        external_id (str | Unset):
        status (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentList | Error]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
        external_id=external_id,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListAgentsSort | Unset = UNSET,
    q: str | Unset = UNSET,
    anchor: ListAgentsAnchor | Unset = UNSET,
    external_id: str | Unset = UNSET,
    status: str | Unset = UNSET,
) -> AgentList | Error | None:
    """List all agents

     Returns AI agents deployed in the workspace. Each agent includes its deployment status, runtime
    configuration, and global inference endpoint URL. Starting with API version 2026-04-28 the response
    is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions keep returning a bare array with all agents.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListAgentsSort | Unset):
        q (str | Unset):
        anchor (ListAgentsAnchor | Unset):
        external_id (str | Unset):
        status (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentList | Error
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
        external_id=external_id,
        status=status,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListAgentsSort | Unset = UNSET,
    q: str | Unset = UNSET,
    anchor: ListAgentsAnchor | Unset = UNSET,
    external_id: str | Unset = UNSET,
    status: str | Unset = UNSET,
) -> Response[AgentList | Error]:
    """List all agents

     Returns AI agents deployed in the workspace. Each agent includes its deployment status, runtime
    configuration, and global inference endpoint URL. Starting with API version 2026-04-28 the response
    is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions keep returning a bare array with all agents.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListAgentsSort | Unset):
        q (str | Unset):
        anchor (ListAgentsAnchor | Unset):
        external_id (str | Unset):
        status (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentList | Error]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
        external_id=external_id,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListAgentsSort | Unset = UNSET,
    q: str | Unset = UNSET,
    anchor: ListAgentsAnchor | Unset = UNSET,
    external_id: str | Unset = UNSET,
    status: str | Unset = UNSET,
) -> AgentList | Error | None:
    """List all agents

     Returns AI agents deployed in the workspace. Each agent includes its deployment status, runtime
    configuration, and global inference endpoint URL. Starting with API version 2026-04-28 the response
    is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query
    parameters; older versions keep returning a bare array with all agents.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListAgentsSort | Unset):
        q (str | Unset):
        anchor (ListAgentsAnchor | Unset):
        external_id (str | Unset):
        status (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentList | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            sort=sort,
            q=q,
            anchor=anchor,
            external_id=external_id,
            status=status,
        )
    ).parsed

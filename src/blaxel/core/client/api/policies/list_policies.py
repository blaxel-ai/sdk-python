from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.list_policies_anchor import ListPoliciesAnchor
from ...models.list_policies_sort import ListPoliciesSort
from ...models.policy_list import PolicyList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListPoliciesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListPoliciesAnchor] = UNSET,
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
        "url": "/policies",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> PolicyList | None:
    if response.status_code == 200:
        response_200 = PolicyList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[PolicyList]:
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
    sort: Union[Unset, ListPoliciesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListPoliciesAnchor] = UNSET,
) -> Response[PolicyList]:
    """List governance policies

     Returns governance policies in the workspace. Policies control deployment locations, hardware
    flavors, and token limits for agents, functions, and models. Starting with API version 2026-04-28
    the response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and
    `limit` query parameters; older versions keep returning a bare array with all policies.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListPoliciesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListPoliciesAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PolicyList]
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
    sort: Union[Unset, ListPoliciesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListPoliciesAnchor] = UNSET,
) -> PolicyList | None:
    """List governance policies

     Returns governance policies in the workspace. Policies control deployment locations, hardware
    flavors, and token limits for agents, functions, and models. Starting with API version 2026-04-28
    the response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and
    `limit` query parameters; older versions keep returning a bare array with all policies.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListPoliciesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListPoliciesAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PolicyList
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
    sort: Union[Unset, ListPoliciesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListPoliciesAnchor] = UNSET,
) -> Response[PolicyList]:
    """List governance policies

     Returns governance policies in the workspace. Policies control deployment locations, hardware
    flavors, and token limits for agents, functions, and models. Starting with API version 2026-04-28
    the response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and
    `limit` query parameters; older versions keep returning a bare array with all policies.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListPoliciesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListPoliciesAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PolicyList]
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
    sort: Union[Unset, ListPoliciesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListPoliciesAnchor] = UNSET,
) -> PolicyList | None:
    """List governance policies

     Returns governance policies in the workspace. Policies control deployment locations, hardware
    flavors, and token limits for agents, functions, and models. Starting with API version 2026-04-28
    the response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and
    `limit` query parameters; older versions keep returning a bare array with all policies.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListPoliciesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListPoliciesAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PolicyList
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

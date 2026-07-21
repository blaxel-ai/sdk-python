from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.list_sandboxes_anchor import ListSandboxesAnchor
from ...models.list_sandboxes_sort import ListSandboxesSort
from ...models.sandbox_list import SandboxList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    show_terminated: Union[Unset, bool] = False,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListSandboxesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListSandboxesAnchor] = UNSET,
    external_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["showTerminated"] = show_terminated

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

    params["externalId"] = external_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sandboxes",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Error, SandboxList] | None:
    if response.status_code == 200:
        response_200 = SandboxList.from_dict(response.json())

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
) -> Response[Union[Error, SandboxList]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    show_terminated: Union[Unset, bool] = False,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListSandboxesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListSandboxesAnchor] = UNSET,
    external_id: Union[Unset, str] = UNSET,
) -> Response[Union[Error, SandboxList]]:
    """List sandboxes

     Returns sandboxes in the workspace. Each sandbox includes its configuration, status, and endpoint
    URL. Terminated sandboxes are hidden by default; pass `showTerminated=true` to include them.
    Starting with API version 2026-04-28 the response is wrapped in `{data, meta}` and supports cursor
    pagination via the `cursor` and `limit` query parameters; older versions keep returning a bare array
    of all sandboxes.

    Args:
        show_terminated (Union[Unset, bool]):  Default: False.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListSandboxesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListSandboxesAnchor]):
        external_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxList]]
    """

    kwargs = _get_kwargs(
        show_terminated=show_terminated,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
        external_id=external_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    show_terminated: Union[Unset, bool] = False,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListSandboxesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListSandboxesAnchor] = UNSET,
    external_id: Union[Unset, str] = UNSET,
) -> Union[Error, SandboxList] | None:
    """List sandboxes

     Returns sandboxes in the workspace. Each sandbox includes its configuration, status, and endpoint
    URL. Terminated sandboxes are hidden by default; pass `showTerminated=true` to include them.
    Starting with API version 2026-04-28 the response is wrapped in `{data, meta}` and supports cursor
    pagination via the `cursor` and `limit` query parameters; older versions keep returning a bare array
    of all sandboxes.

    Args:
        show_terminated (Union[Unset, bool]):  Default: False.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListSandboxesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListSandboxesAnchor]):
        external_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxList]
    """

    return sync_detailed(
        client=client,
        show_terminated=show_terminated,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
        external_id=external_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    show_terminated: Union[Unset, bool] = False,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListSandboxesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListSandboxesAnchor] = UNSET,
    external_id: Union[Unset, str] = UNSET,
) -> Response[Union[Error, SandboxList]]:
    """List sandboxes

     Returns sandboxes in the workspace. Each sandbox includes its configuration, status, and endpoint
    URL. Terminated sandboxes are hidden by default; pass `showTerminated=true` to include them.
    Starting with API version 2026-04-28 the response is wrapped in `{data, meta}` and supports cursor
    pagination via the `cursor` and `limit` query parameters; older versions keep returning a bare array
    of all sandboxes.

    Args:
        show_terminated (Union[Unset, bool]):  Default: False.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListSandboxesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListSandboxesAnchor]):
        external_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxList]]
    """

    kwargs = _get_kwargs(
        show_terminated=show_terminated,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
        external_id=external_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    show_terminated: Union[Unset, bool] = False,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListSandboxesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListSandboxesAnchor] = UNSET,
    external_id: Union[Unset, str] = UNSET,
) -> Union[Error, SandboxList] | None:
    """List sandboxes

     Returns sandboxes in the workspace. Each sandbox includes its configuration, status, and endpoint
    URL. Terminated sandboxes are hidden by default; pass `showTerminated=true` to include them.
    Starting with API version 2026-04-28 the response is wrapped in `{data, meta}` and supports cursor
    pagination via the `cursor` and `limit` query parameters; older versions keep returning a bare array
    of all sandboxes.

    Args:
        show_terminated (Union[Unset, bool]):  Default: False.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListSandboxesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListSandboxesAnchor]):
        external_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxList]
    """

    return (
        await asyncio_detailed(
            client=client,
            show_terminated=show_terminated,
            cursor=cursor,
            limit=limit,
            sort=sort,
            q=q,
            anchor=anchor,
            external_id=external_id,
        )
    ).parsed

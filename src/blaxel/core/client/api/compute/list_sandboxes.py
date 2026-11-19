from http import HTTPStatus
from typing import Any

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
    show_terminated: bool | Unset = False,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListSandboxesSort | Unset = UNSET,
    q: str | Unset = UNSET,
    anchor: ListSandboxesAnchor | Unset = UNSET,
    status: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["showTerminated"] = show_terminated

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

    params["status"] = status

    params["externalId"] = external_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sandboxes",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Error | SandboxList | None:
    if response.status_code == 200:
        response_200 = SandboxList.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Error | SandboxList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    show_terminated: bool | Unset = False,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListSandboxesSort | Unset = UNSET,
    q: str | Unset = UNSET,
    anchor: ListSandboxesAnchor | Unset = UNSET,
    status: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
) -> Response[Error | SandboxList]:
    """List sandboxes

     Returns sandboxes in the workspace. Each sandbox includes its configuration, status, and endpoint
    URL. Terminated sandboxes are hidden by default; pass `showTerminated=true` to include them.
    Starting with API version 2026-04-28 the response is wrapped in `{data, meta}` and supports cursor
    pagination via the `cursor` and `limit` query parameters; older versions keep returning a bare array
    of all sandboxes.

    Args:
        show_terminated (bool | Unset):  Default: False.
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListSandboxesSort | Unset):
        q (str | Unset):
        anchor (ListSandboxesAnchor | Unset):
        status (str | Unset):
        external_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxList]
    """

    kwargs = _get_kwargs(
        show_terminated=show_terminated,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
        status=status,
        external_id=external_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    show_terminated: bool | Unset = False,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListSandboxesSort | Unset = UNSET,
    q: str | Unset = UNSET,
    anchor: ListSandboxesAnchor | Unset = UNSET,
    status: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
) -> Error | SandboxList | None:
    """List sandboxes

     Returns sandboxes in the workspace. Each sandbox includes its configuration, status, and endpoint
    URL. Terminated sandboxes are hidden by default; pass `showTerminated=true` to include them.
    Starting with API version 2026-04-28 the response is wrapped in `{data, meta}` and supports cursor
    pagination via the `cursor` and `limit` query parameters; older versions keep returning a bare array
    of all sandboxes.

    Args:
        show_terminated (bool | Unset):  Default: False.
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListSandboxesSort | Unset):
        q (str | Unset):
        anchor (ListSandboxesAnchor | Unset):
        status (str | Unset):
        external_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxList
    """

    return sync_detailed(
        client=client,
        show_terminated=show_terminated,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
        status=status,
        external_id=external_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    show_terminated: bool | Unset = False,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListSandboxesSort | Unset = UNSET,
    q: str | Unset = UNSET,
    anchor: ListSandboxesAnchor | Unset = UNSET,
    status: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
) -> Response[Error | SandboxList]:
    """List sandboxes

     Returns sandboxes in the workspace. Each sandbox includes its configuration, status, and endpoint
    URL. Terminated sandboxes are hidden by default; pass `showTerminated=true` to include them.
    Starting with API version 2026-04-28 the response is wrapped in `{data, meta}` and supports cursor
    pagination via the `cursor` and `limit` query parameters; older versions keep returning a bare array
    of all sandboxes.

    Args:
        show_terminated (bool | Unset):  Default: False.
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListSandboxesSort | Unset):
        q (str | Unset):
        anchor (ListSandboxesAnchor | Unset):
        status (str | Unset):
        external_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxList]
    """

    kwargs = _get_kwargs(
        show_terminated=show_terminated,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
        status=status,
        external_id=external_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    show_terminated: bool | Unset = False,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListSandboxesSort | Unset = UNSET,
    q: str | Unset = UNSET,
    anchor: ListSandboxesAnchor | Unset = UNSET,
    status: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
) -> Error | SandboxList | None:
    """List sandboxes

     Returns sandboxes in the workspace. Each sandbox includes its configuration, status, and endpoint
    URL. Terminated sandboxes are hidden by default; pass `showTerminated=true` to include them.
    Starting with API version 2026-04-28 the response is wrapped in `{data, meta}` and supports cursor
    pagination via the `cursor` and `limit` query parameters; older versions keep returning a bare array
    of all sandboxes.

    Args:
        show_terminated (bool | Unset):  Default: False.
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListSandboxesSort | Unset):
        q (str | Unset):
        anchor (ListSandboxesAnchor | Unset):
        status (str | Unset):
        external_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxList
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
            status=status,
            external_id=external_id,
        )
    ).parsed

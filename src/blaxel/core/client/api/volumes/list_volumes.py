from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.list_volumes_anchor import ListVolumesAnchor
from ...models.list_volumes_sort import ListVolumesSort
from ...models.volume_list import VolumeList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListVolumesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListVolumesAnchor] = UNSET,
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
        "url": "/volumes",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Error, VolumeList] | None:
    if response.status_code == 200:
        response_200 = VolumeList.from_dict(response.json())

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
) -> Response[Union[Error, VolumeList]]:
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
    sort: Union[Unset, ListVolumesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListVolumesAnchor] = UNSET,
) -> Response[Union[Error, VolumeList]]:
    """List persistent volumes

     Returns persistent storage volumes in the workspace. Volumes can be attached to sandboxes for
    durable file storage that persists across sessions and sandbox deletions. Starting with API version
    2026-04-28 the response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor`
    and `limit` query parameters; older versions keep returning a bare array of volumes.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListVolumesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListVolumesAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, VolumeList]]
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
    sort: Union[Unset, ListVolumesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListVolumesAnchor] = UNSET,
) -> Union[Error, VolumeList] | None:
    """List persistent volumes

     Returns persistent storage volumes in the workspace. Volumes can be attached to sandboxes for
    durable file storage that persists across sessions and sandbox deletions. Starting with API version
    2026-04-28 the response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor`
    and `limit` query parameters; older versions keep returning a bare array of volumes.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListVolumesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListVolumesAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, VolumeList]
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
    sort: Union[Unset, ListVolumesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListVolumesAnchor] = UNSET,
) -> Response[Union[Error, VolumeList]]:
    """List persistent volumes

     Returns persistent storage volumes in the workspace. Volumes can be attached to sandboxes for
    durable file storage that persists across sessions and sandbox deletions. Starting with API version
    2026-04-28 the response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor`
    and `limit` query parameters; older versions keep returning a bare array of volumes.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListVolumesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListVolumesAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, VolumeList]]
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
    sort: Union[Unset, ListVolumesSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListVolumesAnchor] = UNSET,
) -> Union[Error, VolumeList] | None:
    """List persistent volumes

     Returns persistent storage volumes in the workspace. Volumes can be attached to sandboxes for
    durable file storage that persists across sessions and sandbox deletions. Starting with API version
    2026-04-28 the response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor`
    and `limit` query parameters; older versions keep returning a bare array of volumes.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListVolumesSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListVolumesAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, VolumeList]
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

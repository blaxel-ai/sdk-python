from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.list_image_tags_response_200 import ListImageTagsResponse200
from ...models.list_image_tags_sort import ListImageTagsSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    resource_type: str,
    image_name: str,
    *,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListImageTagsSort | Unset = ListImageTagsSort.NAMEASC,
    q: str | Unset = UNSET,
    name: str | Unset = UNSET,
    source_workspace: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    params["name"] = name

    params["sourceWorkspace"] = source_workspace

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/images/{resource_type}/{image_name}/tags".format(
            resource_type=quote(str(resource_type), safe=""),
            image_name=quote(str(image_name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> ListImageTagsResponse200 | None:
    if response.status_code == 200:
        response_200 = ListImageTagsResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[ListImageTagsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListImageTagsSort | Unset = ListImageTagsSort.NAMEASC,
    q: str | Unset = UNSET,
    name: str | Unset = UNSET,
    source_workspace: str | Unset = UNSET,
) -> Response[ListImageTagsResponse200]:
    """List image tags

     Returns a bounded page of image tags. Search by prefix or exact name. Tags are ordered by name only.
    Send Blaxel-Version 2026-09-22 with image catalog requests.

    Args:
        resource_type (str):
        image_name (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListImageTagsSort | Unset):  Default: ListImageTagsSort.NAMEASC.
        q (str | Unset):
        name (str | Unset):
        source_workspace (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListImageTagsResponse200]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        name=name,
        source_workspace=source_workspace,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListImageTagsSort | Unset = ListImageTagsSort.NAMEASC,
    q: str | Unset = UNSET,
    name: str | Unset = UNSET,
    source_workspace: str | Unset = UNSET,
) -> ListImageTagsResponse200 | None:
    """List image tags

     Returns a bounded page of image tags. Search by prefix or exact name. Tags are ordered by name only.
    Send Blaxel-Version 2026-09-22 with image catalog requests.

    Args:
        resource_type (str):
        image_name (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListImageTagsSort | Unset):  Default: ListImageTagsSort.NAMEASC.
        q (str | Unset):
        name (str | Unset):
        source_workspace (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListImageTagsResponse200
    """

    return sync_detailed(
        resource_type=resource_type,
        image_name=image_name,
        client=client,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        name=name,
        source_workspace=source_workspace,
    ).parsed


async def asyncio_detailed(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListImageTagsSort | Unset = ListImageTagsSort.NAMEASC,
    q: str | Unset = UNSET,
    name: str | Unset = UNSET,
    source_workspace: str | Unset = UNSET,
) -> Response[ListImageTagsResponse200]:
    """List image tags

     Returns a bounded page of image tags. Search by prefix or exact name. Tags are ordered by name only.
    Send Blaxel-Version 2026-09-22 with image catalog requests.

    Args:
        resource_type (str):
        image_name (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListImageTagsSort | Unset):  Default: ListImageTagsSort.NAMEASC.
        q (str | Unset):
        name (str | Unset):
        source_workspace (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListImageTagsResponse200]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        name=name,
        source_workspace=source_workspace,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListImageTagsSort | Unset = ListImageTagsSort.NAMEASC,
    q: str | Unset = UNSET,
    name: str | Unset = UNSET,
    source_workspace: str | Unset = UNSET,
) -> ListImageTagsResponse200 | None:
    """List image tags

     Returns a bounded page of image tags. Search by prefix or exact name. Tags are ordered by name only.
    Send Blaxel-Version 2026-09-22 with image catalog requests.

    Args:
        resource_type (str):
        image_name (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListImageTagsSort | Unset):  Default: ListImageTagsSort.NAMEASC.
        q (str | Unset):
        name (str | Unset):
        source_workspace (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListImageTagsResponse200
    """

    return (
        await asyncio_detailed(
            resource_type=resource_type,
            image_name=image_name,
            client=client,
            cursor=cursor,
            limit=limit,
            sort=sort,
            q=q,
            name=name,
            source_workspace=source_workspace,
        )
    ).parsed

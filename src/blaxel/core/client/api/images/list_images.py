from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.list_images_response_200 import ListImagesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: str | Unset = UNSET,
    q: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    params["sort"] = sort

    params["q"] = q

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/images",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> ListImagesResponse200 | None:
    if response.status_code == 200:
        response_200 = ListImagesResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ListImagesResponse200]:
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
    sort: str | Unset = UNSET,
    q: str | Unset = UNSET,
) -> Response[ListImagesResponse200]:
    """List container images

     Returns paginated image summaries starting with API version 2026-09-22. Older versions return a bare
    array including all tags.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (str | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListImagesResponse200]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
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
    sort: str | Unset = UNSET,
    q: str | Unset = UNSET,
) -> ListImagesResponse200 | None:
    """List container images

     Returns paginated image summaries starting with API version 2026-09-22. Older versions return a bare
    array including all tags.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (str | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListImagesResponse200
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: str | Unset = UNSET,
    q: str | Unset = UNSET,
) -> Response[ListImagesResponse200]:
    """List container images

     Returns paginated image summaries starting with API version 2026-09-22. Older versions return a bare
    array including all tags.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (str | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListImagesResponse200]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: str | Unset = UNSET,
    q: str | Unset = UNSET,
) -> ListImagesResponse200 | None:
    """List container images

     Returns paginated image summaries starting with API version 2026-09-22. Older versions return a bare
    array including all tags.

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (str | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListImagesResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            sort=sort,
            q=q,
        )
    ).parsed

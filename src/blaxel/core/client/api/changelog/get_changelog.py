from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.changelog_response import ChangelogResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/changelog",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> ChangelogResponse | None:
    if response.status_code == 200:
        response_200 = ChangelogResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ChangelogResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[ChangelogResponse]:
    """Get latest changelog entries

     Returns the latest public changelog entries for the controlplane UI. The origin response is
    intentionally not cached in memory; CloudFront caches this endpoint according to the Cache-Control
    header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangelogResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
) -> ChangelogResponse | None:
    """Get latest changelog entries

     Returns the latest public changelog entries for the controlplane UI. The origin response is
    intentionally not cached in memory; CloudFront caches this endpoint according to the Cache-Control
    header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangelogResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[ChangelogResponse]:
    """Get latest changelog entries

     Returns the latest public changelog entries for the controlplane UI. The origin response is
    intentionally not cached in memory; CloudFront caches this endpoint according to the Cache-Control
    header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangelogResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
) -> ChangelogResponse | None:
    """Get latest changelog entries

     Returns the latest public changelog entries for the controlplane UI. The origin response is
    intentionally not cached in memory; CloudFront caches this endpoint according to the Cache-Control
    header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangelogResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

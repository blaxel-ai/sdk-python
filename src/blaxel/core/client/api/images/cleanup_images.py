from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.cleanup_images_response_200 import CleanupImagesResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/images",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> CleanupImagesResponse200 | None:
    if response.status_code == 200:
        response_200 = CleanupImagesResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[CleanupImagesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[CleanupImagesResponse200]:
    """Cleanup unused container images

     Cleans up unused container images in the workspace registry. Only removes images that are not
    currently referenced by any active agent, function, sandbox, or job deployment.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CleanupImagesResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
) -> CleanupImagesResponse200 | None:
    """Cleanup unused container images

     Cleans up unused container images in the workspace registry. Only removes images that are not
    currently referenced by any active agent, function, sandbox, or job deployment.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CleanupImagesResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[CleanupImagesResponse200]:
    """Cleanup unused container images

     Cleans up unused container images in the workspace registry. Only removes images that are not
    currently referenced by any active agent, function, sandbox, or job deployment.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CleanupImagesResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
) -> CleanupImagesResponse200 | None:
    """Cleanup unused container images

     Cleans up unused container images in the workspace registry. Only removes images that are not
    currently referenced by any active agent, function, sandbox, or job deployment.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CleanupImagesResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.preview import Preview
from ...types import Response


def _get_kwargs(
    sandbox_name: str,
    preview_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sandboxes/{sandbox_name}/previews/{preview_name}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Preview]:
    if response.status_code == 200:
        response_200 = Preview.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Preview]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_name: str,
    preview_name: str,
    *,
    client: Union[Client],
) -> Response[Preview]:
    """Get Sandbox Preview

     Returns a Sandbox Preview by name.

    Args:
        sandbox_name (str):
        preview_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Preview]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        preview_name=preview_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_name: str,
    preview_name: str,
    *,
    client: Union[Client],
) -> Optional[Preview]:
    """Get Sandbox Preview

     Returns a Sandbox Preview by name.

    Args:
        sandbox_name (str):
        preview_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Preview
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        preview_name=preview_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    preview_name: str,
    *,
    client: Union[Client],
) -> Response[Preview]:
    """Get Sandbox Preview

     Returns a Sandbox Preview by name.

    Args:
        sandbox_name (str):
        preview_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Preview]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        preview_name=preview_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    preview_name: str,
    *,
    client: Union[Client],
) -> Optional[Preview]:
    """Get Sandbox Preview

     Returns a Sandbox Preview by name.

    Args:
        sandbox_name (str):
        preview_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Preview
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            preview_name=preview_name,
            client=client,
        )
    ).parsed

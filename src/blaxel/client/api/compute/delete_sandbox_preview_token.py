from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.delete_sandbox_preview_token_response_200 import DeleteSandboxPreviewTokenResponse200
from ...types import Response


def _get_kwargs(
    sandbox_name: str,
    preview_name: str,
    token_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/sandboxes/{sandbox_name}/previews/{preview_name}/tokens/{token_name}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[DeleteSandboxPreviewTokenResponse200]:
    if response.status_code == 200:
        response_200 = DeleteSandboxPreviewTokenResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[DeleteSandboxPreviewTokenResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_name: str,
    preview_name: str,
    token_name: str,
    *,
    client: Union[Client],
) -> Response[DeleteSandboxPreviewTokenResponse200]:
    """Delete token for Sandbox Preview

     Deletes a token for a Sandbox Preview by name.

    Args:
        sandbox_name (str):
        preview_name (str):
        token_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteSandboxPreviewTokenResponse200]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        preview_name=preview_name,
        token_name=token_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_name: str,
    preview_name: str,
    token_name: str,
    *,
    client: Union[Client],
) -> Optional[DeleteSandboxPreviewTokenResponse200]:
    """Delete token for Sandbox Preview

     Deletes a token for a Sandbox Preview by name.

    Args:
        sandbox_name (str):
        preview_name (str):
        token_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteSandboxPreviewTokenResponse200
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        preview_name=preview_name,
        token_name=token_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    preview_name: str,
    token_name: str,
    *,
    client: Union[Client],
) -> Response[DeleteSandboxPreviewTokenResponse200]:
    """Delete token for Sandbox Preview

     Deletes a token for a Sandbox Preview by name.

    Args:
        sandbox_name (str):
        preview_name (str):
        token_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteSandboxPreviewTokenResponse200]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        preview_name=preview_name,
        token_name=token_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    preview_name: str,
    token_name: str,
    *,
    client: Union[Client],
) -> Optional[DeleteSandboxPreviewTokenResponse200]:
    """Delete token for Sandbox Preview

     Deletes a token for a Sandbox Preview by name.

    Args:
        sandbox_name (str):
        preview_name (str):
        token_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteSandboxPreviewTokenResponse200
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            preview_name=preview_name,
            token_name=token_name,
            client=client,
        )
    ).parsed

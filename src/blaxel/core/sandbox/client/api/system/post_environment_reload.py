from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.handler_reload_response import HandlerReloadResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/environment/reload",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[ErrorResponse, HandlerReloadResponse] | None:
    if response.status_code == 200:
        response_200 = HandlerReloadResponse.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ErrorResponse, HandlerReloadResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Union[ErrorResponse, HandlerReloadResponse]]:
    """Reload environment from guest metadata

     Re-reads /bl/metadata and applies its environment to the sandbox-api process, so this process and
    every process started afterwards see the current values. Called by the guest init after an
    environment update; safe to call manually.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, HandlerReloadResponse]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
) -> Union[ErrorResponse, HandlerReloadResponse] | None:
    """Reload environment from guest metadata

     Re-reads /bl/metadata and applies its environment to the sandbox-api process, so this process and
    every process started afterwards see the current values. Called by the guest init after an
    environment update; safe to call manually.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, HandlerReloadResponse]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Union[ErrorResponse, HandlerReloadResponse]]:
    """Reload environment from guest metadata

     Re-reads /bl/metadata and applies its environment to the sandbox-api process, so this process and
    every process started afterwards see the current values. Called by the guest init after an
    environment update; safe to call manually.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, HandlerReloadResponse]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
) -> Union[ErrorResponse, HandlerReloadResponse] | None:
    """Reload environment from guest metadata

     Re-reads /bl/metadata and applies its environment to the sandbox-api process, so this process and
    every process started afterwards see the current values. Called by the guest init after an
    environment update; safe to call manually.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, HandlerReloadResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

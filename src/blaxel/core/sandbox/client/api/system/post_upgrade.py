from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.success_response import SuccessResponse
from ...models.upgrade_request import UpgradeRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: UpgradeRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/upgrade",
    }

    if body and not isinstance(body, Unset) and not isinstance(body, dict):
        _kwargs["json"] = body.to_dict()
    elif body and isinstance(body, dict):
        _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> ErrorResponse | SuccessResponse | None:
    if response.status_code == 200:
        response_200 = SuccessResponse.from_dict(response.json())

        return response_200

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(errors.error_json(response))

        errors.retain_response(response_500, response)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[ErrorResponse | SuccessResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: UpgradeRequest | Unset = UNSET,
) -> Response[ErrorResponse | SuccessResponse]:
    """Upgrade the sandbox-api

     Triggers an upgrade of the sandbox-api process. Returns 200 immediately before upgrading.
    The upgrade will: download the specified binary from GitHub releases, validate it, and restart.
    All running processes will be preserved across the upgrade.
    Available versions: "latest" (default, most recent release), "develop", "main", or specific tag like
    "v1.0.0"
    You can also specify a custom baseUrl for forks (defaults to https://github.com/blaxel-
    ai/sandbox/releases)

    Args:
        body (UpgradeRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SuccessResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    body: UpgradeRequest | Unset = UNSET,
) -> ErrorResponse | SuccessResponse | None:
    """Upgrade the sandbox-api

     Triggers an upgrade of the sandbox-api process. Returns 200 immediately before upgrading.
    The upgrade will: download the specified binary from GitHub releases, validate it, and restart.
    All running processes will be preserved across the upgrade.
    Available versions: "latest" (default, most recent release), "develop", "main", or specific tag like
    "v1.0.0"
    You can also specify a custom baseUrl for forks (defaults to https://github.com/blaxel-
    ai/sandbox/releases)

    Args:
        body (UpgradeRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SuccessResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: UpgradeRequest | Unset = UNSET,
) -> Response[ErrorResponse | SuccessResponse]:
    """Upgrade the sandbox-api

     Triggers an upgrade of the sandbox-api process. Returns 200 immediately before upgrading.
    The upgrade will: download the specified binary from GitHub releases, validate it, and restart.
    All running processes will be preserved across the upgrade.
    Available versions: "latest" (default, most recent release), "develop", "main", or specific tag like
    "v1.0.0"
    You can also specify a custom baseUrl for forks (defaults to https://github.com/blaxel-
    ai/sandbox/releases)

    Args:
        body (UpgradeRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SuccessResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: UpgradeRequest | Unset = UNSET,
) -> ErrorResponse | SuccessResponse | None:
    """Upgrade the sandbox-api

     Triggers an upgrade of the sandbox-api process. Returns 200 immediately before upgrading.
    The upgrade will: download the specified binary from GitHub releases, validate it, and restart.
    All running processes will be preserved across the upgrade.
    Available versions: "latest" (default, most recent release), "develop", "main", or specific tag like
    "v1.0.0"
    You can also specify a custom baseUrl for forks (defaults to https://github.com/blaxel-
    ai/sandbox/releases)

    Args:
        body (UpgradeRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SuccessResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

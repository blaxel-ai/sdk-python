from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.secret import Secret
from ...types import Response


def _get_kwargs(
    *,
    body: Secret,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/secrets",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Secret | None:
    if response.status_code == 200:
        response_200 = Secret.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Secret]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: Secret,
) -> Response[Secret]:
    """Upsert secret

     Creates or updates a secret by name. Each call stores a new immutable version; the latest version is
    the one resolved by the proxy.

    Args:
        body (Secret): Workspace secret, referenced from proxy routing as {{SECRET:name}}. Values
            are write-only and can never be read back. Every upsert stores a new immutable version and
            the latest one is resolved at runtime.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Secret]
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
    body: Secret,
) -> Secret | None:
    """Upsert secret

     Creates or updates a secret by name. Each call stores a new immutable version; the latest version is
    the one resolved by the proxy.

    Args:
        body (Secret): Workspace secret, referenced from proxy routing as {{SECRET:name}}. Values
            are write-only and can never be read back. Every upsert stores a new immutable version and
            the latest one is resolved at runtime.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Secret
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: Secret,
) -> Response[Secret]:
    """Upsert secret

     Creates or updates a secret by name. Each call stores a new immutable version; the latest version is
    the one resolved by the proxy.

    Args:
        body (Secret): Workspace secret, referenced from proxy routing as {{SECRET:name}}. Values
            are write-only and can never be read back. Every upsert stores a new immutable version and
            the latest one is resolved at runtime.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Secret]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: Secret,
) -> Secret | None:
    """Upsert secret

     Creates or updates a secret by name. Each call stores a new immutable version; the latest version is
    the one resolved by the proxy.

    Args:
        body (Secret): Workspace secret, referenced from proxy routing as {{SECRET:name}}. Values
            are write-only and can never be read back. Every upsert stores a new immutable version and
            the latest one is resolved at runtime.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Secret
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

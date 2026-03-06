from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.get_drive_jwks_response_200 import GetDriveJWKSResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/drives/jwks.json",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> GetDriveJWKSResponse200 | None:
    if response.status_code == 200:
        response_200 = GetDriveJWKSResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[GetDriveJWKSResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[GetDriveJWKSResponse200]:
    """Get drive token JWKS

     Returns the JSON Web Key Set containing the Ed25519 public key used to verify drive access tokens.
    SeaweedFS or other S3-compatible storage can use this endpoint to validate Bearer tokens.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDriveJWKSResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
) -> GetDriveJWKSResponse200 | None:
    """Get drive token JWKS

     Returns the JSON Web Key Set containing the Ed25519 public key used to verify drive access tokens.
    SeaweedFS or other S3-compatible storage can use this endpoint to validate Bearer tokens.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDriveJWKSResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[GetDriveJWKSResponse200]:
    """Get drive token JWKS

     Returns the JSON Web Key Set containing the Ed25519 public key used to verify drive access tokens.
    SeaweedFS or other S3-compatible storage can use this endpoint to validate Bearer tokens.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDriveJWKSResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
) -> GetDriveJWKSResponse200 | None:
    """Get drive token JWKS

     Returns the JSON Web Key Set containing the Ed25519 public key used to verify drive access tokens.
    SeaweedFS or other S3-compatible storage can use this endpoint to validate Bearer tokens.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDriveJWKSResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

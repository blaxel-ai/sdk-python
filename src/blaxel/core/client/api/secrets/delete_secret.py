from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.secret import Secret
from ...types import Response


def _get_kwargs(
    secret_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/secrets/{secret_name}",
    }

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
    secret_name: str,
    *,
    client: Client,
) -> Response[Secret]:
    """Delete secret

     Deletes a secret and all its versions from the workspace.

    Args:
        secret_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Secret]
    """

    kwargs = _get_kwargs(
        secret_name=secret_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    secret_name: str,
    *,
    client: Client,
) -> Secret | None:
    """Delete secret

     Deletes a secret and all its versions from the workspace.

    Args:
        secret_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Secret
    """

    return sync_detailed(
        secret_name=secret_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    secret_name: str,
    *,
    client: Client,
) -> Response[Secret]:
    """Delete secret

     Deletes a secret and all its versions from the workspace.

    Args:
        secret_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Secret]
    """

    kwargs = _get_kwargs(
        secret_name=secret_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    secret_name: str,
    *,
    client: Client,
) -> Secret | None:
    """Delete secret

     Deletes a secret and all its versions from the workspace.

    Args:
        secret_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Secret
    """

    return (
        await asyncio_detailed(
            secret_name=secret_name,
            client=client,
        )
    ).parsed

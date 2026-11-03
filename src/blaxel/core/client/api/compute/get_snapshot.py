from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.sandbox_snapshot import SandboxSnapshot
from ...types import Response


def _get_kwargs(
    snapshot_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/snapshots/{snapshot_name}".format(
            snapshot_name=quote(str(snapshot_name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Error | SandboxSnapshot | None:
    if response.status_code == 200:
        response_200 = SandboxSnapshot.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        errors.retain_response(response_404, response)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Error | SandboxSnapshot]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    snapshot_name: str,
    *,
    client: Client,
) -> Response[Error | SandboxSnapshot]:
    """Get snapshot

     Returns a snapshot of the workspace by ID.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxSnapshot]
    """

    kwargs = _get_kwargs(
        snapshot_name=snapshot_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    snapshot_name: str,
    *,
    client: Client,
) -> Error | SandboxSnapshot | None:
    """Get snapshot

     Returns a snapshot of the workspace by ID.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxSnapshot
    """

    return sync_detailed(
        snapshot_name=snapshot_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    snapshot_name: str,
    *,
    client: Client,
) -> Response[Error | SandboxSnapshot]:
    """Get snapshot

     Returns a snapshot of the workspace by ID.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxSnapshot]
    """

    kwargs = _get_kwargs(
        snapshot_name=snapshot_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    snapshot_name: str,
    *,
    client: Client,
) -> Error | SandboxSnapshot | None:
    """Get snapshot

     Returns a snapshot of the workspace by ID.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxSnapshot
    """

    return (
        await asyncio_detailed(
            snapshot_name=snapshot_name,
            client=client,
        )
    ).parsed

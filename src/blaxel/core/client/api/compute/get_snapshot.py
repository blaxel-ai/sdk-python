from http import HTTPStatus
from typing import Any, Union

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
        "url": f"/snapshots/{snapshot_name}",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Error, SandboxSnapshot] | None:
    if response.status_code == 200:
        response_200 = SandboxSnapshot.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Error, SandboxSnapshot]]:
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
) -> Response[Union[Error, SandboxSnapshot]]:
    """Get snapshot

     Returns a snapshot of the workspace by name.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxSnapshot]]
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
) -> Union[Error, SandboxSnapshot] | None:
    """Get snapshot

     Returns a snapshot of the workspace by name.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxSnapshot]
    """

    return sync_detailed(
        snapshot_name=snapshot_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    snapshot_name: str,
    *,
    client: Client,
) -> Response[Union[Error, SandboxSnapshot]]:
    """Get snapshot

     Returns a snapshot of the workspace by name.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxSnapshot]]
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
) -> Union[Error, SandboxSnapshot] | None:
    """Get snapshot

     Returns a snapshot of the workspace by name.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxSnapshot]
    """

    return (
        await asyncio_detailed(
            snapshot_name=snapshot_name,
            client=client,
        )
    ).parsed

from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.sandbox_restore_response import SandboxRestoreResponse
from ...types import Response


def _get_kwargs(
    sandbox_name: str,
    snapshot_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sandboxes/{sandbox_name}/snapshots/{snapshot_id}/restore".format(
            sandbox_name=quote(str(sandbox_name), safe=""),
            snapshot_id=quote(str(snapshot_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Error | SandboxRestoreResponse | None:
    if response.status_code == 200:
        response_200 = SandboxRestoreResponse.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        errors.retain_response(response_404, response)
        return response_404

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

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
) -> Response[Error | SandboxRestoreResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_name: str,
    snapshot_id: str,
    *,
    client: Client,
) -> Response[Error | SandboxRestoreResponse]:
    """Restore sandbox from snapshot

     Restores a sandbox to one of its own snapshots. The running sandbox is torn down and rebuilt from
    the snapshot under the same name and URLs, so everything it held since the snapshot was taken is
    lost unless it was itself snapshotted.

    Args:
        sandbox_name (str):
        snapshot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxRestoreResponse]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        snapshot_id=snapshot_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_name: str,
    snapshot_id: str,
    *,
    client: Client,
) -> Error | SandboxRestoreResponse | None:
    """Restore sandbox from snapshot

     Restores a sandbox to one of its own snapshots. The running sandbox is torn down and rebuilt from
    the snapshot under the same name and URLs, so everything it held since the snapshot was taken is
    lost unless it was itself snapshotted.

    Args:
        sandbox_name (str):
        snapshot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxRestoreResponse
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        snapshot_id=snapshot_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    snapshot_id: str,
    *,
    client: Client,
) -> Response[Error | SandboxRestoreResponse]:
    """Restore sandbox from snapshot

     Restores a sandbox to one of its own snapshots. The running sandbox is torn down and rebuilt from
    the snapshot under the same name and URLs, so everything it held since the snapshot was taken is
    lost unless it was itself snapshotted.

    Args:
        sandbox_name (str):
        snapshot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxRestoreResponse]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        snapshot_id=snapshot_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    snapshot_id: str,
    *,
    client: Client,
) -> Error | SandboxRestoreResponse | None:
    """Restore sandbox from snapshot

     Restores a sandbox to one of its own snapshots. The running sandbox is torn down and rebuilt from
    the snapshot under the same name and URLs, so everything it held since the snapshot was taken is
    lost unless it was itself snapshotted.

    Args:
        sandbox_name (str):
        snapshot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxRestoreResponse
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            snapshot_id=snapshot_id,
            client=client,
        )
    ).parsed

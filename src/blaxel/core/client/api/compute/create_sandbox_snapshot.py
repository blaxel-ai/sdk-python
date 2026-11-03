from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.sandbox_snapshot import SandboxSnapshot
from ...models.sandbox_snapshot_request import SandboxSnapshotRequest
from ...types import Response


def _get_kwargs(
    sandbox_name: str,
    *,
    body: SandboxSnapshotRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sandboxes/{sandbox_name}/snapshots".format(
            sandbox_name=quote(str(sandbox_name), safe=""),
        ),
    }

    if type(body) is dict:
        _kwargs["json"] = body
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Error | SandboxSnapshot | None:
    if response.status_code == 200:
        response_200 = SandboxSnapshot.from_dict(response.json())

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
) -> Response[Error | SandboxSnapshot]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_name: str,
    *,
    client: Client,
    body: SandboxSnapshotRequest,
) -> Response[Error | SandboxSnapshot]:
    """Create sandbox snapshot

     Creates a point-in-time snapshot of a sandbox. Snapshots capture the sandbox state and can be used
    for forking into new sandboxes or applications. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxSnapshotRequest): Request body for creating a snapshot. The source object is
            required at the root endpoint and implied by the path on the nested one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxSnapshot]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_name: str,
    *,
    client: Client,
    body: SandboxSnapshotRequest,
) -> Error | SandboxSnapshot | None:
    """Create sandbox snapshot

     Creates a point-in-time snapshot of a sandbox. Snapshots capture the sandbox state and can be used
    for forking into new sandboxes or applications. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxSnapshotRequest): Request body for creating a snapshot. The source object is
            required at the root endpoint and implied by the path on the nested one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxSnapshot
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    *,
    client: Client,
    body: SandboxSnapshotRequest,
) -> Response[Error | SandboxSnapshot]:
    """Create sandbox snapshot

     Creates a point-in-time snapshot of a sandbox. Snapshots capture the sandbox state and can be used
    for forking into new sandboxes or applications. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxSnapshotRequest): Request body for creating a snapshot. The source object is
            required at the root endpoint and implied by the path on the nested one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxSnapshot]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    *,
    client: Client,
    body: SandboxSnapshotRequest,
) -> Error | SandboxSnapshot | None:
    """Create sandbox snapshot

     Creates a point-in-time snapshot of a sandbox. Snapshots capture the sandbox state and can be used
    for forking into new sandboxes or applications. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxSnapshotRequest): Request body for creating a snapshot. The source object is
            required at the root endpoint and implied by the path on the nested one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxSnapshot
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            client=client,
            body=body,
        )
    ).parsed

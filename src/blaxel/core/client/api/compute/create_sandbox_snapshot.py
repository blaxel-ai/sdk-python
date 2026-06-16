from http import HTTPStatus
from typing import Any, Union

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
        "url": f"/sandboxes/{sandbox_name}/snapshots",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
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
    sandbox_name: str,
    *,
    client: Client,
    body: SandboxSnapshotRequest,
) -> Response[Union[Error, SandboxSnapshot]]:
    """Create sandbox snapshot

     Creates a point-in-time snapshot of a sandbox. Snapshots capture the sandbox state and can be used
    for forking into new sandboxes or applications. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxSnapshotRequest): Request body for creating a snapshot of a sandbox. Captures
            the current sandbox state.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxSnapshot]]
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
) -> Union[Error, SandboxSnapshot] | None:
    """Create sandbox snapshot

     Creates a point-in-time snapshot of a sandbox. Snapshots capture the sandbox state and can be used
    for forking into new sandboxes or applications. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxSnapshotRequest): Request body for creating a snapshot of a sandbox. Captures
            the current sandbox state.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxSnapshot]
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
) -> Response[Union[Error, SandboxSnapshot]]:
    """Create sandbox snapshot

     Creates a point-in-time snapshot of a sandbox. Snapshots capture the sandbox state and can be used
    for forking into new sandboxes or applications. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxSnapshotRequest): Request body for creating a snapshot of a sandbox. Captures
            the current sandbox state.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxSnapshot]]
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
) -> Union[Error, SandboxSnapshot] | None:
    """Create sandbox snapshot

     Creates a point-in-time snapshot of a sandbox. Snapshots capture the sandbox state and can be used
    for forking into new sandboxes or applications. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxSnapshotRequest): Request body for creating a snapshot of a sandbox. Captures
            the current sandbox state.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxSnapshot]
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            client=client,
            body=body,
        )
    ).parsed

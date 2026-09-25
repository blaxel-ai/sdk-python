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
    *,
    body: SandboxSnapshotRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/snapshots",
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
    *,
    client: Client,
    body: SandboxSnapshotRequest,
) -> Response[Union[Error, SandboxSnapshot]]:
    """Create snapshot

     Captures a snapshot from a source object. The snapshot belongs to the workspace rather than to its
    source, so it survives the deletion of the object it was captured from, and carries what creating a
    sandbox or an application from it needs.

    Args:
        body (SandboxSnapshotRequest): Request body for creating a snapshot. The source object is
            required at the root endpoint and implied by the path on the nested one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxSnapshot]]
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
    body: SandboxSnapshotRequest,
) -> Union[Error, SandboxSnapshot] | None:
    """Create snapshot

     Captures a snapshot from a source object. The snapshot belongs to the workspace rather than to its
    source, so it survives the deletion of the object it was captured from, and carries what creating a
    sandbox or an application from it needs.

    Args:
        body (SandboxSnapshotRequest): Request body for creating a snapshot. The source object is
            required at the root endpoint and implied by the path on the nested one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxSnapshot]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: SandboxSnapshotRequest,
) -> Response[Union[Error, SandboxSnapshot]]:
    """Create snapshot

     Captures a snapshot from a source object. The snapshot belongs to the workspace rather than to its
    source, so it survives the deletion of the object it was captured from, and carries what creating a
    sandbox or an application from it needs.

    Args:
        body (SandboxSnapshotRequest): Request body for creating a snapshot. The source object is
            required at the root endpoint and implied by the path on the nested one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxSnapshot]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: SandboxSnapshotRequest,
) -> Union[Error, SandboxSnapshot] | None:
    """Create snapshot

     Captures a snapshot from a source object. The snapshot belongs to the workspace rather than to its
    source, so it survives the deletion of the object it was captured from, and carries what creating a
    sandbox or an application from it needs.

    Args:
        body (SandboxSnapshotRequest): Request body for creating a snapshot. The source object is
            required at the root endpoint and implied by the path on the nested one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxSnapshot]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.sandbox_fork_request import SandboxForkRequest
from ...models.sandbox_fork_response import SandboxForkResponse
from ...types import Response


def _get_kwargs(
    snapshot_name: str,
    *,
    body: SandboxForkRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/snapshots/{snapshot_name}/fork".format(
            snapshot_name=quote(str(snapshot_name), safe=""),
        ),
    }

    if type(body) is dict:
        _kwargs["json"] = body
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Error | SandboxForkResponse | None:
    if response.status_code == 200:
        response_200 = SandboxForkResponse.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_404, response)
        return response_404

    if response.status_code == 500:
        response_500 = Error.from_dict(errors.error_json(response))

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
) -> Response[Error | SandboxForkResponse]:
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
    body: SandboxForkRequest,
) -> Response[Error | SandboxForkResponse]:
    """Fork snapshot

     Creates a new sandbox or application from a snapshot. The snapshot is enough on its own, so this
    works after the object it was captured from has been deleted.

    Args:
        snapshot_name (str):
        body (SandboxForkRequest): Request body for forking a sandbox into an application. Creates
            a new application or adds a canary revision to an existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxForkResponse]
    """

    kwargs = _get_kwargs(
        snapshot_name=snapshot_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    snapshot_name: str,
    *,
    client: Client,
    body: SandboxForkRequest,
) -> Error | SandboxForkResponse | None:
    """Fork snapshot

     Creates a new sandbox or application from a snapshot. The snapshot is enough on its own, so this
    works after the object it was captured from has been deleted.

    Args:
        snapshot_name (str):
        body (SandboxForkRequest): Request body for forking a sandbox into an application. Creates
            a new application or adds a canary revision to an existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxForkResponse
    """

    return sync_detailed(
        snapshot_name=snapshot_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    snapshot_name: str,
    *,
    client: Client,
    body: SandboxForkRequest,
) -> Response[Error | SandboxForkResponse]:
    """Fork snapshot

     Creates a new sandbox or application from a snapshot. The snapshot is enough on its own, so this
    works after the object it was captured from has been deleted.

    Args:
        snapshot_name (str):
        body (SandboxForkRequest): Request body for forking a sandbox into an application. Creates
            a new application or adds a canary revision to an existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxForkResponse]
    """

    kwargs = _get_kwargs(
        snapshot_name=snapshot_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    snapshot_name: str,
    *,
    client: Client,
    body: SandboxForkRequest,
) -> Error | SandboxForkResponse | None:
    """Fork snapshot

     Creates a new sandbox or application from a snapshot. The snapshot is enough on its own, so this
    works after the object it was captured from has been deleted.

    Args:
        snapshot_name (str):
        body (SandboxForkRequest): Request body for forking a sandbox into an application. Creates
            a new application or adds a canary revision to an existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxForkResponse
    """

    return (
        await asyncio_detailed(
            snapshot_name=snapshot_name,
            client=client,
            body=body,
        )
    ).parsed

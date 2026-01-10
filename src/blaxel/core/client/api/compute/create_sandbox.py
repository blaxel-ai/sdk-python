from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.sandbox import Sandbox
from ...models.sandbox_error import SandboxError
from ...types import Response


def _get_kwargs(
    *,
    body: Sandbox,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sandboxes",
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
) -> Union[Sandbox, SandboxError] | None:
    if response.status_code == 200:
        response_200 = Sandbox.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = SandboxError.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = SandboxError.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = SandboxError.from_dict(response.json())

        return response_403
    if response.status_code == 409:
        response_409 = SandboxError.from_dict(response.json())

        return response_409
    if response.status_code == 500:
        response_500 = SandboxError.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Sandbox, SandboxError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: Sandbox,
) -> Response[Union[Sandbox, SandboxError]]:
    """Create sandbox

     Creates a new sandbox VM for secure AI code execution. Sandboxes automatically scale to zero when
    idle and resume instantly, preserving memory state including running processes and filesystem.

    Args:
        body (Sandbox): Lightweight virtual machine for secure AI code execution. Sandboxes resume
            from standby in under 25ms and automatically scale to zero after inactivity, preserving
            memory state including running processes and filesystem.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Sandbox, SandboxError]]
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
    body: Sandbox,
) -> Union[Sandbox, SandboxError] | None:
    """Create sandbox

     Creates a new sandbox VM for secure AI code execution. Sandboxes automatically scale to zero when
    idle and resume instantly, preserving memory state including running processes and filesystem.

    Args:
        body (Sandbox): Lightweight virtual machine for secure AI code execution. Sandboxes resume
            from standby in under 25ms and automatically scale to zero after inactivity, preserving
            memory state including running processes and filesystem.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Sandbox, SandboxError]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: Sandbox,
) -> Response[Union[Sandbox, SandboxError]]:
    """Create sandbox

     Creates a new sandbox VM for secure AI code execution. Sandboxes automatically scale to zero when
    idle and resume instantly, preserving memory state including running processes and filesystem.

    Args:
        body (Sandbox): Lightweight virtual machine for secure AI code execution. Sandboxes resume
            from standby in under 25ms and automatically scale to zero after inactivity, preserving
            memory state including running processes and filesystem.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Sandbox, SandboxError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: Sandbox,
) -> Union[Sandbox, SandboxError] | None:
    """Create sandbox

     Creates a new sandbox VM for secure AI code execution. Sandboxes automatically scale to zero when
    idle and resume instantly, preserving memory state including running processes and filesystem.

    Args:
        body (Sandbox): Lightweight virtual machine for secure AI code execution. Sandboxes resume
            from standby in under 25ms and automatically scale to zero after inactivity, preserving
            memory state including running processes and filesystem.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Sandbox, SandboxError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

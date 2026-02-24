from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.sandbox import Sandbox
from ...types import Response


def _get_kwargs(
    sandbox_name: str,
    *,
    body: Sandbox,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/sandboxes/{sandbox_name}",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Error, Sandbox] | None:
    if response.status_code == 200:
        response_200 = Sandbox.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403
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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Error, Sandbox]]:
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
    body: Sandbox,
) -> Response[Union[Error, Sandbox]]:
    """Update sandbox

     Updates a sandbox's configuration. Note that certain changes (like image or memory) may reset the
    sandbox state. Use lifecycle policies to control automatic cleanup.

    Args:
        sandbox_name (str):
        body (Sandbox): Lightweight virtual machine for secure AI code execution. Sandboxes resume
            from standby in under 25ms and automatically scale to zero after inactivity, preserving
            memory state including running processes and filesystem.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Sandbox]]
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
    body: Sandbox,
) -> Union[Error, Sandbox] | None:
    """Update sandbox

     Updates a sandbox's configuration. Note that certain changes (like image or memory) may reset the
    sandbox state. Use lifecycle policies to control automatic cleanup.

    Args:
        sandbox_name (str):
        body (Sandbox): Lightweight virtual machine for secure AI code execution. Sandboxes resume
            from standby in under 25ms and automatically scale to zero after inactivity, preserving
            memory state including running processes and filesystem.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Sandbox]
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
    body: Sandbox,
) -> Response[Union[Error, Sandbox]]:
    """Update sandbox

     Updates a sandbox's configuration. Note that certain changes (like image or memory) may reset the
    sandbox state. Use lifecycle policies to control automatic cleanup.

    Args:
        sandbox_name (str):
        body (Sandbox): Lightweight virtual machine for secure AI code execution. Sandboxes resume
            from standby in under 25ms and automatically scale to zero after inactivity, preserving
            memory state including running processes and filesystem.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Sandbox]]
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
    body: Sandbox,
) -> Union[Error, Sandbox] | None:
    """Update sandbox

     Updates a sandbox's configuration. Note that certain changes (like image or memory) may reset the
    sandbox state. Use lifecycle policies to control automatic cleanup.

    Args:
        sandbox_name (str):
        body (Sandbox): Lightweight virtual machine for secure AI code execution. Sandboxes resume
            from standby in under 25ms and automatically scale to zero after inactivity, preserving
            memory state including running processes and filesystem.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Sandbox]
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            client=client,
            body=body,
        )
    ).parsed

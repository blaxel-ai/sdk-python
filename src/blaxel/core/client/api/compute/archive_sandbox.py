from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.sandbox import Sandbox
from ...types import Response


def _get_kwargs(
    sandbox_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sandboxes/{sandbox_name}/archive".format(
            sandbox_name=quote(str(sandbox_name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Error | Sandbox | None:
    if response.status_code == 200:
        response_200 = Sandbox.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_401, response)
        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_403, response)
        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_404, response)
        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_409, response)
        return response_409

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Error | Sandbox]:
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
) -> Response[Error | Sandbox]:
    """Archive sandbox

     Archives a sandbox. The changes its filesystem accumulated over its image are exported to the
    archive store, then the sandbox is shut down while its definition is kept, so it can be recreated
    later with the same disk. Memory and running processes are not preserved, processes are started
    again from their configuration when the sandbox is unarchived.

    Args:
        sandbox_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Sandbox]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_name: str,
    *,
    client: Client,
) -> Error | Sandbox | None:
    """Archive sandbox

     Archives a sandbox. The changes its filesystem accumulated over its image are exported to the
    archive store, then the sandbox is shut down while its definition is kept, so it can be recreated
    later with the same disk. Memory and running processes are not preserved, processes are started
    again from their configuration when the sandbox is unarchived.

    Args:
        sandbox_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Sandbox
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    *,
    client: Client,
) -> Response[Error | Sandbox]:
    """Archive sandbox

     Archives a sandbox. The changes its filesystem accumulated over its image are exported to the
    archive store, then the sandbox is shut down while its definition is kept, so it can be recreated
    later with the same disk. Memory and running processes are not preserved, processes are started
    again from their configuration when the sandbox is unarchived.

    Args:
        sandbox_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Sandbox]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    *,
    client: Client,
) -> Error | Sandbox | None:
    """Archive sandbox

     Archives a sandbox. The changes its filesystem accumulated over its image are exported to the
    archive store, then the sandbox is shut down while its definition is kept, so it can be recreated
    later with the same disk. Memory and running processes are not preserved, processes are started
    again from their configuration when the sandbox is unarchived.

    Args:
        sandbox_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Sandbox
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            client=client,
        )
    ).parsed

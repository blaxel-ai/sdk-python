from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    path: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/ws/watch/filesystem/{path}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[ErrorResponse, str]]:
    if response.status_code == 101:
        response_101 = cast(str, response.json())
        return response_101
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[ErrorResponse, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    path: str,
    *,
    client: Union[Client],
) -> Response[Union[ErrorResponse, str]]:
    """Stream file modification events in a directory via WebSocket

     Streams JSON events of modified files in the given directory. Closes when the client disconnects.

    Args:
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, str]]
    """

    kwargs = _get_kwargs(
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    path: str,
    *,
    client: Union[Client],
) -> Optional[Union[ErrorResponse, str]]:
    """Stream file modification events in a directory via WebSocket

     Streams JSON events of modified files in the given directory. Closes when the client disconnects.

    Args:
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, str]
    """

    return sync_detailed(
        path=path,
        client=client,
    ).parsed


async def asyncio_detailed(
    path: str,
    *,
    client: Union[Client],
) -> Response[Union[ErrorResponse, str]]:
    """Stream file modification events in a directory via WebSocket

     Streams JSON events of modified files in the given directory. Closes when the client disconnects.

    Args:
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, str]]
    """

    kwargs = _get_kwargs(
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    path: str,
    *,
    client: Union[Client],
) -> Optional[Union[ErrorResponse, str]]:
    """Stream file modification events in a directory via WebSocket

     Streams JSON events of modified files in the given directory. Closes when the client disconnects.

    Args:
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, str]
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
        )
    ).parsed

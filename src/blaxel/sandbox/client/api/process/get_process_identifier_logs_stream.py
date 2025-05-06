from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.get_process_identifier_logs_stream_response_200 import (
    GetProcessIdentifierLogsStreamResponse200,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    identifier: str,
    *,
    stream: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["stream"] = stream

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/process/{identifier}/logs/stream",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[ErrorResponse, GetProcessIdentifierLogsStreamResponse200]]:
    if response.status_code == 200:
        response_200 = GetProcessIdentifierLogsStreamResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ErrorResponse, GetProcessIdentifierLogsStreamResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    identifier: str,
    *,
    client: Union[Client],
    stream: Union[Unset, bool] = UNSET,
) -> Response[Union[ErrorResponse, GetProcessIdentifierLogsStreamResponse200]]:
    """Get process logs in realtime

     Get the stdout and stderr output of a process in realtime

    Args:
        identifier (str):
        stream (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, GetProcessIdentifierLogsStreamResponse200]]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        stream=stream,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    identifier: str,
    *,
    client: Union[Client],
    stream: Union[Unset, bool] = UNSET,
) -> Optional[Union[ErrorResponse, GetProcessIdentifierLogsStreamResponse200]]:
    """Get process logs in realtime

     Get the stdout and stderr output of a process in realtime

    Args:
        identifier (str):
        stream (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, GetProcessIdentifierLogsStreamResponse200]
    """

    return sync_detailed(
        identifier=identifier,
        client=client,
        stream=stream,
    ).parsed


async def asyncio_detailed(
    identifier: str,
    *,
    client: Union[Client],
    stream: Union[Unset, bool] = UNSET,
) -> Response[Union[ErrorResponse, GetProcessIdentifierLogsStreamResponse200]]:
    """Get process logs in realtime

     Get the stdout and stderr output of a process in realtime

    Args:
        identifier (str):
        stream (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, GetProcessIdentifierLogsStreamResponse200]]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        stream=stream,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    identifier: str,
    *,
    client: Union[Client],
    stream: Union[Unset, bool] = UNSET,
) -> Optional[Union[ErrorResponse, GetProcessIdentifierLogsStreamResponse200]]:
    """Get process logs in realtime

     Get the stdout and stderr output of a process in realtime

    Args:
        identifier (str):
        stream (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, GetProcessIdentifierLogsStreamResponse200]
    """

    return (
        await asyncio_detailed(
            identifier=identifier,
            client=client,
            stream=stream,
        )
    ).parsed

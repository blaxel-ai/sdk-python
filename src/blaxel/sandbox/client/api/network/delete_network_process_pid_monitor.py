from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.delete_network_process_pid_monitor_response_200 import (
    DeleteNetworkProcessPidMonitorResponse200,
)
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    pid: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/network/process/{pid}/monitor",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]]:
    if response.status_code == 200:
        response_200 = DeleteNetworkProcessPidMonitorResponse200.from_dict(response.json())

        return response_200
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


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pid: int,
    *,
    client: Union[Client],
) -> Response[Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]]:
    """Stop monitoring ports for a process

     Stop monitoring for new ports opened by a process

    Args:
        pid (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        pid=pid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pid: int,
    *,
    client: Union[Client],
) -> Optional[Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]]:
    """Stop monitoring ports for a process

     Stop monitoring for new ports opened by a process

    Args:
        pid (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]
    """

    return sync_detailed(
        pid=pid,
        client=client,
    ).parsed


async def asyncio_detailed(
    pid: int,
    *,
    client: Union[Client],
) -> Response[Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]]:
    """Stop monitoring ports for a process

     Stop monitoring for new ports opened by a process

    Args:
        pid (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        pid=pid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pid: int,
    *,
    client: Union[Client],
) -> Optional[Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]]:
    """Stop monitoring ports for a process

     Stop monitoring for new ports opened by a process

    Args:
        pid (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            pid=pid,
            client=client,
        )
    ).parsed

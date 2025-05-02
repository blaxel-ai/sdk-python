from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.port_monitor_request import PortMonitorRequest
from ...models.post_network_process_pid_monitor_response_200 import (
    PostNetworkProcessPidMonitorResponse200,
)
from ...types import Response


def _get_kwargs(
    pid: int,
    *,
    body: PortMonitorRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/network/process/{pid}/monitor",
    }

    if type(body) == dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]]:
    if response.status_code == 200:
        response_200 = PostNetworkProcessPidMonitorResponse200.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]]:
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
    body: PortMonitorRequest,
) -> Response[Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]]:
    """Start monitoring ports for a process

     Start monitoring for new ports opened by a process

    Args:
        pid (int):
        body (PortMonitorRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]]
    """

    kwargs = _get_kwargs(
        pid=pid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pid: int,
    *,
    client: Union[Client],
    body: PortMonitorRequest,
) -> Optional[Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]]:
    """Start monitoring ports for a process

     Start monitoring for new ports opened by a process

    Args:
        pid (int):
        body (PortMonitorRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]
    """

    return sync_detailed(
        pid=pid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    pid: int,
    *,
    client: Union[Client],
    body: PortMonitorRequest,
) -> Response[Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]]:
    """Start monitoring ports for a process

     Start monitoring for new ports opened by a process

    Args:
        pid (int):
        body (PortMonitorRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]]
    """

    kwargs = _get_kwargs(
        pid=pid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pid: int,
    *,
    client: Union[Client],
    body: PortMonitorRequest,
) -> Optional[Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]]:
    """Start monitoring ports for a process

     Start monitoring for new ports opened by a process

    Args:
        pid (int):
        body (PortMonitorRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]
    """

    return (
        await asyncio_detailed(
            pid=pid,
            client=client,
            body=body,
        )
    ).parsed

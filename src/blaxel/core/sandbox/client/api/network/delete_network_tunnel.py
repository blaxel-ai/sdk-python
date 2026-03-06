from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.success_response import SuccessResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/network/tunnel",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[ErrorResponse, SuccessResponse] | None:
    if response.status_code == 200:
        response_200 = SuccessResponse.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, SuccessResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Union[ErrorResponse, SuccessResponse]]:
    """Disconnect tunnel

     Stop the network tunnel and restore the original network configuration. WARNING: After
    disconnecting, the sandbox will lose all outbound internet connectivity (no egress). Inbound
    connections to the sandbox will still work. Use PUT /network/tunnel/config to re-establish the
    tunnel.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
) -> Union[ErrorResponse, SuccessResponse] | None:
    """Disconnect tunnel

     Stop the network tunnel and restore the original network configuration. WARNING: After
    disconnecting, the sandbox will lose all outbound internet connectivity (no egress). Inbound
    connections to the sandbox will still work. Use PUT /network/tunnel/config to re-establish the
    tunnel.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SuccessResponse]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Union[ErrorResponse, SuccessResponse]]:
    """Disconnect tunnel

     Stop the network tunnel and restore the original network configuration. WARNING: After
    disconnecting, the sandbox will lose all outbound internet connectivity (no egress). Inbound
    connections to the sandbox will still work. Use PUT /network/tunnel/config to re-establish the
    tunnel.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
) -> Union[ErrorResponse, SuccessResponse] | None:
    """Disconnect tunnel

     Stop the network tunnel and restore the original network configuration. WARNING: After
    disconnecting, the sandbox will lose all outbound internet connectivity (no egress). Inbound
    connections to the sandbox will still work. Use PUT /network/tunnel/config to re-establish the
    tunnel.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SuccessResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed

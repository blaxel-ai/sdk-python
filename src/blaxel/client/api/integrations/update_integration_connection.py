from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.integration_connection import IntegrationConnection
from ...types import Response


def _get_kwargs(
    connection_name: str,
    *,
    body: IntegrationConnection,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/integrations/connections/{connection_name}",
    }

    if type(body) == dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[IntegrationConnection]:
    if response.status_code == 200:
        response_200 = IntegrationConnection.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[IntegrationConnection]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    connection_name: str,
    *,
    client: Union[Client],
    body: IntegrationConnection,
) -> Response[IntegrationConnection]:
    """Update integration connection

     Update an integration connection by integration name and connection name.

    Args:
        connection_name (str):
        body (IntegrationConnection): Integration Connection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IntegrationConnection]
    """

    kwargs = _get_kwargs(
        connection_name=connection_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    connection_name: str,
    *,
    client: Union[Client],
    body: IntegrationConnection,
) -> Optional[IntegrationConnection]:
    """Update integration connection

     Update an integration connection by integration name and connection name.

    Args:
        connection_name (str):
        body (IntegrationConnection): Integration Connection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IntegrationConnection
    """

    return sync_detailed(
        connection_name=connection_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    connection_name: str,
    *,
    client: Union[Client],
    body: IntegrationConnection,
) -> Response[IntegrationConnection]:
    """Update integration connection

     Update an integration connection by integration name and connection name.

    Args:
        connection_name (str):
        body (IntegrationConnection): Integration Connection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IntegrationConnection]
    """

    kwargs = _get_kwargs(
        connection_name=connection_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    connection_name: str,
    *,
    client: Union[Client],
    body: IntegrationConnection,
) -> Optional[IntegrationConnection]:
    """Update integration connection

     Update an integration connection by integration name and connection name.

    Args:
        connection_name (str):
        body (IntegrationConnection): Integration Connection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IntegrationConnection
    """

    return (
        await asyncio_detailed(
            connection_name=connection_name,
            client=client,
            body=body,
        )
    ).parsed

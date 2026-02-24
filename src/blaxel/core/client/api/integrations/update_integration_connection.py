from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
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
) -> Union[Error, IntegrationConnection] | None:
    if response.status_code == 200:
        response_200 = IntegrationConnection.from_dict(response.json())

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


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Error, IntegrationConnection]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    connection_name: str,
    *,
    client: Client,
    body: IntegrationConnection,
) -> Response[Union[Error, IntegrationConnection]]:
    """Update integration connection

     Updates an integration connection's configuration or credentials. Changes take effect immediately
    for all resources using this connection.

    Args:
        connection_name (str):
        body (IntegrationConnection): Configured connection to an external service (LLM provider,
            API, SaaS, database) storing credentials and settings for use by workspace resources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, IntegrationConnection]]
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
    client: Client,
    body: IntegrationConnection,
) -> Union[Error, IntegrationConnection] | None:
    """Update integration connection

     Updates an integration connection's configuration or credentials. Changes take effect immediately
    for all resources using this connection.

    Args:
        connection_name (str):
        body (IntegrationConnection): Configured connection to an external service (LLM provider,
            API, SaaS, database) storing credentials and settings for use by workspace resources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, IntegrationConnection]
    """

    return sync_detailed(
        connection_name=connection_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    connection_name: str,
    *,
    client: Client,
    body: IntegrationConnection,
) -> Response[Union[Error, IntegrationConnection]]:
    """Update integration connection

     Updates an integration connection's configuration or credentials. Changes take effect immediately
    for all resources using this connection.

    Args:
        connection_name (str):
        body (IntegrationConnection): Configured connection to an external service (LLM provider,
            API, SaaS, database) storing credentials and settings for use by workspace resources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, IntegrationConnection]]
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
    client: Client,
    body: IntegrationConnection,
) -> Union[Error, IntegrationConnection] | None:
    """Update integration connection

     Updates an integration connection's configuration or credentials. Changes take effect immediately
    for all resources using this connection.

    Args:
        connection_name (str):
        body (IntegrationConnection): Configured connection to an external service (LLM provider,
            API, SaaS, database) storing credentials and settings for use by workspace resources.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, IntegrationConnection]
    """

    return (
        await asyncio_detailed(
            connection_name=connection_name,
            client=client,
            body=body,
        )
    ).parsed

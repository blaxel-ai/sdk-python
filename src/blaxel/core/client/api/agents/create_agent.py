from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.agent import Agent
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: Agent,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Agent, Error] | None:
    if response.status_code == 200:
        response_200 = Agent.from_dict(response.json())

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
    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Agent, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: Agent,
) -> Response[Union[Agent, Error]]:
    """Create agent

     Creates a new AI agent deployment from your code. The agent will be built and deployed as a
    serverless auto-scaling endpoint. Use the Blaxel CLI 'bl deploy' for a simpler deployment
    experience.

    Args:
        body (Agent): Serverless AI agent deployment that runs your custom agent code as an auto-
            scaling API endpoint. Agents are deployed from your code repository and expose a global
            inference URL for querying.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Agent, Error]]
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
    body: Agent,
) -> Union[Agent, Error] | None:
    """Create agent

     Creates a new AI agent deployment from your code. The agent will be built and deployed as a
    serverless auto-scaling endpoint. Use the Blaxel CLI 'bl deploy' for a simpler deployment
    experience.

    Args:
        body (Agent): Serverless AI agent deployment that runs your custom agent code as an auto-
            scaling API endpoint. Agents are deployed from your code repository and expose a global
            inference URL for querying.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Agent, Error]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: Agent,
) -> Response[Union[Agent, Error]]:
    """Create agent

     Creates a new AI agent deployment from your code. The agent will be built and deployed as a
    serverless auto-scaling endpoint. Use the Blaxel CLI 'bl deploy' for a simpler deployment
    experience.

    Args:
        body (Agent): Serverless AI agent deployment that runs your custom agent code as an auto-
            scaling API endpoint. Agents are deployed from your code repository and expose a global
            inference URL for querying.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Agent, Error]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: Agent,
) -> Union[Agent, Error] | None:
    """Create agent

     Creates a new AI agent deployment from your code. The agent will be built and deployed as a
    serverless auto-scaling endpoint. Use the Blaxel CLI 'bl deploy' for a simpler deployment
    experience.

    Args:
        body (Agent): Serverless AI agent deployment that runs your custom agent code as an auto-
            scaling API endpoint. Agents are deployed from your code repository and expose a global
            inference URL for querying.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Agent, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

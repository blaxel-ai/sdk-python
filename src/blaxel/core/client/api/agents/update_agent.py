from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.agent import Agent
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    agent_name: str,
    *,
    body: Agent,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/agents/{agent_name}",
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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Agent, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_name: str,
    *,
    client: Client,
    body: Agent,
) -> Response[Union[Agent, Error]]:
    """Update agent

     Updates an agent's configuration and triggers a new deployment. Changes to runtime settings,
    environment variables, or scaling parameters will be applied on the next deployment.

    Args:
        agent_name (str):
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
        agent_name=agent_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    agent_name: str,
    *,
    client: Client,
    body: Agent,
) -> Union[Agent, Error] | None:
    """Update agent

     Updates an agent's configuration and triggers a new deployment. Changes to runtime settings,
    environment variables, or scaling parameters will be applied on the next deployment.

    Args:
        agent_name (str):
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
        agent_name=agent_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    agent_name: str,
    *,
    client: Client,
    body: Agent,
) -> Response[Union[Agent, Error]]:
    """Update agent

     Updates an agent's configuration and triggers a new deployment. Changes to runtime settings,
    environment variables, or scaling parameters will be applied on the next deployment.

    Args:
        agent_name (str):
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
        agent_name=agent_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    agent_name: str,
    *,
    client: Client,
    body: Agent,
) -> Union[Agent, Error] | None:
    """Update agent

     Updates an agent's configuration and triggers a new deployment. Changes to runtime settings,
    environment variables, or scaling parameters will be applied on the next deployment.

    Args:
        agent_name (str):
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
            agent_name=agent_name,
            client=client,
            body=body,
        )
    ).parsed

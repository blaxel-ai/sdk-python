from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.agent import Agent
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

    if type(body) == dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Agent]:
    if response.status_code == 200:
        response_200 = Agent.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Agent]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_name: str,
    *,
    client: Union[Client],
    body: Agent,
) -> Response[Agent]:
    """Update agent by name

    Args:
        agent_name (str):
        body (Agent): Agent

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Agent]
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
    client: Union[Client],
    body: Agent,
) -> Optional[Agent]:
    """Update agent by name

    Args:
        agent_name (str):
        body (Agent): Agent

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Agent
    """

    return sync_detailed(
        agent_name=agent_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    agent_name: str,
    *,
    client: Union[Client],
    body: Agent,
) -> Response[Agent]:
    """Update agent by name

    Args:
        agent_name (str):
        body (Agent): Agent

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Agent]
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
    client: Union[Client],
    body: Agent,
) -> Optional[Agent]:
    """Update agent by name

    Args:
        agent_name (str):
        body (Agent): Agent

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Agent
    """

    return (
        await asyncio_detailed(
            agent_name=agent_name,
            client=client,
            body=body,
        )
    ).parsed

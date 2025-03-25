from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.knowledgebase import Knowledgebase
from ...types import Response


def _get_kwargs(
    *,
    body: Knowledgebase,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/knowledgebases",
    }

    if type(body) == dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Knowledgebase]:
    if response.status_code == 200:
        response_200 = Knowledgebase.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Knowledgebase]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[Client],
    body: Knowledgebase,
) -> Response[Knowledgebase]:
    """Create knowledgebase

     Creates an knowledgebase.

    Args:
        body (Knowledgebase): Knowledgebase

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Knowledgebase]
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
    client: Union[Client],
    body: Knowledgebase,
) -> Optional[Knowledgebase]:
    """Create knowledgebase

     Creates an knowledgebase.

    Args:
        body (Knowledgebase): Knowledgebase

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Knowledgebase
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[Client],
    body: Knowledgebase,
) -> Response[Knowledgebase]:
    """Create knowledgebase

     Creates an knowledgebase.

    Args:
        body (Knowledgebase): Knowledgebase

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Knowledgebase]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[Client],
    body: Knowledgebase,
) -> Optional[Knowledgebase]:
    """Create knowledgebase

     Creates an knowledgebase.

    Args:
        body (Knowledgebase): Knowledgebase

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Knowledgebase
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.knowledgebase import Knowledgebase
from ...types import Response


def _get_kwargs(
    knowledgebase_name: str,
    *,
    body: Knowledgebase,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/knowledgebases/{knowledgebase_name}",
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
    knowledgebase_name: str,
    *,
    client: Union[Client],
    body: Knowledgebase,
) -> Response[Knowledgebase]:
    """Update knowledgebase

     Updates an knowledgebase.

    Args:
        knowledgebase_name (str):
        body (Knowledgebase): Knowledgebase

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Knowledgebase]
    """

    kwargs = _get_kwargs(
        knowledgebase_name=knowledgebase_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    knowledgebase_name: str,
    *,
    client: Union[Client],
    body: Knowledgebase,
) -> Optional[Knowledgebase]:
    """Update knowledgebase

     Updates an knowledgebase.

    Args:
        knowledgebase_name (str):
        body (Knowledgebase): Knowledgebase

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Knowledgebase
    """

    return sync_detailed(
        knowledgebase_name=knowledgebase_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    knowledgebase_name: str,
    *,
    client: Union[Client],
    body: Knowledgebase,
) -> Response[Knowledgebase]:
    """Update knowledgebase

     Updates an knowledgebase.

    Args:
        knowledgebase_name (str):
        body (Knowledgebase): Knowledgebase

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Knowledgebase]
    """

    kwargs = _get_kwargs(
        knowledgebase_name=knowledgebase_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    knowledgebase_name: str,
    *,
    client: Union[Client],
    body: Knowledgebase,
) -> Optional[Knowledgebase]:
    """Update knowledgebase

     Updates an knowledgebase.

    Args:
        knowledgebase_name (str):
        body (Knowledgebase): Knowledgebase

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Knowledgebase
    """

    return (
        await asyncio_detailed(
            knowledgebase_name=knowledgebase_name,
            client=client,
            body=body,
        )
    ).parsed

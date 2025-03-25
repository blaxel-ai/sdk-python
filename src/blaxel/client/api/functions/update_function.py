from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.function import Function
from ...types import Response


def _get_kwargs(
    function_name: str,
    *,
    body: Function,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/functions/{function_name}",
    }

    if type(body) == dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Function]:
    if response.status_code == 200:
        response_200 = Function.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Function]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    function_name: str,
    *,
    client: Union[Client],
    body: Function,
) -> Response[Function]:
    """Update function by name

    Args:
        function_name (str):
        body (Function): Function

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Function]
    """

    kwargs = _get_kwargs(
        function_name=function_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    function_name: str,
    *,
    client: Union[Client],
    body: Function,
) -> Optional[Function]:
    """Update function by name

    Args:
        function_name (str):
        body (Function): Function

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Function
    """

    return sync_detailed(
        function_name=function_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    function_name: str,
    *,
    client: Union[Client],
    body: Function,
) -> Response[Function]:
    """Update function by name

    Args:
        function_name (str):
        body (Function): Function

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Function]
    """

    kwargs = _get_kwargs(
        function_name=function_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    function_name: str,
    *,
    client: Union[Client],
    body: Function,
) -> Optional[Function]:
    """Update function by name

    Args:
        function_name (str):
        body (Function): Function

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Function
    """

    return (
        await asyncio_detailed(
            function_name=function_name,
            client=client,
            body=body,
        )
    ).parsed

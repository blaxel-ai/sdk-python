from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.function import Function
from ...types import Response


def _get_kwargs(
    function_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/functions/{function_name}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Error, Function] | None:
    if response.status_code == 200:
        response_200 = Function.from_dict(response.json())

        return response_200
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
) -> Response[Union[Error, Function]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    function_name: str,
    *,
    client: Client,
) -> Response[Union[Error, Function]]:
    """Delete MCP server

     Permanently deletes an MCP server function and all its deployment history. Any agents using this
    function's tools will no longer be able to invoke them.

    Args:
        function_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Function]]
    """

    kwargs = _get_kwargs(
        function_name=function_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    function_name: str,
    *,
    client: Client,
) -> Union[Error, Function] | None:
    """Delete MCP server

     Permanently deletes an MCP server function and all its deployment history. Any agents using this
    function's tools will no longer be able to invoke them.

    Args:
        function_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Function]
    """

    return sync_detailed(
        function_name=function_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    function_name: str,
    *,
    client: Client,
) -> Response[Union[Error, Function]]:
    """Delete MCP server

     Permanently deletes an MCP server function and all its deployment history. Any agents using this
    function's tools will no longer be able to invoke them.

    Args:
        function_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Function]]
    """

    kwargs = _get_kwargs(
        function_name=function_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    function_name: str,
    *,
    client: Client,
) -> Union[Error, Function] | None:
    """Delete MCP server

     Permanently deletes an MCP server function and all its deployment history. Any agents using this
    function's tools will no longer be able to invoke them.

    Args:
        function_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Function]
    """

    return (
        await asyncio_detailed(
            function_name=function_name,
            client=client,
        )
    ).parsed

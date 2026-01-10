from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.function import Function
from ...types import UNSET, Response, Unset


def _get_kwargs(
    function_name: str,
    *,
    show_secrets: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["show_secrets"] = show_secrets

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/functions/{function_name}",
        "params": params,
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
    show_secrets: Union[Unset, bool] = UNSET,
) -> Response[Union[Error, Function]]:
    """Get MCP server

     Returns detailed information about an MCP server function including its deployment status, available
    tools, transport configuration, and endpoint URL.

    Args:
        function_name (str):
        show_secrets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Function]]
    """

    kwargs = _get_kwargs(
        function_name=function_name,
        show_secrets=show_secrets,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    function_name: str,
    *,
    client: Client,
    show_secrets: Union[Unset, bool] = UNSET,
) -> Union[Error, Function] | None:
    """Get MCP server

     Returns detailed information about an MCP server function including its deployment status, available
    tools, transport configuration, and endpoint URL.

    Args:
        function_name (str):
        show_secrets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Function]
    """

    return sync_detailed(
        function_name=function_name,
        client=client,
        show_secrets=show_secrets,
    ).parsed


async def asyncio_detailed(
    function_name: str,
    *,
    client: Client,
    show_secrets: Union[Unset, bool] = UNSET,
) -> Response[Union[Error, Function]]:
    """Get MCP server

     Returns detailed information about an MCP server function including its deployment status, available
    tools, transport configuration, and endpoint URL.

    Args:
        function_name (str):
        show_secrets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Function]]
    """

    kwargs = _get_kwargs(
        function_name=function_name,
        show_secrets=show_secrets,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    function_name: str,
    *,
    client: Client,
    show_secrets: Union[Unset, bool] = UNSET,
) -> Union[Error, Function] | None:
    """Get MCP server

     Returns detailed information about an MCP server function including its deployment status, available
    tools, transport configuration, and endpoint URL.

    Args:
        function_name (str):
        show_secrets (Union[Unset, bool]):

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
            show_secrets=show_secrets,
        )
    ).parsed

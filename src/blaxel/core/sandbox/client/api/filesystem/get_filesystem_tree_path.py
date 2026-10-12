from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.directory import Directory
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    path: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/filesystem/tree/{path}",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Directory, ErrorResponse] | None:
    if response.status_code == 200:
        response_200 = Directory.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_400, response)
        return response_400
    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_422, response)
        return response_422
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_500, response)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Directory, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    path: str,
    *,
    client: Client,
) -> Response[Union[Directory, ErrorResponse]]:
    """Get directory tree

     Get a recursive directory tree structure starting from the specified path

    Args:
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Directory, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    path: str,
    *,
    client: Client,
) -> Union[Directory, ErrorResponse] | None:
    """Get directory tree

     Get a recursive directory tree structure starting from the specified path

    Args:
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Directory, ErrorResponse]
    """

    return sync_detailed(
        path=path,
        client=client,
    ).parsed


async def asyncio_detailed(
    path: str,
    *,
    client: Client,
) -> Response[Union[Directory, ErrorResponse]]:
    """Get directory tree

     Get a recursive directory tree structure starting from the specified path

    Args:
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Directory, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    path: str,
    *,
    client: Client,
) -> Union[Directory, ErrorResponse] | None:
    """Get directory tree

     Get a recursive directory tree structure starting from the specified path

    Args:
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Directory, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
        )
    ).parsed

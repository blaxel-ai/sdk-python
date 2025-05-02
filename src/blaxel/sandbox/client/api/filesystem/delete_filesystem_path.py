from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.success_response import SuccessResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    path: str,
    *,
    recursive: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["recursive"] = recursive

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/filesystem/{path}",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[ErrorResponse, SuccessResponse]]:
    if response.status_code == 200:
        response_200 = SuccessResponse.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[ErrorResponse, SuccessResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    path: str,
    *,
    client: Union[Client],
    recursive: Union[Unset, bool] = UNSET,
) -> Response[Union[ErrorResponse, SuccessResponse]]:
    """Delete file or directory

     Delete a file or directory

    Args:
        path (str):
        recursive (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]
    """

    kwargs = _get_kwargs(
        path=path,
        recursive=recursive,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    path: str,
    *,
    client: Union[Client],
    recursive: Union[Unset, bool] = UNSET,
) -> Optional[Union[ErrorResponse, SuccessResponse]]:
    """Delete file or directory

     Delete a file or directory

    Args:
        path (str):
        recursive (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SuccessResponse]
    """

    return sync_detailed(
        path=path,
        client=client,
        recursive=recursive,
    ).parsed


async def asyncio_detailed(
    path: str,
    *,
    client: Union[Client],
    recursive: Union[Unset, bool] = UNSET,
) -> Response[Union[ErrorResponse, SuccessResponse]]:
    """Delete file or directory

     Delete a file or directory

    Args:
        path (str):
        recursive (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]
    """

    kwargs = _get_kwargs(
        path=path,
        recursive=recursive,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    path: str,
    *,
    client: Union[Client],
    recursive: Union[Unset, bool] = UNSET,
) -> Optional[Union[ErrorResponse, SuccessResponse]]:
    """Delete file or directory

     Delete a file or directory

    Args:
        path (str):
        recursive (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SuccessResponse]
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
            recursive=recursive,
        )
    ).parsed

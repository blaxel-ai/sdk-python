from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.success_response import SuccessResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    path: str,
    *,
    recursive: bool | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["recursive"] = recursive

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/filesystem/{path}".format(
            path=quote(str(path), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> ErrorResponse | SuccessResponse | None:
    if response.status_code == 200:
        response_200 = SuccessResponse.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(errors.error_json(response))

        errors.retain_response(response_404, response)
        return response_404

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(errors.error_json(response))

        errors.retain_response(response_422, response)
        return response_422

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(errors.error_json(response))

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
) -> Response[ErrorResponse | SuccessResponse]:
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
    recursive: bool | Unset = UNSET,
) -> Response[ErrorResponse | SuccessResponse]:
    """Delete file or directory

     Delete a file or directory

    Args:
        path (str):
        recursive (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SuccessResponse]
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
    client: Client,
    recursive: bool | Unset = UNSET,
) -> ErrorResponse | SuccessResponse | None:
    """Delete file or directory

     Delete a file or directory

    Args:
        path (str):
        recursive (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SuccessResponse
    """

    return sync_detailed(
        path=path,
        client=client,
        recursive=recursive,
    ).parsed


async def asyncio_detailed(
    path: str,
    *,
    client: Client,
    recursive: bool | Unset = UNSET,
) -> Response[ErrorResponse | SuccessResponse]:
    """Delete file or directory

     Delete a file or directory

    Args:
        path (str):
        recursive (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SuccessResponse]
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
    client: Client,
    recursive: bool | Unset = UNSET,
) -> ErrorResponse | SuccessResponse | None:
    """Delete file or directory

     Delete a file or directory

    Args:
        path (str):
        recursive (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SuccessResponse
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
            recursive=recursive,
        )
    ).parsed

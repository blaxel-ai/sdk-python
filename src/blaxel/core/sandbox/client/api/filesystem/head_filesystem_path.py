from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...types import Response


def _get_kwargs(
    path: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": f"/filesystem/{path}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Any | None:
    if response.status_code == 200:
        return None
    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any]:
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
) -> Response[Any]:
    """Stat a file or directory

     Returns the metadata of a file or directory as headers, with no body. This checks stat availability,
    not permission to read file contents or list a directory. When the path does not exist or its
    metadata cannot be accessed, the response is an empty 200 without the X-File-Type header.

    Args:
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    path: str,
    *,
    client: Client,
) -> Response[Any]:
    """Stat a file or directory

     Returns the metadata of a file or directory as headers, with no body. This checks stat availability,
    not permission to read file contents or list a directory. When the path does not exist or its
    metadata cannot be accessed, the response is an empty 200 without the X-File-Type header.

    Args:
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)

from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...types import UNSET, Response


def _get_kwargs(
    drive_name: str,
    *,
    path: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/drives/{drive_name}/folders",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Any | None:
    if response.status_code == 204:
        return None
    if response.status_code == 400:
        return None
    if response.status_code == 401:
        return None
    if response.status_code == 403:
        return None
    if response.status_code == 404:
        return None
    if response.status_code == 409:
        return None
    if response.status_code == 502:
        return None
    if response.status_code == 504:
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
    drive_name: str,
    *,
    client: Client,
    path: str,
) -> Response[Any]:
    """Delete a folder and its contents

     Deletes a folder and all its contents directly in drive storage. This is synchronous and non-atomic.
    If it times out or fails, some contents may have been deleted; retry the same path to finish
    cleanup. An absent folder succeeds. The drive root and internal metadata cannot be deleted.

    Args:
        drive_name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        drive_name=drive_name,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    drive_name: str,
    *,
    client: Client,
    path: str,
) -> Response[Any]:
    """Delete a folder and its contents

     Deletes a folder and all its contents directly in drive storage. This is synchronous and non-atomic.
    If it times out or fails, some contents may have been deleted; retry the same path to finish
    cleanup. An absent folder succeeds. The drive root and internal metadata cannot be deleted.

    Args:
        drive_name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        drive_name=drive_name,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)

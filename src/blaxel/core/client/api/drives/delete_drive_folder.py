from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
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
        "url": "/drives/{drive_name}/folders".format(
            drive_name=quote(str(drive_name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        errors.retain_response(response_400, response)
        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        errors.retain_response(response_401, response)
        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        errors.retain_response(response_403, response)
        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        errors.retain_response(response_404, response)
        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        errors.retain_response(response_409, response)
        return response_409

    if response.status_code == 502:
        response_502 = Error.from_dict(response.json())

        errors.retain_response(response_502, response)
        return response_502

    if response.status_code == 504:
        response_504 = Error.from_dict(response.json())

        errors.retain_response(response_504, response)
        return response_504

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any | Error]:
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
) -> Response[Any | Error]:
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
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        drive_name=drive_name,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    drive_name: str,
    *,
    client: Client,
    path: str,
) -> Any | Error | None:
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
        Any | Error
    """

    return sync_detailed(
        drive_name=drive_name,
        client=client,
        path=path,
    ).parsed


async def asyncio_detailed(
    drive_name: str,
    *,
    client: Client,
    path: str,
) -> Response[Any | Error]:
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
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        drive_name=drive_name,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    drive_name: str,
    *,
    client: Client,
    path: str,
) -> Any | Error | None:
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
        Any | Error
    """

    return (
        await asyncio_detailed(
            drive_name=drive_name,
            client=client,
            path=path,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.drive_unmount_response import DriveUnmountResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    mount_path: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/drives/mount/{mount_path}",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[DriveUnmountResponse, ErrorResponse] | None:
    if response.status_code == 200:
        response_200 = DriveUnmountResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[DriveUnmountResponse, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    mount_path: str,
    *,
    client: Client,
) -> Response[Union[DriveUnmountResponse, ErrorResponse]]:
    """Detach a drive from a local path

     Unmounts a previously mounted drive from the specified local path

    Args:
        mount_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DriveUnmountResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        mount_path=mount_path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    mount_path: str,
    *,
    client: Client,
) -> Union[DriveUnmountResponse, ErrorResponse] | None:
    """Detach a drive from a local path

     Unmounts a previously mounted drive from the specified local path

    Args:
        mount_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DriveUnmountResponse, ErrorResponse]
    """

    return sync_detailed(
        mount_path=mount_path,
        client=client,
    ).parsed


async def asyncio_detailed(
    mount_path: str,
    *,
    client: Client,
) -> Response[Union[DriveUnmountResponse, ErrorResponse]]:
    """Detach a drive from a local path

     Unmounts a previously mounted drive from the specified local path

    Args:
        mount_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DriveUnmountResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        mount_path=mount_path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    mount_path: str,
    *,
    client: Client,
) -> Union[DriveUnmountResponse, ErrorResponse] | None:
    """Detach a drive from a local path

     Unmounts a previously mounted drive from the specified local path

    Args:
        mount_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DriveUnmountResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            mount_path=mount_path,
            client=client,
        )
    ).parsed

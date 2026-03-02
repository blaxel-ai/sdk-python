from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.delete_drive_response_200 import DeleteDriveResponse200
from ...types import Response


def _get_kwargs(
    drive_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/drives/{drive_name}",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Any, DeleteDriveResponse200] | None:
    if response.status_code == 200:
        response_200 = DeleteDriveResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, DeleteDriveResponse200]]:
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
) -> Response[Union[Any, DeleteDriveResponse200]]:
    """Delete a drive

     Deletes a drive immediately. The drive record is removed from the database synchronously.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteDriveResponse200]]
    """

    kwargs = _get_kwargs(
        drive_name=drive_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    drive_name: str,
    *,
    client: Client,
) -> Union[Any, DeleteDriveResponse200] | None:
    """Delete a drive

     Deletes a drive immediately. The drive record is removed from the database synchronously.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteDriveResponse200]
    """

    return sync_detailed(
        drive_name=drive_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    drive_name: str,
    *,
    client: Client,
) -> Response[Union[Any, DeleteDriveResponse200]]:
    """Delete a drive

     Deletes a drive immediately. The drive record is removed from the database synchronously.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteDriveResponse200]]
    """

    kwargs = _get_kwargs(
        drive_name=drive_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    drive_name: str,
    *,
    client: Client,
) -> Union[Any, DeleteDriveResponse200] | None:
    """Delete a drive

     Deletes a drive immediately. The drive record is removed from the database synchronously.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteDriveResponse200]
    """

    return (
        await asyncio_detailed(
            drive_name=drive_name,
            client=client,
        )
    ).parsed

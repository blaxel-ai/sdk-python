from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.drive import Drive
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    drive_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/drives/{drive_name}".format(
            drive_name=quote(str(drive_name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Drive | Error | None:
    if response.status_code == 200:
        response_200 = Drive.from_dict(response.json())

        return response_200

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

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Drive | Error]:
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
) -> Response[Drive | Error]:
    """Get a drive

     Retrieves details of a specific drive including its status and events.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Drive | Error]
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
) -> Drive | Error | None:
    """Get a drive

     Retrieves details of a specific drive including its status and events.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Drive | Error
    """

    return sync_detailed(
        drive_name=drive_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    drive_name: str,
    *,
    client: Client,
) -> Response[Drive | Error]:
    """Get a drive

     Retrieves details of a specific drive including its status and events.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Drive | Error]
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
) -> Drive | Error | None:
    """Get a drive

     Retrieves details of a specific drive including its status and events.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Drive | Error
    """

    return (
        await asyncio_detailed(
            drive_name=drive_name,
            client=client,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.drive import Drive
from ...types import Response


def _get_kwargs(
    drive_name: str,
    *,
    body: Drive,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/drives/{drive_name}".format(
            drive_name=quote(str(drive_name), safe=""),
        ),
    }

    if type(body) is dict:
        _kwargs["json"] = body
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Any | Drive | None:
    if response.status_code == 200:
        response_200 = Drive.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        errors.retain_response(response_401, response)
        return response_401

    if response.status_code == 404:
        response_404 = cast(Any, None)
        errors.retain_response(response_404, response)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any | Drive]:
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
    body: Drive,
) -> Response[Any | Drive]:
    """Update a drive

     Updates an existing drive. Metadata fields like displayName and labels can be changed. Size can be
    set if not already configured.

    Args:
        drive_name (str):
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives can be mounted at runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Drive]
    """

    kwargs = _get_kwargs(
        drive_name=drive_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    drive_name: str,
    *,
    client: Client,
    body: Drive,
) -> Any | Drive | None:
    """Update a drive

     Updates an existing drive. Metadata fields like displayName and labels can be changed. Size can be
    set if not already configured.

    Args:
        drive_name (str):
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives can be mounted at runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Drive
    """

    return sync_detailed(
        drive_name=drive_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    drive_name: str,
    *,
    client: Client,
    body: Drive,
) -> Response[Any | Drive]:
    """Update a drive

     Updates an existing drive. Metadata fields like displayName and labels can be changed. Size can be
    set if not already configured.

    Args:
        drive_name (str):
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives can be mounted at runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Drive]
    """

    kwargs = _get_kwargs(
        drive_name=drive_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    drive_name: str,
    *,
    client: Client,
    body: Drive,
) -> Any | Drive | None:
    """Update a drive

     Updates an existing drive. Metadata fields like displayName and labels can be changed. Size can be
    set if not already configured.

    Args:
        drive_name (str):
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives can be mounted at runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Drive
    """

    return (
        await asyncio_detailed(
            drive_name=drive_name,
            client=client,
            body=body,
        )
    ).parsed

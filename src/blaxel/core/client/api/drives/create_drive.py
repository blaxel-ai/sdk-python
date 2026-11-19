from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.drive import Drive
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: Drive,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/drives",
    }

    if type(body) is dict:
        _kwargs["json"] = body
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    *,
    client: Client,
    body: Drive,
) -> Response[Drive | Error]:
    """Create a drive

     Creates a new drive in the workspace. Drives can be buckets and can be mounted at runtime to
    sandboxes.

    Args:
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives can be mounted at runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Drive | Error]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    body: Drive,
) -> Drive | Error | None:
    """Create a drive

     Creates a new drive in the workspace. Drives can be buckets and can be mounted at runtime to
    sandboxes.

    Args:
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives can be mounted at runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Drive | Error
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: Drive,
) -> Response[Drive | Error]:
    """Create a drive

     Creates a new drive in the workspace. Drives can be buckets and can be mounted at runtime to
    sandboxes.

    Args:
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives can be mounted at runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Drive | Error]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: Drive,
) -> Drive | Error | None:
    """Create a drive

     Creates a new drive in the workspace. Drives can be buckets and can be mounted at runtime to
    sandboxes.

    Args:
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives can be mounted at runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Drive | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

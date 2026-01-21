from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.volume import Volume
from ...types import Response


def _get_kwargs(
    volume_name: str,
    *,
    body: Volume,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/volumes/{volume_name}",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Volume | None:
    if response.status_code == 200:
        response_200 = Volume.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Volume]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    volume_name: str,
    *,
    client: Client,
    body: Volume,
) -> Response[Volume]:
    """Update volume

     Updates a volume.

    Args:
        volume_name (str):
        body (Volume): Persistent storage volume that can be attached to sandboxes for durable
            file storage across sessions. Volumes survive sandbox deletion and can be reattached to
            new sandboxes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Volume]
    """

    kwargs = _get_kwargs(
        volume_name=volume_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    volume_name: str,
    *,
    client: Client,
    body: Volume,
) -> Volume | None:
    """Update volume

     Updates a volume.

    Args:
        volume_name (str):
        body (Volume): Persistent storage volume that can be attached to sandboxes for durable
            file storage across sessions. Volumes survive sandbox deletion and can be reattached to
            new sandboxes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Volume
    """

    return sync_detailed(
        volume_name=volume_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    volume_name: str,
    *,
    client: Client,
    body: Volume,
) -> Response[Volume]:
    """Update volume

     Updates a volume.

    Args:
        volume_name (str):
        body (Volume): Persistent storage volume that can be attached to sandboxes for durable
            file storage across sessions. Volumes survive sandbox deletion and can be reattached to
            new sandboxes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Volume]
    """

    kwargs = _get_kwargs(
        volume_name=volume_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    volume_name: str,
    *,
    client: Client,
    body: Volume,
) -> Volume | None:
    """Update volume

     Updates a volume.

    Args:
        volume_name (str):
        body (Volume): Persistent storage volume that can be attached to sandboxes for durable
            file storage across sessions. Volumes survive sandbox deletion and can be reattached to
            new sandboxes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Volume
    """

    return (
        await asyncio_detailed(
            volume_name=volume_name,
            client=client,
            body=body,
        )
    ).parsed

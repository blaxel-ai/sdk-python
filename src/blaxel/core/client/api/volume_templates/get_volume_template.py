from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.volume_template import VolumeTemplate
from ...types import Response


def _get_kwargs(
    volume_template_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/volume_templates/{volume_template_name}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> VolumeTemplate | None:
    if response.status_code == 200:
        response_200 = VolumeTemplate.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[VolumeTemplate]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    volume_template_name: str,
    *,
    client: Client,
) -> Response[VolumeTemplate]:
    """Get volume template

     Returns a volume template by name.

    Args:
        volume_template_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VolumeTemplate]
    """

    kwargs = _get_kwargs(
        volume_template_name=volume_template_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    volume_template_name: str,
    *,
    client: Client,
) -> VolumeTemplate | None:
    """Get volume template

     Returns a volume template by name.

    Args:
        volume_template_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VolumeTemplate
    """

    return sync_detailed(
        volume_template_name=volume_template_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    volume_template_name: str,
    *,
    client: Client,
) -> Response[VolumeTemplate]:
    """Get volume template

     Returns a volume template by name.

    Args:
        volume_template_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VolumeTemplate]
    """

    kwargs = _get_kwargs(
        volume_template_name=volume_template_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    volume_template_name: str,
    *,
    client: Client,
) -> VolumeTemplate | None:
    """Get volume template

     Returns a volume template by name.

    Args:
        volume_template_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VolumeTemplate
    """

    return (
        await asyncio_detailed(
            volume_template_name=volume_template_name,
            client=client,
        )
    ).parsed

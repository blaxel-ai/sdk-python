from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.app_revision import AppRevision
from ...types import Response


def _get_kwargs(
    application_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/applications/{application_name}/revisions",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> list["AppRevision"] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AppRevision.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[list["AppRevision"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    application_name: str,
    *,
    client: Client,
) -> Response[list["AppRevision"]]:
    """List all application revisions

    Args:
        application_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AppRevision']]
    """

    kwargs = _get_kwargs(
        application_name=application_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    application_name: str,
    *,
    client: Client,
) -> list["AppRevision"] | None:
    """List all application revisions

    Args:
        application_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AppRevision']
    """

    return sync_detailed(
        application_name=application_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    application_name: str,
    *,
    client: Client,
) -> Response[list["AppRevision"]]:
    """List all application revisions

    Args:
        application_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AppRevision']]
    """

    kwargs = _get_kwargs(
        application_name=application_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    application_name: str,
    *,
    client: Client,
) -> list["AppRevision"] | None:
    """List all application revisions

    Args:
        application_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AppRevision']
    """

    return (
        await asyncio_detailed(
            application_name=application_name,
            client=client,
        )
    ).parsed

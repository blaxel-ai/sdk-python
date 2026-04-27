from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.list_pending_image_shares_direction import ListPendingImageSharesDirection
from ...models.pending_image_share_render import PendingImageShareRender
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    direction: Union[Unset, ListPendingImageSharesDirection] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_direction: Union[Unset, str] = UNSET
    if not isinstance(direction, Unset):
        json_direction = direction.value

    params["direction"] = json_direction

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/pending-image-shares",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> list["PendingImageShareRender"] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PendingImageShareRender.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[list["PendingImageShareRender"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    direction: Union[Unset, ListPendingImageSharesDirection] = UNSET,
) -> Response[list["PendingImageShareRender"]]:
    """List pending image shares

     Lists pending cross-account image shares targeting the caller's workspace (incoming) or originating
    from it (outgoing). Expired shares are cleaned up opportunistically.

    Args:
        direction (Union[Unset, ListPendingImageSharesDirection]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PendingImageShareRender']]
    """

    kwargs = _get_kwargs(
        direction=direction,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    direction: Union[Unset, ListPendingImageSharesDirection] = UNSET,
) -> list["PendingImageShareRender"] | None:
    """List pending image shares

     Lists pending cross-account image shares targeting the caller's workspace (incoming) or originating
    from it (outgoing). Expired shares are cleaned up opportunistically.

    Args:
        direction (Union[Unset, ListPendingImageSharesDirection]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PendingImageShareRender']
    """

    return sync_detailed(
        client=client,
        direction=direction,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    direction: Union[Unset, ListPendingImageSharesDirection] = UNSET,
) -> Response[list["PendingImageShareRender"]]:
    """List pending image shares

     Lists pending cross-account image shares targeting the caller's workspace (incoming) or originating
    from it (outgoing). Expired shares are cleaned up opportunistically.

    Args:
        direction (Union[Unset, ListPendingImageSharesDirection]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PendingImageShareRender']]
    """

    kwargs = _get_kwargs(
        direction=direction,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    direction: Union[Unset, ListPendingImageSharesDirection] = UNSET,
) -> list["PendingImageShareRender"] | None:
    """List pending image shares

     Lists pending cross-account image shares targeting the caller's workspace (incoming) or originating
    from it (outgoing). Expired shares are cleaned up opportunistically.

    Args:
        direction (Union[Unset, ListPendingImageSharesDirection]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PendingImageShareRender']
    """

    return (
        await asyncio_detailed(
            client=client,
            direction=direction,
        )
    ).parsed

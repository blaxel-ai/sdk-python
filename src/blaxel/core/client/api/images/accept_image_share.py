from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.image import Image
from ...types import UNSET, Response, Unset


def _get_kwargs(
    pending_share_id: str,
    *,
    force: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["force"] = force

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/pending-image-shares/{pending_share_id}/accept",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Any, Image] | None:
    if response.status_code == 200:
        response_200 = Image.from_dict(response.json())

        return response_200
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409
    if response.status_code == 410:
        response_410 = cast(Any, None)
        return response_410
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, Image]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pending_share_id: str,
    *,
    client: Client,
    force: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, Image]]:
    """Accept a pending image share

     Accepts a pending cross-account image share and copies the image metadata to the target workspace.
    Caller must be an admin of the target workspace.

    Args:
        pending_share_id (str):
        force (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Image]]
    """

    kwargs = _get_kwargs(
        pending_share_id=pending_share_id,
        force=force,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pending_share_id: str,
    *,
    client: Client,
    force: Union[Unset, bool] = UNSET,
) -> Union[Any, Image] | None:
    """Accept a pending image share

     Accepts a pending cross-account image share and copies the image metadata to the target workspace.
    Caller must be an admin of the target workspace.

    Args:
        pending_share_id (str):
        force (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Image]
    """

    return sync_detailed(
        pending_share_id=pending_share_id,
        client=client,
        force=force,
    ).parsed


async def asyncio_detailed(
    pending_share_id: str,
    *,
    client: Client,
    force: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, Image]]:
    """Accept a pending image share

     Accepts a pending cross-account image share and copies the image metadata to the target workspace.
    Caller must be an admin of the target workspace.

    Args:
        pending_share_id (str):
        force (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Image]]
    """

    kwargs = _get_kwargs(
        pending_share_id=pending_share_id,
        force=force,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pending_share_id: str,
    *,
    client: Client,
    force: Union[Unset, bool] = UNSET,
) -> Union[Any, Image] | None:
    """Accept a pending image share

     Accepts a pending cross-account image share and copies the image metadata to the target workspace.
    Caller must be an admin of the target workspace.

    Args:
        pending_share_id (str):
        force (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Image]
    """

    return (
        await asyncio_detailed(
            pending_share_id=pending_share_id,
            client=client,
            force=force,
        )
    ).parsed

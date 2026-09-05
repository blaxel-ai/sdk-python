from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    snapshot_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/snapshots/{snapshot_name}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Any, Error] | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    snapshot_name: str,
    *,
    client: Client,
) -> Response[Union[Any, Error]]:
    """Delete snapshot

     Deletes a snapshot. There is a single snapshot object, so this removes it for the whole workspace,
    whether or not the object it was captured from still exists.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        snapshot_name=snapshot_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    snapshot_name: str,
    *,
    client: Client,
) -> Union[Any, Error] | None:
    """Delete snapshot

     Deletes a snapshot. There is a single snapshot object, so this removes it for the whole workspace,
    whether or not the object it was captured from still exists.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return sync_detailed(
        snapshot_name=snapshot_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    snapshot_name: str,
    *,
    client: Client,
) -> Response[Union[Any, Error]]:
    """Delete snapshot

     Deletes a snapshot. There is a single snapshot object, so this removes it for the whole workspace,
    whether or not the object it was captured from still exists.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        snapshot_name=snapshot_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    snapshot_name: str,
    *,
    client: Client,
) -> Union[Any, Error] | None:
    """Delete snapshot

     Deletes a snapshot. There is a single snapshot object, so this removes it for the whole workspace,
    whether or not the object it was captured from still exists.

    Args:
        snapshot_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return (
        await asyncio_detailed(
            snapshot_name=snapshot_name,
            client=client,
        )
    ).parsed

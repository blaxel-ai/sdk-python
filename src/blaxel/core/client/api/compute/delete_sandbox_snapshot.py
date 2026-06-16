from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    sandbox_name: str,
    snapshot_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/sandboxes/{sandbox_name}/snapshots/{snapshot_id}",
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
        raise errors.UnexpectedStatus(response.status_code, response.content)
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
    sandbox_name: str,
    snapshot_id: str,
    *,
    client: Client,
) -> Response[Union[Any, Error]]:
    """Delete sandbox snapshot

     Deletes a snapshot of a sandbox by its ID.

    Args:
        sandbox_name (str):
        snapshot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        snapshot_id=snapshot_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_name: str,
    snapshot_id: str,
    *,
    client: Client,
) -> Union[Any, Error] | None:
    """Delete sandbox snapshot

     Deletes a snapshot of a sandbox by its ID.

    Args:
        sandbox_name (str):
        snapshot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        snapshot_id=snapshot_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    snapshot_id: str,
    *,
    client: Client,
) -> Response[Union[Any, Error]]:
    """Delete sandbox snapshot

     Deletes a snapshot of a sandbox by its ID.

    Args:
        sandbox_name (str):
        snapshot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        snapshot_id=snapshot_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    snapshot_id: str,
    *,
    client: Client,
) -> Union[Any, Error] | None:
    """Delete sandbox snapshot

     Deletes a snapshot of a sandbox by its ID.

    Args:
        sandbox_name (str):
        snapshot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            snapshot_id=snapshot_id,
            client=client,
        )
    ).parsed

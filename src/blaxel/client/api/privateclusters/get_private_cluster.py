from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.private_cluster import PrivateCluster
from ...types import Response


def _get_kwargs(
    private_cluster_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/privateclusters/{private_cluster_name}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, PrivateCluster]]:
    if response.status_code == 200:
        response_200 = PrivateCluster.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, PrivateCluster]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    private_cluster_name: str,
    *,
    client: Union[Client],
) -> Response[Union[Any, PrivateCluster]]:
    """Get private cluster by name

    Args:
        private_cluster_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PrivateCluster]]
    """

    kwargs = _get_kwargs(
        private_cluster_name=private_cluster_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    private_cluster_name: str,
    *,
    client: Union[Client],
) -> Optional[Union[Any, PrivateCluster]]:
    """Get private cluster by name

    Args:
        private_cluster_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PrivateCluster]
    """

    return sync_detailed(
        private_cluster_name=private_cluster_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    private_cluster_name: str,
    *,
    client: Union[Client],
) -> Response[Union[Any, PrivateCluster]]:
    """Get private cluster by name

    Args:
        private_cluster_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PrivateCluster]]
    """

    kwargs = _get_kwargs(
        private_cluster_name=private_cluster_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    private_cluster_name: str,
    *,
    client: Union[Client],
) -> Optional[Union[Any, PrivateCluster]]:
    """Get private cluster by name

    Args:
        private_cluster_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PrivateCluster]
    """

    return (
        await asyncio_detailed(
            private_cluster_name=private_cluster_name,
            client=client,
        )
    ).parsed

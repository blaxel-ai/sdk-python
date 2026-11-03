from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.image import Image
from ...types import Response


def _get_kwargs(
    resource_type: str,
    image_name: str,
    target_workspace: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/images/{resource_type}/{image_name}/share/{target_workspace}".format(
            resource_type=quote(str(resource_type), safe=""),
            image_name=quote(str(image_name), safe=""),
            target_workspace=quote(str(target_workspace), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Any | Image | None:
    if response.status_code == 200:
        response_200 = Image.from_dict(response.json())

        return response_200

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any | Image]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    resource_type: str,
    image_name: str,
    target_workspace: str,
    *,
    client: Client,
) -> Response[Any | Image]:
    """Unshare a container image

     Revokes sharing of a container image with a target workspace. Removes the metadata copy from the
    target workspace. The source image is not affected.

    Args:
        resource_type (str):
        image_name (str):
        target_workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Image]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
        target_workspace=target_workspace,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    resource_type: str,
    image_name: str,
    target_workspace: str,
    *,
    client: Client,
) -> Any | Image | None:
    """Unshare a container image

     Revokes sharing of a container image with a target workspace. Removes the metadata copy from the
    target workspace. The source image is not affected.

    Args:
        resource_type (str):
        image_name (str):
        target_workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Image
    """

    return sync_detailed(
        resource_type=resource_type,
        image_name=image_name,
        target_workspace=target_workspace,
        client=client,
    ).parsed


async def asyncio_detailed(
    resource_type: str,
    image_name: str,
    target_workspace: str,
    *,
    client: Client,
) -> Response[Any | Image]:
    """Unshare a container image

     Revokes sharing of a container image with a target workspace. Removes the metadata copy from the
    target workspace. The source image is not affected.

    Args:
        resource_type (str):
        image_name (str):
        target_workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Image]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
        target_workspace=target_workspace,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    resource_type: str,
    image_name: str,
    target_workspace: str,
    *,
    client: Client,
) -> Any | Image | None:
    """Unshare a container image

     Revokes sharing of a container image with a target workspace. Removes the metadata copy from the
    target workspace. The source image is not affected.

    Args:
        resource_type (str):
        image_name (str):
        target_workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Image
    """

    return (
        await asyncio_detailed(
            resource_type=resource_type,
            image_name=image_name,
            target_workspace=target_workspace,
            client=client,
        )
    ).parsed

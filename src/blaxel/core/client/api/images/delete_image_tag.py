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
    tag_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/images/{resource_type}/{image_name}/tags/{tag_name}".format(
            resource_type=quote(str(resource_type), safe=""),
            image_name=quote(str(image_name), safe=""),
            tag_name=quote(str(tag_name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Any | Image | None:
    if response.status_code == 200:
        response_200 = Image.from_dict(response.json())

        return response_200

    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = cast(Any, None)
        errors.retain_response(response_400, response)
        return response_400

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
    tag_name: str,
    *,
    client: Client,
) -> Response[Any | Image]:
    """Delete container image tag

     Deletes a specific tag from a container image. The underlying image layers are kept if other tags
    reference them. Will fail if the tag is currently in use.

    Args:
        resource_type (str):
        image_name (str):
        tag_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Image]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
        tag_name=tag_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    resource_type: str,
    image_name: str,
    tag_name: str,
    *,
    client: Client,
) -> Any | Image | None:
    """Delete container image tag

     Deletes a specific tag from a container image. The underlying image layers are kept if other tags
    reference them. Will fail if the tag is currently in use.

    Args:
        resource_type (str):
        image_name (str):
        tag_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Image
    """

    return sync_detailed(
        resource_type=resource_type,
        image_name=image_name,
        tag_name=tag_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    resource_type: str,
    image_name: str,
    tag_name: str,
    *,
    client: Client,
) -> Response[Any | Image]:
    """Delete container image tag

     Deletes a specific tag from a container image. The underlying image layers are kept if other tags
    reference them. Will fail if the tag is currently in use.

    Args:
        resource_type (str):
        image_name (str):
        tag_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Image]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
        tag_name=tag_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    resource_type: str,
    image_name: str,
    tag_name: str,
    *,
    client: Client,
) -> Any | Image | None:
    """Delete container image tag

     Deletes a specific tag from a container image. The underlying image layers are kept if other tags
    reference them. Will fail if the tag is currently in use.

    Args:
        resource_type (str):
        image_name (str):
        tag_name (str):

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
            tag_name=tag_name,
            client=client,
        )
    ).parsed

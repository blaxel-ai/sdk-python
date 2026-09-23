from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.image_summary import ImageSummary
from ...types import UNSET, Response, Unset


def _get_kwargs(
    resource_type: str,
    image_name: str,
    *,
    source_workspace: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["sourceWorkspace"] = source_workspace

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/images/{resource_type}/{image_name}",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> ImageSummary | None:
    if response.status_code == 200:
        response_200 = ImageSummary.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ImageSummary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
    source_workspace: Union[Unset, str] = UNSET,
) -> Response[ImageSummary]:
    """Get container image

     Returns a bounded image summary starting with API version 2026-09-22. Older versions return the
    image with all tags.

    Args:
        resource_type (str):
        image_name (str):
        source_workspace (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ImageSummary]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
        source_workspace=source_workspace,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
    source_workspace: Union[Unset, str] = UNSET,
) -> ImageSummary | None:
    """Get container image

     Returns a bounded image summary starting with API version 2026-09-22. Older versions return the
    image with all tags.

    Args:
        resource_type (str):
        image_name (str):
        source_workspace (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ImageSummary
    """

    return sync_detailed(
        resource_type=resource_type,
        image_name=image_name,
        client=client,
        source_workspace=source_workspace,
    ).parsed


async def asyncio_detailed(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
    source_workspace: Union[Unset, str] = UNSET,
) -> Response[ImageSummary]:
    """Get container image

     Returns a bounded image summary starting with API version 2026-09-22. Older versions return the
    image with all tags.

    Args:
        resource_type (str):
        image_name (str):
        source_workspace (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ImageSummary]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
        source_workspace=source_workspace,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
    source_workspace: Union[Unset, str] = UNSET,
) -> ImageSummary | None:
    """Get container image

     Returns a bounded image summary starting with API version 2026-09-22. Older versions return the
    image with all tags.

    Args:
        resource_type (str):
        image_name (str):
        source_workspace (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ImageSummary
    """

    return (
        await asyncio_detailed(
            resource_type=resource_type,
            image_name=image_name,
            client=client,
            source_workspace=source_workspace,
        )
    ).parsed

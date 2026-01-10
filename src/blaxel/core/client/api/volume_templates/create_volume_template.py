from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.volume_template import VolumeTemplate
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: VolumeTemplate,
    upload: Union[Unset, bool] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["upload"] = upload

    params["version"] = version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/volume_templates",
        "params": params,
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    *,
    client: Client,
    body: VolumeTemplate,
    upload: Union[Unset, bool] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> Response[VolumeTemplate]:
    """Create volume template

     Creates a new volume template for initializing volumes with pre-configured filesystem contents.
    Optionally returns a presigned URL for uploading the template archive.

    Args:
        upload (Union[Unset, bool]):
        version (Union[Unset, str]):
        body (VolumeTemplate): Volume template for creating pre-configured volumes

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VolumeTemplate]
    """

    kwargs = _get_kwargs(
        body=body,
        upload=upload,
        version=version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    body: VolumeTemplate,
    upload: Union[Unset, bool] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> VolumeTemplate | None:
    """Create volume template

     Creates a new volume template for initializing volumes with pre-configured filesystem contents.
    Optionally returns a presigned URL for uploading the template archive.

    Args:
        upload (Union[Unset, bool]):
        version (Union[Unset, str]):
        body (VolumeTemplate): Volume template for creating pre-configured volumes

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VolumeTemplate
    """

    return sync_detailed(
        client=client,
        body=body,
        upload=upload,
        version=version,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: VolumeTemplate,
    upload: Union[Unset, bool] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> Response[VolumeTemplate]:
    """Create volume template

     Creates a new volume template for initializing volumes with pre-configured filesystem contents.
    Optionally returns a presigned URL for uploading the template archive.

    Args:
        upload (Union[Unset, bool]):
        version (Union[Unset, str]):
        body (VolumeTemplate): Volume template for creating pre-configured volumes

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VolumeTemplate]
    """

    kwargs = _get_kwargs(
        body=body,
        upload=upload,
        version=version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: VolumeTemplate,
    upload: Union[Unset, bool] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> VolumeTemplate | None:
    """Create volume template

     Creates a new volume template for initializing volumes with pre-configured filesystem contents.
    Optionally returns a presigned URL for uploading the template archive.

    Args:
        upload (Union[Unset, bool]):
        version (Union[Unset, str]):
        body (VolumeTemplate): Volume template for creating pre-configured volumes

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VolumeTemplate
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            upload=upload,
            version=version,
        )
    ).parsed

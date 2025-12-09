from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.delete_volume_template_version_response_200 import (
    DeleteVolumeTemplateVersionResponse200,
)
from ...types import Response


def _get_kwargs(
    volume_template_name: str,
    version_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/volume_templates/{volume_template_name}/versions/{version_name}",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Any, DeleteVolumeTemplateVersionResponse200] | None:
    if response.status_code == 200:
        response_200 = DeleteVolumeTemplateVersionResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, DeleteVolumeTemplateVersionResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    volume_template_name: str,
    version_name: str,
    *,
    client: Client,
) -> Response[Union[Any, DeleteVolumeTemplateVersionResponse200]]:
    """Delete volume template version

     Deletes a specific version of a volume template.

    Args:
        volume_template_name (str):
        version_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteVolumeTemplateVersionResponse200]]
    """

    kwargs = _get_kwargs(
        volume_template_name=volume_template_name,
        version_name=version_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    volume_template_name: str,
    version_name: str,
    *,
    client: Client,
) -> Union[Any, DeleteVolumeTemplateVersionResponse200] | None:
    """Delete volume template version

     Deletes a specific version of a volume template.

    Args:
        volume_template_name (str):
        version_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteVolumeTemplateVersionResponse200]
    """

    return sync_detailed(
        volume_template_name=volume_template_name,
        version_name=version_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    volume_template_name: str,
    version_name: str,
    *,
    client: Client,
) -> Response[Union[Any, DeleteVolumeTemplateVersionResponse200]]:
    """Delete volume template version

     Deletes a specific version of a volume template.

    Args:
        volume_template_name (str):
        version_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteVolumeTemplateVersionResponse200]]
    """

    kwargs = _get_kwargs(
        volume_template_name=volume_template_name,
        version_name=version_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    volume_template_name: str,
    version_name: str,
    *,
    client: Client,
) -> Union[Any, DeleteVolumeTemplateVersionResponse200] | None:
    """Delete volume template version

     Deletes a specific version of a volume template.

    Args:
        volume_template_name (str):
        version_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteVolumeTemplateVersionResponse200]
    """

    return (
        await asyncio_detailed(
            volume_template_name=volume_template_name,
            version_name=version_name,
            client=client,
        )
    ).parsed

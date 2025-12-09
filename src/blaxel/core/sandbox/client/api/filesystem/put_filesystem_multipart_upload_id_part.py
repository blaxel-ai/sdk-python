from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.multipart_upload_part_response import MultipartUploadPartResponse
from ...models.put_filesystem_multipart_upload_id_part_body import (
    PutFilesystemMultipartUploadIdPartBody,
)
from ...types import UNSET, Response


def _get_kwargs(
    upload_id: str,
    *,
    body: PutFilesystemMultipartUploadIdPartBody,
    part_number: int,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["partNumber"] = part_number

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/filesystem-multipart/{upload_id}/part",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[ErrorResponse, MultipartUploadPartResponse] | None:
    if response.status_code == 200:
        response_200 = MultipartUploadPartResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ErrorResponse, MultipartUploadPartResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    upload_id: str,
    *,
    client: Client,
    body: PutFilesystemMultipartUploadIdPartBody,
    part_number: int,
) -> Response[Union[ErrorResponse, MultipartUploadPartResponse]]:
    """Upload part

     Upload a single part of a multipart upload

    Args:
        upload_id (str):
        part_number (int):
        body (PutFilesystemMultipartUploadIdPartBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MultipartUploadPartResponse]]
    """

    kwargs = _get_kwargs(
        upload_id=upload_id,
        body=body,
        part_number=part_number,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    upload_id: str,
    *,
    client: Client,
    body: PutFilesystemMultipartUploadIdPartBody,
    part_number: int,
) -> Union[ErrorResponse, MultipartUploadPartResponse] | None:
    """Upload part

     Upload a single part of a multipart upload

    Args:
        upload_id (str):
        part_number (int):
        body (PutFilesystemMultipartUploadIdPartBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MultipartUploadPartResponse]
    """

    return sync_detailed(
        upload_id=upload_id,
        client=client,
        body=body,
        part_number=part_number,
    ).parsed


async def asyncio_detailed(
    upload_id: str,
    *,
    client: Client,
    body: PutFilesystemMultipartUploadIdPartBody,
    part_number: int,
) -> Response[Union[ErrorResponse, MultipartUploadPartResponse]]:
    """Upload part

     Upload a single part of a multipart upload

    Args:
        upload_id (str):
        part_number (int):
        body (PutFilesystemMultipartUploadIdPartBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MultipartUploadPartResponse]]
    """

    kwargs = _get_kwargs(
        upload_id=upload_id,
        body=body,
        part_number=part_number,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    upload_id: str,
    *,
    client: Client,
    body: PutFilesystemMultipartUploadIdPartBody,
    part_number: int,
) -> Union[ErrorResponse, MultipartUploadPartResponse] | None:
    """Upload part

     Upload a single part of a multipart upload

    Args:
        upload_id (str):
        part_number (int):
        body (PutFilesystemMultipartUploadIdPartBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MultipartUploadPartResponse]
    """

    return (
        await asyncio_detailed(
            upload_id=upload_id,
            client=client,
            body=body,
            part_number=part_number,
        )
    ).parsed

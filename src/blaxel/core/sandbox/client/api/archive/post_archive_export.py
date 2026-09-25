from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.export_options import ExportOptions
from ...models.export_progress import ExportProgress
from ...models.export_result import ExportResult
from ...types import Response


def _get_kwargs(
    *,
    body: ExportOptions,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/archive/export",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[ErrorResponse, ExportProgress, ExportResult] | None:
    if response.status_code == 200:
        response_200 = ExportResult.from_dict(response.json())

        return response_200
    if response.status_code == 202:
        response_202 = ExportProgress.from_dict(response.json())

        return response_202
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ErrorResponse, ExportProgress, ExportResult]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: ExportOptions,
) -> Response[Union[ErrorResponse, ExportProgress, ExportResult]]:
    """Export the filesystem changes to a presigned URL

     Archives everything the sandbox changed on top of its base image and streams it, uncompressed, to a
    presigned S3 PUT URL. The memory of the sandbox is not archived.
    The sandbox is quiesced first: the process list is saved (unless saveProcesses is false), every
    process is stopped, and the API then refuses the calls that would write to the filesystem. The
    freeze is not lifted afterwards, since an exported sandbox is meant to be restored elsewhere; call
    POST /archive/resume to lift it.
    Use dryRun to get the archive's content and exact size without stopping anything and without
    uploading.
    Set async to start the export and answer immediately, which is what archiving a large filesystem
    needs: the export then reports itself through GET /archive/status.

    Args:
        body (ExportOptions):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ExportProgress, ExportResult]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    body: ExportOptions,
) -> Union[ErrorResponse, ExportProgress, ExportResult] | None:
    """Export the filesystem changes to a presigned URL

     Archives everything the sandbox changed on top of its base image and streams it, uncompressed, to a
    presigned S3 PUT URL. The memory of the sandbox is not archived.
    The sandbox is quiesced first: the process list is saved (unless saveProcesses is false), every
    process is stopped, and the API then refuses the calls that would write to the filesystem. The
    freeze is not lifted afterwards, since an exported sandbox is meant to be restored elsewhere; call
    POST /archive/resume to lift it.
    Use dryRun to get the archive's content and exact size without stopping anything and without
    uploading.
    Set async to start the export and answer immediately, which is what archiving a large filesystem
    needs: the export then reports itself through GET /archive/status.

    Args:
        body (ExportOptions):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ExportProgress, ExportResult]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: ExportOptions,
) -> Response[Union[ErrorResponse, ExportProgress, ExportResult]]:
    """Export the filesystem changes to a presigned URL

     Archives everything the sandbox changed on top of its base image and streams it, uncompressed, to a
    presigned S3 PUT URL. The memory of the sandbox is not archived.
    The sandbox is quiesced first: the process list is saved (unless saveProcesses is false), every
    process is stopped, and the API then refuses the calls that would write to the filesystem. The
    freeze is not lifted afterwards, since an exported sandbox is meant to be restored elsewhere; call
    POST /archive/resume to lift it.
    Use dryRun to get the archive's content and exact size without stopping anything and without
    uploading.
    Set async to start the export and answer immediately, which is what archiving a large filesystem
    needs: the export then reports itself through GET /archive/status.

    Args:
        body (ExportOptions):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ExportProgress, ExportResult]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: ExportOptions,
) -> Union[ErrorResponse, ExportProgress, ExportResult] | None:
    """Export the filesystem changes to a presigned URL

     Archives everything the sandbox changed on top of its base image and streams it, uncompressed, to a
    presigned S3 PUT URL. The memory of the sandbox is not archived.
    The sandbox is quiesced first: the process list is saved (unless saveProcesses is false), every
    process is stopped, and the API then refuses the calls that would write to the filesystem. The
    freeze is not lifted afterwards, since an exported sandbox is meant to be restored elsewhere; call
    POST /archive/resume to lift it.
    Use dryRun to get the archive's content and exact size without stopping anything and without
    uploading.
    Set async to start the export and answer immediately, which is what archiving a large filesystem
    needs: the export then reports itself through GET /archive/status.

    Args:
        body (ExportOptions):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ExportProgress, ExportResult]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

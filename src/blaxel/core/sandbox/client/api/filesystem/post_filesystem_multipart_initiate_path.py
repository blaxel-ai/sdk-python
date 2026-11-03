from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.multipart_initiate_request import MultipartInitiateRequest
from ...models.multipart_initiate_response import MultipartInitiateResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    path: str,
    *,
    body: MultipartInitiateRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/filesystem-multipart/initiate/{path}".format(
            path=quote(str(path), safe=""),
        ),
    }

    if body and not isinstance(body, Unset) and not isinstance(body, dict):
        _kwargs["json"] = body.to_dict()
    elif body and isinstance(body, dict):
        _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> ErrorResponse | MultipartInitiateResponse | None:
    if response.status_code == 200:
        response_200 = MultipartInitiateResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_400, response)
        return response_400

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_500, response)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[ErrorResponse | MultipartInitiateResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    path: str,
    *,
    client: Client,
    body: MultipartInitiateRequest | Unset = UNSET,
) -> Response[ErrorResponse | MultipartInitiateResponse]:
    """Initiate multipart upload

     Initiate a multipart upload session for a file

    Args:
        path (str):
        body (MultipartInitiateRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MultipartInitiateResponse]
    """

    kwargs = _get_kwargs(
        path=path,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    path: str,
    *,
    client: Client,
    body: MultipartInitiateRequest | Unset = UNSET,
) -> ErrorResponse | MultipartInitiateResponse | None:
    """Initiate multipart upload

     Initiate a multipart upload session for a file

    Args:
        path (str):
        body (MultipartInitiateRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MultipartInitiateResponse
    """

    return sync_detailed(
        path=path,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    path: str,
    *,
    client: Client,
    body: MultipartInitiateRequest | Unset = UNSET,
) -> Response[ErrorResponse | MultipartInitiateResponse]:
    """Initiate multipart upload

     Initiate a multipart upload session for a file

    Args:
        path (str):
        body (MultipartInitiateRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MultipartInitiateResponse]
    """

    kwargs = _get_kwargs(
        path=path,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    path: str,
    *,
    client: Client,
    body: MultipartInitiateRequest | Unset = UNSET,
) -> ErrorResponse | MultipartInitiateResponse | None:
    """Initiate multipart upload

     Initiate a multipart upload session for a file

    Args:
        path (str):
        body (MultipartInitiateRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MultipartInitiateResponse
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
            body=body,
        )
    ).parsed

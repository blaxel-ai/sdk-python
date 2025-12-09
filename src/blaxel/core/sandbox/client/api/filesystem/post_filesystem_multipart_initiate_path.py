from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.multipart_initiate_request import MultipartInitiateRequest
from ...models.multipart_initiate_response import MultipartInitiateResponse
from ...types import Response


def _get_kwargs(
    path: str,
    *,
    body: MultipartInitiateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/filesystem-multipart/initiate/{path}",
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
) -> Union[ErrorResponse, MultipartInitiateResponse] | None:
    if response.status_code == 200:
        response_200 = MultipartInitiateResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ErrorResponse, MultipartInitiateResponse]]:
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
    body: MultipartInitiateRequest,
) -> Response[Union[ErrorResponse, MultipartInitiateResponse]]:
    """Initiate multipart upload

     Initiate a multipart upload session for a file

    Args:
        path (str):
        body (MultipartInitiateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MultipartInitiateResponse]]
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
    body: MultipartInitiateRequest,
) -> Union[ErrorResponse, MultipartInitiateResponse] | None:
    """Initiate multipart upload

     Initiate a multipart upload session for a file

    Args:
        path (str):
        body (MultipartInitiateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MultipartInitiateResponse]
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
    body: MultipartInitiateRequest,
) -> Response[Union[ErrorResponse, MultipartInitiateResponse]]:
    """Initiate multipart upload

     Initiate a multipart upload session for a file

    Args:
        path (str):
        body (MultipartInitiateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, MultipartInitiateResponse]]
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
    body: MultipartInitiateRequest,
) -> Union[ErrorResponse, MultipartInitiateResponse] | None:
    """Initiate multipart upload

     Initiate a multipart upload session for a file

    Args:
        path (str):
        body (MultipartInitiateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, MultipartInitiateResponse]
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
            body=body,
        )
    ).parsed

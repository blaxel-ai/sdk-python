from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.success_response import SuccessResponse
from ...types import Response


def _get_kwargs(
    identifier: str,
    *,
    body: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/process/{identifier}/stdin",
    }

    _body = body

    _kwargs["content"] = _body
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[ErrorResponse, SuccessResponse] | None:
    if response.status_code == 200:
        response_200 = SuccessResponse.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409
    if response.status_code == 413:
        response_413 = ErrorResponse.from_dict(response.json())

        return response_413
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ErrorResponse, SuccessResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    identifier: str,
    *,
    client: Client,
    body: str,
) -> Response[Union[ErrorResponse, SuccessResponse]]:
    r"""Write to a process's stdin

     Write the raw request body to the stdin of a process started with \"stdin\": true. Bytes are
    forwarded verbatim, so include the trailing newline your protocol expects. Sequential requests keep
    their order; each body is written atomically with respect to other writers. The pipe does not
    survive a sandbox-api restart: once it is gone this returns 409 and the process must be restarted.

    Args:
        identifier (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    identifier: str,
    *,
    client: Client,
    body: str,
) -> Union[ErrorResponse, SuccessResponse] | None:
    r"""Write to a process's stdin

     Write the raw request body to the stdin of a process started with \"stdin\": true. Bytes are
    forwarded verbatim, so include the trailing newline your protocol expects. Sequential requests keep
    their order; each body is written atomically with respect to other writers. The pipe does not
    survive a sandbox-api restart: once it is gone this returns 409 and the process must be restarted.

    Args:
        identifier (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SuccessResponse]
    """

    return sync_detailed(
        identifier=identifier,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    identifier: str,
    *,
    client: Client,
    body: str,
) -> Response[Union[ErrorResponse, SuccessResponse]]:
    r"""Write to a process's stdin

     Write the raw request body to the stdin of a process started with \"stdin\": true. Bytes are
    forwarded verbatim, so include the trailing newline your protocol expects. Sequential requests keep
    their order; each body is written atomically with respect to other writers. The pipe does not
    survive a sandbox-api restart: once it is gone this returns 409 and the process must be restarted.

    Args:
        identifier (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    identifier: str,
    *,
    client: Client,
    body: str,
) -> Union[ErrorResponse, SuccessResponse] | None:
    r"""Write to a process's stdin

     Write the raw request body to the stdin of a process started with \"stdin\": true. Bytes are
    forwarded verbatim, so include the trailing newline your protocol expects. Sequential requests keep
    their order; each body is written atomically with respect to other writers. The pipe does not
    survive a sandbox-api restart: once it is gone this returns 409 and the process must be restarted.

    Args:
        identifier (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SuccessResponse]
    """

    return (
        await asyncio_detailed(
            identifier=identifier,
            client=client,
            body=body,
        )
    ).parsed

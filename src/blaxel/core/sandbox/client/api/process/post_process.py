from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.process_request import ProcessRequest
from ...models.process_response import ProcessResponse
from ...types import Response


def _get_kwargs(
    *,
    body: ProcessRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/process",
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
) -> Union[ErrorResponse, ProcessResponse] | None:
    if response.status_code == 200:
        response_200 = ProcessResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_400, response)
        return response_400
    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_422, response)
        return response_422
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
) -> Response[Union[ErrorResponse, ProcessResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: ProcessRequest,
) -> Response[Union[ErrorResponse, ProcessResponse]]:
    r"""Execute a command

     Execute a command and return process information.

    Streaming: with `Accept: application/x-ndjson` (or `Accept: text/event-stream`, kept for
    compatibility) the response is NDJSON (`Content-Type: application/x-ndjson`), not SSE: one JSON
    object per line, `{\"type\": \"...\", \"data\": \"...\"}`.
    `type` is `stdout` or `stderr` (`data` is a raw output chunk, sent as soon as the process writes it,
    newlines included; if the process finished before any chunk was streamed, its output is sent instead
    as one event per line, without the newline), `keepalive` (every 5 seconds, no data), `error` (`data`
    is the message, ends the stream) or `result` (last event, `data` is the ProcessResponse as a JSON
    string).

    Args:
        body (ProcessRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ProcessResponse]]
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
    body: ProcessRequest,
) -> Union[ErrorResponse, ProcessResponse] | None:
    r"""Execute a command

     Execute a command and return process information.

    Streaming: with `Accept: application/x-ndjson` (or `Accept: text/event-stream`, kept for
    compatibility) the response is NDJSON (`Content-Type: application/x-ndjson`), not SSE: one JSON
    object per line, `{\"type\": \"...\", \"data\": \"...\"}`.
    `type` is `stdout` or `stderr` (`data` is a raw output chunk, sent as soon as the process writes it,
    newlines included; if the process finished before any chunk was streamed, its output is sent instead
    as one event per line, without the newline), `keepalive` (every 5 seconds, no data), `error` (`data`
    is the message, ends the stream) or `result` (last event, `data` is the ProcessResponse as a JSON
    string).

    Args:
        body (ProcessRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ProcessResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: ProcessRequest,
) -> Response[Union[ErrorResponse, ProcessResponse]]:
    r"""Execute a command

     Execute a command and return process information.

    Streaming: with `Accept: application/x-ndjson` (or `Accept: text/event-stream`, kept for
    compatibility) the response is NDJSON (`Content-Type: application/x-ndjson`), not SSE: one JSON
    object per line, `{\"type\": \"...\", \"data\": \"...\"}`.
    `type` is `stdout` or `stderr` (`data` is a raw output chunk, sent as soon as the process writes it,
    newlines included; if the process finished before any chunk was streamed, its output is sent instead
    as one event per line, without the newline), `keepalive` (every 5 seconds, no data), `error` (`data`
    is the message, ends the stream) or `result` (last event, `data` is the ProcessResponse as a JSON
    string).

    Args:
        body (ProcessRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, ProcessResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: ProcessRequest,
) -> Union[ErrorResponse, ProcessResponse] | None:
    r"""Execute a command

     Execute a command and return process information.

    Streaming: with `Accept: application/x-ndjson` (or `Accept: text/event-stream`, kept for
    compatibility) the response is NDJSON (`Content-Type: application/x-ndjson`), not SSE: one JSON
    object per line, `{\"type\": \"...\", \"data\": \"...\"}`.
    `type` is `stdout` or `stderr` (`data` is a raw output chunk, sent as soon as the process writes it,
    newlines included; if the process finished before any chunk was streamed, its output is sent instead
    as one event per line, without the newline), `keepalive` (every 5 seconds, no data), `error` (`data`
    is the message, ends the stream) or `result` (last event, `data` is the ProcessResponse as a JSON
    string).

    Args:
        body (ProcessRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, ProcessResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

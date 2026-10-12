from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    identifier: str,
    *,
    accept: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/process/{identifier}/logs/stream",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[ErrorResponse, str] | None:
    if response.status_code == 200:
        response_200 = response.text
        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_400, response)
        return response_400
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_404, response)
        return response_404
    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_409, response)
        return response_409
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
) -> Response[Union[ErrorResponse, str]]:
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
    accept: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, str]]:
    r"""Stream process logs in real time

     Streams the stdout and stderr output of a process in real time: the output so far, then live output
    as the process writes it. Closes when the process exits or the client disconnects.
    By default, output is plain text with `stdout:` or `stderr:` prefixes at the start of each source
    stream's lines. Partial lines (e.g. prompts) are sent without waiting for a newline; their
    continuations have no new prefix. The other stream is not held back while a line is incomplete, and
    chronological order across stdout and stderr is not guaranteed.
    This format does not provide unambiguous framing: output from the other stream, or a `[keepalive]`
    marker sent every 30 seconds, can appear inside an unfinished line. A later continuation can
    therefore lack a prefix identifying its source. Do not rely on this text stream to reconstruct
    stdout and stderr separately; request NDJSON for source-preserving streaming, or use GET
    /process/{identifier}/logs for separate output snapshots.
    With `Accept: application/x-ndjson`, each line is a JSON object with `type` (`stdout`, `stderr`,
    `keepalive`, `restart`, `truncated`, or `error`) and optional `data`. Output records retain source
    identity and original bytes, including partial lines and newlines, for both retained history and
    live output. For `encoding: \"base64\"`, decode `data` before concatenating bytes per source; this
    occurs for binary data or a UTF-8 character split across chunks. Chunk boundaries are arbitrary and
    ordering is collection order, not a strict chronology across streams.
    `keepalive` has no output data. A quiet active stream sends an initial keepalive after attachment so
    clients can receive the response before sending stdin; subsequent keepalives are sent every 30
    seconds. `restart` carries a supervisor restart notice, not process output. `truncated` reports a
    retention or slow-reader gap and must not be appended to stdout/stderr. `error` reports a streaming
    failure. The connection ends after the final process exit, including automatic restarts; there is no
    `result` record. Older processes without structured history return HTTP 409 for NDJSON; their text
    stream remains available.

    Args:
        identifier (str):
        accept (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, str]]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        accept=accept,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    identifier: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Union[ErrorResponse, str] | None:
    r"""Stream process logs in real time

     Streams the stdout and stderr output of a process in real time: the output so far, then live output
    as the process writes it. Closes when the process exits or the client disconnects.
    By default, output is plain text with `stdout:` or `stderr:` prefixes at the start of each source
    stream's lines. Partial lines (e.g. prompts) are sent without waiting for a newline; their
    continuations have no new prefix. The other stream is not held back while a line is incomplete, and
    chronological order across stdout and stderr is not guaranteed.
    This format does not provide unambiguous framing: output from the other stream, or a `[keepalive]`
    marker sent every 30 seconds, can appear inside an unfinished line. A later continuation can
    therefore lack a prefix identifying its source. Do not rely on this text stream to reconstruct
    stdout and stderr separately; request NDJSON for source-preserving streaming, or use GET
    /process/{identifier}/logs for separate output snapshots.
    With `Accept: application/x-ndjson`, each line is a JSON object with `type` (`stdout`, `stderr`,
    `keepalive`, `restart`, `truncated`, or `error`) and optional `data`. Output records retain source
    identity and original bytes, including partial lines and newlines, for both retained history and
    live output. For `encoding: \"base64\"`, decode `data` before concatenating bytes per source; this
    occurs for binary data or a UTF-8 character split across chunks. Chunk boundaries are arbitrary and
    ordering is collection order, not a strict chronology across streams.
    `keepalive` has no output data. A quiet active stream sends an initial keepalive after attachment so
    clients can receive the response before sending stdin; subsequent keepalives are sent every 30
    seconds. `restart` carries a supervisor restart notice, not process output. `truncated` reports a
    retention or slow-reader gap and must not be appended to stdout/stderr. `error` reports a streaming
    failure. The connection ends after the final process exit, including automatic restarts; there is no
    `result` record. Older processes without structured history return HTTP 409 for NDJSON; their text
    stream remains available.

    Args:
        identifier (str):
        accept (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, str]
    """

    return sync_detailed(
        identifier=identifier,
        client=client,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    identifier: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, str]]:
    r"""Stream process logs in real time

     Streams the stdout and stderr output of a process in real time: the output so far, then live output
    as the process writes it. Closes when the process exits or the client disconnects.
    By default, output is plain text with `stdout:` or `stderr:` prefixes at the start of each source
    stream's lines. Partial lines (e.g. prompts) are sent without waiting for a newline; their
    continuations have no new prefix. The other stream is not held back while a line is incomplete, and
    chronological order across stdout and stderr is not guaranteed.
    This format does not provide unambiguous framing: output from the other stream, or a `[keepalive]`
    marker sent every 30 seconds, can appear inside an unfinished line. A later continuation can
    therefore lack a prefix identifying its source. Do not rely on this text stream to reconstruct
    stdout and stderr separately; request NDJSON for source-preserving streaming, or use GET
    /process/{identifier}/logs for separate output snapshots.
    With `Accept: application/x-ndjson`, each line is a JSON object with `type` (`stdout`, `stderr`,
    `keepalive`, `restart`, `truncated`, or `error`) and optional `data`. Output records retain source
    identity and original bytes, including partial lines and newlines, for both retained history and
    live output. For `encoding: \"base64\"`, decode `data` before concatenating bytes per source; this
    occurs for binary data or a UTF-8 character split across chunks. Chunk boundaries are arbitrary and
    ordering is collection order, not a strict chronology across streams.
    `keepalive` has no output data. A quiet active stream sends an initial keepalive after attachment so
    clients can receive the response before sending stdin; subsequent keepalives are sent every 30
    seconds. `restart` carries a supervisor restart notice, not process output. `truncated` reports a
    retention or slow-reader gap and must not be appended to stdout/stderr. `error` reports a streaming
    failure. The connection ends after the final process exit, including automatic restarts; there is no
    `result` record. Older processes without structured history return HTTP 409 for NDJSON; their text
    stream remains available.

    Args:
        identifier (str):
        accept (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, str]]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        accept=accept,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    identifier: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Union[ErrorResponse, str] | None:
    r"""Stream process logs in real time

     Streams the stdout and stderr output of a process in real time: the output so far, then live output
    as the process writes it. Closes when the process exits or the client disconnects.
    By default, output is plain text with `stdout:` or `stderr:` prefixes at the start of each source
    stream's lines. Partial lines (e.g. prompts) are sent without waiting for a newline; their
    continuations have no new prefix. The other stream is not held back while a line is incomplete, and
    chronological order across stdout and stderr is not guaranteed.
    This format does not provide unambiguous framing: output from the other stream, or a `[keepalive]`
    marker sent every 30 seconds, can appear inside an unfinished line. A later continuation can
    therefore lack a prefix identifying its source. Do not rely on this text stream to reconstruct
    stdout and stderr separately; request NDJSON for source-preserving streaming, or use GET
    /process/{identifier}/logs for separate output snapshots.
    With `Accept: application/x-ndjson`, each line is a JSON object with `type` (`stdout`, `stderr`,
    `keepalive`, `restart`, `truncated`, or `error`) and optional `data`. Output records retain source
    identity and original bytes, including partial lines and newlines, for both retained history and
    live output. For `encoding: \"base64\"`, decode `data` before concatenating bytes per source; this
    occurs for binary data or a UTF-8 character split across chunks. Chunk boundaries are arbitrary and
    ordering is collection order, not a strict chronology across streams.
    `keepalive` has no output data. A quiet active stream sends an initial keepalive after attachment so
    clients can receive the response before sending stdin; subsequent keepalives are sent every 30
    seconds. `restart` carries a supervisor restart notice, not process output. `truncated` reports a
    retention or slow-reader gap and must not be appended to stdout/stderr. `error` reports a streaming
    failure. The connection ends after the final process exit, including automatic restarts; there is no
    `result` record. Older processes without structured history return HTTP 409 for NDJSON; their text
    stream remains available.

    Args:
        identifier (str):
        accept (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, str]
    """

    return (
        await asyncio_detailed(
            identifier=identifier,
            client=client,
            accept=accept,
        )
    ).parsed

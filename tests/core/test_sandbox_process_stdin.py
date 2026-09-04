"""Wire-format tests for process stdin.

stdin bodies must reach the wire verbatim as ``application/octet-stream``: a
JSON encoding would turn a JSON-RPC line into a quoted string.
"""

from typing import Any, cast

import httpx
import pytest

from blaxel.core.sandbox.client.api.process import post_process_identifier_stdin
from blaxel.core.sandbox.client.client import Client
from blaxel.core.sandbox.client.models import SuccessResponse
from blaxel.core.sandbox.default.process import SandboxProcess
from blaxel.core.sandbox.sync.process import SyncSandboxProcess
from blaxel.core.sandbox.types import ResponseError

BASE_URL = "http://sandbox"
LINE = '{"jsonrpc":"2.0","id":1,"method":"ping"}\n'


class RecordingTransport(httpx.MockTransport):
    """Answers every request with the given response and keeps what it saw."""

    def __init__(self, status_code: int = 200, body: dict[str, Any] | None = None):
        self.requests: list[httpx.Request] = []
        self._status_code = status_code
        self._body = body if body is not None else {"message": "ok"}
        super().__init__(self._handle)

    def _handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return httpx.Response(self._status_code, json=self._body)

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]


def api_client(transport: httpx.MockTransport) -> Client:
    """Generated client whose sync and async httpx clients both use ``transport``."""
    return Client(
        base_url=BASE_URL,
        headers={},
        raise_on_unexpected_status=False,
        httpx_args={"transport": transport},
    )


def async_process(transport: httpx.MockTransport) -> Any:
    process = cast(Any, object.__new__(SandboxProcess))
    process.get_api_client = lambda: api_client(transport)
    return process


def sync_process(transport: httpx.MockTransport) -> Any:
    process = cast(Any, object.__new__(SyncSandboxProcess))
    process.get_api_client = lambda: api_client(transport)
    return process


def assert_stdin_write(request: httpx.Request, body: bytes) -> None:
    assert request.method == "POST"
    assert request.url.path == "/process/mcp/stdin"
    assert request.headers["content-type"] == "application/octet-stream"
    assert request.content == body


def assert_stdin_close(request: httpx.Request) -> None:
    assert request.method == "DELETE"
    assert request.url.path == "/process/mcp/stdin"
    assert request.content == b""


def test_generated_stdin_endpoint_sends_a_str_body():
    """The generated octet-stream helper must accept a plain str (no ``.payload``)."""
    transport = RecordingTransport()
    result = post_process_identifier_stdin.sync("mcp", client=api_client(transport), body=LINE)
    assert_stdin_write(transport.last, LINE.encode())
    assert isinstance(result, SuccessResponse)


async def test_async_write_stdin_sends_body_verbatim():
    transport = RecordingTransport()
    result = await async_process(transport).write_stdin("mcp", LINE)
    assert_stdin_write(transport.last, LINE.encode())
    assert isinstance(result, SuccessResponse)


async def test_async_write_stdin_accepts_bytes():
    transport = RecordingTransport()
    await async_process(transport).write_stdin("mcp", b"\x00\xffraw\n")
    assert_stdin_write(transport.last, b"\x00\xffraw\n")


async def test_async_close_stdin_sends_delete():
    transport = RecordingTransport()
    result = await async_process(transport).close_stdin("mcp")
    assert_stdin_close(transport.last)
    assert isinstance(result, SuccessResponse)


async def test_async_write_stdin_surfaces_409():
    transport = RecordingTransport(409, {"error": "process has no stdin"})
    with pytest.raises(ResponseError) as raised:
        await async_process(transport).write_stdin("mcp", LINE)
    assert raised.value.response.status_code == 409


async def test_async_write_stdin_surfaces_undocumented_502():
    transport = RecordingTransport(502, {})
    with pytest.raises(ResponseError) as raised:
        await async_process(transport).write_stdin("mcp", LINE)
    assert raised.value.response.status_code == 502


def test_sync_write_stdin_sends_body_verbatim():
    transport = RecordingTransport()
    result = sync_process(transport).write_stdin("mcp", LINE)
    assert_stdin_write(transport.last, LINE.encode())
    assert isinstance(result, SuccessResponse)


def test_sync_write_stdin_accepts_bytes():
    transport = RecordingTransport()
    sync_process(transport).write_stdin("mcp", b"\x00\xffraw\n")
    assert_stdin_write(transport.last, b"\x00\xffraw\n")


def test_sync_close_stdin_sends_delete():
    transport = RecordingTransport()
    result = sync_process(transport).close_stdin("mcp")
    assert_stdin_close(transport.last)
    assert isinstance(result, SuccessResponse)


def test_sync_write_stdin_surfaces_409():
    transport = RecordingTransport(409, {"error": "process has no stdin"})
    with pytest.raises(ResponseError) as raised:
        sync_process(transport).write_stdin("mcp", LINE)
    assert raised.value.response.status_code == 409

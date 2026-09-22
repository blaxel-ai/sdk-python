import asyncio
from typing import Any, cast

import httpx
import pytest

from blaxel.core.common.settings import settings
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.default.process import SandboxProcess
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem
from blaxel.core.sandbox.transient_retry import (
    is_transient_reset_error,
    retry_on_transient_reset,
    retry_on_transient_reset_async,
)
from blaxel.core.sandbox.types import ResponseError


class LoopbackFaultServer:
    def __init__(self, *handlers):
        self.handlers = handlers
        self.requests = 0
        self.server: asyncio.Server | None = None
        self.url = ""

    async def __aenter__(self):
        self.server = await asyncio.start_server(self._handle, "127.0.0.1", 0)
        socket = self.server.sockets[0]
        host, port = socket.getsockname()[:2]
        self.url = f"http://{host}:{port}"
        return self

    async def __aexit__(self, *args):
        if self.server is not None:
            self.server.close()
            await self.server.wait_closed()

    async def _handle(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        index = self.requests
        self.requests += 1
        handler = self.handlers[min(index, len(self.handlers) - 1)]
        await handler(reader, writer)


class AsyncSequenceClient:
    def __init__(self, *results):
        self.results = list(results)
        self.calls = 0

    async def get(self, *args, **kwargs):
        self.calls += 1
        result = self.results.pop(0)
        if isinstance(result, BaseException):
            raise result
        return result

    async def post(self, *args, **kwargs):
        self.calls += 1
        result = self.results.pop(0)
        if isinstance(result, BaseException):
            raise result
        return result


class SyncSequenceClient:
    def __init__(self, *results):
        self.results = list(results)
        self.calls = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def get(self, *args, **kwargs):
        self.calls += 1
        result = self.results.pop(0)
        if isinstance(result, BaseException):
            raise result
        return result


def ok_json_response(data):
    return httpx.Response(
        200,
        json=data,
        request=httpx.Request("GET", "https://sandbox.test"),
    )


def app_error_response() -> ResponseError:
    response = httpx.Response(
        500,
        json={"error": "GOAWAY in an application body"},
        request=httpx.Request("GET", "https://sandbox.test"),
    )
    return ResponseError(response)


async def close_without_response(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    try:
        await asyncio.wait_for(reader.read(1024), timeout=0.2)
    except TimeoutError:
        pass
    writer.close()
    await writer.wait_closed()


async def send_ok_response(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    try:
        await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout=1.0)
    except (TimeoutError, asyncio.IncompleteReadError, asyncio.LimitOverrunError):
        pass
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\nok")
    await writer.drain()
    writer.close()
    await writer.wait_closed()


@pytest.fixture(autouse=True)
def no_retry_sleep(monkeypatch):
    monkeypatch.setattr(
        "blaxel.core.sandbox.transient_retry._backoff_delay_seconds",
        lambda *args: 0,
    )


def test_retry_settings_defaults_and_env(monkeypatch):
    monkeypatch.delenv("BL_FS_PART_RETRIES", raising=False)
    monkeypatch.delenv("BL_SANDBOX_READ_RETRIES", raising=False)
    assert settings.fs_part_retries == 3
    assert settings.sandbox_read_retries == 5

    monkeypatch.setenv("BL_FS_PART_RETRIES", "1")
    monkeypatch.setenv("BL_SANDBOX_READ_RETRIES", "2")
    assert settings.fs_part_retries == 1
    assert settings.sandbox_read_retries == 2


def test_classifier_accepts_httpx_transport_drops():
    assert is_transient_reset_error(httpx.ConnectError("All connection attempts failed"))
    assert is_transient_reset_error(httpx.RemoteProtocolError("GOAWAY received"))
    assert is_transient_reset_error(httpx.ReadTimeout("timed out"))


def test_classifier_rejects_application_responses():
    assert not is_transient_reset_error(app_error_response())


@pytest.mark.asyncio
async def test_real_httpx_transport_drop_is_classified_transient():
    async with LoopbackFaultServer(close_without_response) as server:
        async with httpx.AsyncClient(timeout=2.0) as client:
            with pytest.raises(httpx.TransportError) as exc_info:
                await client.get(server.url)

    assert is_transient_reset_error(exc_info.value)
    assert server.requests == 1


@pytest.mark.asyncio
async def test_async_retry_counts_real_transport_fault_attempts():
    async with LoopbackFaultServer(close_without_response) as server:
        async with httpx.AsyncClient(timeout=2.0) as client:
            with pytest.raises(httpx.TransportError):
                await retry_on_transient_reset_async(
                    lambda: client.get(server.url),
                    retries=2,
                )

    assert server.requests == 3


@pytest.mark.asyncio
async def test_async_retry_self_heals_after_real_transport_fault_clears():
    async with LoopbackFaultServer(close_without_response, send_ok_response) as server:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await retry_on_transient_reset_async(
                lambda: client.get(server.url),
                retries=1,
            )

    assert response.status_code == 200
    assert response.text == "ok"
    assert server.requests == 2


@pytest.mark.asyncio
async def test_async_retry_recovers_once():
    calls = 0

    async def flaky():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ConnectError("All connection attempts failed")
        return "ok"

    assert await retry_on_transient_reset_async(flaky, retries=1) == "ok"
    assert calls == 2


def test_sync_retry_recovers_once():
    calls = 0

    def flaky():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ConnectError("All connection attempts failed")
        return "ok"

    assert retry_on_transient_reset(flaky, retries=1) == "ok"
    assert calls == 2


def test_sync_retry_does_not_retry_application_response():
    calls = 0

    def app_error():
        nonlocal calls
        calls += 1
        raise app_error_response()

    with pytest.raises(ResponseError):
        retry_on_transient_reset(app_error, retries=3)
    assert calls == 1


@pytest.mark.asyncio
async def test_async_filesystem_read_retries_transport_reset(monkeypatch):
    monkeypatch.setenv("BL_SANDBOX_READ_RETRIES", "1")
    client = AsyncSequenceClient(
        httpx.ConnectError("All connection attempts failed"),
        ok_json_response({"content": "hello"}),
    )
    filesystem = cast(Any, object.__new__(SandboxFileSystem))
    filesystem.get_client = lambda: client

    assert await filesystem.read("/file.txt") == "hello"
    assert client.calls == 2


def test_sync_filesystem_read_retries_transport_reset(monkeypatch):
    monkeypatch.setenv("BL_SANDBOX_READ_RETRIES", "1")
    client = SyncSequenceClient(
        httpx.ConnectError("All connection attempts failed"),
        ok_json_response({"content": "hello"}),
    )
    filesystem = cast(Any, object.__new__(SyncSandboxFileSystem))
    filesystem.get_client = lambda: client

    assert filesystem.read("/file.txt") == "hello"
    assert client.calls == 2


@pytest.mark.asyncio
async def test_process_exec_is_not_retried_on_transport_reset():
    client = AsyncSequenceClient(httpx.ConnectError("All connection attempts failed"))
    process = cast(Any, object.__new__(SandboxProcess))
    process.get_client = lambda: client

    with pytest.raises(httpx.ConnectError):
        await process.exec({"command": "echo nope"})
    assert client.calls == 1

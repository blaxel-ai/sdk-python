import asyncio
import json
from typing import Any, cast

import httpx
import pytest

from blaxel.core.common.settings import settings
from blaxel.core.sandbox.client import errors as sandbox_errors
from blaxel.core.sandbox.default.drive import SandboxDrive
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.default.network import SandboxNetwork
from blaxel.core.sandbox.default.process import SandboxProcess
from blaxel.core.sandbox.sync.drive import SyncSandboxDrive
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem
from blaxel.core.sandbox.sync.process import SyncSandboxProcess
from blaxel.core.sandbox.transient_retry import (
    is_transient_reset_error,
    retry_on_transient_reset,
    retry_on_transient_reset_async,
)
from blaxel.core.sandbox.types import ResponseError, SandboxConfiguration


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


SAFE_WORKLOAD_UNAVAILABLE_BODY = json.dumps(
    {
        "error": {
            "code": "WORKLOAD_UNAVAILABLE",
            "origin": "platform",
            "retryable": True,
            "dispatch_state": "not_dispatched",
            "safe_to_retry_request": True,
        }
    }
).encode()


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


async def read_request(reader: asyncio.StreamReader) -> None:
    headers = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout=1.0)
    content_length = 0
    for line in headers.decode(errors="ignore").split("\r\n"):
        if line.lower().startswith("content-length:"):
            content_length = int(line.split(":", 1)[1].strip())
            break
    if content_length:
        await asyncio.wait_for(reader.readexactly(content_length), timeout=1.0)


def response_handler(
    status: str,
    content: bytes,
    headers: tuple[bytes, ...] = (),
):
    async def send(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            await read_request(reader)
        except (TimeoutError, asyncio.IncompleteReadError, asyncio.LimitOverrunError):
            pass
        writer.write(
            f"HTTP/1.1 {status}\r\n".encode()
            + b"Content-Type: application/json\r\n"
            + b"".join(header + b"\r\n" for header in headers)
            + f"Content-Length: {len(content)}\r\n".encode()
            + b"Connection: close\r\n\r\n"
            + content
        )
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    return send


send_ok_response = response_handler("200 OK", b"ok")
send_safe_workload_unavailable = response_handler(
    "404 Not Found",
    SAFE_WORKLOAD_UNAVAILABLE_BODY,
    (
        b"X-Blaxel-Source: platform",
        b"X-Blaxel-Error-Code: WORKLOAD_UNAVAILABLE",
        b"X-Blaxel-Dispatch-State: not_dispatched",
    ),
)
send_untrusted_workload_unavailable = response_handler(
    "404 Not Found",
    SAFE_WORKLOAD_UNAVAILABLE_BODY,
)
send_empty_drive_list = response_handler("200 OK", b'{"mounts":[]}')
send_completed_process = response_handler(
    "200 OK",
    json.dumps(
        {
            "command": "echo ok",
            "completedAt": "now",
            "exitCode": 0,
            "logs": "ok",
            "name": "test",
            "pid": "1",
            "startedAt": "now",
            "status": "completed",
            "stderr": "",
            "stdout": "ok",
            "workingDir": "/tmp",
        }
    ).encode(),
)
send_file_written = response_handler(
    "200 OK",
    b'{"message":"written","path":"/file.bin"}',
)


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
async def test_async_drive_list_retries_trusted_pre_dispatch_response():
    async with LoopbackFaultServer(
        send_safe_workload_unavailable,
        send_empty_drive_list,
    ) as server:
        drive = SandboxDrive(SandboxConfiguration(cast(Any, None), force_url=server.url))

        assert await drive.list() == []

    assert server.requests == 2


@pytest.mark.asyncio
async def test_async_process_exec_retries_trusted_pre_dispatch_response():
    async with LoopbackFaultServer(
        send_safe_workload_unavailable,
        send_completed_process,
    ) as server:
        process = SandboxProcess(SandboxConfiguration(cast(Any, None), force_url=server.url))

        result = await process.exec({"command": "echo ok", "wait_for_completion": True})

    assert result.logs == "ok"
    assert server.requests == 2


@pytest.mark.asyncio
async def test_sync_drive_list_retries_trusted_pre_dispatch_response():
    async with LoopbackFaultServer(
        send_safe_workload_unavailable,
        send_empty_drive_list,
    ) as server:
        drive = SyncSandboxDrive(SandboxConfiguration(cast(Any, None), force_url=server.url))

        assert await asyncio.to_thread(drive.list) == []

    assert server.requests == 2


@pytest.mark.asyncio
async def test_sync_process_exec_retries_trusted_pre_dispatch_response():
    async with LoopbackFaultServer(
        send_safe_workload_unavailable,
        send_completed_process,
    ) as server:
        process = SyncSandboxProcess(SandboxConfiguration(cast(Any, None), force_url=server.url))

        result = await asyncio.to_thread(
            process.exec,
            {"command": "echo ok", "wait_for_completion": True},
        )

    assert result.logs == "ok"
    assert server.requests == 2


@pytest.mark.asyncio
async def test_async_fetch_does_not_replay_one_shot_body():
    async def body():
        yield b"payload"

    async with LoopbackFaultServer(
        send_safe_workload_unavailable,
        send_ok_response,
    ) as server:
        network = SandboxNetwork(SandboxConfiguration(cast(Any, None), force_url=server.url))

        response = await network.fetch(3000, "/upload", method="POST", content=body())

    assert response.status_code == 404
    assert server.requests == 1


@pytest.mark.asyncio
async def test_async_drive_list_does_not_retry_untrusted_response():
    async with LoopbackFaultServer(send_untrusted_workload_unavailable) as server:
        drive = SandboxDrive(SandboxConfiguration(cast(Any, None), force_url=server.url))

        with pytest.raises(sandbox_errors.UnexpectedStatus):
            await drive.list()

    assert server.requests == 1


@pytest.mark.asyncio
async def test_async_drive_list_preserves_final_retryable_error(monkeypatch):
    monkeypatch.setattr(
        "blaxel.core.sandbox.transient_retry.SAFE_RETRY_BUDGET_SECONDS",
        0,
    )
    async with LoopbackFaultServer(send_safe_workload_unavailable) as server:
        drive = SandboxDrive(SandboxConfiguration(cast(Any, None), force_url=server.url))

        with pytest.raises(sandbox_errors.APIStatusError) as exc_info:
            await drive.list()

    assert exc_info.value.status_code == 404
    assert exc_info.value.error_code == "WORKLOAD_UNAVAILABLE"
    assert exc_info.value.retryable is True
    assert server.requests == 1


@pytest.mark.asyncio
async def test_async_streaming_process_exec_retries_before_dispatch():
    async with LoopbackFaultServer(
        send_safe_workload_unavailable,
        send_completed_process,
    ) as server:
        process = SandboxProcess(SandboxConfiguration(cast(Any, None), force_url=server.url))

        result = await process.exec(
            {
                "command": "echo ok",
                "wait_for_completion": True,
                "on_log": lambda _: None,
            }
        )

    assert result.logs == "ok"
    assert server.requests == 2


@pytest.mark.asyncio
async def test_sync_streaming_process_exec_retries_before_dispatch():
    async with LoopbackFaultServer(
        send_safe_workload_unavailable,
        send_completed_process,
    ) as server:
        process = SyncSandboxProcess(SandboxConfiguration(cast(Any, None), force_url=server.url))

        result = await asyncio.to_thread(
            process.exec,
            {
                "command": "echo ok",
                "wait_for_completion": True,
                "on_log": lambda _: None,
            },
        )

    assert result.logs == "ok"
    assert server.requests == 2


@pytest.mark.asyncio
async def test_async_write_binary_rebuilds_body_for_safe_retry():
    async with LoopbackFaultServer(
        send_safe_workload_unavailable,
        send_file_written,
    ) as server:
        filesystem = SandboxFileSystem(SandboxConfiguration(cast(Any, None), force_url=server.url))

        result = await filesystem.write_binary("/file.bin", b"payload")

    assert result.path == "/file.bin"
    assert server.requests == 2


@pytest.mark.asyncio
async def test_sync_write_binary_rebuilds_body_for_safe_retry():
    async with LoopbackFaultServer(
        send_safe_workload_unavailable,
        send_file_written,
    ) as server:
        filesystem = SyncSandboxFileSystem(
            SandboxConfiguration(cast(Any, None), force_url=server.url)
        )

        result = await asyncio.to_thread(filesystem.write_binary, "/file.bin", b"payload")

    assert result.path == "/file.bin"
    assert server.requests == 2


@pytest.mark.asyncio
async def test_sync_retry_uses_bounded_exponential_backoff(monkeypatch):
    sleeps = []
    monkeypatch.setattr("blaxel.core.sandbox.transient_retry.time.sleep", sleeps.append)
    async with LoopbackFaultServer(
        send_safe_workload_unavailable,
        send_safe_workload_unavailable,
        send_empty_drive_list,
    ) as server:
        drive = SyncSandboxDrive(SandboxConfiguration(cast(Any, None), force_url=server.url))

        assert await asyncio.to_thread(drive.list) == []

    assert sleeps == [0.5, 1.0]
    assert server.requests == 3


@pytest.mark.asyncio
async def test_sync_retry_returns_final_error_when_budget_expires(monkeypatch):
    sleeps = []
    monkeypatch.setattr("blaxel.core.sandbox.transient_retry.time.sleep", sleeps.append)
    monkeypatch.setattr(
        "blaxel.core.sandbox.transient_retry.SAFE_RETRY_BUDGET_SECONDS",
        1.0,
    )
    async with LoopbackFaultServer(send_safe_workload_unavailable) as server:
        drive = SyncSandboxDrive(SandboxConfiguration(cast(Any, None), force_url=server.url))

        with pytest.raises(sandbox_errors.APIStatusError):
            await asyncio.to_thread(drive.list)

    assert sleeps == [0.5, 0.5]
    assert server.requests == 3


@pytest.mark.asyncio
async def test_async_retry_respects_cancellation():
    async with LoopbackFaultServer(send_safe_workload_unavailable) as server:
        drive = SandboxDrive(SandboxConfiguration(cast(Any, None), force_url=server.url))
        task = asyncio.create_task(drive.list())
        while server.requests == 0:
            await asyncio.sleep(0)
        await asyncio.sleep(0.05)
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task

    assert server.requests == 1


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

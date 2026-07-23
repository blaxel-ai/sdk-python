import asyncio
from http import HTTPStatus
from types import SimpleNamespace
from typing import Any, cast

import httpx
import pytest

from blaxel.core.common.settings import settings
from blaxel.core.sandbox.client.types import Response
from blaxel.core.sandbox.default.drive import SandboxDrive
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.default.network import SandboxNetwork
from blaxel.core.sandbox.default.process import SandboxProcess
from blaxel.core.sandbox.default.system import SandboxSystem
from blaxel.core.sandbox.sync.drive import SyncSandboxDrive
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem
from blaxel.core.sandbox.sync.network import SyncSandboxNetwork
from blaxel.core.sandbox.sync.system import SyncSandboxSystem
from blaxel.core.sandbox.transient_retry import (
    is_transient_reset_error,
    is_transient_sandbox_read_response,
    retry_on_transient_reset,
    retry_on_transient_reset_async,
    retry_on_transient_sandbox_read,
    retry_on_transient_sandbox_read_async,
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

    async def request(self, *args, **kwargs):
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

    def request(self, *args, **kwargs):
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


def status_response(status_code: int) -> httpx.Response:
    return httpx.Response(
        status_code,
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


def test_read_response_classifier_accepts_resume_gateway_statuses():
    assert is_transient_sandbox_read_response(status_response(502))
    assert is_transient_sandbox_read_response(status_response(503))
    assert is_transient_sandbox_read_response(
        Response(status_code=HTTPStatus.SERVICE_UNAVAILABLE, content=b"", headers={}, parsed=None)
    )


def test_read_response_classifier_rejects_application_statuses():
    assert not is_transient_sandbox_read_response(status_response(500))
    assert not is_transient_sandbox_read_response(status_response(404))


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


@pytest.mark.asyncio
async def test_async_sandbox_read_retry_recovers_from_resume_status():
    calls = 0

    async def flaky_gateway():
        nonlocal calls
        calls += 1
        if calls == 1:
            return status_response(503)
        return status_response(200)

    response = await retry_on_transient_sandbox_read_async(flaky_gateway, retries=1)

    assert response.status_code == 200
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


def test_sync_sandbox_read_retry_recovers_from_resume_status():
    calls = 0

    def flaky_gateway():
        nonlocal calls
        calls += 1
        if calls == 1:
            return status_response(502)
        return status_response(200)

    response = retry_on_transient_sandbox_read(flaky_gateway, retries=1)

    assert response.status_code == 200
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


@pytest.mark.asyncio
async def test_async_network_fetch_retries_resume_gateway_status(monkeypatch):
    monkeypatch.setenv("BL_SANDBOX_READ_RETRIES", "1")
    client = AsyncSequenceClient(status_response(503), status_response(200))
    network = cast(Any, object.__new__(SandboxNetwork))
    network.get_client = lambda: client

    response = await network.fetch(8080, "/health")

    assert response.status_code == 200
    assert client.calls == 2


class GeneratedClientContext:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None


@pytest.mark.asyncio
async def test_async_drive_list_exposes_transient_response_to_retry(monkeypatch):
    from blaxel.core.sandbox.default import drive as drive_module

    clients = []
    responses = [
        Response(status_code=503, content=b"", headers={}, parsed=None),
        Response(
            status_code=200,
            content=b"",
            headers={},
            parsed=SimpleNamespace(mounts=[]),
        ),
    ]

    def make_client(**kwargs):
        client = GeneratedClientContext(**kwargs)
        clients.append(client)
        return client

    async def get_drives_mount(**kwargs):
        return responses.pop(0)

    monkeypatch.setattr(drive_module, "Client", make_client)
    monkeypatch.setattr(drive_module, "get_drives_mount", get_drives_mount)
    monkeypatch.setattr(drive_module, "settings", SimpleNamespace(headers={}))
    monkeypatch.setenv("BL_SANDBOX_READ_RETRIES", "1")

    drive = cast(Any, object.__new__(SandboxDrive))
    drive.sandbox_config = SimpleNamespace(
        force_url="https://sandbox.test",
        headers={},
        metadata=None,
    )

    assert await drive.list() == []
    assert len(clients) == 2
    assert all(client.kwargs["raise_on_unexpected_status"] is False for client in clients)


def test_sync_drive_list_exposes_transient_response_to_retry(monkeypatch):
    from blaxel.core.sandbox.sync import drive as drive_module

    clients = []
    responses = [
        Response(status_code=502, content=b"", headers={}, parsed=None),
        Response(
            status_code=200,
            content=b"",
            headers={},
            parsed=SimpleNamespace(mounts=[]),
        ),
    ]

    def make_client(**kwargs):
        client = GeneratedClientContext(**kwargs)
        clients.append(client)
        return client

    def get_drives_mount(**kwargs):
        return responses.pop(0)

    monkeypatch.setattr(drive_module, "Client", make_client)
    monkeypatch.setattr(drive_module, "get_drives_mount", get_drives_mount)
    monkeypatch.setattr(drive_module, "settings", SimpleNamespace(headers={}))
    monkeypatch.setenv("BL_SANDBOX_READ_RETRIES", "1")

    drive = cast(Any, object.__new__(SyncSandboxDrive))
    drive.sandbox_config = SimpleNamespace(
        force_url="https://sandbox.test",
        headers={},
        metadata=None,
    )

    assert drive.list() == []
    assert len(clients) == 2
    assert all(client.kwargs["raise_on_unexpected_status"] is False for client in clients)


@pytest.mark.asyncio
async def test_async_health_exposes_transient_response_to_retry(monkeypatch):
    from blaxel.core.sandbox.default import system as system_module

    clients = []
    expected = object()
    responses = [
        Response(status_code=504, content=b"", headers={}, parsed=None),
        Response(status_code=200, content=b"", headers={}, parsed=expected),
    ]

    def make_client(**kwargs):
        client = GeneratedClientContext(**kwargs)
        clients.append(client)
        return client

    async def get_health(**kwargs):
        return responses.pop(0)

    monkeypatch.setattr(system_module, "Client", make_client)
    monkeypatch.setattr(system_module, "get_health", get_health)
    monkeypatch.setattr(system_module, "settings", SimpleNamespace(headers={}))
    monkeypatch.setenv("BL_SANDBOX_READ_RETRIES", "1")

    system = cast(Any, object.__new__(SandboxSystem))
    system.sandbox_config = SimpleNamespace(
        force_url="https://sandbox.test",
        headers={},
        metadata=None,
    )

    assert await system.health() is expected
    assert len(clients) == 2
    assert all(client.kwargs["raise_on_unexpected_status"] is False for client in clients)


def test_sync_health_exposes_transient_response_to_retry(monkeypatch):
    from blaxel.core.sandbox.sync import system as system_module

    clients = []
    expected = object()
    responses = [
        Response(status_code=429, content=b"", headers={}, parsed=None),
        Response(status_code=200, content=b"", headers={}, parsed=expected),
    ]

    def make_client(**kwargs):
        client = GeneratedClientContext(**kwargs)
        clients.append(client)
        return client

    def get_health(**kwargs):
        return responses.pop(0)

    monkeypatch.setattr(system_module, "Client", make_client)
    monkeypatch.setattr(system_module, "get_health", get_health)
    monkeypatch.setattr(system_module, "settings", SimpleNamespace(headers={}))
    monkeypatch.setenv("BL_SANDBOX_READ_RETRIES", "1")

    system = cast(Any, object.__new__(SyncSandboxSystem))
    system.sandbox_config = SimpleNamespace(
        force_url="https://sandbox.test",
        headers={},
        metadata=None,
    )

    assert system.health() is expected
    assert len(clients) == 2
    assert all(client.kwargs["raise_on_unexpected_status"] is False for client in clients)


@pytest.mark.asyncio
async def test_async_network_fetch_does_not_retry_post_status(monkeypatch):
    monkeypatch.setenv("BL_SANDBOX_READ_RETRIES", "1")
    client = AsyncSequenceClient(status_response(503), status_response(200))
    network = cast(Any, object.__new__(SandboxNetwork))
    network.get_client = lambda: client

    response = await network.fetch(8080, "/mutate", method="POST")

    assert response.status_code == 503
    assert client.calls == 1


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


def test_sync_network_fetch_retries_resume_gateway_status(monkeypatch):
    monkeypatch.setenv("BL_SANDBOX_READ_RETRIES", "1")
    client = SyncSequenceClient(status_response(502), status_response(200))
    network = cast(Any, object.__new__(SyncSandboxNetwork))
    network.get_client = lambda: client

    response = network.fetch(8080, "/health")

    assert response.status_code == 200
    assert client.calls == 2


@pytest.mark.asyncio
async def test_process_exec_is_not_retried_on_transport_reset():
    client = AsyncSequenceClient(httpx.ConnectError("All connection attempts failed"))
    process = cast(Any, object.__new__(SandboxProcess))
    process.get_client = lambda: client

    with pytest.raises(httpx.ConnectError):
        await process.exec({"command": "echo nope"})
    assert client.calls == 1

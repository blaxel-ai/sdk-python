"""fs.watch reports server keepalives and a server-side end of stream."""

import asyncio
import threading
from typing import Any

import httpx
import pytest

from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem
from blaxel.core.sandbox.types import SandboxConfiguration

STREAM = b'[keepalive]\n{"op":"CREATE","path":"/d","name":"f"}\n[keepalive]\n'


def ok(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, content=STREAM)


def http_error(request: httpx.Request) -> httpx.Response:
    return httpx.Response(500)


def dropped(request: httpx.Request) -> httpx.Response:
    raise httpx.ReadError("connection reset", request=request)


def patch_transport(monkeypatch, cls_name: str, handler=ok) -> None:
    transport = httpx.MockTransport(handler)
    original = getattr(httpx, cls_name)
    monkeypatch.setattr(httpx, cls_name, lambda **kw: original(transport=transport, **kw))


def config() -> SandboxConfiguration:
    return SandboxConfiguration(sandbox=None, force_url="http://sandbox")  # type: ignore[arg-type]


async def test_async_watch_reports_keepalive_and_close(monkeypatch):
    patch_transport(monkeypatch, "AsyncClient")
    seen: list[Any] = []
    closed = asyncio.Event()

    async def on_event(event):
        seen.append(event.name)

    SandboxFileSystem(config()).watch(
        "/d",
        on_event,  # pyright: ignore[reportArgumentType]  (async watch awaits the callback)
        {"on_keepalive": lambda: seen.append("keepalive"), "on_close": closed.set},
    )
    await asyncio.wait_for(closed.wait(), 5)
    assert seen == ["keepalive", "f", "keepalive"]


def test_sync_watch_reports_keepalive_and_close(monkeypatch):
    patch_transport(monkeypatch, "Client")
    seen: list[Any] = []
    closed = threading.Event()

    SyncSandboxFileSystem(config()).watch(
        "/d",
        lambda event: seen.append(event.name),
        {"on_keepalive": lambda: seen.append("keepalive"), "on_close": closed.set},
    )
    assert closed.wait(5)
    assert seen == ["keepalive", "f", "keepalive"]


@pytest.mark.parametrize("handler", [http_error, dropped])
async def test_async_watch_reports_stream_failure(monkeypatch, handler):
    patch_transport(monkeypatch, "AsyncClient", handler)
    errors: list[Exception] = []
    failed = asyncio.Event()

    def on_error(e):
        errors.append(e)
        failed.set()

    SandboxFileSystem(config()).watch("/d", lambda _: None, {"on_error": on_error})  # pyright: ignore[reportArgumentType]
    await asyncio.wait_for(failed.wait(), 5)
    assert len(errors) == 1


@pytest.mark.parametrize("handler", [http_error, dropped])
def test_sync_watch_reports_stream_failure(monkeypatch, handler):
    patch_transport(monkeypatch, "Client", handler)
    failed = threading.Event()
    errors: list[Exception] = []

    def on_error(e):
        errors.append(e)
        failed.set()

    SyncSandboxFileSystem(config()).watch("/d", lambda _: None, {"on_error": on_error})
    assert failed.wait(5)
    assert len(errors) == 1


def test_sync_close_releases_an_idle_stream():
    """close() must drop the connection while the server is still silent.

    The sandbox API sends no headers until the first event or keepalive, so the
    worker is blocked waiting for them when the caller closes.
    """
    import socket

    server = socket.create_server(("127.0.0.1", 0))
    port = server.getsockname()[1]
    requested = threading.Event()
    released = threading.Event()

    def serve():
        conn, _ = server.accept()
        conn.recv(65536)
        requested.set()
        conn.settimeout(10)
        try:
            if conn.recv(1) == b"":  # client hung up
                released.set()
        except OSError:
            released.set()
        finally:
            conn.close()

    threading.Thread(target=serve, daemon=True).start()
    errors: list[Exception] = []
    handle = SyncSandboxFileSystem(
        SandboxConfiguration(sandbox=None, force_url=f"http://127.0.0.1:{port}")  # type: ignore[arg-type]
    ).watch("/d", lambda _: None, {"on_error": errors.append})
    assert requested.wait(5)
    handle.close()
    assert released.wait(3)
    assert not errors  # our own close() is not reported
    server.close()

"""Regression tests for the async process log streamer's error handling.

The async background log stream must not re-raise a transport failure (such as
``httpx.ConnectError: [Errno 65] No route to host`` when a sandbox becomes
unreachable) inside its ``asyncio.create_task`` coroutine. A fire-and-forget
caller -- one that passes log callbacks and later calls ``close()`` without ever
awaiting ``wait()`` -- never retrieves a task exception, so a raised error would
surface as an unhandled SDK exception on the event loop (and be reported as an
SDK crash). Instead the error is stored and surfaced only through ``wait()``,
matching the synchronous streamer.
"""

import asyncio
import gc
from types import SimpleNamespace
from typing import Any, cast

import httpx
import pytest

import blaxel.core.sandbox.default.process as process_mod
from blaxel.core.sandbox.default.process import SandboxProcess


def _make_failing_httpx(error: BaseException) -> SimpleNamespace:
    """A stand-in for the ``httpx`` module whose client fails on stream connect."""

    class _StreamCtx:
        async def __aenter__(self):
            raise error

        async def __aexit__(self, *exc):
            return False

    class _AsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        def stream(self, *args, **kwargs):
            return _StreamCtx()

    return SimpleNamespace(AsyncClient=_AsyncClient)


def _make_async_process() -> SandboxProcess:
    process = cast(Any, object.__new__(SandboxProcess))
    # ``force_url`` makes the ``url`` property resolve without real sandbox config.
    process.sandbox_config = SimpleNamespace(force_url="http://sandbox.test", headers={})
    return process


@pytest.fixture(autouse=True)
def _stub_auth_headers(monkeypatch):
    # Auth headers require real credentials; the streamer is what is under test.
    monkeypatch.setattr(type(process_mod.settings), "headers", property(lambda _self: {}))


@pytest.mark.asyncio
async def test_async_stream_logs_transport_failure_surfaces_through_wait(monkeypatch):
    error = httpx.ConnectError("[Errno 65] No route to host")
    monkeypatch.setattr(process_mod, "httpx", _make_failing_httpx(error))

    process = _make_async_process()
    handle = process._stream_logs("proc")

    with pytest.raises(httpx.ConnectError) as exc_info:
        await handle.wait()
    assert exc_info.value is error


@pytest.mark.asyncio
async def test_async_stream_logs_transport_failure_does_not_leak_unretrieved_task(monkeypatch):
    error = httpx.ConnectError("[Errno 65] No route to host")
    monkeypatch.setattr(process_mod, "httpx", _make_failing_httpx(error))

    loop = asyncio.get_running_loop()
    recorded: list[dict] = []
    previous_handler = loop.get_exception_handler()
    loop.set_exception_handler(lambda _loop, context: recorded.append(context))
    try:
        process = _make_async_process()
        handle = process._stream_logs("proc")

        # Let the background task connect, fail, and finish.
        for _ in range(10):
            await asyncio.sleep(0)

        # Fire-and-forget: drop the handle without ever awaiting wait().
        del handle
        gc.collect()
        await asyncio.sleep(0)
    finally:
        loop.set_exception_handler(previous_handler)

    assert recorded == [], f"background log stream leaked a task exception: {recorded}"


@pytest.mark.asyncio
async def test_async_stream_logs_close_does_not_surface_error(monkeypatch):
    error = httpx.ConnectError("[Errno 65] No route to host")
    monkeypatch.setattr(process_mod, "httpx", _make_failing_httpx(error))

    process = _make_async_process()
    handle = process._stream_logs("proc")
    # Closing before anything is awaited must be silent teardown.
    handle.close()

    for _ in range(10):
        await asyncio.sleep(0)

    # wait() after close() returns without raising the transport error.
    await handle.wait()

"""Existing process API: bounded observation and visible stream failures."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox.default.process import SandboxProcess
from blaxel.core.sandbox.sync.process import SyncSandboxProcess
from blaxel.core.sandbox.types import ResponseError, SandboxConfiguration


def observer(cls, responses):
    p = object.__new__(cls)
    p.get = (
        AsyncMock(side_effect=responses) if cls is SandboxProcess else Mock(side_effect=responses)
    )
    return p


async def wait(p, **kwargs):
    return (
        await p.wait("original", **kwargs)
        if isinstance(p, SandboxProcess)
        else p.wait("original", **kwargs)
    )


@pytest.mark.parametrize("status", ["completed", "failed", "killed", "stopped"])
@pytest.mark.asyncio
async def test_terminal_state_needs_one_read(status):
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = observer(cls, [SimpleNamespace(status=status)])
        assert (await wait(p)).status == status
        assert p.get.call_count == 1


@pytest.mark.parametrize("code", [401, 403, 404])
@pytest.mark.asyncio
async def test_permanent_error_is_not_a_running_result(code):
    error = ResponseError(httpx.Response(code, json={"error": "unavailable"}))
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = observer(cls, [SimpleNamespace(status="running"), error])
        with pytest.raises(ResponseError) as caught:
            await wait(p, interval=1)
        assert caught.value is error


@pytest.mark.parametrize("code", [408, 429, 500, 502, 503, 504])
@pytest.mark.asyncio
async def test_retryable_http_error_recovers(code):
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = observer(
            cls,
            [ResponseError(httpx.Response(code)), SimpleNamespace(status="failed", exit_code=7)],
        )
        assert (await wait(p, interval=1)).exit_code == 7
        assert p.get.call_count == 2


@pytest.mark.asyncio
async def test_network_failure_recovers_and_timeout_preserves_cause():
    error = httpx.ReadError("response lost")
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = observer(cls, [error, SimpleNamespace(status="completed")])
        assert (await wait(p, interval=1)).status == "completed"
        p = observer(cls, [error] * 100)
        with pytest.raises(TimeoutError) as caught:
            await wait(p, interval=100, max_wait=10)
        assert caught.value.__cause__ is error
        assert p.get.call_count == 1


@pytest.mark.asyncio
async def test_hung_read_is_bounded_and_cancelled():
    cancelled = asyncio.Event()

    async def get(*args, **kwargs):
        try:
            await asyncio.Future()
        finally:
            cancelled.set()

    p = object.__new__(SandboxProcess)
    p.get = get
    with pytest.raises(TimeoutError, match="original"):
        await p.wait("original", max_wait=10)
    assert cancelled.is_set()


@pytest.mark.parametrize("max_wait", [100, -1])
@pytest.mark.parametrize("during_read", [True, False])
@pytest.mark.asyncio
async def test_cancellation_propagates_without_another_read(during_read, max_wait):
    entered = asyncio.Event()

    async def get(*args, **kwargs):
        entered.set()
        if during_read:
            await asyncio.Future()
        return SimpleNamespace(status="running")

    p = object.__new__(SandboxProcess)
    p.get = AsyncMock(side_effect=get)
    task = asyncio.create_task(p.wait("original", max_wait=max_wait))
    await entered.wait()
    await asyncio.sleep(0)
    task.cancel()
    try:
        done, _ = await asyncio.wait({task}, timeout=0.5)
        assert task in done, "cancellation did not finish promptly"
        with pytest.raises(asyncio.CancelledError):
            await task
        assert p.get.call_count == 1
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)


@pytest.mark.asyncio
async def test_unknown_state_and_zero_deadline_fail():
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = observer(cls, [SimpleNamespace(status="unknown")])
        with pytest.raises(ValueError, match="Unknown process status"):
            await wait(p)
        p = observer(cls, [])
        with pytest.raises(TimeoutError):
            await wait(p, max_wait=0)
        assert not p.get.called


@pytest.mark.asyncio
async def test_stream_errors_are_visible_and_explicit_close_is_clean(monkeypatch):
    config = SandboxConfiguration(
        Sandbox(metadata=Metadata(name="test"), spec=SandboxSpec()), force_url="http://localhost"
    )
    error = httpx.ReadError("stream lost")

    def fail(request):
        raise error

    real_client, real_async_client = httpx.Client, httpx.AsyncClient
    monkeypatch.setattr(
        httpx, "Client", lambda **kwargs: real_client(transport=httpx.MockTransport(fail))
    )
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: real_async_client(transport=httpx.MockTransport(fail)),
    )
    for cls in (SandboxProcess, SyncSandboxProcess):
        handle = cls(config)._stream_logs("original")
        try:
            with pytest.raises(httpx.ReadError) as caught:
                if cls is SandboxProcess:
                    await handle.wait()
                else:
                    handle.wait(timeout=1)
            assert caught.value is error
        finally:
            handle.close()

    async def hang(request):
        await asyncio.Future()

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: real_async_client(transport=httpx.MockTransport(hang)),
    )
    handle = SandboxProcess(config)._stream_logs("original")
    await asyncio.sleep(0)
    handle.close()
    await handle.wait()


@pytest.mark.asyncio
async def test_late_terminal_result_is_rejected():
    import time

    for cls in (SandboxProcess, SyncSandboxProcess):

        def late(*args, **kwargs):
            time.sleep(0.02)
            return SimpleNamespace(status="completed")

        p = object.__new__(cls)
        p.get = AsyncMock(side_effect=late) if cls is SandboxProcess else Mock(side_effect=late)
        with pytest.raises(TimeoutError):
            await wait(p, max_wait=5)


def test_sync_get_receives_remaining_transport_timeout(monkeypatch):
    config = SandboxConfiguration(
        Sandbox(metadata=Metadata(name="test"), spec=SandboxSpec()), force_url="http://localhost"
    )
    p = SyncSandboxProcess(config)

    def respond(request):
        assert 0 < request.extensions["timeout"]["read"] <= 0.1
        return httpx.Response(404, json={"error": "process not found"})

    monkeypatch.setattr(
        p,
        "get_client",
        lambda: httpx.Client(base_url="http://localhost", transport=httpx.MockTransport(respond)),
    )
    with pytest.raises(ResponseError):
        p.wait("original", max_wait=100)


@pytest.mark.asyncio
async def test_unlimited_wait_recovers_and_returns_terminal_state(monkeypatch):
    original_wait = asyncio.wait
    deadlines = []

    async def observe_wait(tasks, *, timeout):
        deadlines.append(timeout)
        return await original_wait(tasks, timeout=timeout)

    monkeypatch.setattr(asyncio, "wait", observe_wait)
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = observer(
            cls,
            [
                SimpleNamespace(status="running"),
                httpx.ReadError("lost"),
                SimpleNamespace(status="failed", exit_code=7),
            ],
        )
        assert (await wait(p, max_wait=-1, interval=1)).exit_code == 7
        assert p.get.call_count == 3
        if cls is SyncSandboxProcess:
            assert all(call.kwargs["timeout"] is None for call in p.get.call_args_list)
        error = ResponseError(httpx.Response(403))
        p = observer(cls, [error])
        with pytest.raises(ResponseError) as caught:
            await wait(p, max_wait=-1)
        assert caught.value is error
        assert p.get.call_count == 1
    assert deadlines and all(timeout is None for timeout in deadlines)


@pytest.mark.parametrize("max_wait", [-2, -0.5, float("inf"), float("nan")])
@pytest.mark.asyncio
async def test_only_minus_one_is_an_unlimited_wait(max_wait):
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = observer(cls, [])
        with pytest.raises(ValueError):
            await wait(p, max_wait=max_wait)
        assert not p.get.called

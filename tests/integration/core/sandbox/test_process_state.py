"""Recover a real process after a lost status response, without another POST."""

import os
import time

import httpx
import pytest
import pytest_asyncio

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox import SandboxInstance, SyncSandboxInstance
from blaxel.core.sandbox.types import is_missing_route
from tests.helpers import default_image, default_labels, unique_name


@pytest_asyncio.fixture
async def sandbox():
    local_url = os.environ.get("LOCAL_PROCESS_API_URL")
    # Reuse an existing sandbox (never deleted here) instead of creating one.
    existing = os.environ.get("PROCESS_SANDBOX_NAME")
    name = unique_name("process-recovery")
    if local_url:
        instance = SandboxInstance(
            Sandbox(metadata=Metadata(name=name), spec=SandboxSpec()), force_url=local_url
        )
    elif existing:
        instance = await SandboxInstance.get(existing)
    else:
        instance = await SandboxInstance.create(
            {"name": name, "image": default_image, "labels": default_labels}
        )
    try:
        yield instance
    finally:
        if not local_url and not existing:
            await instance.delete()
        for subsystem in (instance.process, instance.fs):
            if subsystem._client is not None:
                await subsystem._client.aclose()


@pytest.mark.parametrize("synchronous", [False, True])
@pytest.mark.asyncio
async def test_wait_recovers_lost_status_without_starting_twice(sandbox, synchronous, monkeypatch):
    # Exercise wait's retry policy without standalone get() retries hiding a lost poll.
    monkeypatch.setenv("BL_SANDBOX_READ_RETRIES", "0")
    api = SyncSandboxInstance(sandbox.config) if synchronous else sandbox
    name = unique_name("interrupted-command")
    marker = f"/tmp/{name}"
    reads, starts = 0, 0
    async_send, sync_send = httpx.AsyncClient.send, httpx.Client.send

    def count(request):
        """True for the first status read: its response gets lost."""
        nonlocal reads, starts
        if request.method == "POST" and request.url.path.endswith("/process"):
            starts += 1
        # Long-poll (/wait) or plain GET, depending on the sandbox version.
        if request.method == "GET" and request.url.path.endswith(
            (f"/process/{name}", f"/process/{name}/wait")
        ):
            reads += 1
            return reads == 1
        return False

    # Release before the first read is sent: a /wait read holds until the
    # process exits, so releasing after its response would never happen.
    async def interrupted_async(client, request, **kwargs):
        lose = count(request)
        if lose:
            await sandbox.fs.write(f"{marker}.release", "continue")
        response = await async_send(client, request, **kwargs)
        if lose:
            raise httpx.ReadError("status response lost", request=request)
        return response

    def interrupted_sync(client, request, **kwargs):
        lose = count(request)
        if lose:
            api.fs.write(f"{marker}.release", "continue")
        response = sync_send(client, request, **kwargs)
        if lose:
            raise httpx.ReadError("status response lost", request=request)
        return response

    monkeypatch.setattr(httpx.AsyncClient, "send", interrupted_async)
    monkeypatch.setattr(httpx.Client, "send", interrupted_sync)
    request = {
        "name": name,
        "command": f"echo started >> {marker}; while [ ! -f {marker}.release ]; do sleep 0.1; done; echo recovered-output; exit 7",
        "wait_for_completion": False,
        "keep_alive": False,
    }
    try:
        if synchronous:
            api.process.exec(request)
            result = api.process.wait(name, max_wait=10000, interval=100)
            logs, content = api.process.logs(name), api.fs.read(marker)
        else:
            await api.process.exec(request)
            result = await api.process.wait(name, max_wait=10000, interval=100)
            logs, content = await api.process.logs(name), await api.fs.read(marker)
        assert result.name == name
        assert result.status == "failed"
        assert result.exit_code == 7
        assert "recovered-output" in logs
        assert content == "started\n"
        assert starts == 1
        assert reads >= 2
    finally:
        # Observation errors leave the command running, so cleanup is explicit.
        try:
            await sandbox.process.kill(name)
        except Exception:
            pass
        for path in (marker, f"{marker}.release"):
            try:
                await sandbox.fs.rm(path)
            except Exception:
                pass


@pytest.mark.parametrize("synchronous", [False, True])
@pytest.mark.asyncio
async def test_wait_long_polls_until_exit(sandbox, synchronous, monkeypatch):
    api = SyncSandboxInstance(sandbox.config) if synchronous else sandbox
    name = unique_name("long-poll")
    # Old sandboxes answer an unknown route with a plain-text 404; the endpoint uses JSON.
    probe = await sandbox.process.get_client().get(f"/process/{name}/wait", params={"timeout": 0})
    has_route = not is_missing_route(probe)

    calls = {"_wait_once": 0, "get": 0}
    for attr in calls:
        original = getattr(api.process, attr)
        if synchronous:

            def spy(*args, _attr=attr, _original=original, **kwargs):
                calls[_attr] += 1
                return _original(*args, **kwargs)
        else:

            async def spy(*args, _attr=attr, _original=original, **kwargs):
                calls[_attr] += 1
                return await _original(*args, **kwargs)

        monkeypatch.setattr(api.process, attr, spy)

    request = {"name": name, "command": "sleep 2; exit 3", "wait_for_completion": False}
    # Polling with a 5s interval needs at least 5s; the long-poll returns at exit (~2s).
    started = time.monotonic()
    try:
        if synchronous:
            api.process.exec(request)
            result = api.process.wait(name, max_wait=30000, interval=5000)
        else:
            await api.process.exec(request)
            result = await api.process.wait(name, max_wait=30000, interval=5000)
        elapsed = time.monotonic() - started
    finally:
        try:
            await sandbox.process.kill(name)
        except Exception:
            pass
    assert result.name == name
    assert result.status == "failed"
    assert result.exit_code == 3
    if not has_route:
        pytest.skip("sandbox has no GET /process/{id}/wait: wait fell back to polling")
    assert calls["_wait_once"] >= 1
    assert calls["get"] == 0
    assert elapsed < 4.5

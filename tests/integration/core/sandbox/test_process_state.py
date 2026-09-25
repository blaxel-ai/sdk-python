"""Recover a real process after a lost status response, without another POST."""

import os

import httpx
import pytest
import pytest_asyncio

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox import SandboxInstance, SyncSandboxInstance
from tests.helpers import default_image, default_labels, unique_name


@pytest_asyncio.fixture
async def sandbox():
    local_url = os.environ.get("LOCAL_PROCESS_API_URL")
    name = unique_name("process-recovery")
    instance = (
        SandboxInstance(
            Sandbox(metadata=Metadata(name=name), spec=SandboxSpec()), force_url=local_url
        )
        if local_url
        else await SandboxInstance.create(
            {"name": name, "image": default_image, "labels": default_labels}
        )
    )
    try:
        yield instance
    finally:
        if not local_url:
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
    async_request, sync_request = httpx.AsyncClient.request, httpx.Client.request

    def count(response):
        nonlocal reads, starts
        request = response.request
        if request.method == "POST" and request.url.path.endswith("/process"):
            starts += 1
        if request.method == "GET" and request.url.path.endswith(f"/process/{name}"):
            reads += 1
            return reads == 2
        return False

    async def interrupted_async(client, *args, **kwargs):
        response = await async_request(client, *args, **kwargs)
        if count(response):
            await sandbox.fs.write(f"{marker}.release", "continue")
            raise httpx.ReadError("status response lost", request=response.request)
        return response

    def interrupted_sync(client, *args, **kwargs):
        response = sync_request(client, *args, **kwargs)
        if count(response):
            api.fs.write(f"{marker}.release", "continue")
            raise httpx.ReadError("status response lost", request=response.request)
        return response

    monkeypatch.setattr(httpx.AsyncClient, "request", interrupted_async)
    monkeypatch.setattr(httpx.Client, "request", interrupted_sync)
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
        assert reads >= 3
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

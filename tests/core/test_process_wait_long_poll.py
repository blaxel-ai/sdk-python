"""process.wait long-polls GET /process/{id}/wait and falls back to polling on old sandboxes."""

import httpx
import pytest

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox.client.client import Client
from blaxel.core.sandbox.default.process import SandboxProcess
from blaxel.core.sandbox.sync.process import SyncSandboxProcess
from blaxel.core.sandbox.types import ResponseError, SandboxConfiguration

CONFIG = SandboxConfiguration(
    Sandbox(metadata=Metadata(name="test"), spec=SandboxSpec()), force_url="http://localhost"
)


def process(status):
    body = dict.fromkeys(["command", "completedAt", "logs", "startedAt", "stderr", "stdout"], "")
    body.update(status=status, exitCode=0, name="original", pid="1", workingDir="/")
    return httpx.Response(200, json=body)


async def run_wait(cls, monkeypatch, routes, **kwargs):
    """Run wait against a mocked transport; routes maps 'wait'/'get' to response lists."""
    requests = []

    def respond(request):
        requests.append(request)
        kind = "wait" if request.url.path.endswith("/wait") else "get"
        return routes[kind].pop(0)

    transport = httpx.MockTransport(respond)
    p = cls(CONFIG)
    if cls is SandboxProcess:
        client = httpx.AsyncClient(base_url="http://localhost", transport=transport)
        monkeypatch.setattr(p, "get_client", lambda: client)
        # The generated client drops an injected AsyncClient inside a running loop: hand it the transport.
        monkeypatch.setattr(
            p,
            "get_api_client",
            lambda: Client(base_url="http://localhost", httpx_args={"transport": transport}),
        )
        result = await p.wait("original", **kwargs)
    else:
        monkeypatch.setattr(
            p, "get_client", lambda: httpx.Client(base_url="http://localhost", transport=transport)
        )
        result = p.wait("original", **kwargs)
    return result, requests


CLASSES = [SandboxProcess, SyncSandboxProcess]


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.asyncio
async def test_finishes_on_first_wait_call(cls, monkeypatch):
    result, requests = await run_wait(cls, monkeypatch, {"wait": [process("completed")]})
    assert result.status == "completed"
    assert len(requests) == 1
    assert requests[0].url.path == "/process/original/wait"
    assert requests[0].url.params["timeout"] == "60"  # default max_wait=60000 ms


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.asyncio
async def test_loops_on_running(cls, monkeypatch):
    routes = {"wait": [process("running"), process("running"), process("failed")]}
    result, requests = await run_wait(cls, monkeypatch, routes, max_wait=-1, interval=1)
    assert result.status == "failed"
    assert [r.url.path for r in requests] == ["/process/original/wait"] * 3
    assert all(r.url.params["timeout"] == "119" for r in requests)


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.asyncio
async def test_falls_back_to_polling_on_plain_404(cls, monkeypatch):
    routes = {
        "wait": [httpx.Response(404, text="404 page not found")],
        "get": [process("running"), process("completed")],
    }
    result, requests = await run_wait(cls, monkeypatch, routes, interval=1)
    assert result.status == "completed"
    # One /wait probe, then polling for the rest of the call.
    assert [r.url.path for r in requests] == [
        "/process/original/wait",
        "/process/original",
        "/process/original",
    ]


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.asyncio
async def test_json_404_means_process_not_found(cls, monkeypatch):
    routes = {"wait": [httpx.Response(404, json={"error": "process not found"})]}
    with pytest.raises(ResponseError) as caught:
        await run_wait(cls, monkeypatch, routes)
    assert caught.value.status == 404


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.asyncio
async def test_respects_max_wait(cls, monkeypatch):
    async def run():
        routes = {"wait": [process("running")] * 1000}
        try:
            await run_wait(cls, monkeypatch, routes, max_wait=300, interval=50)
        finally:
            assert 1 <= 1000 - len(routes["wait"]) <= 10

    with pytest.raises(TimeoutError):
        await run()


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.asyncio
async def test_hold_is_capped_by_max_wait_and_client_timeout_ends_near_deadline(cls, monkeypatch):
    _, requests = await run_wait(cls, monkeypatch, {"wait": [process("completed")]}, max_wait=1500)
    # Hold is what is left of max_wait, rounded up to a whole second.
    assert requests[0].url.params["timeout"] == "2"
    # The client gives up at most 1s past the deadline, not hold + 10s.
    assert 2 < requests[0].extensions["timeout"]["read"] <= 2.5


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.asyncio
async def test_small_max_wait_bounds_request_timeout(cls, monkeypatch):
    # A held request cannot be interrupted: its timeout must stop near the 100ms deadline.
    _, requests = await run_wait(cls, monkeypatch, {"wait": [process("completed")]}, max_wait=100)
    assert requests[0].url.params["timeout"] == "1"
    timeout = requests[0].extensions["timeout"]
    assert all(0 < timeout[phase] <= 1.1 for phase in ("connect", "read", "write", "pool"))


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.asyncio
async def test_default_hold_and_client_timeout(cls, monkeypatch):
    _, requests = await run_wait(cls, monkeypatch, {"wait": [process("completed")]}, max_wait=-1)
    assert requests[0].url.params["timeout"] == "119"
    assert requests[0].extensions["timeout"]["read"] == 129

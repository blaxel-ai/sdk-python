"""Process outcome recovery, including real loopback HTTP failures."""

import asyncio
import json
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox import ProcessExecutionError, ProcessObservationError, ProcessWaitTimeout
from blaxel.core.sandbox.default.process import SandboxProcess
from blaxel.core.sandbox.sync.process import SyncSandboxProcess
from blaxel.core.sandbox.types import SandboxConfiguration


def response(status="running", name="example"):
    return dict(
        command="echo hello",
        completedAt="",
        exitCode=0,
        logs="hello",
        name=name,
        pid="1",
        startedAt="",
        status=status,
        stderr="",
        stdout="hello",
        workingDir="/",
    )


@pytest.mark.parametrize("status", ["completed", "failed", "killed", "stopped"])
@pytest.mark.asyncio
async def test_terminal_state_uses_one_read(status):
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = object.__new__(cls)
        p._get_once = (
            AsyncMock(return_value=SimpleNamespace(status=status))
            if cls is SandboxProcess
            else Mock(return_value=SimpleNamespace(status=status))
        )
        result = await p.wait("example") if cls is SandboxProcess else p.wait("example")
        assert result.status == status
        assert p._get_once.call_count == 1


@pytest.mark.asyncio
async def test_async_cancel_is_not_a_process_result():
    p = object.__new__(SandboxProcess)
    p._get_once = AsyncMock(
        side_effect=[SimpleNamespace(status="running"), asyncio.CancelledError()]
    )
    with pytest.raises(asyncio.CancelledError):
        await p.wait("example", interval=1)


@pytest.mark.parametrize("status", [401, 403, 404])
@pytest.mark.asyncio
async def test_permanent_failure_preserves_last_observation(status):
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = object.__new__(cls)
        last = SimpleNamespace(status="running")
        error = httpx.HTTPStatusError(
            "unavailable",
            request=httpx.Request("GET", "https://example.com"),
            response=httpx.Response(status),
        )
        p._get_once = (
            AsyncMock(side_effect=[last, error])
            if cls is SandboxProcess
            else Mock(side_effect=[last, error])
        )
        with pytest.raises(ProcessObservationError) as caught:
            if cls is SandboxProcess:
                await p.wait("example", interval=1)
            else:
                p.wait("example", interval=1)
        assert caught.value.identifier == "example"
        assert caught.value.last_observation is last
        assert caught.value.__cause__ is error


@pytest.mark.asyncio
async def test_unknown_status_does_not_count_as_completion():
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = object.__new__(cls)
        p._get_once = (
            AsyncMock(return_value=SimpleNamespace(status="mystery"))
            if cls is SandboxProcess
            else Mock(return_value=SimpleNamespace(status="mystery"))
        )
        with pytest.raises(ProcessObservationError):
            if cls is SandboxProcess:
                await p.wait("example")
            else:
                p.wait("example")


@pytest.fixture
def server():
    state = SimpleNamespace(posts=[], reads=0, deletes=[], mode="recover", name=None)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send_json(self, value, status=200):
            body = json.dumps(value).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def do_POST(self):
            payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            state.posts.append(payload)
            state.name = payload["name"]
            # Command accepted, but its response is lost.
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()

        def do_GET(self):
            state.reads += 1
            if state.mode == "slow":
                time.sleep(0.15)
            if state.mode == "retry" and state.reads == 1:
                self.send_json({"error": "unavailable"}, 503)
            elif state.mode == "fail":
                self.send_json({"error": "unavailable"}, 503)
            else:
                self.send_json(
                    response("killed" if state.deletes else "completed", state.name or "example")
                )

        def do_DELETE(self):
            state.deletes.append(self.path)
            if state.mode == "lost-delete":
                self.connection.shutdown(socket.SHUT_RDWR)
                self.connection.close()
                return
            if state.mode == "slow-delete":
                time.sleep(0.15)
            self.send_json({"message": "ok"})

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    state.url = f"http://127.0.0.1:{httpd.server_port}"
    yield state
    httpd.shutdown()
    httpd.server_close()
    thread.join()


def client(cls, server):
    return cls(
        SandboxConfiguration(
            Sandbox(metadata=Metadata(name="test"), spec=SandboxSpec()), force_url=server.url
        )
    )


@pytest.mark.asyncio
async def test_real_http_recovers_original_execution_without_replaying(server):
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = client(cls, server)
        request = {"command": "echo hello"}
        with pytest.raises(ProcessExecutionError) as caught:
            if cls is SandboxProcess:
                await p.exec(request)
            else:
                p.exec(request)
        assert "name" not in request
        assert caught.value.identifier == server.posts[-1]["name"]
        result = (
            await p.wait(caught.value.identifier)
            if cls is SandboxProcess
            else p.wait(caught.value.identifier)
        )
        assert result.status == "completed"
        assert result.logs == "hello"
        assert result.exit_code == 0
        if cls is SandboxProcess:
            await p.get_client().aclose()
    assert len(server.posts) == 2  # One POST per independent caller; never replayed.


@pytest.mark.asyncio
async def test_real_http_retries_status_then_confirms_explicit_kill(server):
    for cls in (SandboxProcess, SyncSandboxProcess):
        server.reads = 0
        server.mode = "retry"
        p = client(cls, server)
        result = (
            await p.wait("example", max_wait=1000, interval=1)
            if cls is SandboxProcess
            else p.wait("example", max_wait=1000, interval=1)
        )
        assert result.status in {"completed", "killed"}
        assert server.reads == 2
        result = (
            await p.kill_and_wait("example", interval=1)
            if cls is SandboxProcess
            else p.kill_and_wait("example", interval=1)
        )
        assert result.status == "killed"
        if cls is SandboxProcess:
            await p.get_client().aclose()
    assert server.deletes == ["/process/example/kill", "/process/example/kill"]


@pytest.mark.parametrize("mode", ["slow", "fail"])
@pytest.mark.asyncio
async def test_real_http_deadline_never_kills(server, mode):
    server.mode = mode
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = client(cls, server)
        start = time.monotonic()
        with pytest.raises(ProcessWaitTimeout) as caught:
            if cls is SandboxProcess:
                await p.wait("example", max_wait=40, interval=1)
            else:
                p.wait("example", max_wait=40, interval=1)
        assert time.monotonic() - start < 0.5
        assert caught.value.identifier == "example"
        if cls is SandboxProcess:
            await p.get_client().aclose()
    assert not server.deletes


@pytest.mark.asyncio
async def test_execution_inputs_preserve_name_and_callbacks():
    from blaxel.core.sandbox.client.models import ProcessRequest
    from blaxel.core.sandbox.types import ProcessRequestWithLog

    for cls in (SandboxProcess, SyncSandboxProcess):
        callback = Mock()
        requests = [
            {"command": "echo hello", "name": "chosen", "on_log": callback},
            ProcessRequest(command="echo hello", name="chosen"),
            ProcessRequestWithLog(command="echo hello", name="chosen", on_log=callback),
        ]
        for request in requests:
            p = object.__new__(cls)
            p._exec = (
                AsyncMock(return_value="result")
                if cls is SandboxProcess
                else Mock(return_value="result")
            )
            result = await p.exec(request) if cls is SandboxProcess else p.exec(request)
            assert result == "result"
            sent = p._exec.call_args.args[0]
            assert sent is not request
            assert (sent["name"] if isinstance(sent, dict) else sent.name) == "chosen"
            if isinstance(request, dict | ProcessRequestWithLog):
                assert (sent["on_log"] if isinstance(sent, dict) else sent.on_log) is callback


@pytest.mark.asyncio
async def test_cancelled_exec_preserves_identity():
    p = object.__new__(SandboxProcess)
    p._exec = AsyncMock(side_effect=asyncio.CancelledError())
    with pytest.raises(asyncio.CancelledError) as caught:
        await p.exec({"command": "sleep 10"})
    assert caught.value.identifier.startswith("process-")


@pytest.mark.asyncio
async def test_log_stream_cancellation_and_explicit_close():
    # The wait on a live stream must preserve caller cancellation; close remains intentional.
    p = client(SandboxProcess, SimpleNamespace(url="http://127.0.0.1:1"))
    from unittest.mock import patch

    async def forever():
        await asyncio.Future()

    real_create_task = asyncio.create_task

    def task_for_stream(coro):
        coro.close()
        return real_create_task(forever())

    with patch(
        "blaxel.core.sandbox.default.process.asyncio.create_task", side_effect=task_for_stream
    ):
        handle = p._stream_logs("example")
    task = asyncio.create_task(handle.wait())
    await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    with patch(
        "blaxel.core.sandbox.default.process.asyncio.create_task", side_effect=task_for_stream
    ):
        closed = p._stream_logs("example")
    closed.close()
    await closed.wait()


@pytest.mark.asyncio
async def test_lost_signal_response_is_observed_without_repeating_delete(server):
    server.mode = "lost-delete"
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = client(cls, server)
        result = (
            await p.stop_and_wait("example", interval=1)
            if cls is SandboxProcess
            else p.stop_and_wait("example", interval=1)
        )
        assert result.status == "killed"
        if cls is SandboxProcess:
            await p.get_client().aclose()
    assert server.deletes == ["/process/example", "/process/example"]


@pytest.mark.asyncio
async def test_signal_and_wait_share_one_deadline(server):
    server.mode = "slow-delete"
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = client(cls, server)
        with pytest.raises(ProcessWaitTimeout) as caught:
            if cls is SandboxProcess:
                await p.kill_and_wait("example", max_wait=30, interval=1)
            else:
                p.kill_and_wait("example", max_wait=30, interval=1)
        assert caught.value.__cause__ is not None
        if cls is SandboxProcess:
            await p.get_client().aclose()
    assert server.reads == 0
    assert len(server.deletes) == 2


@pytest.mark.asyncio
async def test_early_timeout_can_recover_before_deadline():
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = object.__new__(cls)
        sequence = [TimeoutError("early socket timeout"), SimpleNamespace(status="completed")]
        p._get_once = (
            AsyncMock(side_effect=sequence) if cls is SandboxProcess else Mock(side_effect=sequence)
        )
        result = (
            await p.wait("example", max_wait=1000)
            if cls is SandboxProcess
            else p.wait("example", max_wait=1000)
        )
        assert result.status == "completed"
        assert p._get_once.call_count == 2


def test_sync_log_stream_reports_background_failure(server):
    server.mode = "fail"
    p = client(SyncSandboxProcess, server)
    handle = p._stream_logs("example")
    try:
        with pytest.raises(Exception, match="Failed to stream logs"):
            handle.wait(timeout=2)
    finally:
        handle.close()

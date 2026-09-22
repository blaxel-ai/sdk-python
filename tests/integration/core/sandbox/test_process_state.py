"""Process recovery against a disposable real sandbox API.

Run with BL_PROCESS_TEST_URL pointing to an isolated sandbox API (never production).
The loopback proxy deliberately drops one accepted execution response.
"""

import asyncio
import json
import os
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import SimpleNamespace
from uuid import uuid4

import httpx
import pytest

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox import ProcessExecutionError, ProcessWaitTimeout
from blaxel.core.sandbox.default.process import SandboxProcess
from blaxel.core.sandbox.sync.process import SyncSandboxProcess
from blaxel.core.sandbox.types import SandboxConfiguration

pytestmark = pytest.mark.skipif(
    not os.environ.get("BL_PROCESS_TEST_URL"), reason="requires an isolated sandbox API"
)


def process(cls, url):
    return cls(
        SandboxConfiguration(
            Sandbox(metadata=Metadata(name="process-state-test"), spec=SandboxSpec()), force_url=url
        )
    )


@pytest.fixture
def interrupted_api():
    target = os.environ["BL_PROCESS_TEST_URL"]
    posts = []
    expected = SimpleNamespace(name="")

    class Proxy(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            if self.path != "/process":
                self.send_error(404)
                return
            body = self.rfile.read(int(self.headers["Content-Length"]))
            posts.append(json.loads(body))
            response = httpx.post(
                target + "/process",
                content=body,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()

        def do_GET(self):
            # Forward only URLs configured by the test, never a client-supplied path.
            upstream = target + "/process/" + expected.name
            if self.path == f"/process/{expected.name}/logs":
                upstream += "/logs"
            elif self.path != f"/process/{expected.name}":
                self.send_error(404)
                return
            response = httpx.get(upstream, timeout=10)
            self.send_response(response.status_code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response.content)))
            self.end_headers()
            self.wfile.write(response.content)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Proxy)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}", posts, expected
    server.shutdown()
    server.server_close()
    thread.join()


@pytest.mark.asyncio
async def test_real_api_recovery_after_response_loss(interrupted_api):
    url, posts, expected = interrupted_api
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = process(cls, url)
        name = f"py-recover-{uuid4().hex[:12]}"
        expected.name = name
        request = {
            "name": name,
            "command": "sh -c 'echo recovered; exit 7'",
            "wait_for_completion": False,
            "keep_alive": False,
        }
        with pytest.raises(ProcessExecutionError) as caught:
            if cls is SandboxProcess:
                await p.exec(request)
            else:
                p.exec(request)
        assert caught.value.identifier == name
        result = (
            await p.wait(name, max_wait=5000, interval=20)
            if cls is SandboxProcess
            else p.wait(name, max_wait=5000, interval=20)
        )
        assert result.status == "failed"
        assert result.exit_code == 7
        assert "recovered" in result.logs
        logs = await p.logs(name) if cls is SandboxProcess else p.logs(name)
        assert "recovered" in logs
        assert sum(item["name"] == name for item in posts) == 1
        if cls is SandboxProcess:
            await p.get_client().aclose()


@pytest.mark.asyncio
async def test_real_api_timeout_and_cancellation_leave_command_running():
    for cls in (SandboxProcess, SyncSandboxProcess):
        p = process(cls, os.environ["BL_PROCESS_TEST_URL"])
        name = f"py-cancel-{uuid4().hex[:12]}"
        request = {
            "name": name,
            "command": "sleep 15",
            "wait_for_completion": False,
            "keep_alive": False,
        }
        if cls is SandboxProcess:
            await p.exec(request)
        else:
            p.exec(request)
        try:
            with pytest.raises(ProcessWaitTimeout):
                if cls is SandboxProcess:
                    await p.wait(name, max_wait=40, interval=10)
                else:
                    p.wait(name, max_wait=40, interval=10)
            if cls is SandboxProcess:
                task = asyncio.create_task(p.wait(name, interval=10))
                await asyncio.sleep(0.02)
                task.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await task
                running = await p.get(name)
                assert running.status == "running"
                stopped = await p.kill_and_wait(name, max_wait=2000, interval=10)
            else:
                running = p.get(name)
                assert running.status == "running"
                stopped = p.stop_and_wait(name, max_wait=2000, interval=10)
            assert stopped.status in {"killed", "stopped", "completed", "failed"}
        finally:
            if cls is SandboxProcess:
                await p.kill(name)
                await p.get_client().aclose()
            else:
                p.kill(name)


@pytest.mark.asyncio
async def test_real_api_callback_model_preserves_callbacks():
    from blaxel.core.sandbox.types import ProcessRequestWithLog

    for cls in (SandboxProcess, SyncSandboxProcess):
        p = process(cls, os.environ["BL_PROCESS_TEST_URL"])
        logs = []
        request = ProcessRequestWithLog(
            command="echo model-callback",
            wait_for_completion=True,
            keep_alive=False,
            on_log=logs.append,
        )
        result = await p.exec(request) if cls is SandboxProcess else p.exec(request)
        assert result.status == "completed"
        assert any("model-callback" in line for line in logs)
        if cls is SandboxProcess and p._client is not None:
            await p.get_client().aclose()


def test_recovery_proxy_rejects_unexpected_routes(interrupted_api):
    url, posts, expected = interrupted_api
    expected.name = "only-this-process"
    assert httpx.get(url + "/unexpected-target").status_code == 404
    assert httpx.post(url + "/unexpected-target", json={}).status_code == 404
    assert posts == []

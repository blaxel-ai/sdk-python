"""Exec streaming negotiates NDJSON with the sandbox API."""

import json

import httpx

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox.client.models.process_request import ProcessRequest
from blaxel.core.sandbox.default.process import SandboxProcess
from blaxel.core.sandbox.sync.process import SyncSandboxProcess
from blaxel.core.sandbox.types import SandboxConfiguration


def _config():
    return SandboxConfiguration(
        Sandbox(metadata=Metadata(name="test"), spec=SandboxSpec()), force_url="http://localhost"
    )


def _patch_clients(monkeypatch, handler):
    real_client, real_async_client = httpx.Client, httpx.AsyncClient
    monkeypatch.setattr(
        httpx, "Client", lambda **kwargs: real_client(transport=httpx.MockTransport(handler))
    )
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: real_async_client(transport=httpx.MockTransport(handler)),
    )


class _Chunks(httpx.SyncByteStream, httpx.AsyncByteStream):
    def __init__(self, chunks):
        self.chunks = [chunk.encode() for chunk in chunks]

    def __iter__(self):
        yield from self.chunks

    async def __aiter__(self):
        for chunk in self.chunks:
            yield chunk


def _collect():
    seen = {"on_log": [], "on_stdout": [], "on_stderr": []}
    return seen, {name: seen[name].append for name in seen}


async def test_exec_streaming_negotiates_and_parses_ndjson(monkeypatch):
    result = json.dumps(
        {
            "name": "proc",
            "pid": "1",
            "command": "echo",
            "status": "completed",
            "exitCode": 0,
            "workingDir": "/",
            "startedAt": "",
            "completedAt": "",
            "stdout": "hi\n",
            "stderr": "warn\n",
            "logs": "hi\nwarn\n",
        }
    )
    lines = [
        json.dumps({"type": "stdout", "data": "hi\n"}),
        "",
        json.dumps({"type": "stderr", "data": "warn\n"}),
        json.dumps({"type": "result", "data": result}),
    ]
    body = "\n".join(lines) + "\n"
    accepts = []

    def handler(request: httpx.Request) -> httpx.Response:
        accepts.append(request.headers["Accept"])
        return httpx.Response(
            200,
            headers={"Content-Type": "application/x-ndjson"},
            stream=_Chunks([body[:20], body[20:]]),
        )

    _patch_clients(monkeypatch, handler)

    for cls in (SandboxProcess, SyncSandboxProcess):
        seen, options = _collect()
        request = ProcessRequest(command="echo")
        process = cls(_config())
        if cls is SandboxProcess:
            response = await process._exec_with_streaming(request, **options)
        else:
            response = process._exec_with_streaming(request, **options)
        assert response.exit_code == 0
        assert seen == {
            "on_log": ["hi\n", "warn\n"],
            "on_stdout": ["hi\n"],
            "on_stderr": ["warn\n"],
        }
    assert accepts == ["application/x-ndjson, text/event-stream"] * 2

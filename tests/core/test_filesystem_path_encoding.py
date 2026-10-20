"""Filesystem names must survive URL parsing without becoming queries or fragments."""

import json
from urllib.parse import unquote

import httpx
import pytest

from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem
from blaxel.core.sandbox.types import SandboxConfiguration


@pytest.mark.parametrize(
    "path", ["/tmp/report#1.txt", "/tmp/report?draft.txt", "/tmp/literal%2F.txt", "/tmp/plain.txt"]
)
@pytest.mark.parametrize(
    "operation",
    [
        "read",
        "write",
        "read_binary",
        "write_binary",
        "mkdir",
        "rm",
        "ls",
        "write_tree",
        "_initiate_multipart_upload",
    ],
)
@pytest.mark.parametrize("asynchronous", [False, True])
async def test_filesystem_preserves_literal_paths(monkeypatch, path, operation, asynchronous):
    requests = []

    def respond(request):
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "content": "hello",
                "message": "ok",
                "files": [],
                "name": "test",
                "path": path,
                "subdirectories": [],
                "uploadId": "test-upload",
            },
        )

    transport = httpx.MockTransport(respond)
    config = SandboxConfiguration(sandbox=None, force_url="https://sandbox.example.test")
    filesystem = (SandboxFileSystem if asynchronous else SyncSandboxFileSystem)(config)
    if asynchronous:
        async with httpx.AsyncClient(base_url=config.force_url, transport=transport) as client:
            monkeypatch.setattr(filesystem, "get_client", lambda: client)
            arguments = [path]
            if operation.startswith("write"):
                arguments.append(b"hello" if operation.endswith("binary") else "hello")
            if operation == "write_tree":
                arguments = [[{"path": path, "content": "hello"}], path]
            await getattr(filesystem, operation)(*arguments)
    else:
        monkeypatch.setattr(
            filesystem,
            "get_client",
            lambda: httpx.Client(base_url=config.force_url, transport=transport),
        )
        arguments = [path]
        if operation.startswith("write"):
            arguments.append(b"hello" if operation.endswith("binary") else "hello")
        if operation == "write_tree":
            arguments = [[{"path": path, "content": "hello"}], path]
        getattr(filesystem, operation)(*arguments)

    assert len(requests) == 1
    request = requests[0]
    prefix = "/filesystem/"
    if operation == "write_tree":
        prefix = "/filesystem/tree/"
        assert json.loads(request.content)["files"] == {path: "hello"}
    elif operation == "_initiate_multipart_upload":
        prefix = "/filesystem-multipart/initiate/"
    # rm has its own documented recursive query parameter.
    assert unquote(request.url.raw_path.decode().split("?", 1)[0]) == f"{prefix}{path}"
    assert not request.url.query or operation == "rm"
    assert not request.url.fragment
    if operation == "write_binary":
        # The multipart form is data, not a URL: leave the original name intact.
        assert path.encode() in request.content

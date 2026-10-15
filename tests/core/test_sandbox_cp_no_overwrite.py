"""cp(..., no_overwrite=True) sends one sandbox API copy request, async and sync."""

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from blaxel.core.client.models import Metadata, SandboxSpec
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem
from blaxel.core.sandbox.types import ResponseError, Sandbox, SandboxConfiguration

modes = pytest.mark.parametrize("mode", ["async", "sync"])


def harness(mode, respond):
    """Return a cp callable whose HTTP requests go to ``respond``, the requests, and the process."""
    requests = []

    def handler(request):
        requests.append(request)
        return respond(request)

    config = SandboxConfiguration(
        sandbox=Sandbox(metadata=Metadata(name="cp-test"), spec=SandboxSpec()),
        force_url="https://example.test",
    )
    transport = httpx.MockTransport(handler)
    done = SimpleNamespace(pid="pid-1", status="completed", exit_code=0, logs="")
    if mode == "sync":
        process = Mock()
        process.exec.return_value = done
        process.wait.return_value = done
        fs = SyncSandboxFileSystem(config, process)
        fs.get_client = lambda: httpx.Client(base_url="https://example.test", transport=transport)
        return fs.cp, requests, process

    process = Mock()
    process.exec = AsyncMock(return_value=done)
    process.wait = AsyncMock(return_value=done)
    fs = SandboxFileSystem(config, process)
    fs.get_client = lambda: httpx.AsyncClient(base_url="https://example.test", transport=transport)

    def call(*args, **kwargs):
        return asyncio.run(fs.cp(*args, **kwargs))

    return call, requests, process


def ok(request):
    return httpx.Response(200, json={"message": "Files copied"})


@modes
@pytest.mark.parametrize("options", [{}, {"no_overwrite": False}])
def test_default_cp_keeps_the_process_path(mode, options):
    call, requests, process = harness(mode, ok)
    result = call("source", "destination", **options)
    assert (result.source, result.destination) == ("source", "destination")
    process.exec.assert_called_once_with({"command": "cp -r source destination"})
    assert requests == []


@modes
def test_no_overwrite_sends_one_copy_request_without_a_process(mode):
    call, requests, process = harness(mode, ok)
    source = "-source ' ; $(touch BAD)\nユニコード"
    result = call(source, "/tmp/destination", no_overwrite=True)
    assert (result.message, result.source, result.destination) == (
        "Files copied",
        source,
        "/tmp/destination",
    )
    assert len(requests) == 1
    assert (requests[0].method, requests[0].url.path) == ("POST", "/filesystem-copy")
    assert json.loads(requests[0].content) == {
        "source": source,
        "destination": "/tmp/destination",
        "noOverwrite": True,
    }
    process.exec.assert_not_called()


@modes
def test_conflict_raises_file_exists_error(mode):
    body = {"error": "error copying destination dst: file exists", "code": "FILE_ALREADY_EXISTS"}
    call, _, _ = harness(mode, lambda request: httpx.Response(409, json=body))
    with pytest.raises(
        FileExistsError, match="Could not copy src to dst: destination already exists"
    ):
        call("src", "dst", no_overwrite=True)


@modes
def test_older_sandbox_api_fails_closed(mode):
    call, requests, process = harness(
        mode, lambda request: httpx.Response(404, text="404 page not found")
    )
    with pytest.raises(RuntimeError, match="needs a newer sandbox API"):
        call("src", "dst", no_overwrite=True)
    assert len(requests) == 1
    process.exec.assert_not_called()


@modes
@pytest.mark.parametrize(
    "status, body",
    [
        (409, {"error": "conflict without a code"}),
        (422, {"error": "error copying destination dst: no such file or directory"}),
        (400, {"error": "bad request"}),
    ],
)
def test_other_errors_are_response_errors_not_conflicts(mode, status, body):
    call, _, _ = harness(mode, lambda request: httpx.Response(status, json=body))
    with pytest.raises(ResponseError) as error:
        call("src", "dst", no_overwrite=True)
    assert error.value.response.status_code == status


@modes
@pytest.mark.parametrize("source, destination", [("", "dst"), ("src", "")])
def test_rejects_empty_paths_before_any_request(mode, source, destination):
    call, requests, _ = harness(mode, ok)
    with pytest.raises(ValueError):
        call(source, destination, no_overwrite=True)
    assert requests == []


@modes
def test_a_failed_request_is_not_retried(mode):
    def reset(request):
        raise httpx.ReadError("connection reset")

    call, requests, _ = harness(mode, reset)
    with pytest.raises(httpx.ReadError):
        call("src", "dst", no_overwrite=True)
    assert len(requests) == 1

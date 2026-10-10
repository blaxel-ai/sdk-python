import asyncio

import httpx
import pytest

from blaxel.core.client.models import Metadata, SandboxSpec
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem
from blaxel.core.sandbox.types import ResponseError, Sandbox, SandboxConfiguration

modes = pytest.mark.parametrize("mode", ["async", "sync"])


def tree(path, files, recursive=True):
    body = {"path": path, "name": path.rsplit("/", 1)[-1], "files": files, "subdirectories": []}
    if recursive:
        body["recursive"] = True
    return body


def harness(mode, respond):
    """Return a read_tree callable whose requests go to ``respond`` and the request list."""
    requests = []

    def handler(request):
        requests.append(request)
        return respond(request)

    config = SandboxConfiguration(
        sandbox=Sandbox(metadata=Metadata(name="read-tree-test"), spec=SandboxSpec()),
        force_url="https://example.test",
    )
    transport = httpx.MockTransport(handler)
    if mode == "sync":
        fs = SyncSandboxFileSystem(config)
        fs.get_client = lambda: httpx.Client(base_url="https://example.test", transport=transport)
        return fs.read_tree, requests

    fs = SandboxFileSystem(config)
    fs.get_client = lambda: httpx.AsyncClient(base_url="https://example.test", transport=transport)

    def call(*args, **kwargs):
        return asyncio.run(fs.read_tree(*args, **kwargs))

    return call, requests


@modes
def test_reads_the_whole_tree_in_one_request(mode):
    call, requests = harness(
        mode, lambda request: httpx.Response(200, json=tree("/data dir#1", []))
    )
    assert call("/data dir#1") == {}
    assert len(requests) == 1
    assert requests[0].url.raw_path.decode().startswith("/filesystem/tree//data%20dir%231?")
    assert dict(requests[0].url.params) == {"recursive": "true", "content": "true"}


@modes
def test_passes_selection_and_limits_as_query_parameters(mode):
    call, requests = harness(mode, lambda request: httpx.Response(200, json=tree("/root", [])))
    call(
        "/root",
        patterns=["*.json", "*.md"],
        exclude_dirs=["node_modules", "dist"],
        exclude_hidden=False,
        max_files=5,
        max_bytes=1024,
    )
    assert dict(requests[0].url.params) == {
        "recursive": "true",
        "content": "true",
        "patterns": "*.json,*.md",
        "excludeDirs": "node_modules,dist",
        "excludeHidden": "false",
        "maxFiles": "5",
        "maxBytes": "1024",
    }


@modes
def test_returns_sorted_relative_paths_and_skips_entries_without_content(mode):
    files = [
        {"path": "/root/z.json", "name": "z.json", "content": "z"},
        {"path": "/root/nested/b.json", "name": "b.json", "content": ""},
        {"path": "/root/dir-link", "name": "dir-link"},
        {"path": "/root/a.json", "name": "a.json", "content": "a"},
    ]
    call, _ = harness(mode, lambda request: httpx.Response(200, json=tree("/root", files)))
    result = call("/root/")
    assert list(result) == ["a.json", "nested/b.json", "z.json"]
    assert result["nested/b.json"] == ""


@modes
def test_strips_the_prefix_when_the_root_is_slash(mode):
    files = [{"path": "/a.json", "name": "a.json", "content": "a"}]
    call, _ = harness(mode, lambda request: httpx.Response(200, json=tree("/", files)))
    assert call("/") == {"a.json": "a"}


@modes
def test_fails_on_an_older_sandbox_api_that_lists_one_level(mode):
    files = [{"path": "/root/a.json", "name": "a.json"}]
    call, _ = harness(
        mode, lambda request: httpx.Response(200, json=tree("/root", files, recursive=False))
    )
    with pytest.raises(RuntimeError, match="needs a newer sandbox API"):
        call("/root")


@modes
def test_surfaces_a_limit_error_from_the_api(mode):
    body = {"error": "tree read limit exceeded: more than 5 files match under /root"}
    call, _ = harness(mode, lambda request: httpx.Response(422, json=body))
    with pytest.raises(ResponseError) as error:
        call("/root", max_files=5)
    assert error.value.status == 422

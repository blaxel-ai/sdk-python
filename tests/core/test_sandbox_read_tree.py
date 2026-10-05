import asyncio
import threading
import time

import httpx
import pytest

from blaxel.core import FilesystemReadTreeError
from blaxel.core.client.models import Metadata, SandboxSpec
from blaxel.core.sandbox.client.models import FindMatch, FindResponse
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.read_tree import _read_tree_async, _read_tree_sync
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem
from blaxel.core.sandbox.types import Sandbox, SandboxConfiguration

modes = pytest.mark.parametrize("mode", ["async", "sync"])


def found(*paths):
    matches = [FindMatch(path=path, type_="file") for path in paths]
    return FindResponse(matches=matches, total=len(matches))


def run(mode, find, read, root="/root", max_files=100, concurrency=4):
    """Run the shared async or sync implementation with plain functions as find and read."""
    if mode == "sync":
        return _read_tree_sync(root, max_files, concurrency, find, read)
    return asyncio.run(
        _read_tree_async(
            root,
            max_files,
            concurrency,
            lambda limit: asyncio.to_thread(find, limit),
            lambda path: asyncio.to_thread(read, path),
        )
    )


@modes
def test_returns_sorted_relative_paths_and_asks_find_for_one_extra(mode):
    limits = []
    result = run(
        mode,
        lambda limit: limits.append(limit) or found("z.json", "nested/a.json", "a.json"),
        lambda path: f"read {path}",
        root="/root/",
    )
    assert list(result) == ["a.json", "nested/a.json", "z.json"]
    assert result["nested/a.json"] == "read /root/nested/a.json"
    assert limits == [101]


@modes
def test_rejects_with_max_files_before_reading(mode):
    reads = []
    assert len(run(mode, lambda limit: found("a", "b"), lambda path: path, max_files=2)) == 2
    with pytest.raises(FilesystemReadTreeError) as error:
        run(mode, lambda limit: found("a", "b", "c"), reads.append, max_files=2)
    assert (error.value.code, error.value.root, reads) == ("MAX_FILES", "/root", [])


@modes
@pytest.mark.parametrize("options", [{"max_files": 1000}, {"concurrency": 0}])
def test_rejects_options_find_cannot_honor_before_any_request(mode, options):
    calls = []
    with pytest.raises(ValueError):
        run(mode, lambda limit: calls.append(limit), lambda path: path, **options)
    assert calls == []


@modes
def test_concurrency_is_bounded(mode):
    lock = threading.Lock()
    active = {"now": 0, "peak": 0}

    def read(path):
        with lock:
            active["now"] += 1
            active["peak"] = max(active["peak"], active["now"])
        time.sleep(0.02)
        with lock:
            active["now"] -= 1
        return path

    run(mode, lambda limit: found(*"abcdef"), read, concurrency=2)
    assert active["peak"] == 2


@modes
def test_read_failure_raises_read_with_path_and_stops_reading(mode):
    paths = [f"{i:02}" for i in range(20)]
    cause = OSError("boom")
    reads = []

    def read(path):
        reads.append(path)
        if path.endswith("/00"):
            raise cause
        time.sleep(0.01)
        return path

    with pytest.raises(FilesystemReadTreeError) as error:
        run(mode, lambda limit: found(*paths), read, concurrency=2)
    assert (error.value.code, error.value.root, error.value.path) == ("READ", "/root", "00")
    assert error.value.__cause__ is cause
    assert len(reads) < 20


@modes
def test_discovery_failure_raises_discovery_and_does_not_read(mode):
    cause = OSError("no such directory")
    reads = []

    def find(limit):
        raise cause

    with pytest.raises(FilesystemReadTreeError) as error:
        run(mode, find, reads.append)
    assert (error.value.code, error.value.path, reads) == ("DISCOVERY", None, [])
    assert error.value.__cause__ is cause


@modes
def test_public_method_sends_selection_to_find_and_encodes_names(mode):
    requests = []

    def handler(request):
        requests.append(request)
        if "/filesystem-find/" in request.url.path:
            matches = [{"path": "a b#1.json", "type": "file"}, {"path": "c.json", "type": "file"}]
            return httpx.Response(200, json={"matches": matches, "total": 2})
        return httpx.Response(200, json={"content": "text"})

    config = SandboxConfiguration(
        sandbox=Sandbox(metadata=Metadata(name="read-tree-test"), spec=SandboxSpec()),
        force_url="https://example.test",
    )
    transport = httpx.MockTransport(handler)
    if mode == "sync":
        fs = SyncSandboxFileSystem(config)
        fs.get_client = lambda: httpx.Client(base_url="https://example.test", transport=transport)
        call = fs.read_tree
    else:
        fs = SandboxFileSystem(config)
        fs.get_client = lambda: httpx.AsyncClient(
            base_url="https://example.test", transport=transport
        )

        def call(*args, **kwargs):
            return asyncio.run(fs.read_tree(*args, **kwargs))

    result = call(
        "/data dir#1",
        patterns=["*.json"],
        exclude_dirs=["dist"],
        exclude_hidden=False,
        max_files=20,
    )
    assert result == {"a b#1.json": "text", "c.json": "text"}
    find_request = next(r for r in requests if "/filesystem-find/" in r.url.path)
    assert find_request.url.raw_path.decode().startswith("/filesystem-find//data%20dir%231?")
    assert dict(find_request.url.params) == {
        "type": "file",
        "maxResults": "21",
        "patterns": "*.json",
        "excludeDirs": "dist",
        "excludeHidden": "false",
    }
    assert sorted(r.url.raw_path.decode() for r in requests if r is not find_request) == [
        "/filesystem//data%20dir%231/a%20b%231.json",
        "/filesystem//data%20dir%231/c.json",
    ]

"""Sandbox URLs are joined the same way with or without a trailing slash."""

import httpx
import pytest

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox.default.action import SandboxAction
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.sync.action import SyncSandboxAction
from blaxel.core.sandbox.types import SandboxConfiguration

BASES = ["https://sbx.example.com", "https://sbx.example.com/", "https://sbx.example.com//"]


@pytest.mark.parametrize("cls", [SandboxAction, SyncSandboxAction])
@pytest.mark.parametrize("base", BASES)
def test_metadata_url_is_normalized(cls, base):
    sandbox = Sandbox(metadata=Metadata(name="sbx", url=base), spec=SandboxSpec())
    action = cls(SandboxConfiguration(sandbox))
    assert action.external_url == "https://sbx.example.com"


@pytest.mark.parametrize("cls", [SandboxAction, SyncSandboxAction])
@pytest.mark.parametrize("base", BASES)
def test_forced_url_is_normalized(cls, base):
    sandbox = Sandbox(metadata=Metadata(name="sbx"), spec=SandboxSpec())
    action = cls(SandboxConfiguration(sandbox, force_url=base))
    assert action.url == "https://sbx.example.com"


@pytest.mark.parametrize("base", BASES)
async def test_requests_have_no_double_slash(base):
    paths = []

    def handler(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.raw_path.decode())
        return httpx.Response(200, json={"matches": [], "query": "x", "total": 0})

    sandbox = Sandbox(metadata=Metadata(name="sbx", url=base), spec=SandboxSpec())
    filesystem = SandboxFileSystem(SandboxConfiguration(sandbox))
    filesystem._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    await filesystem.grep("x", "app")
    assert paths == ["/filesystem-content-search/app?query=x"]

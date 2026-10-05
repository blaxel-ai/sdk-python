import asyncio

import pytest
import pytest_asyncio

from blaxel.core import FilesystemReadTreeError, SandboxInstance, SyncSandboxInstance
from tests.helpers import (
    default_image,
    default_labels,
    default_region,
    unique_name,
    wait_for_sandbox_deletion,
)

ROOT = "/tmp/read-tree"
FILES = {
    "a.json": '{"a": "café 🌳"}\n',
    "nested/b c#1.json": '{"b": 2}\n',
    "node_modules/skipped.json": "{}",
    "dist/built.json": "{}",
    "notes.txt": "not selected",
}


@pytest.mark.asyncio(loop_scope="class")
class TestReadTree:
    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        name = unique_name("read-tree")
        try:
            sandbox = await SandboxInstance.create(
                {
                    "name": name,
                    "image": default_image,
                    "region": default_region,
                    "ttl": "1h",
                    "labels": default_labels,
                }
            )
            request.cls.sandbox = sandbox
            request.cls.sync_sandbox = SyncSandboxInstance(sandbox.config)
            await sandbox.fs.write_tree(
                [{"path": path, "content": content} for path, content in FILES.items()], ROOT
            )
            await sandbox.fs.mkdir("/tmp/read-tree-empty")
            await sandbox.process.exec(
                {
                    "command": f"mkdir {ROOT}-link && ln -s {ROOT}/nested {ROOT}-link/current",
                    "wait_for_completion": True,
                }
            )
            yield
        finally:
            await SandboxInstance.delete(name)
            assert await wait_for_sandbox_deletion(name, max_attempts=10)

    async def read_tree(self, mode, path, **kwargs):
        if mode == "async":
            return await self.sandbox.fs.read_tree(path, **kwargs)
        return await asyncio.to_thread(self.sync_sandbox.fs.read_tree, path, **kwargs)

    @pytest.mark.parametrize("mode", ["async", "sync"])
    async def test_reads_selected_files_and_replaces_default_exclusions(self, mode):
        assert await self.read_tree(mode, ROOT, patterns=["*.json"]) == {
            "a.json": FILES["a.json"],
            "nested/b c#1.json": FILES["nested/b c#1.json"],
        }
        assert await self.read_tree(mode, "/tmp/read-tree-empty") == {}
        replaced = await self.read_tree(
            mode, ROOT, patterns=["*.json"], exclude_dirs=["node_modules"]
        )
        assert list(replaced) == ["a.json", "dist/built.json", "nested/b c#1.json"]

    @pytest.mark.parametrize("mode", ["async", "sync"])
    async def test_failures_raise_filesystem_read_tree_error(self, mode):
        with pytest.raises(FilesystemReadTreeError) as too_many:
            await self.read_tree(mode, ROOT, patterns=["*.json"], max_files=1)
        assert (too_many.value.code, too_many.value.root) == ("MAX_FILES", ROOT)
        with pytest.raises(FilesystemReadTreeError) as missing:
            await self.read_tree(mode, "/tmp/read-tree-missing")
        assert missing.value.code == "DISCOVERY"
        # find reports a symlink to a directory as a file; reading it fails.
        with pytest.raises(FilesystemReadTreeError) as symlink:
            await self.read_tree(mode, f"{ROOT}-link")
        assert (symlink.value.code, symlink.value.path) == ("READ", "current")

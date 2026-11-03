"""Live copy contract, including stable-target races and default overwrite."""

import asyncio
import inspect
from typing import Any

import pytest
import pytest_asyncio

from blaxel.core import SandboxInstance, SyncSandboxInstance
from tests.helpers import default_image, default_labels, unique_name


async def call(fn, *args, **kwargs):
    if inspect.iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    return await asyncio.to_thread(fn, *args, **kwargs)


@pytest.mark.asyncio(loop_scope="class")
class TestCopyNoOverwrite:
    sandbox: Any

    @pytest_asyncio.fixture(
        autouse=True,
        scope="class",
        loop_scope="class",
        params=[SandboxInstance, SyncSandboxInstance],
        ids=["async", "sync"],
    )
    async def cleanup(self, request):
        cls = request.param
        name = unique_name("cp-no-overwrite")
        try:
            request.cls.sandbox = await call(
                cls.create,
                {
                    "name": name,
                    "image": default_image,
                    "region": "us-was-1",
                    "memory": 512,
                    "labels": default_labels,
                },
            )
            yield
        finally:
            await call(cls.delete, name)

    async def test_copy_contract(self):
        fs = self.sandbox.fs
        await call(fs.write, "/tmp/source.txt", "source-new")
        await call(fs.write, "/tmp/target.txt", "target-original")
        with pytest.raises(FileExistsError, match="destination already exists"):
            await call(fs.cp, "/tmp/source.txt", "/tmp/target.txt", no_overwrite=True)
        assert await call(fs.read, "/tmp/target.txt") == "target-original"
        copied = await call(fs.cp, "/tmp/source.txt", "/tmp/new-target.txt", no_overwrite=True)
        assert copied.__dict__ == {
            "message": "Files copied",
            "source": "/tmp/source.txt",
            "destination": "/tmp/new-target.txt",
        }
        assert await call(fs.read, "/tmp/new-target.txt") == "source-new"
        with pytest.raises(FileExistsError):
            await call(fs.cp, "/tmp/source.txt", "/tmp/new-target.txt", no_overwrite=True)
        setup = await call(
            self.sandbox.process.exec,
            {
                "command": "mkdir -p /tmp/container /tmp/tree/sub; printf hidden > /tmp/tree/.hidden; "
                "printf data > /tmp/tree/sub/file; ln -s sub/file /tmp/tree/link; "
                "ln -s missing /tmp/source-link; ln -s missing /tmp/target-link",
                "wait_for_completion": True,
            },
        )
        assert setup.status == "completed"
        await call(fs.cp, "/tmp/source.txt", "/tmp/container", no_overwrite=True)
        assert await call(fs.read, "/tmp/container/source.txt") == "source-new"
        with pytest.raises(FileExistsError):
            await call(fs.cp, "/tmp/source.txt", "/tmp/container", no_overwrite=True)
        await call(fs.cp, "/tmp/tree", "/tmp/new-tree", no_overwrite=True)
        assert await call(fs.read, "/tmp/new-tree/.hidden") == "hidden"
        assert await call(fs.read, "/tmp/new-tree/sub/file") == "data"
        await call(fs.cp, "/tmp/source-link", "/tmp/new-link", no_overwrite=True)
        with pytest.raises(FileExistsError):
            await call(fs.cp, "/tmp/source.txt", "/tmp/target-link", no_overwrite=True)
        check = await call(
            self.sandbox.process.exec,
            {
                "command": "test -L /tmp/new-tree/link && test -L /tmp/new-link && "
                'test "$(readlink /tmp/new-link)" = missing && test ! -e /tmp/new-tree/tree',
                "wait_for_completion": True,
            },
        )
        assert check.status == "completed"
        results = await asyncio.gather(
            *[
                call(fs.cp, "/tmp/source.txt", "/tmp/race-target", no_overwrite=True)
                for _ in range(6)
            ],
            return_exceptions=True,
        )
        assert sum(not isinstance(result, BaseException) for result in results) == 1
        assert sum(isinstance(result, FileExistsError) for result in results) == 5
        assert await call(fs.read, "/tmp/race-target") == "source-new"
        await call(fs.cp, "/tmp/source.txt", "/tmp/target.txt", no_overwrite=False)
        assert await call(fs.read, "/tmp/target.txt") == "source-new"

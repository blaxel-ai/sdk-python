import asyncio
import os

import httpx
import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name, wait_for_sandbox_deletion

# Archiving exports the whole filesystem to the archive store and shuts the
# sandbox down; the restore writes it back over a fresh instance. Even an empty
# image takes minutes both ways, well past the one-minute budget of the default
# run, so this is opt-in.
pytestmark = pytest.mark.skipif(
    not os.environ.get("RUN_SLOW_TESTS"),
    reason="slow test; set RUN_SLOW_TESTS=1 to enable",
)


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxArchive:
    """Archive a sandbox to its filesystem, and unarchive it back."""

    name = unique_name("archive")

    @pytest_asyncio.fixture(autouse=True)
    async def cleanup(self):
        yield
        try:
            await SandboxInstance.delete(TestSandboxArchive.name)
        except Exception:
            pass

    async def test_keeps_the_filesystem_across_an_archive_and_its_restore(self):
        sandbox = await SandboxInstance.create(
            {
                "name": TestSandboxArchive.name,
                "image": default_image,
                "labels": default_labels,
            }
        )
        await sandbox.fs.write("/blaxel/archived.txt", "kept")

        await sandbox.archive()
        assert sandbox.status == "ARCHIVED"

        await sandbox.unarchive()
        assert sandbox.status == "DEPLOYED"
        assert await sandbox.fs.read("/blaxel/archived.txt") == "kept"


async def _serves(url: str, attempts: int = 40, delay: float = 3.0) -> int:
    """Status of ``url`` once it answers, polling while the app comes back up."""
    status = 0
    async with httpx.AsyncClient(timeout=60.0) as client:
        for _ in range(attempts):
            try:
                status = (await client.get(url)).status_code
            except httpx.HTTPError:
                status = 0
            if status == 200:
                return status
            await asyncio.sleep(delay)
    return status


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxArchiveLifecycle:
    """The lifecycle a customer goes through: an app behind a preview, archived
    and given back, then deleted.

    An archive keeps the record, its name and its previews, and releases only
    the compute — so the preview URL that served before the archive is the one
    that serves after the restore.
    """

    name = unique_name("archive-preview")
    preview_name = "archive-preview"

    @pytest_asyncio.fixture(autouse=True)
    async def cleanup(self):
        yield
        try:
            await SandboxInstance.delete(TestSandboxArchiveLifecycle.name)
        except Exception:
            pass

    async def test_serves_the_same_preview_before_and_after_an_archive(self):
        sandbox = await SandboxInstance.create(
            {
                "name": TestSandboxArchiveLifecycle.name,
                "image": "blaxel/nextjs:latest",
                "memory": 4096,
                "ports": [{"target": 3000}],
                "labels": default_labels,
            }
        )
        await sandbox.process.exec(
            {
                "command": "npm run dev -- --port 3000",
                "working_dir": "/blaxel/app",
                "wait_for_ports": [3000],
            }
        )

        preview = await sandbox.previews.create(
            {
                "metadata": {"name": TestSandboxArchiveLifecycle.preview_name},
                "spec": {"port": 3000, "public": True},
            }
        )
        url = preview.spec.url
        assert url
        assert await _serves(url) == 200

        await sandbox.archive()
        assert sandbox.status == "ARCHIVED"

        await sandbox.unarchive()
        assert sandbox.status == "DEPLOYED"

        # The archive holds the filesystem, not the running processes: the dev
        # server is started again from the configuration the export saved, so
        # the preview answers once it is listening again.
        previews = await sandbox.previews.list()
        restored = next(
            (p for p in previews if p.name == TestSandboxArchiveLifecycle.preview_name), None
        )
        assert restored is not None
        assert restored.spec.url == url
        assert await _serves(url) == 200

        await SandboxInstance.delete(TestSandboxArchiveLifecycle.name)
        assert await wait_for_sandbox_deletion(TestSandboxArchiveLifecycle.name, 120)

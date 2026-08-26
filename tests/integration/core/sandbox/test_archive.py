import os

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name

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

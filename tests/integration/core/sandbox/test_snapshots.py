import asyncio
import os

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name

# A restore tears the running instance down and builds it back from the
# snapshot, so it costs a full sandbox start on top of taking the snapshot —
# past the one-minute budget of the default run.
pytestmark = pytest.mark.skipif(
    not os.environ.get("RUN_SLOW_TESTS"),
    reason="slow test; set RUN_SLOW_TESTS=1 to enable",
)


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxSnapshotRestore:
    """Restore a sandbox to one of its own snapshots."""

    name = unique_name("restore")

    @pytest_asyncio.fixture(autouse=True)
    async def cleanup(self):
        yield
        try:
            await SandboxInstance.delete(TestSandboxSnapshotRestore.name)
        except Exception:
            pass

    async def test_puts_the_filesystem_back_to_the_snapshot_it_restores(self):
        sandbox = await SandboxInstance.create(
            {
                "name": TestSandboxSnapshotRestore.name,
                "image": default_image,
                "labels": default_labels,
            }
        )
        await sandbox.fs.write("/blaxel/snapshotted.txt", "kept")

        snapshot = await sandbox.snapshot("restore-point")
        assert snapshot.id

        # Only a ready snapshot holds the filesystem it captured.
        for _ in range(60):
            snapshots = await sandbox.list_snapshots()
            if any(s.id == snapshot.id and s.status == "ready" for s in snapshots):
                break
            await asyncio.sleep(2)
        else:
            pytest.fail(f"snapshot {snapshot.id} never became ready")

        # Written after the snapshot: the restore is expected to lose it.
        await sandbox.fs.write("/blaxel/after-snapshot.txt", "lost")

        restored = await sandbox.restore(snapshot.id)
        assert restored.name == TestSandboxSnapshotRestore.name
        assert restored.snapshot_id == snapshot.id

        # The restore is asked for without waiting on the instance, so the
        # sandbox answers again only once it is back up.
        for _ in range(60):
            try:
                assert await sandbox.fs.read("/blaxel/snapshotted.txt") == "kept"
                break
            except Exception:
                await asyncio.sleep(2)
        else:
            pytest.fail("the restored sandbox never served its snapshotted filesystem")

        with pytest.raises(Exception):
            await sandbox.fs.read("/blaxel/after-snapshot.txt")

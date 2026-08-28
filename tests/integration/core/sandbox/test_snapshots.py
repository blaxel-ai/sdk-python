import asyncio
import os
import time

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import (
    default_image,
    default_labels,
    default_region,
    skip_unless_generation_mk31,
    unique_name,
)

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
        # Snapshots, and therefore restores, only exist on mk3.1 sandboxes.
        await skip_unless_generation_mk31("snapshots and restores")

        # Timed step by step: a restore is only ever as slow as one of create,
        # snapshot-ready or instance-back-up, and the logs must say which.
        started_at = time.monotonic()

        def step(label: str) -> None:
            print(f"[restore] {label} +{time.monotonic() - started_at:.1f}s")

        sandbox = await SandboxInstance.create(
            {
                "name": TestSandboxSnapshotRestore.name,
                "image": default_image,
                "region": default_region,
                "labels": default_labels,
            }
        )
        step("sandbox created")

        await sandbox.fs.write("/blaxel/snapshotted.txt", "kept")

        snapshot = await sandbox.snapshot("restore-point")
        assert snapshot.id
        step("snapshot asked for")

        # Only a ready snapshot holds the filesystem it captured.
        for _ in range(300):
            snapshots = await sandbox.list_snapshots()
            if any(s.id == snapshot.id and s.status == "ready" for s in snapshots):
                break
            await asyncio.sleep(0.25)
        else:
            pytest.fail(f"snapshot {snapshot.id} never became ready")
        step("snapshot ready")

        # Written after the snapshot: the restore is expected to lose it.
        await sandbox.fs.write("/blaxel/after-snapshot.txt", "lost")

        restored = await sandbox.restore(snapshot.id)
        assert restored.name == TestSandboxSnapshotRestore.name
        assert restored.snapshot_id == snapshot.id
        step("restore asked for")

        # The restore is asked for without waiting on the guest, so the sandbox
        # answers again only once its instance is back up. A read issued while
        # it is down is held open by the edge until its own minute-long
        # timeout, so each attempt is abandoned after a few seconds instead of
        # waiting on it.
        deadline = time.monotonic() + 45
        while True:
            try:
                content = await asyncio.wait_for(
                    sandbox.fs.read("/blaxel/snapshotted.txt"), timeout=3
                )
                assert content == "kept"
                break
            except Exception as err:
                failure = f"{type(err).__name__}: {err}" if str(err) else type(err).__name__
                # The record's status separates "the guest is still coming
                # back" from "the sandbox is up but the connection is stale".
                try:
                    status = (await SandboxInstance.get(TestSandboxSnapshotRestore.name)).status
                except Exception:
                    status = "unreadable"
                step(f"sandbox not back yet (record {status}): {failure}")
                if time.monotonic() >= deadline:
                    pytest.fail(
                        f"the restored sandbox never served its snapshotted filesystem: {failure}"
                    )
                await asyncio.sleep(0.5)
        step("sandbox back up on the snapshot")

        with pytest.raises(Exception):
            await sandbox.fs.read("/blaxel/after-snapshot.txt")

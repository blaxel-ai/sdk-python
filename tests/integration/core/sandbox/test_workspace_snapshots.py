import asyncio
import os

import pytest
import pytest_asyncio

from blaxel.core import Snapshot
from blaxel.core.sandbox import SandboxInstance
from tests.helpers import (
    default_image,
    default_labels,
    default_region,
    skip_unless_generation_mk31,
    unique_name,
    wait_for_sandbox_deletion,
)

# Taking a snapshot and waiting for it to be ready costs a sandbox start on top
# of the capture — past the one-minute budget of the default run.
pytestmark = pytest.mark.skipif(
    not os.environ.get("RUN_SLOW_TESTS"),
    reason="slow test; set RUN_SLOW_TESTS=1 to enable",
)


@pytest.mark.asyncio(loop_scope="class")
class TestWorkspaceSnapshots:
    """A snapshot is a workspace resource that outlives the sandbox it came from."""

    sandbox_name = unique_name("snap-src")
    snapshot_name = unique_name("snap")
    fork_name = unique_name("snap-fork")

    @pytest_asyncio.fixture(autouse=True)
    async def cleanup(self):
        yield
        for delete in (
            lambda: Snapshot.delete(TestWorkspaceSnapshots.snapshot_name),
            lambda: SandboxInstance.delete(TestWorkspaceSnapshots.sandbox_name),
            lambda: SandboxInstance.delete(TestWorkspaceSnapshots.fork_name),
        ):
            try:
                await delete()
            except Exception:
                pass

    async def test_keeps_a_snapshot_after_the_sandbox_it_was_captured_from_is_deleted(self):
        # Snapshots only exist on mk3.1 sandboxes.
        await skip_unless_generation_mk31("snapshots")

        sandbox = await SandboxInstance.create(
            {
                "name": TestWorkspaceSnapshots.sandbox_name,
                "image": default_image,
                "region": default_region,
                "labels": default_labels,
            }
        )

        snapshot = await sandbox.snapshots.create(TestWorkspaceSnapshots.snapshot_name)
        assert snapshot.name == TestWorkspaceSnapshots.snapshot_name
        assert snapshot.source.name == TestWorkspaceSnapshots.sandbox_name
        assert snapshot.source.kind == "sandbox"

        from_sandbox = await sandbox.snapshots.list()
        assert TestWorkspaceSnapshots.snapshot_name in [s.name for s in from_sandbox]

        from_workspace = await Snapshot.list(limit=200)
        names = [s.name async for s in from_workspace.auto_paging_iter()]
        assert TestWorkspaceSnapshots.snapshot_name in names

        # Only a ready snapshot holds the filesystem it captured, and only a
        # ready one is worth outliving its sandbox.
        for _ in range(300):
            if (await Snapshot.get(TestWorkspaceSnapshots.snapshot_name)).status == "ready":
                break
            await asyncio.sleep(0.25)
        else:
            pytest.fail(f"snapshot {TestWorkspaceSnapshots.snapshot_name} never became ready")

        await SandboxInstance.delete(TestWorkspaceSnapshots.sandbox_name)
        await wait_for_sandbox_deletion(TestWorkspaceSnapshots.sandbox_name)

        orphan = await Snapshot.get(TestWorkspaceSnapshots.snapshot_name)
        assert orphan.name == TestWorkspaceSnapshots.snapshot_name
        assert orphan.source.deleted is True
        # What a fork needs to run is on the snapshot itself, not on the source.
        assert orphan.spec.image

        # A fork of a sourceless snapshot is a full sandbox start on top of the
        # snapshot above, so it is asked for only when explicitly enabled.
        if not os.environ.get("RUN_SLOW_SNAPSHOT_FORK"):
            return

        fork = await orphan.fork(TestWorkspaceSnapshots.fork_name)
        assert fork.name == TestWorkspaceSnapshots.fork_name
        forked = await SandboxInstance.get(TestWorkspaceSnapshots.fork_name)
        assert forked.metadata.name == TestWorkspaceSnapshots.fork_name

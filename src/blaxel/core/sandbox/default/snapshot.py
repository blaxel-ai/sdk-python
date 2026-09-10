from ...client.api.compute.create_sandbox_snapshot import asyncio as create_sandbox_snapshot
from ...client.api.compute.delete_sandbox_snapshot import asyncio as delete_sandbox_snapshot
from ...client.api.compute.list_sandbox_snapshots import asyncio as list_sandbox_snapshots
from ...client.api.compute.restore_sandbox_snapshot import asyncio as restore_sandbox_snapshot
from ...client.client import client
from ...client.models import Sandbox, SandboxRestoreResponse, SandboxSnapshotRequest
from ...snapshot import Snapshot


class SandboxSnapshots:
    """The snapshots captured from a sandbox.

    These are the same workspace snapshot objects ``Snapshot`` addresses: they
    stay after this sandbox is deleted, and deleting one here removes it for
    the whole workspace.
    """

    def __init__(self, sandbox: Sandbox, unwrap):
        self._sandbox = sandbox
        self._unwrap = unwrap

    @property
    def _sandbox_name(self) -> str:
        return self._sandbox.metadata.name

    async def create(self, name: str | None = None) -> Snapshot:
        """Capture a snapshot of this sandbox.

        Args:
            name: Name of the snapshot. Generated when omitted.
        """
        body = SandboxSnapshotRequest(name=name) if name is not None else SandboxSnapshotRequest()
        response = await create_sandbox_snapshot(self._sandbox_name, client=client, body=body)
        return Snapshot(self._unwrap(response, "create snapshot"))

    async def list(self) -> list[Snapshot]:
        """List the snapshots captured from this sandbox."""
        response = await list_sandbox_snapshots(self._sandbox_name, client=client)
        snapshots = self._unwrap(response, "list snapshots")
        return [Snapshot(snapshot) for snapshot in snapshots]

    async def get(self, snapshot_name: str) -> Snapshot:
        """Read one snapshot by name."""
        return await Snapshot.get(snapshot_name)

    async def delete(self, snapshot_name: str) -> None:
        """Delete a snapshot, removing it for the whole workspace."""
        response = await delete_sandbox_snapshot(self._sandbox_name, snapshot_name, client=client)
        self._unwrap(response, "delete snapshot", allow_none=True)

    async def restore(self, snapshot_name: str) -> SandboxRestoreResponse:
        """Restore this sandbox to one of its snapshots.

        The sandbox keeps its name, its URLs and its previews: the running
        instance is torn down and rebuilt from the snapshot, so everything
        written since the snapshot was taken is lost unless it was snapshotted
        too.
        """
        response = await restore_sandbox_snapshot(self._sandbox_name, snapshot_name, client=client)
        return self._unwrap(response, "restore snapshot")

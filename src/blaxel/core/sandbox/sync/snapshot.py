from ...client.api.compute.create_sandbox_snapshot import sync as create_sandbox_snapshot
from ...client.api.compute.delete_sandbox_snapshot import sync as delete_sandbox_snapshot
from ...client.api.compute.list_sandbox_snapshots import sync as list_sandbox_snapshots
from ...client.api.compute.restore_sandbox_snapshot import sync as restore_sandbox_snapshot
from ...client.client import client
from ...client.models import Sandbox, SandboxRestoreResponse, SandboxSnapshotRequest
from ...snapshot import SyncSnapshot


class SyncSandboxSnapshots:
    """The snapshots captured from a sandbox.

    These are the same workspace snapshot objects ``SyncSnapshot`` addresses:
    they stay after this sandbox is deleted, and deleting one here removes it
    for the whole workspace.
    """

    def __init__(self, sandbox: Sandbox, unwrap):
        self._sandbox = sandbox
        self._unwrap = unwrap

    @property
    def _sandbox_name(self) -> str:
        return self._sandbox.metadata.name

    def create(self, name: str | None = None) -> SyncSnapshot:
        """Capture a snapshot of this sandbox.

        Args:
            name: Name of the snapshot. Generated when omitted.
        """
        body = SandboxSnapshotRequest(name=name) if name is not None else SandboxSnapshotRequest()
        response = create_sandbox_snapshot(self._sandbox_name, client=client, body=body)
        return SyncSnapshot(self._unwrap(response, "create snapshot"))

    def list(self) -> list[SyncSnapshot]:
        """List the snapshots captured from this sandbox."""
        response = list_sandbox_snapshots(self._sandbox_name, client=client)
        snapshots = self._unwrap(response, "list snapshots")
        return [SyncSnapshot(snapshot) for snapshot in snapshots]

    def get(self, snapshot_name: str) -> SyncSnapshot:
        """Read one snapshot by name."""
        return SyncSnapshot.get(snapshot_name)

    def delete(self, snapshot_name: str) -> None:
        """Delete a snapshot, removing it for the whole workspace."""
        response = delete_sandbox_snapshot(self._sandbox_name, snapshot_name, client=client)
        self._unwrap(response, "delete snapshot", allow_none=True)

    def restore(self, snapshot_name: str) -> SandboxRestoreResponse:
        """Restore this sandbox to one of its snapshots.

        The sandbox keeps its name, its URLs and its previews: the running
        instance is torn down and rebuilt from the snapshot, so everything
        written since the snapshot was taken is lost unless it was snapshotted
        too.
        """
        response = restore_sandbox_snapshot(self._sandbox_name, snapshot_name, client=client)
        return self._unwrap(response, "restore snapshot")

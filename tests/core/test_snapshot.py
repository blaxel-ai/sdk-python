"""Tests for workspace-level snapshots and the sandbox snapshots sub-resource."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from blaxel.core import Snapshot
from blaxel.core.client.models import (
    Metadata,
    PaginationMeta,
    Sandbox,
    SandboxSnapshot,
    SandboxSnapshotList,
    SandboxSnapshotSource,
    SandboxSpec,
)
from blaxel.core.sandbox import SandboxInstance


def snapshot_model(name: str = "my-snapshot") -> SandboxSnapshot:
    return SandboxSnapshot(
        id="snap_abc123",
        name=name,
        status="ready",
        workspace="my-workspace",
        created_at="2026-01-01T00:00:00Z",
        source=SandboxSnapshotSource(name="my-sandbox"),
    )


def sandbox_instance(name: str = "my-sandbox") -> SandboxInstance:
    return SandboxInstance(Sandbox(metadata=Metadata(name=name), spec=SandboxSpec()))


@pytest.mark.asyncio
async def test_create_requires_a_source_name():
    with pytest.raises(ValueError):
        await Snapshot.create({"name": "my-snapshot", "source": {}})


@pytest.mark.asyncio
async def test_create_omits_the_kind_when_it_is_not_given():
    with patch(
        "blaxel.core.snapshot.snapshot.create_snapshot", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = snapshot_model()

        snapshot = await Snapshot.create({"name": "my-snapshot", "source": {"name": "my-sandbox"}})

        body = mock_create.call_args.kwargs["body"]
        assert body.name == "my-snapshot"
        assert body.source.name == "my-sandbox"
        # The control plane defaults an unset kind to sandbox.
        assert "kind" not in body.to_dict()["source"]
        assert snapshot.name == "my-snapshot"
        assert snapshot.id == "snap_abc123"


@pytest.mark.asyncio
async def test_create_forwards_an_explicit_kind_and_generates_the_name_when_omitted():
    with patch(
        "blaxel.core.snapshot.snapshot.create_snapshot", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = snapshot_model()

        await Snapshot.create({"source": {"name": "my-sandbox", "kind": "sandbox"}})

        body = mock_create.call_args.kwargs["body"]
        assert body.to_dict()["source"]["kind"] == "sandbox"
        assert "name" not in body.to_dict()


@pytest.mark.asyncio
async def test_get_addresses_a_snapshot_by_name():
    with patch("blaxel.core.snapshot.snapshot.get_snapshot", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = snapshot_model()

        snapshot = await Snapshot.get("my-snapshot")

        assert mock_get.call_args.args[0] == "my-snapshot"
        assert snapshot.source.name == "my-sandbox"


@pytest.mark.asyncio
async def test_list_returns_a_page_of_snapshots():
    with patch("blaxel.core.snapshot.snapshot.list_snapshots", new_callable=AsyncMock) as mock_list:
        mock_list.return_value = SandboxSnapshotList(
            data=[snapshot_model("first"), snapshot_model("second")],
            meta=PaginationMeta(has_more=False),
        )

        page = await Snapshot.list(limit=2)

        assert mock_list.call_args.kwargs["limit"] == 2
        assert [snapshot.name for snapshot in page.data] == ["first", "second"]
        assert all(isinstance(snapshot, Snapshot) for snapshot in page.data)
        assert page.has_more is False


@pytest.mark.asyncio
async def test_delete_works_from_the_class_and_from_an_instance():
    with patch(
        "blaxel.core.snapshot.snapshot.delete_snapshot", new_callable=AsyncMock
    ) as mock_delete:
        # A successful delete answers 204 No Content, hence None.
        mock_delete.return_value = None

        await Snapshot.delete("my-snapshot")
        assert mock_delete.call_args.args[0] == "my-snapshot"

        await Snapshot(snapshot_model("other")).delete()
        assert mock_delete.call_args.args[0] == "other"


@pytest.mark.asyncio
async def test_fork_forwards_the_target_and_its_options():
    with patch("blaxel.core.snapshot.snapshot.fork_snapshot", new_callable=AsyncMock) as mock_fork:
        mock_fork.return_value = MagicMock()

        snapshot = Snapshot(snapshot_model())
        await snapshot.fork(
            "my-app",
            target_type="application",
            port=8080,
            traffic=100,
            custom_domain="app.example.com",
            prefix="preview",
        )

        assert mock_fork.call_args.args[0] == "my-snapshot"
        body = mock_fork.call_args.kwargs["body"]
        assert body.target_name == "my-app"
        assert body.target_type == "application"
        assert body.port == 8080
        assert body.traffic == 100
        assert body.custom_domain == "app.example.com"
        assert body.prefix == "preview"


@pytest.mark.asyncio
async def test_fork_defaults_to_a_sandbox_target():
    with patch("blaxel.core.snapshot.snapshot.fork_snapshot", new_callable=AsyncMock) as mock_fork:
        mock_fork.return_value = MagicMock()

        await Snapshot(snapshot_model()).fork("my-sandbox-copy")

        body = mock_fork.call_args.kwargs["body"]
        assert body.target_name == "my-sandbox-copy"
        assert body.target_type == "sandbox"


@pytest.mark.asyncio
async def test_sandbox_snapshots_create_and_list_answer_snapshots():
    sandbox = sandbox_instance()

    with patch(
        "blaxel.core.sandbox.default.snapshot.create_sandbox_snapshot", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = snapshot_model()

        snapshot = await sandbox.snapshots.create("my-snapshot")

        assert mock_create.call_args.args[0] == "my-sandbox"
        assert mock_create.call_args.kwargs["body"].name == "my-snapshot"
        assert isinstance(snapshot, Snapshot)

    with patch(
        "blaxel.core.sandbox.default.snapshot.list_sandbox_snapshots", new_callable=AsyncMock
    ) as mock_list:
        mock_list.return_value = [snapshot_model("first")]

        snapshots = await sandbox.snapshots.list()

        assert mock_list.call_args.args[0] == "my-sandbox"
        assert [snapshot.name for snapshot in snapshots] == ["first"]


@pytest.mark.asyncio
async def test_sandbox_snapshots_delete_and_restore_use_the_sandbox_routes():
    sandbox = sandbox_instance()

    with patch(
        "blaxel.core.sandbox.default.snapshot.delete_sandbox_snapshot", new_callable=AsyncMock
    ) as mock_delete:
        mock_delete.return_value = None

        await sandbox.snapshots.delete("my-snapshot")

        assert mock_delete.call_args.args == ("my-sandbox", "my-snapshot")

    with patch(
        "blaxel.core.sandbox.default.snapshot.restore_sandbox_snapshot", new_callable=AsyncMock
    ) as mock_restore:
        mock_restore.return_value = MagicMock()

        await sandbox.snapshots.restore("my-snapshot")

        assert mock_restore.call_args.args == ("my-sandbox", "my-snapshot")


@pytest.mark.asyncio
async def test_sandbox_snapshots_get_reads_the_workspace_snapshot():
    sandbox = sandbox_instance()

    with patch("blaxel.core.snapshot.snapshot.get_snapshot", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = snapshot_model()

        snapshot = await sandbox.snapshots.get("my-snapshot")

        assert mock_get.call_args.args[0] == "my-snapshot"
        assert isinstance(snapshot, Snapshot)

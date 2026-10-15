"""Tests for workspace-level snapshots and the sandbox snapshots sub-resource."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from blaxel.core import Snapshot
from blaxel.core.client.models import (
    Env,
    Metadata,
    PaginationMeta,
    Sandbox,
    SandboxSnapshot,
    SandboxSnapshotList,
    SandboxSnapshotRequest,
    SandboxSnapshotSource,
    SandboxSpec,
)
from blaxel.core.sandbox import SandboxInstance
from blaxel.core.snapshot import SyncSnapshot


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
async def test_create_validates_typed_requests_like_mappings():
    with pytest.raises(ValueError):
        await Snapshot.create(SandboxSnapshotRequest())
    with pytest.raises(ValueError):
        await Snapshot.create(SandboxSnapshotRequest(source=SandboxSnapshotSource(name="")))
    with pytest.raises(ValueError):
        await Snapshot.create({"source": SandboxSnapshotSource(name="")})

    with patch(
        "blaxel.core.snapshot.snapshot.create_snapshot", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = snapshot_model()
        request = SandboxSnapshotRequest(source=SandboxSnapshotSource(name="my-sandbox"))

        await Snapshot.create(request)

        assert mock_create.call_args.kwargs["body"] is request


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
async def test_get_addresses_a_snapshot_by_id():
    with patch("blaxel.core.snapshot.snapshot.get_snapshot", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = snapshot_model()

        snapshot = await Snapshot.get("snap_abc123")

        assert mock_get.call_args.args[0] == "snap_abc123"
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
async def test_list_answers_an_empty_page_when_the_body_is_an_empty_array():
    # Before the workspace-level routes, a listing was a bare array, so a
    # workspace without snapshots answers `[]`, which the model parses to None.
    with patch("blaxel.core.snapshot.snapshot.list_snapshots", new_callable=AsyncMock) as mock_list:
        mock_list.return_value = SandboxSnapshotList.from_dict([])

        page = await Snapshot.list()

        assert page.data == []
        assert page.has_more is False

    with patch("blaxel.core.snapshot.snapshot.list_snapshots_sync") as mock_list_sync:
        mock_list_sync.return_value = SandboxSnapshotList.from_dict([])

        assert SyncSnapshot.list().data == []


@pytest.mark.asyncio
async def test_delete_works_from_the_class_and_from_an_instance():
    with patch(
        "blaxel.core.snapshot.snapshot.delete_snapshot", new_callable=AsyncMock
    ) as mock_delete:
        # A successful delete answers 204 No Content, hence None.
        mock_delete.return_value = None

        await Snapshot.delete("snap_abc123")
        assert mock_delete.call_args.args[0] == "snap_abc123"

        # An instance is addressed by id, never by its per-sandbox name.
        await Snapshot(snapshot_model("other")).delete()
        assert mock_delete.call_args.args[0] == "snap_abc123"


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

        assert mock_fork.call_args.args[0] == "snap_abc123"
        body = mock_fork.call_args.kwargs["body"]
        assert body.target_name == "my-app"
        assert body.target_type == "application"
        assert body.port == 8080
        assert body.traffic == 100
        assert body.custom_domain == "app.example.com"
        assert body.prefix == "preview"


@pytest.mark.asyncio
async def test_fork_forwards_envs_as_models_or_mappings():
    with patch("blaxel.core.snapshot.snapshot.fork_snapshot", new_callable=AsyncMock) as mock_fork:
        mock_fork.return_value = MagicMock()

        await Snapshot(snapshot_model()).fork(
            "copy", envs=[{"name": "FOO", "value": "bar"}, Env(name="BAZ", value="qux")]
        )

        body = mock_fork.call_args.kwargs["body"].to_dict()
        assert body["envs"] == [{"name": "FOO", "value": "bar"}, {"name": "BAZ", "value": "qux"}]


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
async def test_sandbox_snapshots_get_resolves_a_name_or_id_among_the_sandbox_snapshots():
    sandbox = sandbox_instance()

    with patch(
        "blaxel.core.sandbox.default.snapshot.list_sandbox_snapshots", new_callable=AsyncMock
    ) as mock_list:
        mock_list.return_value = [snapshot_model()]

        by_name = await sandbox.snapshots.get("my-snapshot")
        by_id = await sandbox.snapshots.get("snap_abc123")

        assert mock_list.call_args.args[0] == "my-sandbox"
        assert isinstance(by_name, Snapshot)
        assert by_name.id == "snap_abc123"
        assert by_id.name == "my-snapshot"
        with pytest.raises(ValueError):
            await sandbox.snapshots.get("unknown")

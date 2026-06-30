"""Integration tests for per-drive ACL enforcement (ENG-2761).

Exercises the full DrivePermission enforcement matrix:
  - open-access (no permissions = allow all)
  - label-match / label-mismatch
  - read-only mode
  - multiple permissions (OR logic)
  - AND logic within a single permission
  - path scoping
  - update permissions on existing drive
  - wildcard permission (empty labels = match all)

Prerequisites: all ENG-2761 PRs deployed (controlplane#4582, seaweedfs#27,
executionplane#171).
"""

import asyncio
import os

import pytest
import pytest_asyncio

from blaxel.core.client.models import Drive, DriveSpec, Metadata, MetadataLabels
from blaxel.core.client.models.drive_permission import DrivePermission
from blaxel.core.client.models.drive_permission_labels import DrivePermissionLabels
from blaxel.core.client.models.drive_permission_mode import DrivePermissionMode
from blaxel.core.client.types import UNSET
from blaxel.core.drive import DriveInstance
from blaxel.core.sandbox import SandboxInstance
from tests.helpers import (
    default_image,
    default_labels,
    unique_name,
    wait_for_sandbox_deletion,
)

default_region = "eu-dub-1" if os.environ.get("BL_ENV") == "dev" else "us-was-1"

MOUNT_SETTLE_S = 3


def _make_permissions(perms: list[dict]) -> list[DrivePermission]:
    result = []
    for p in perms:
        raw_labels = p.get("labels", {})
        if raw_labels:
            labels = DrivePermissionLabels.from_dict(raw_labels)
        else:
            labels = DrivePermissionLabels()
        mode = DrivePermissionMode(p.get("mode", "read-write"))
        path = p.get("path", UNSET)
        result.append(DrivePermission(labels=labels, mode=mode, path=path))
    return result


async def _create_drive_with_permissions(name: str, permissions: list[dict]) -> DriveInstance:
    drive = Drive(
        metadata=Metadata(
            name=name,
            labels=MetadataLabels.from_dict(default_labels),
        ),
        spec=DriveSpec(
            region=default_region,
            size=1,
            permissions=_make_permissions(permissions),
        ),
    )
    return await DriveInstance.create(drive)


async def _create_sandbox(name: str, labels: dict[str, str]) -> SandboxInstance:
    return await SandboxInstance.create(
        {
            "name": name,
            "image": default_image,
            "memory": 2048,
            "region": default_region,
            "labels": {**default_labels, **labels},
        },
        safe=True,
    )


async def _exec(sbx: SandboxInstance, command: str) -> tuple[bool, str]:
    try:
        result = await asyncio.wait_for(
            sbx.process.exec({"command": command, "wait_for_completion": True}),
            timeout=30,
        )
        return (True, result.logs or "")
    except Exception as err:
        return (False, str(err))


async def _update_drive_permissions(drive_name: str, permissions: list[dict]) -> None:
    drive_permissions = _make_permissions(permissions)
    await DriveInstance.update(
        drive_name,
        Drive(
            metadata=Metadata(name=drive_name),
            spec=DriveSpec(permissions=drive_permissions),
        ),
    )


def _is_acl_denial(msg: str) -> bool:
    return any(
        s in msg for s in ("timeout", "denied", "Permission", "exited unexpectedly: exit status 2")
    )


class _DriveACLBase:
    """Base class with cleanup tracking for drive ACL tests."""

    created_sandboxes: list[str] = []
    created_drives: list[str] = []

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def cleanup(self, request):
        request.cls.created_sandboxes = []
        request.cls.created_drives = []
        yield
        await asyncio.gather(
            *[self._safe_delete_sandbox(n) for n in request.cls.created_sandboxes],
            return_exceptions=True,
        )
        await asyncio.gather(
            *[self._safe_delete_drive(n) for n in request.cls.created_drives],
            return_exceptions=True,
        )

    async def _safe_delete_sandbox(self, name: str) -> None:
        try:
            await SandboxInstance.delete(name)
            await wait_for_sandbox_deletion(name)
        except Exception:
            pass

    async def _safe_delete_drive(self, name: str) -> None:
        try:
            await DriveInstance.delete(name)
        except Exception:
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestDriveACLOpenAccess(_DriveACLBase):
    """Drive with NO permissions (empty array) -- any sandbox can access."""

    async def test_open_access_write_and_read(self):
        drive_name = unique_name("acl-open")
        sbx_name = unique_name("acl-open-sbx")

        await _create_drive_with_permissions(drive_name, [])
        self.created_drives.append(drive_name)

        sbx = await _create_sandbox(sbx_name, {"role": "anything"})
        self.created_sandboxes.append(sbx_name)

        await sbx.drives.mount(drive_name, "/mnt/open")
        await asyncio.sleep(MOUNT_SETTLE_S)

        ok, logs = await _exec(sbx, "echo 'open-access-ok' > /mnt/open/test.txt")
        assert ok, f"write failed: {logs}"

        ok, logs = await _exec(sbx, "cat /mnt/open/test.txt")
        assert ok and "open-access-ok" in logs


@pytest.mark.asyncio(loop_scope="class")
class TestDriveACLLabelMatch(_DriveACLBase):
    """Drive with label-based permission -- matching sandbox gets access."""

    async def test_label_match_write_and_read(self):
        drive_name = unique_name("acl-match")
        sbx_name = unique_name("acl-match-sbx")

        await _create_drive_with_permissions(
            drive_name,
            [
                {"labels": {"team": "backend", "project": "acl-test"}, "mode": "read-write"},
            ],
        )
        self.created_drives.append(drive_name)

        sbx = await _create_sandbox(sbx_name, {"team": "backend", "project": "acl-test"})
        self.created_sandboxes.append(sbx_name)

        await sbx.drives.mount(drive_name, "/mnt/match")
        await asyncio.sleep(MOUNT_SETTLE_S)

        ok, logs = await _exec(sbx, "echo 'label-match-ok' > /mnt/match/test.txt")
        assert ok, f"write failed: {logs}"

        ok, logs = await _exec(sbx, "cat /mnt/match/test.txt")
        assert ok and "label-match-ok" in logs


@pytest.mark.asyncio(loop_scope="class")
class TestDriveACLLabelMismatch(_DriveACLBase):
    """Drive with label-based permission -- non-matching sandbox is denied."""

    async def test_label_mismatch_denied(self):
        drive_name = unique_name("acl-mis")
        sbx_name = unique_name("acl-mis-sbx")

        await _create_drive_with_permissions(
            drive_name,
            [
                {"labels": {"team": "secret-team"}, "mode": "read-write"},
            ],
        )
        self.created_drives.append(drive_name)

        sbx = await _create_sandbox(sbx_name, {"team": "other"})
        self.created_sandboxes.append(sbx_name)

        try:
            await sbx.drives.mount(drive_name, "/mnt/mis")
            await asyncio.sleep(MOUNT_SETTLE_S)
            ok, logs = await _exec(sbx, "echo 'should-fail' > /mnt/mis/test.txt")
            assert not ok, f"write should have been denied but succeeded: {logs}"
        except Exception as err:
            assert _is_acl_denial(str(err)), f"unexpected error (not ACL denial): {err}"


@pytest.mark.asyncio(loop_scope="class")
class TestDriveACLReadOnly(_DriveACLBase):
    """Read-only mode: matching sandbox can read but NOT write."""

    async def test_read_only_blocks_writes(self):
        drive_name = unique_name("acl-ro")
        writer_name = unique_name("acl-ro-writer")
        reader_name = unique_name("acl-ro-reader")

        await _create_drive_with_permissions(
            drive_name,
            [
                {"labels": {"role": "reader"}, "mode": "read"},
                {"labels": {"role": "writer"}, "mode": "read-write"},
            ],
        )
        self.created_drives.append(drive_name)

        # Writer seeds data
        writer = await _create_sandbox(writer_name, {"role": "writer"})
        self.created_sandboxes.append(writer_name)
        await writer.drives.mount(drive_name, "/mnt/ro")
        await asyncio.sleep(MOUNT_SETTLE_S)

        ok, logs = await _exec(writer, "echo 'read-only-test-data' > /mnt/ro/readonly.txt")
        assert ok, f"seed write failed: {logs}"

        # Reader mounts read-only
        reader = await _create_sandbox(reader_name, {"role": "reader"})
        self.created_sandboxes.append(reader_name)
        await reader.drives.mount(drive_name, "/mnt/ro", read_only=True)
        await asyncio.sleep(MOUNT_SETTLE_S)

        ok, logs = await _exec(reader, "cat /mnt/ro/readonly.txt")
        assert ok and "read-only-test-data" in logs, f"read failed: {logs}"

        ok, logs = await _exec(reader, "echo 'should-fail' > /mnt/ro/illegal.txt")
        assert not ok or any(s in logs for s in ("denied", "Read-only", "Permission", "error")), (
            f"write should have been denied: {logs}"
        )


@pytest.mark.asyncio(loop_scope="class")
class TestDriveACLMultiplePermissionsOR(_DriveACLBase):
    """Two permissions with OR logic -- second rule match grants access."""

    async def test_or_logic_second_rule_matches(self):
        drive_name = unique_name("acl-or")
        sbx_name = unique_name("acl-or-sbx")

        await _create_drive_with_permissions(
            drive_name,
            [
                {"labels": {"team": "alpha"}, "mode": "read-write"},
                {"labels": {"team": "beta"}, "mode": "read-write"},
            ],
        )
        self.created_drives.append(drive_name)

        sbx = await _create_sandbox(sbx_name, {"team": "beta"})
        self.created_sandboxes.append(sbx_name)

        await sbx.drives.mount(drive_name, "/mnt/or")
        await asyncio.sleep(MOUNT_SETTLE_S)

        ok, logs = await _exec(sbx, "echo 'or-logic-ok' > /mnt/or/test.txt")
        assert ok, f"write failed: {logs}"

        ok, logs = await _exec(sbx, "cat /mnt/or/test.txt")
        assert ok and "or-logic-ok" in logs


@pytest.mark.asyncio(loop_scope="class")
class TestDriveACLANDLogic(_DriveACLBase):
    """AND logic within a single permission -- all labels must match."""

    async def test_partial_label_match_denied(self):
        drive_name = unique_name("acl-and")
        sbx_name = unique_name("acl-and-partial")

        await _create_drive_with_permissions(
            drive_name,
            [
                {"labels": {"team": "core", "tier": "staging"}, "mode": "read-write"},
            ],
        )
        self.created_drives.append(drive_name)

        # Partial match: has team=core but NOT tier=staging
        partial = await _create_sandbox(sbx_name, {"team": "core"})
        self.created_sandboxes.append(sbx_name)

        try:
            await partial.drives.mount(drive_name, "/mnt/and")
            await asyncio.sleep(MOUNT_SETTLE_S)
            ok, logs = await _exec(partial, "echo 'should-fail' > /mnt/and/test.txt")
            assert not ok, f"write should have been denied: {logs}"
        except Exception as err:
            assert _is_acl_denial(str(err)), f"unexpected error: {err}"

    async def test_full_label_match_allowed(self):
        drive_name = unique_name("acl-and-f")
        sbx_name = unique_name("acl-and-full")

        await _create_drive_with_permissions(
            drive_name,
            [
                {"labels": {"team": "core", "tier": "staging"}, "mode": "read-write"},
            ],
        )
        self.created_drives.append(drive_name)

        full = await _create_sandbox(sbx_name, {"team": "core", "tier": "staging"})
        self.created_sandboxes.append(sbx_name)

        await full.drives.mount(drive_name, "/mnt/and")
        await asyncio.sleep(MOUNT_SETTLE_S)

        ok, logs = await _exec(full, "echo 'and-logic-ok' > /mnt/and/test.txt")
        assert ok, f"write failed: {logs}"


@pytest.mark.asyncio(loop_scope="class")
class TestDriveACLPathScoping(_DriveACLBase):
    """Permission restricts access to /data/ subfolder."""

    async def test_scoped_sandbox_reads_subfolder_only(self):
        drive_name = unique_name("acl-path")
        admin_name = unique_name("acl-path-admin")
        scoped_name = unique_name("acl-path-scoped")

        await _create_drive_with_permissions(
            drive_name,
            [
                {"labels": {"role": "admin"}, "mode": "read-write", "path": "/"},
                {"labels": {"role": "scoped"}, "mode": "read-write", "path": "/data"},
            ],
        )
        self.created_drives.append(drive_name)

        # Admin seeds data
        admin = await _create_sandbox(admin_name, {"role": "admin"})
        self.created_sandboxes.append(admin_name)
        await admin.drives.mount(drive_name, "/mnt/path")
        await asyncio.sleep(MOUNT_SETTLE_S)

        await _exec(admin, "echo 'root-secret' > /mnt/path/secret.txt")
        await _exec(admin, "mkdir -p /mnt/path/data && echo 'data-ok' > /mnt/path/data/file.txt")

        # Scoped sandbox mounts only /data
        scoped = await _create_sandbox(scoped_name, {"role": "scoped"})
        self.created_sandboxes.append(scoped_name)
        await scoped.drives.mount(drive_name, "/mnt/scoped", drive_path="/data")
        await asyncio.sleep(MOUNT_SETTLE_S)

        ok, logs = await _exec(scoped, "cat /mnt/scoped/file.txt")
        assert ok and "data-ok" in logs, f"read /data failed: {logs}"

        ok, logs = await _exec(scoped, "cat /mnt/scoped/secret.txt")
        assert not ok or "No such file" in logs, f"root file should not be visible: {logs}"


@pytest.mark.asyncio(loop_scope="class")
class TestDriveACLUpdatePermissions(_DriveACLBase):
    """Update permissions on an existing drive, verify enforcement changes."""

    async def test_update_permissions_restricts_access(self):
        drive_name = unique_name("acl-upd")
        sbx_open_name = unique_name("acl-upd-open")
        sbx_denied_name = unique_name("acl-upd-denied")
        sbx_allowed_name = unique_name("acl-upd-allowed")

        # Step 1: open access
        await _create_drive_with_permissions(drive_name, [])
        self.created_drives.append(drive_name)

        sbx_open = await _create_sandbox(sbx_open_name, {"role": "tester"})
        self.created_sandboxes.append(sbx_open_name)
        await sbx_open.drives.mount(drive_name, "/mnt/upd")
        await asyncio.sleep(MOUNT_SETTLE_S)

        ok, _ = await _exec(sbx_open, "echo 'before-update' > /mnt/upd/test.txt")
        assert ok, "write before restriction failed"

        # Step 2: restrict to team=restricted
        await _update_drive_permissions(
            drive_name,
            [
                {"labels": {"team": "restricted"}, "mode": "read-write"},
            ],
        )

        # Step 3: verify persisted
        updated = await DriveInstance.get(drive_name)
        perms = updated.spec.permissions if updated.spec else None
        assert perms is not None and len(perms) == 1
        assert perms[0].labels is not None
        assert perms[0].labels.additional_properties.get("team") == "restricted"

        # Step 4: denied without label
        sbx_denied = await _create_sandbox(sbx_denied_name, {"team": "other"})
        self.created_sandboxes.append(sbx_denied_name)
        try:
            await sbx_denied.drives.mount(drive_name, "/mnt/upd")
            await asyncio.sleep(MOUNT_SETTLE_S)
            ok, logs = await _exec(sbx_denied, "echo 'should-fail' > /mnt/upd/test.txt")
            assert not ok, f"write should have been denied: {logs}"
        except Exception as err:
            assert _is_acl_denial(str(err)), f"unexpected error: {err}"

        # Step 5: allowed with label
        sbx_allowed = await _create_sandbox(sbx_allowed_name, {"team": "restricted"})
        self.created_sandboxes.append(sbx_allowed_name)
        await sbx_allowed.drives.mount(drive_name, "/mnt/upd")
        await asyncio.sleep(MOUNT_SETTLE_S)

        ok, logs = await _exec(sbx_allowed, "echo 'after-update-ok' > /mnt/upd/test2.txt")
        assert ok, f"write with correct labels failed: {logs}"

        ok, logs = await _exec(sbx_allowed, "cat /mnt/upd/test2.txt")
        assert ok and "after-update-ok" in logs


@pytest.mark.asyncio(loop_scope="class")
class TestDriveACLWildcard(_DriveACLBase):
    """Wildcard permission (empty labels = match all workloads)."""

    async def test_wildcard_permission_allows_all(self):
        drive_name = unique_name("acl-wild")
        sbx_name = unique_name("acl-wild-sbx")

        await _create_drive_with_permissions(
            drive_name,
            [
                {"labels": {}, "mode": "read-write"},
            ],
        )
        self.created_drives.append(drive_name)

        sbx = await _create_sandbox(sbx_name, {"random": "anything"})
        self.created_sandboxes.append(sbx_name)

        await sbx.drives.mount(drive_name, "/mnt/wild")
        await asyncio.sleep(MOUNT_SETTLE_S)

        ok, logs = await _exec(sbx, "echo 'wildcard-ok' > /mnt/wild/test.txt")
        assert ok, f"write failed: {logs}"

        ok, logs = await _exec(sbx, "cat /mnt/wild/test.txt")
        assert ok and "wildcard-ok" in logs

"""Tests for DriveInstance permissions support."""

from unittest.mock import AsyncMock, patch

import pytest

from blaxel.core.client.models import Drive, DrivePermission, DriveSpec, Metadata
from blaxel.core.client.models.drive_permission_labels import DrivePermissionLabels
from blaxel.core.client.models.drive_permission_mode import DrivePermissionMode
from blaxel.core.client.types import UNSET
from blaxel.core.drive.drive import (
    DriveCreateConfiguration,
    DriveInstance,
    SyncDriveInstance,
)


def make_permission(mode="read-write", path="/", labels=None):
    return DrivePermission(
        mode=DrivePermissionMode(mode),
        path=path,
        labels=DrivePermissionLabels.from_dict(labels or {}),
    )


SAMPLE_PERMISSIONS = [
    make_permission(mode="read-write", path="/data", labels={"app": "worker"}),
    make_permission(mode="read", path="/"),
]


class TestDriveCreateConfiguration:
    def test_permissions_field_default_none(self):
        config = DriveCreateConfiguration(name="d1")
        assert config.permissions is None

    def test_permissions_field_set(self):
        config = DriveCreateConfiguration(name="d1", permissions=SAMPLE_PERMISSIONS)
        assert config.permissions is SAMPLE_PERMISSIONS

    def test_from_dict_with_permissions(self):
        config = DriveCreateConfiguration.from_dict(
            {"name": "d1", "permissions": SAMPLE_PERMISSIONS}
        )
        assert config.permissions is SAMPLE_PERMISSIONS

    def test_from_dict_without_permissions(self):
        config = DriveCreateConfiguration.from_dict({"name": "d1"})
        assert config.permissions is None


class TestDriveInstancePermissionsProperty:
    def test_permissions_from_spec(self):
        drive = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(permissions=SAMPLE_PERMISSIONS),
        )
        instance = DriveInstance(drive)
        assert instance.permissions is SAMPLE_PERMISSIONS

    def test_permissions_none_when_no_spec(self):
        drive = Drive(metadata=Metadata(name="d1"), spec=DriveSpec())
        drive.spec = None
        instance = DriveInstance(drive)
        assert instance.permissions is None


class TestSyncDriveInstancePermissionsProperty:
    def test_permissions_from_spec(self):
        drive = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(permissions=SAMPLE_PERMISSIONS),
        )
        instance = SyncDriveInstance(drive)
        assert instance.permissions is SAMPLE_PERMISSIONS

    def test_permissions_none_when_no_spec(self):
        drive = Drive(metadata=Metadata(name="d1"), spec=DriveSpec())
        drive.spec = None
        instance = SyncDriveInstance(drive)
        assert instance.permissions is None


@pytest.mark.asyncio
class TestDriveCreateWithPermissions:
    @patch("blaxel.core.drive.drive.create_drive", new_callable=AsyncMock)
    async def test_create_with_dict_config_permissions(self, mock_create):
        returned_drive = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(permissions=SAMPLE_PERMISSIONS, region="us-pdx-1"),
        )
        mock_create.return_value = returned_drive

        result = await DriveInstance.create(
            {"name": "d1", "region": "us-pdx-1", "permissions": SAMPLE_PERMISSIONS}
        )

        assert isinstance(result, DriveInstance)
        body = mock_create.call_args.kwargs["body"]
        assert body.spec.permissions is SAMPLE_PERMISSIONS

    @patch("blaxel.core.drive.drive.create_drive", new_callable=AsyncMock)
    async def test_create_with_config_object_permissions(self, mock_create):
        returned_drive = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(permissions=SAMPLE_PERMISSIONS, region="us-pdx-1"),
        )
        mock_create.return_value = returned_drive

        config = DriveCreateConfiguration(
            name="d1", region="us-pdx-1", permissions=SAMPLE_PERMISSIONS
        )
        result = await DriveInstance.create(config)

        assert isinstance(result, DriveInstance)
        body = mock_create.call_args.kwargs["body"]
        assert body.spec.permissions is SAMPLE_PERMISSIONS

    @patch("blaxel.core.drive.drive.create_drive", new_callable=AsyncMock)
    async def test_create_without_permissions_uses_unset(self, mock_create):
        returned_drive = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(region="us-pdx-1"),
        )
        mock_create.return_value = returned_drive

        result = await DriveInstance.create({"name": "d1", "region": "us-pdx-1"})

        assert isinstance(result, DriveInstance)
        body = mock_create.call_args.kwargs["body"]
        assert body.spec.permissions is UNSET

    @patch("blaxel.core.drive.drive.create_drive", new_callable=AsyncMock)
    async def test_create_with_empty_permissions_sends_empty_list(self, mock_create):
        returned_drive = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(permissions=[], region="us-pdx-1"),
        )
        mock_create.return_value = returned_drive

        result = await DriveInstance.create({"name": "d1", "region": "us-pdx-1", "permissions": []})

        assert isinstance(result, DriveInstance)
        body = mock_create.call_args.kwargs["body"]
        assert body.spec.permissions == []
        assert body.spec.permissions is not UNSET


@pytest.mark.asyncio
class TestDriveUpdateWithPermissions:
    @patch("blaxel.core.drive.drive.update_drive", new_callable=AsyncMock)
    @patch.object(DriveInstance, "get", new_callable=AsyncMock)
    async def test_update_permissions_via_config(self, mock_get, mock_update):
        existing = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(size=10, region="us-pdx-1"),
        )
        mock_get.return_value = DriveInstance(existing)

        updated = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(size=10, region="us-pdx-1", permissions=SAMPLE_PERMISSIONS),
        )
        mock_update.return_value = updated

        config = DriveCreateConfiguration(permissions=SAMPLE_PERMISSIONS)
        result = await DriveInstance.update("d1", config)

        body = mock_update.call_args.kwargs["body"]
        assert body.spec.permissions is SAMPLE_PERMISSIONS
        assert isinstance(result, DriveInstance)

    @patch("blaxel.core.drive.drive.update_drive", new_callable=AsyncMock)
    @patch.object(DriveInstance, "get", new_callable=AsyncMock)
    async def test_update_permissions_via_dict(self, mock_get, mock_update):
        existing = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(size=10, region="us-pdx-1"),
        )
        mock_get.return_value = DriveInstance(existing)

        updated = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(size=10, region="us-pdx-1", permissions=SAMPLE_PERMISSIONS),
        )
        mock_update.return_value = updated

        result = await DriveInstance.update("d1", {"permissions": SAMPLE_PERMISSIONS})

        body = mock_update.call_args.kwargs["body"]
        assert body.spec.permissions is SAMPLE_PERMISSIONS
        assert isinstance(result, DriveInstance)

    @patch("blaxel.core.drive.drive.update_drive", new_callable=AsyncMock)
    @patch.object(DriveInstance, "get", new_callable=AsyncMock)
    async def test_update_preserves_existing_permissions(self, mock_get, mock_update):
        existing = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(size=10, region="us-pdx-1", permissions=SAMPLE_PERMISSIONS),
        )
        mock_get.return_value = DriveInstance(existing)

        updated = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(size=20, region="us-pdx-1", permissions=SAMPLE_PERMISSIONS),
        )
        mock_update.return_value = updated

        await DriveInstance.update("d1", {"size": 20})

        body = mock_update.call_args.kwargs["body"]
        assert body.spec.permissions is SAMPLE_PERMISSIONS

    @patch("blaxel.core.drive.drive.update_drive", new_callable=AsyncMock)
    @patch.object(DriveInstance, "get", new_callable=AsyncMock)
    async def test_read_back_permissions_from_created_drive(self, mock_get, mock_update):
        new_perms = [make_permission(mode="read", path="/shared")]
        existing = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(size=10, region="us-pdx-1"),
        )
        mock_get.return_value = DriveInstance(existing)

        updated = Drive(
            metadata=Metadata(name="d1"),
            spec=DriveSpec(size=10, region="us-pdx-1", permissions=new_perms),
        )
        mock_update.return_value = updated

        result = await DriveInstance.update("d1", {"permissions": new_perms})
        assert result.permissions is new_perms
        assert result.permissions[0].mode == DrivePermissionMode("read")
        assert result.permissions[0].path == "/shared"

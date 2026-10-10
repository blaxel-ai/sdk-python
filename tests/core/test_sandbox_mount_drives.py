"""mount_drives behaves the same for async and sync sandbox creation."""

import inspect
import re
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from blaxel.core import (
    DriveAPIError,
    DriveInstance,
    SandboxDriveMountConfiguration,
    SandboxDriveSetupError,
    SandboxInstance,
    SyncDriveInstance,
    SyncSandboxInstance,
)
from blaxel.core.client.models import Drive, DriveSpec, Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox.client.models import DriveMountInfo
from blaxel.core.sandbox.default.drive import SandboxDrive
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.sync.drive import SyncSandboxDrive
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem

REGION = "us-was-1"
CONFIG = {"name": "sandbox", "region": REGION}
EXISTING = {"drive_name": "data", "mount_path": "/mnt/data"}


async def call(fn, *args, **kwargs):
    value = fn(*args, **kwargs)
    return await value if inspect.isawaitable(value) else value


@pytest.fixture(params=["async", "sync"])
def h(request, monkeypatch):
    is_async = request.param == "async"
    mock = AsyncMock if is_async else Mock
    sandbox_cls = SandboxInstance if is_async else SyncSandboxInstance
    drive_cls = DriveInstance if is_async else SyncDriveInstance
    mounts_cls = SandboxDrive if is_async else SyncSandboxDrive
    fs_cls = SandboxFileSystem if is_async else SyncSandboxFileSystem
    module = "blaxel.core.sandbox." + ("default" if is_async else "sync") + ".sandbox"
    response = Sandbox(metadata=Metadata(name="sandbox"), spec=SandboxSpec(region=REGION))
    mounted = []

    def drive(name, region=REGION):
        return drive_cls(Drive(metadata=Metadata(name=name), spec=DriveSpec(region=region)))

    def mount(drive_name, mount_path, drive_path, read_only):
        mounted.append(
            DriveMountInfo(drive_name, drive_path, mount_path=mount_path, read_only=read_only)
        )

    h = SimpleNamespace(
        cls=sandbox_cls,
        drive=drive,
        mounted=mounted,
        create_sandbox=mock(return_value=response),
        get=mock(side_effect=drive),
        create=mock(
            side_effect=lambda config: drive(config.name or "drive-1234abcd", config.region)
        ),
        mount=mock(side_effect=mount),
        list=mock(side_effect=lambda: list(mounted)),
        unmount=mock(),
        delete_drive=mock(),
        delete_sandbox=mock(),
    )
    monkeypatch.setattr(module + ".create_sandbox", h.create_sandbox)
    monkeypatch.setattr(fs_cls, "ls", mock(return_value=[]))
    monkeypatch.setattr(drive_cls, "get", h.get)
    monkeypatch.setattr(drive_cls, "create", h.create)
    monkeypatch.setattr(mounts_cls, "mount", h.mount)
    monkeypatch.setattr(mounts_cls, "list", h.list)
    monkeypatch.setattr(mounts_cls, "unmount", h.unmount)
    monkeypatch.setattr(drive_cls, "delete", h.delete_drive)
    monkeypatch.setattr(sandbox_cls, "delete", h.delete_sandbox)
    yield h
    # These cases only use existing drives or succeed: nothing is deleted or unmounted.
    for mock_ in (h.delete_drive, h.delete_sandbox, h.unmount):
        mock_.assert_not_called()


async def test_without_mount_drives_nothing_extra_happens(h):
    await call(h.cls.create, dict(CONFIG))
    h.get.assert_not_called()
    h.mount.assert_not_called()
    h.list.assert_not_called()


async def test_existing_drive_is_looked_up_by_name_only_then_mounted_and_checked(h):
    await call(h.cls.create, dict(CONFIG), mount_drives=[EXISTING])
    h.get.assert_called_once_with("data")
    h.create.assert_not_called()
    h.mount.assert_called_once_with("data", "/mnt/data", "/", False)
    h.list.assert_called_once_with()


async def test_new_drives_are_created_in_the_sandbox_region(h):
    # An unnamed drive is always new; a named one is reused if it already exists.
    mounts = [
        {"create": {}, "mount_path": "/mnt/a"},
        {"create": {"name": "app"}, "mount_path": "/mnt/b"},
    ]
    await call(h.cls.create, dict(CONFIG), mount_drives=mounts)
    configs = {config.name: config for (config,), _ in h.create.call_args_list}
    # An unnamed drive is named here, so a create whose response is lost can be looked up.
    (generated,) = configs.keys() - {"app"}
    assert re.fullmatch(r"drive-[0-9a-f]{16}", generated)
    assert all(config.region == REGION for config in configs.values())
    h.get.assert_not_called()


async def test_named_drive_that_already_exists_is_reused(h):
    h.create.side_effect = DriveAPIError("exists", status_code=409)
    h.get.side_effect = lambda name: h.drive(name)
    mounts = [{"create": {"name": "app"}, "mount_path": "/mnt/data"}]
    await call(h.cls.create, dict(CONFIG), mount_drives=mounts)
    h.get.assert_called_once_with("app")


async def test_new_drive_in_another_region_is_rejected_and_the_sandbox_kept(h):
    mounts = [{"create": {"region": "eu-lon-1"}, "mount_path": "/mnt/data"}]
    with pytest.raises(SandboxDriveSetupError, match="does not match the sandbox region") as caught:
        await call(h.cls.create, dict(CONFIG), mount_drives=mounts)
    assert caught.value.sandbox.metadata.name == "sandbox"
    h.create.assert_not_called()
    h.mount.assert_not_called()


async def test_create_if_not_exists_forwards_mount_drives(h):
    mount = SandboxDriveMountConfiguration("/mnt/data", drive_name="data")
    await call(h.cls.create_if_not_exists, dict(CONFIG), mount_drives=[mount])
    h.mount.assert_called_once_with("data", "/mnt/data", "/", False)


async def test_drive_in_another_region_is_rejected_and_the_sandbox_kept(h):
    h.get.side_effect = lambda name: h.drive(name, "eu-lon-1")
    with pytest.raises(SandboxDriveSetupError, match="eu-lon-1") as caught:
        await call(h.cls.create, dict(CONFIG), mount_drives=[EXISTING])
    assert caught.value.sandbox.metadata.name == "sandbox"
    assert caught.value.drive_names == ["data"]
    h.mount.assert_not_called()


async def test_failed_mount_keeps_everything_and_reports_the_cause(h):
    cause = RuntimeError("409 mount path already in use")
    first = h.mount.side_effect
    calls = []

    def fail_second(*args):
        calls.append(args)
        if len(calls) == 2:
            raise cause
        return first(*args)

    h.mount.side_effect = fail_second
    mounts = [EXISTING, {"drive_name": "other", "mount_path": "/mnt/other"}]
    with pytest.raises(SandboxDriveSetupError) as caught:
        await call(h.cls.create, dict(CONFIG), mount_drives=mounts)
    assert caught.value.__cause__ is cause
    assert caught.value.drive_names == ["data", "other"]
    assert caught.value.sandbox.metadata.name == "sandbox"


@pytest.mark.parametrize(
    ("requested", "actual"),
    [
        ({"read_only": True}, DriveMountInfo("data", "/", mount_path="/mnt/data", read_only=False)),
        (
            {"drive_path": "/sub"},
            DriveMountInfo("data", "/", mount_path="/mnt/data", read_only=False),
        ),
        ({}, DriveMountInfo("other", "/", mount_path="/mnt/data", read_only=False)),
    ],
    ids=["read-only", "drive-path", "drive"],
)
async def test_fails_when_the_sandbox_reports_a_different_mount_than_requested(
    h, requested, actual
):
    # e.g. create_if_not_exist returned a sandbox that already mounts the path differently.
    h.mount.side_effect = lambda *args: None
    h.mounted.append(actual)
    with pytest.raises(SandboxDriveSetupError, match="/mnt/data is not mounted as requested"):
        await call(h.cls.create, dict(CONFIG), mount_drives=[{**EXISTING, **requested}])


@pytest.mark.parametrize(
    ("requested", "listed_drive_path"),
    [
        ({"mount_path": "/mnt/data/"}, "/"),
        ({"mount_path": "mnt/data"}, "/"),
        ({"drive_path": "/sub/"}, "/sub"),
    ],
    ids=["trailing-slash", "relative", "drive-path"],
)
async def test_accepts_a_mount_the_sandbox_lists_with_a_normalised_path(
    h, requested, listed_drive_path
):
    h.mount.side_effect = lambda *args: None
    h.mounted.append(
        DriveMountInfo("data", listed_drive_path, mount_path="/mnt/data", read_only=False)
    )
    await call(h.cls.create, dict(CONFIG), mount_drives=[{**EXISTING, **requested}])


@pytest.mark.parametrize(
    ("entry", "create_if_not_exist"),
    [
        ({**EXISTING, "create": {}}, False),
        ({"mount_path": "/mnt/data"}, False),
        ({"create": {}, "mount_path": "/mnt/data"}, True),
    ],
    ids=["both", "neither", "unnamed-with-create_if_not_exist"],
)
async def test_invalid_entries_are_rejected_before_the_sandbox_is_created(
    h, entry, create_if_not_exist
):
    with pytest.raises(ValueError):
        await call(
            h.cls.create,
            dict(CONFIG),
            create_if_not_exist=create_if_not_exist,
            mount_drives=[entry],
        )
    h.create_sandbox.assert_not_called()

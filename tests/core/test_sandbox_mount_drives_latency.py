"""With mocked latencies, setting up drives alongside the sandbox beats doing it one step after another."""

import asyncio
import time
from unittest.mock import patch

import pytest

from blaxel.core import DriveInstance, SandboxInstance, SyncDriveInstance, SyncSandboxInstance
from blaxel.core.client.models import Drive, DriveSpec, Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox.client.models import DriveMountInfo
from blaxel.core.sandbox.default.drive import SandboxDrive
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.sync.drive import SyncSandboxDrive
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem

REGION = "us-was-1"
# Seconds; scaled down from a 300 ms sandbox, 200 ms drive create, 100 ms mount.
SANDBOX, DRIVE_CREATE, MOUNT, LIST = 0.15, 0.10, 0.05, 0.025


@pytest.mark.parametrize("count", [1, 4, 8])
@pytest.mark.parametrize("mode", ["async", "sync"])
async def test_drives_are_set_up_while_the_sandbox_is_created(mode, count):
    is_async = mode == "async"
    sandbox_cls = SandboxInstance if is_async else SyncSandboxInstance
    drive_cls = DriveInstance if is_async else SyncDriveInstance
    drives_cls = SandboxDrive if is_async else SyncSandboxDrive
    fs_cls = SandboxFileSystem if is_async else SyncSandboxFileSystem
    module = "blaxel.core.sandbox." + ("default" if is_async else "sync") + ".sandbox"
    response = Sandbox(metadata=Metadata(name="sandbox"), spec=SandboxSpec(region=REGION))
    mounted = []

    def new_drive(config):
        return drive_cls(Drive(metadata=Metadata(name=config.name), spec=DriveSpec(region=REGION)))

    def record(name, path, drive_path, read_only):
        mounted.append(DriveMountInfo(name, drive_path, mount_path=path, read_only=read_only))

    if is_async:

        async def create_sandbox(**_):
            await asyncio.sleep(SANDBOX)
            return response

        async def create_drive(config):
            await asyncio.sleep(DRIVE_CREATE)
            return new_drive(config)

        async def mount(_self, *args):
            await asyncio.sleep(MOUNT)
            record(*args)

        async def list_mounts(_self):
            await asyncio.sleep(LIST)
            return list(mounted)

        async def ls(_self, *_):
            return []

    else:

        def create_sandbox(**_):
            time.sleep(SANDBOX)
            return response

        def create_drive(config):
            time.sleep(DRIVE_CREATE)
            return new_drive(config)

        def mount(_self, *args):
            time.sleep(MOUNT)
            record(*args)

        def list_mounts(_self):
            time.sleep(LIST)
            return list(mounted)

        def ls(_self, *_):
            return []

    mounts = [{"create": {"name": f"d{i}"}, "mount_path": f"/mnt/d{i}"} for i in range(count)]
    config = {"name": "sandbox", "region": REGION}
    with (
        patch(module + ".create_sandbox", create_sandbox),
        patch.object(drive_cls, "create", create_drive),
        patch.object(drives_cls, "mount", mount),
        patch.object(drives_cls, "list", list_mounts),
        patch.object(fs_cls, "ls", ls),
    ):
        start = time.monotonic()
        if is_async:
            await sandbox_cls.create(config, mount_drives=mounts)
        else:
            await asyncio.to_thread(sandbox_cls.create, config, mount_drives=mounts)
        elapsed = time.monotonic() - start

    one_after_another = SANDBOX + count * (DRIVE_CREATE + MOUNT) + LIST
    # Drives are created during the sandbox creation and mounted at once; only the mounts
    # past the bound of 5 wait a round.
    assert elapsed < (0.6 * one_after_another if count > 1 else one_after_another)

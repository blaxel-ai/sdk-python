"""Live: create a sandbox with mount_drives, async and sync."""

import inspect
import os

import pytest

from blaxel.core import (
    DriveAPIError,
    DriveInstance,
    SandboxDriveSetupError,
    SandboxInstance,
    SyncSandboxInstance,
)
from blaxel.core.client.errors import UnexpectedStatus
from tests.helpers import default_image, default_labels, unique_name, wait_for_sandbox_deletion

REGION = (
    "eu-dub-1" if os.environ.get("BL_ENV") == "dev" else "us-was-1"
)  # drives: some regions only
OTHER_REGION = "us-was-1" if REGION == "eu-dub-1" else "eu-lon-1"


async def call(fn, *args, **kwargs):
    result = fn(*args, **kwargs)
    return await result if inspect.isawaitable(result) else result


@pytest.fixture
async def created():
    sandboxes, drives = [], []
    yield sandboxes, drives
    for name in sandboxes:
        try:
            await call(SandboxInstance.delete, name)
            await wait_for_sandbox_deletion(name)
        except Exception:
            pass
    for name in drives:
        try:
            await call(DriveInstance.delete, name)
        except Exception:
            pass


@pytest.mark.parametrize("cls", [SandboxInstance, SyncSandboxInstance], ids=["async", "sync"])
async def test_mount_drives_on_create(cls, created):
    sandboxes, drives = created
    config = {"image": default_image, "region": REGION, "labels": default_labels}

    # A new drive with a generated name, usable straight away.
    first = await call(
        cls.create,
        config,
        mount_drives=[{"create": {"labels": default_labels}, "mount_path": "/mnt/data"}],
    )
    sandboxes.append(first.metadata.name)
    drive_name = (await call(first.drives.list))[0].drive_name
    drives.append(drive_name)
    await call(first.fs.write, "/mnt/data/hello.txt", "hello")

    # The same drive, by name, in a second sandbox.
    second = await call(
        cls.create, config, mount_drives=[{"drive_name": drive_name, "mount_path": "/mnt/shared"}]
    )
    sandboxes.append(second.metadata.name)
    assert await call(second.fs.read, "/mnt/shared/hello.txt") == "hello"

    # create_if_not_exists on an existing sandbox that already has the mount.
    reused = await call(
        cls.create_if_not_exists,
        {"name": first.metadata.name, "region": REGION},
        mount_drives=[{"drive_name": drive_name, "mount_path": "/mnt/data"}],
    )
    assert reused.metadata.name == first.metadata.name

    # A drive in another region is rejected; the sandbox stays.
    with pytest.raises(SandboxDriveSetupError) as caught:
        await call(
            cls.create,
            {**config, "region": OTHER_REGION},
            mount_drives=[{"drive_name": drive_name, "mount_path": "/mnt/data"}],
        )
    sandboxes.append(caught.value.sandbox.metadata.name)
    assert caught.value.drive_names == [drive_name]
    assert (await SandboxInstance.get(caught.value.sandbox.metadata.name)).status != "TERMINATED"

    # A missing drive is not created.
    missing = unique_name("missing-drive")
    with pytest.raises(SandboxDriveSetupError) as caught:
        await call(
            cls.create, config, mount_drives=[{"drive_name": missing, "mount_path": "/mnt/x"}]
        )
    sandboxes.append(caught.value.sandbox.metadata.name)
    with pytest.raises((DriveAPIError, UnexpectedStatus)) as not_found:
        await DriveInstance.get(missing)
    assert not_found.value.status_code == 404

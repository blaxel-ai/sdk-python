"""Mount drives while creating a sandbox (``mount_drives``)."""

from typing import NamedTuple

from ..drive import DriveCreateConfiguration, DriveInstance, SyncDriveInstance
from .client.types import Unset
from .types import SandboxDriveMountConfiguration


class SandboxDriveSetupError(Exception):
    """A sandbox is ready, but one of its ``mount_drives`` could not be set up.

    Nothing is rolled back: the sandbox, drives and mounts made so far remain.
    ``drive_names`` lists the drives this call looked up or created; delete only
    the ones you created. The original error is ``__cause__``.
    """

    def __init__(self, sandbox, drive_names: list[str], cause: Exception):
        super().__init__(
            f"Sandbox {sandbox.metadata.name} is ready, but mounting its drives failed: {cause}"
        )
        self.sandbox = sandbox
        self.drive_names = drive_names


class _Mount(NamedTuple):
    drive: str | DriveCreateConfiguration  # a name means an existing drive
    mount_path: str
    drive_path: str
    read_only: bool


def _normalize_mount_drives(
    mount_drives: list[SandboxDriveMountConfiguration | dict] | None, create_if_not_exist: bool
) -> list[_Mount]:
    mounts = []
    for mount in mount_drives or []:
        if isinstance(mount, dict):
            mount = SandboxDriveMountConfiguration(**mount)
        drive: str | DriveCreateConfiguration
        if mount.drive_name is not None and mount.create is None:
            drive = mount.drive_name
        elif mount.create is not None and mount.drive_name is None:
            # Copy so the caller's configuration is not changed.
            create = mount.create
            drive = DriveCreateConfiguration(
                **(create if isinstance(create, dict) else vars(create))
            )
            if create_if_not_exist and not drive.name:
                raise ValueError(
                    "With create_if_not_exist, a new drive in mount_drives needs a name; "
                    "otherwise every call would create another drive."
                )
        else:
            raise ValueError(
                "Each mount_drives entry needs exactly one of 'drive_name' or 'create'."
            )
        mounts.append(_Mount(drive, mount.mount_path, mount.drive_path, mount.read_only))
    return mounts


def _in_sandbox_region(create: DriveCreateConfiguration, region: str) -> DriveCreateConfiguration:
    if create.region not in (None, region):
        raise ValueError(
            f"Drive region {create.region} does not match the sandbox region {region}."
        )
    create.region = region
    return create


def _record_and_check(
    drive: DriveInstance | SyncDriveInstance, region: str, drive_names: list[str]
) -> str:
    assert drive.name is not None
    drive_names.append(drive.name)
    if drive.region != region:
        raise ValueError(
            f"Drive {drive.name} is in {drive.region}, but the sandbox is in {region}."
        )
    return drive.name


def _clean(path: str) -> str:
    return "/" + "/".join(part for part in path.split("/") if part)


def _check_mounted(requests: list[tuple], mounted: list) -> None:
    # Mounting reports success even if an existing mount at that path keeps a
    # different read_only, so check the result.
    by_path = {_clean(mount.mount_path): mount for mount in mounted}
    for drive_name, mount_path, drive_path, read_only in requests:
        actual = by_path.get(_clean(mount_path))
        if (
            actual is None
            or actual.drive_name != drive_name
            or _clean("/" if isinstance(actual.drive_path, Unset) else actual.drive_path)
            != _clean(drive_path)
            or (False if isinstance(actual.read_only, Unset) else actual.read_only) != read_only
        ):
            raise ValueError(
                f"{mount_path} is not mounted as requested; see sandbox.drives.list()."
            )


async def _mount_drives_async(sandbox, mounts: list[_Mount]) -> None:
    drive_names: list[str] = []
    requests = []
    try:
        region = sandbox.spec.region
        for mount in mounts:
            if isinstance(mount.drive, str):
                drive = await DriveInstance.get(mount.drive)
            elif mount.drive.name:
                drive = await DriveInstance.create_if_not_exists(
                    _in_sandbox_region(mount.drive, region)
                )
            else:
                drive = await DriveInstance.create(_in_sandbox_region(mount.drive, region))
            name = _record_and_check(drive, region, drive_names)
            requests.append((name, *mount[1:]))
        for request in requests:
            await sandbox.drives.mount(*request)
        _check_mounted(requests, await sandbox.drives.list())
    except Exception as cause:
        raise SandboxDriveSetupError(sandbox, drive_names, cause) from cause


def _mount_drives_sync(sandbox, mounts: list[_Mount]) -> None:
    drive_names: list[str] = []
    requests = []
    try:
        region = sandbox.spec.region
        for mount in mounts:
            if isinstance(mount.drive, str):
                drive = SyncDriveInstance.get(mount.drive)
            elif mount.drive.name:
                drive = SyncDriveInstance.create_if_not_exists(
                    _in_sandbox_region(mount.drive, region)
                )
            else:
                drive = SyncDriveInstance.create(_in_sandbox_region(mount.drive, region))
            name = _record_and_check(drive, region, drive_names)
            requests.append((name, *mount[1:]))
        for request in requests:
            sandbox.drives.mount(*request)
        _check_mounted(requests, sandbox.drives.list())
    except Exception as cause:
        raise SandboxDriveSetupError(sandbox, drive_names, cause) from cause

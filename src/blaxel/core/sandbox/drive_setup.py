"""Mount drives while creating a sandbox (``mount_drives``).

Drives are looked up or created while the sandbox is being created, at most
``MOUNT_DRIVES_CONCURRENCY`` at a time. Mounting is the only step that waits for
both the sandbox and its drive, and each drive is mounted as soon as it is ready.
"""

import asyncio
import threading
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from typing import NamedTuple

from ..client.errors import UnexpectedStatus
from ..drive import DriveAPIError, DriveCreateConfiguration, DriveInstance, SyncDriveInstance
from .client.types import Unset
from .types import SandboxDriveMountConfiguration

# Most drive lookups/creations, and most mounts, in flight at once.
MOUNT_DRIVES_CONCURRENCY = 5


class SandboxDriveSetupError(Exception):
    """A sandbox is ready, but one of its ``mount_drives`` could not be set up.

    The sandbox, drives and mounts made so far remain. ``drive_names`` lists the
    drives this call looked up or created; delete only the ones you created. The
    original error is ``__cause__``. (If the sandbox itself cannot be created,
    its error is raised instead and the drives this call created are deleted.)
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


def _requested_region(sandbox_spec_region) -> str | None:
    return (
        None
        if isinstance(sandbox_spec_region, Unset) or not sandbox_spec_region
        else sandbox_spec_region
    )


def _in_sandbox_region(create: DriveCreateConfiguration, region: str) -> DriveCreateConfiguration:
    if create.region not in (None, region):
        raise ValueError(
            f"Drive region {create.region} does not match the sandbox region {region}."
        )
    create.region = region
    return create


def _is_conflict(error: Exception) -> bool:
    if isinstance(error, DriveAPIError):
        return error.status_code == 409 or error.code in ["409", "DRIVE_ALREADY_EXISTS"]
    return isinstance(error, UnexpectedStatus) and error.status_code == 409


def _check_region(drive: DriveInstance | SyncDriveInstance, region) -> None:
    if drive.region != region:
        raise ValueError(
            f"Drive {drive.name} is in {drive.region}, but the sandbox is in {region}."
        )


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


def _first_error(errors: dict[int, BaseException]) -> BaseException | None:
    return errors[min(errors)] if errors else None


class _AsyncDriveSetup:
    """Drives for one ``SandboxInstance.create`` call.

    ``start`` runs the lookups/creations alongside the sandbox creation, ``mount``
    mounts them once the sandbox exists, and ``discard`` cleans up when the sandbox
    could not be created: drives this call created are deleted again.
    """

    def __init__(self, mounts: list[_Mount], region: str | None):
        self._mounts = mounts
        self._region: asyncio.Future = asyncio.get_running_loop().create_future()
        if region:
            self._region.set_result(region)
        self._stopped = False
        self._prepared: list[asyncio.Future] = []
        self._looked: list[str | None] = [None] * len(mounts)
        self._created: list[str] = []

    def _set_region(self, region: str | None) -> None:
        if not self._region.done():
            self._region.set_result(region)

    def start(self) -> None:
        semaphore = asyncio.Semaphore(MOUNT_DRIVES_CONCURRENCY)
        self._prepared = [
            asyncio.ensure_future(self._prepare(index, mount, semaphore))
            for index, mount in enumerate(self._mounts)
        ]

    async def _prepare(self, index: int, mount: _Mount, semaphore: asyncio.Semaphore):
        try:
            # A new drive goes in the sandbox's region, so it waits for it if it is not known yet.
            region = None if isinstance(mount.drive, str) else await self._region
            async with semaphore:
                if self._stopped or (region is None and not isinstance(mount.drive, str)):
                    return None
                if isinstance(mount.drive, str):
                    drive = await DriveInstance.get(mount.drive)
                else:
                    assert region is not None
                    config = _in_sandbox_region(mount.drive, region)
                    try:
                        drive = await DriveInstance.create(config)
                        self._created.append(str(drive.name))
                    except Exception as error:
                        # A named drive is reused if it exists; an unnamed one cannot conflict.
                        if not config.name or not _is_conflict(error):
                            raise
                        drive = await DriveInstance.get(config.name)
        except BaseException:
            self._stopped = True
            raise
        self._looked[index] = drive.name
        return drive

    async def discard(self) -> None:
        """The sandbox could not be created: stop, wait for drives in flight, delete new ones."""
        self._stopped = True
        self._set_region(None)
        await asyncio.gather(*self._prepared, return_exceptions=True)
        await asyncio.gather(
            *(DriveInstance.delete(name) for name in self._created),  # pyright: ignore[reportCallIssue]
            return_exceptions=True,
        )

    async def mount(self, sandbox) -> None:
        region = sandbox.spec.region
        self._set_region(_requested_region(region))
        semaphore = asyncio.Semaphore(MOUNT_DRIVES_CONCURRENCY)
        requests: list[tuple] = []

        async def mount_one(index: int, prepared: asyncio.Future) -> None:
            try:
                drive = await prepared
                if drive is None:
                    return
                _check_region(drive, region)
                request = (drive.name, *self._mounts[index][1:])
                requests.append(request)
                async with semaphore:
                    if not self._stopped:
                        await sandbox.drives.mount(*request)
            except BaseException:
                self._stopped = True
                raise

        results = await asyncio.gather(
            *(mount_one(index, prepared) for index, prepared in enumerate(self._prepared)),
            return_exceptions=True,
        )
        drive_names = [name for name in self._looked if name is not None]
        failed = _first_error(
            {index: r for index, r in enumerate(results) if isinstance(r, BaseException)}
        )
        try:
            if failed is not None:
                raise failed
            _check_mounted(requests, await sandbox.drives.list())
        except Exception as cause:
            raise SandboxDriveSetupError(sandbox, drive_names, cause) from cause


class _SyncDriveSetup:
    """Same as ``_AsyncDriveSetup``, with a thread pool in place of tasks."""

    def __init__(self, mounts: list[_Mount], region: str | None):
        self._mounts = mounts
        self._region: str | None = region
        self._region_ready = threading.Event()
        if region:
            self._region_ready.set()
        self._stopped = threading.Event()
        self._lock = threading.Lock()
        self._pool: ThreadPoolExecutor | None = None
        self._prepared: list[Future] = []
        self._looked: list[str | None] = [None] * len(mounts)
        self._created: list[str] = []

    def _set_region(self, region: str | None) -> None:
        if not self._region_ready.is_set():
            self._region = region
            self._region_ready.set()

    def start(self) -> None:
        self._pool = ThreadPoolExecutor(
            max_workers=MOUNT_DRIVES_CONCURRENCY, thread_name_prefix="blaxel-mount-drives"
        )
        self._prepared = [
            self._pool.submit(self._prepare, index, mount)
            for index, mount in enumerate(self._mounts)
        ]

    def _prepare(self, index: int, mount: _Mount):
        try:
            if self._stopped.is_set():
                return None
            if isinstance(mount.drive, str):
                drive = SyncDriveInstance.get(mount.drive)
            else:
                # A new drive goes in the sandbox's region, so it waits for it if it is not known yet.
                self._region_ready.wait()
                if self._stopped.is_set() or self._region is None:
                    return None
                config = _in_sandbox_region(mount.drive, self._region)
                try:
                    drive = SyncDriveInstance.create(config)
                    with self._lock:
                        self._created.append(str(drive.name))
                except Exception as error:
                    if not config.name or not _is_conflict(error):
                        raise
                    drive = SyncDriveInstance.get(config.name)
        except BaseException:
            self._stopped.set()
            raise
        self._looked[index] = drive.name
        return drive

    def _shutdown(self) -> None:
        if self._pool is not None:
            self._pool.shutdown(wait=True)

    def discard(self) -> None:
        """The sandbox could not be created: stop, wait for drives in flight, delete new ones."""
        self._stopped.set()
        self._set_region(None)
        self._shutdown()
        for name in self._created:
            try:
                SyncDriveInstance.delete(name)  # pyright: ignore[reportCallIssue]
            except Exception:
                pass

    def _mount_one(self, sandbox, request: tuple) -> None:
        try:
            if not self._stopped.is_set():
                sandbox.drives.mount(*request)
        except BaseException:
            self._stopped.set()
            raise

    def mount(self, sandbox) -> None:
        region = sandbox.spec.region
        self._set_region(_requested_region(region))
        errors: dict[int, BaseException] = {}
        requests: list[tuple] = []
        mounting: dict[Future, int] = {}
        indexes = {future: index for index, future in enumerate(self._prepared)}
        with ThreadPoolExecutor(
            max_workers=MOUNT_DRIVES_CONCURRENCY, thread_name_prefix="blaxel-mount-drives"
        ) as pool:
            # Mount each drive as soon as it is ready.
            for future in as_completed(self._prepared):
                index = indexes[future]
                try:
                    drive = future.result()
                    if drive is None:
                        continue
                    _check_region(drive, region)
                except BaseException as error:
                    self._stopped.set()
                    errors[index] = error
                    continue
                request = (drive.name, *self._mounts[index][1:])
                requests.append(request)
                mounting[pool.submit(self._mount_one, sandbox, request)] = index
            for future, index in mounting.items():
                error = future.exception()
                if error is not None:
                    errors[index] = error
        self._shutdown()
        drive_names = [name for name in self._looked if name is not None]
        failed = _first_error(errors)
        try:
            if failed is not None:
                raise failed
            _check_mounted(requests, sandbox.drives.list())
        except Exception as cause:
            raise SandboxDriveSetupError(sandbox, drive_names, cause) from cause

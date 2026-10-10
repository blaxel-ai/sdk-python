"""Mount drives while creating a sandbox (``mount_drives``).

Drives are looked up or created while the sandbox is being created, at most
``MOUNT_DRIVES_CONCURRENCY`` at a time. Mounting is the only step that waits for
both the sandbox and its drive, and each drive is mounted as soon as it is ready.
On failure, drives this call created and did not mount are deleted.
"""

import asyncio
import threading
import uuid
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from typing import NamedTuple

from ..client.errors import UnexpectedStatus
from ..drive import DriveAPIError, DriveCreateConfiguration, DriveInstance, SyncDriveInstance
from .client.types import Unset
from .types import SandboxDriveMountConfiguration

# Most drive lookups/creations, mounts and deletions in flight at once.
MOUNT_DRIVES_CONCURRENCY = 5


class SandboxDriveSetupError(Exception):
    """``mount_drives`` could not be set up. The original error is ``__cause__``.

    Drives this call created and did not mount are deleted first;
    ``created_drives`` names the ones it created (or may have created, when a
    response was lost) that are left in place.

    - ``sandbox`` is set when the sandbox is ready: it and the mounts made so far
      are kept. ``drive_names`` lists the drives this call looked up or created
      that are left in place.
    - ``sandbox`` is None when the sandbox could not be created (its error is the
      cause) and some drives created for it could not be deleted. When they all
      could, the sandbox's error is raised as is instead.
    """

    def __init__(
        self, sandbox, drive_names: list[str], created_drives: list[str], cause: BaseException
    ):
        left = (
            f". Drives this call created (or may have created) are left in place: "
            f"{', '.join(created_drives)}."
            if created_drives
            else ""
        )
        super().__init__(
            f"Sandbox {sandbox.metadata.name} is ready, but mounting its drives failed: {cause}{left}"
            if sandbox is not None
            else f"Sandbox creation failed: {cause}{left}"
        )
        self.sandbox = sandbox
        self.drive_names = drive_names
        self.created_drives = created_drives


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


def _new_drive_config(
    entry: "_Entry", create: DriveCreateConfiguration, region: str | None
) -> DriveCreateConfiguration:
    """The create request for a new drive, in the sandbox's region and with a name known up front."""
    if region is None:
        raise ValueError("The sandbox reports no region, so its drives were not created.")
    if create.region not in (None, region):
        raise ValueError(
            f"Drive region {create.region} does not match the sandbox region {region}."
        )
    # Name unnamed drives here so that a create whose response is lost can still be looked up.
    entry.name = create.name or f"drive-{uuid.uuid4().hex[:16]}"
    return DriveCreateConfiguration(**{**vars(create), "name": entry.name, "region": region})


def _status(error: BaseException) -> int | None:
    status = getattr(error, "status_code", None)
    return status if isinstance(status, int) else None


def _is_conflict(error: BaseException) -> bool:
    if isinstance(error, DriveAPIError):
        return error.status_code == 409 or error.code in ["409", "DRIVE_ALREADY_EXISTS"]
    return isinstance(error, UnexpectedStatus) and error.status_code == 409


def _is_rejected(error: BaseException) -> bool:
    """The server answered and refused the request, so it changed nothing.

    Anything else (5xx, network error, timeout) may have gone through.
    """
    status = _status(error)
    return status is not None and 400 <= status < 500 and status != 408


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


class _Entry:
    """What this call did with one ``mount_drives`` entry."""

    def __init__(self):
        self.name: str | None = None  # the drive's name, once known
        self.exists = False  # looked up or created, and not deleted since
        self.created = False  # created by this call (not an existing drive it reused)
        self.unconfirmed = False  # the create request's outcome is unknown: the drive may exist
        # A mount was attempted; on failure the sandbox's mount list decides whether it took.
        self.mounted = False


class _Entries:
    """Bookkeeping shared by the async and sync setups."""

    _entries: list[_Entry]

    def _to_delete(self, mounted_names: set | None) -> list[_Entry]:
        created = [e for e in self._entries if e.created and e.exists]
        if mounted_names is not None:
            for entry in created:
                entry.mounted = entry.name in mounted_names
        return [e for e in created if not e.mounted]

    def _needs_mount_list(self) -> bool:
        return any(e.created and e.exists and e.mounted for e in self._entries)

    def _left_names(self) -> list[str]:
        return [str(e.name) for e in self._entries if e.exists]

    def _left_created(self) -> list[str]:
        return [str(e.name) for e in self._entries if (e.created and e.exists) or e.unconfirmed]


class _AsyncDriveSetup(_Entries):
    """Drives for one ``SandboxInstance.create`` call.

    ``start`` runs the lookups/creations alongside the sandbox creation, ``mount``
    mounts them once the sandbox exists, and ``discard`` cleans up when the sandbox
    could not be created. On failure, drives this call created and did not mount
    are deleted.
    """

    def __init__(self, mounts: list[_Mount], region: str | None):
        """``region`` is the region the sandbox creation request sends, if any.

        New drives are created in it at once; without one they wait for the
        created sandbox and use its region.
        """
        self._mounts = mounts
        self._region: asyncio.Future = asyncio.get_running_loop().create_future()
        if region:
            self._region.set_result(region)
        self._stopped = False
        self._prepared: list[asyncio.Future] = []
        self._entries = [_Entry() for _ in mounts]

    def _set_region(self, region: str | None) -> None:
        if not self._region.done():
            self._region.set_result(region)

    def start(self) -> None:
        semaphore = asyncio.Semaphore(MOUNT_DRIVES_CONCURRENCY)
        self._prepared = [
            asyncio.ensure_future(self._prepare(entry, mount, semaphore))
            for entry, mount in zip(self._entries, self._mounts)
        ]

    async def _prepare(self, entry: _Entry, mount: _Mount, semaphore: asyncio.Semaphore):
        try:
            # A new drive goes in the sandbox's region, so it waits for it if it is not known yet.
            region = None if isinstance(mount.drive, str) else await self._region
            async with semaphore:
                if self._stopped:
                    return None
                if isinstance(mount.drive, str):
                    drive = await DriveInstance.get(mount.drive)
                else:
                    drive = await self._create(entry, mount.drive, region)
        except BaseException:
            self._stopped = True
            raise
        entry.name = drive.name
        entry.exists = True
        return drive

    async def _create(self, entry: _Entry, create: DriveCreateConfiguration, region):
        """Create a drive in the sandbox's region; a named one that already exists is reused."""
        config = _new_drive_config(entry, create, region)
        try:
            drive = await DriveInstance.create(config)
            entry.created = True
            return drive
        except Exception as error:
            if _is_conflict(error):
                # Only a name the caller chose can belong to an existing drive worth reusing.
                if not create.name:
                    raise
                return await DriveInstance.get(str(config.name))
            if _is_rejected(error):
                raise
            # The create may have succeeded server-side: look the drive up by its name.
            entry.unconfirmed = True
            try:
                drive = await DriveInstance.get(str(config.name))
            except Exception:
                raise error from None
            entry.unconfirmed = False
            # A generated name is this call's own; a chosen one may be an existing drive,
            # which is never deleted.
            entry.created = not create.name
            return drive

    async def discard(self, cause: BaseException) -> "SandboxDriveSetupError | None":
        """The sandbox could not be created: stop, wait for drives in flight, delete new ones.

        Returns a ``SandboxDriveSetupError`` naming drives that could not be deleted, if any.
        """
        self._stopped = True
        self._set_region(None)
        await asyncio.gather(*self._prepared, return_exceptions=True)
        await self._rollback(None)
        left = self._left_created()
        return SandboxDriveSetupError(None, self._left_names(), left, cause) if left else None

    async def mount(self, sandbox) -> None:
        region = _requested_region(sandbox.spec.region)
        self._set_region(region)
        semaphore = asyncio.Semaphore(MOUNT_DRIVES_CONCURRENCY)
        requests: list[tuple] = []

        async def mount_one(entry: _Entry, mount: _Mount, prepared: asyncio.Future) -> None:
            try:
                drive = await prepared
                if drive is None:
                    return
                _check_region(drive, region)
                request = (drive.name, mount.mount_path, mount.drive_path, mount.read_only)
                async with semaphore:
                    if self._stopped:
                        return
                    requests.append(request)
                    entry.mounted = True
                    await sandbox.drives.mount(*request)
            except BaseException:
                self._stopped = True
                raise

        results = await asyncio.gather(
            *(
                mount_one(entry, mount, prepared)
                for entry, mount, prepared in zip(self._entries, self._mounts, self._prepared)
            ),
            return_exceptions=True,
        )
        failed = _first_error(
            {index: r for index, r in enumerate(results) if isinstance(r, BaseException)}
        )
        try:
            if failed is not None:
                raise failed
            _check_mounted(requests, await sandbox.drives.list())
        except Exception as cause:
            await self._rollback(sandbox)
            raise SandboxDriveSetupError(
                sandbox, self._left_names(), self._left_created(), cause
            ) from cause

    async def _rollback(self, sandbox) -> None:
        """Delete the drives this call created and did not mount; a failed deletion is reported."""
        mounted_names = None
        if sandbox is not None and self._needs_mount_list():
            # A failed mount call may still have mounted its drive (a lost response), and a
            # successful one may not have (the path was already mounted): ask the sandbox.
            try:
                mounted_names = {mount.drive_name for mount in await sandbox.drives.list()}
            except Exception:
                pass  # Unknown: keep every drive a mount was attempted for.
        semaphore = asyncio.Semaphore(MOUNT_DRIVES_CONCURRENCY)

        async def delete(entry: _Entry) -> None:
            async with semaphore:
                try:
                    await DriveInstance.delete(str(entry.name))  # pyright: ignore[reportCallIssue]
                    entry.exists = False
                except Exception:
                    pass  # Reported through SandboxDriveSetupError.created_drives.

        await asyncio.gather(*(delete(entry) for entry in self._to_delete(mounted_names)))


def _copy_outcome(source: Future, target: Future) -> None:
    error = source.exception()
    if error is not None:
        target.set_exception(error)
    else:
        target.set_result(source.result())


class _SyncDriveSetup(_Entries):
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
        # New drives waiting for the sandbox's region, submitted once it is known.
        self._waiting: list[tuple[Future, _Entry, _Mount]] = []
        self._entries = [_Entry() for _ in mounts]

    def _set_region(self, region: str | None) -> None:
        if self._region_ready.is_set():
            return
        self._region = region
        self._region_ready.set()
        assert self._pool is not None
        for placeholder, entry, mount in self._waiting:
            future = self._pool.submit(self._prepare, entry, mount)
            future.add_done_callback(lambda done, p=placeholder: _copy_outcome(done, p))

    def start(self) -> None:
        self._pool = ThreadPoolExecutor(
            max_workers=MOUNT_DRIVES_CONCURRENCY, thread_name_prefix="blaxel-mount-drives"
        )
        for entry, mount in zip(self._entries, self._mounts):
            if isinstance(mount.drive, str) or self._region_ready.is_set():
                self._prepared.append(self._pool.submit(self._prepare, entry, mount))
            else:
                # A new drive goes in the sandbox's region, so it waits for it, without
                # holding a worker, if it is not known yet.
                placeholder: Future = Future()
                self._waiting.append((placeholder, entry, mount))
                self._prepared.append(placeholder)

    def _prepare(self, entry: _Entry, mount: _Mount):
        try:
            if self._stopped.is_set():
                return None
            if isinstance(mount.drive, str):
                drive = SyncDriveInstance.get(mount.drive)
            else:
                drive = self._create(entry, mount.drive, self._region)
        except BaseException:
            self._stopped.set()
            raise
        entry.name = drive.name
        entry.exists = True
        return drive

    def _create(self, entry: _Entry, create: DriveCreateConfiguration, region):
        config = _new_drive_config(entry, create, region)
        try:
            drive = SyncDriveInstance.create(config)
            entry.created = True
            return drive
        except Exception as error:
            if _is_conflict(error):
                if not create.name:
                    raise
                return SyncDriveInstance.get(str(config.name))
            if _is_rejected(error):
                raise
            entry.unconfirmed = True
            try:
                drive = SyncDriveInstance.get(str(config.name))
            except Exception:
                raise error from None
            entry.unconfirmed = False
            entry.created = not create.name
            return drive

    def _shutdown(self) -> None:
        if self._pool is not None:
            self._pool.shutdown(wait=True)

    def discard(self, cause: BaseException) -> "SandboxDriveSetupError | None":
        """The sandbox could not be created: stop, wait for drives in flight, delete new ones.

        Returns a ``SandboxDriveSetupError`` naming drives that could not be deleted, if any.
        """
        self._stopped.set()
        self._set_region(None)
        self._shutdown()
        self._rollback(None)
        left = self._left_created()
        return SandboxDriveSetupError(None, self._left_names(), left, cause) if left else None

    def _mount_one(self, sandbox, entry: _Entry, request: tuple, requests: list[tuple]) -> None:
        try:
            if self._stopped.is_set():
                return
            with self._lock:
                requests.append(request)
            entry.mounted = True
            sandbox.drives.mount(*request)
        except BaseException:
            self._stopped.set()
            raise

    def mount(self, sandbox) -> None:
        region = _requested_region(sandbox.spec.region)
        self._set_region(region)
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
                mount = self._mounts[index]
                request = (drive.name, mount.mount_path, mount.drive_path, mount.read_only)
                job = pool.submit(self._mount_one, sandbox, self._entries[index], request, requests)
                mounting[job] = index
            for future, index in mounting.items():
                error = future.exception()
                if error is not None:
                    errors[index] = error
        self._shutdown()
        failed = _first_error(errors)
        try:
            if failed is not None:
                raise failed
            _check_mounted(requests, sandbox.drives.list())
        except Exception as cause:
            self._rollback(sandbox)
            raise SandboxDriveSetupError(
                sandbox, self._left_names(), self._left_created(), cause
            ) from cause

    def _rollback(self, sandbox) -> None:
        mounted_names = None
        if sandbox is not None and self._needs_mount_list():
            try:
                mounted_names = {mount.drive_name for mount in sandbox.drives.list()}
            except Exception:
                pass

        def delete(entry: _Entry) -> None:
            try:
                SyncDriveInstance.delete(str(entry.name))  # pyright: ignore[reportCallIssue]
                entry.exists = False
            except Exception:
                pass

        to_delete = self._to_delete(mounted_names)
        if to_delete:
            with ThreadPoolExecutor(
                max_workers=MOUNT_DRIVES_CONCURRENCY, thread_name_prefix="blaxel-mount-drives"
            ) as pool:
                list(pool.map(delete, to_delete))

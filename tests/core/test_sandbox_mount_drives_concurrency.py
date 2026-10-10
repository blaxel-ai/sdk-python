"""mount_drives sets drives up alongside the sandbox, a few at a time, in async and sync alike."""

import asyncio
import threading
import time
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from blaxel.core import (
    DriveAPIError,
    DriveInstance,
    SandboxDriveSetupError,
    SandboxInstance,
    SyncDriveInstance,
    SyncSandboxInstance,
)
from blaxel.core.client.models import Drive, DriveSpec, Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox.client.models import DriveMountInfo
from blaxel.core.sandbox.default.drive import SandboxDrive
from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.drive_setup import MOUNT_DRIVES_CONCURRENCY
from blaxel.core.sandbox.sync.drive import SyncSandboxDrive
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem

REGION = "us-was-1"
CONFIG = {"name": "sandbox", "region": REGION}
TIMEOUT = 5


def entry(name):
    return {"create": {"name": name}, "mount_path": f"/mnt/{name}"}


def unnamed(id):
    """A drive the SDK names; tests tell them apart by a label."""
    return {"create": {"labels": {"id": id}}, "mount_path": f"/mnt/{id}"}


def id_of(config):
    return (config.labels or {}).get("id", config.name)


def id_of_name(h, name):
    """The id of the entry a drive name (generated or not) was created for."""
    return next(id_of(c.args[0]) for c in h.create.call_args_list if c.args[0].name == name)


def deleted_ids(h):
    return sorted(id_of_name(h, c.args[0]) for c in h.delete_drive.call_args_list)


class Gate:
    """Blocks callers until opened, from a task (async) or a thread (sync)."""

    def __init__(self, is_async):
        self.is_async = is_async
        self.event = asyncio.Event() if is_async else threading.Event()

    def open(self):
        self.event.set()

    def wait(self):
        if self.is_async:
            return asyncio.wait_for(self.event.wait(), TIMEOUT)
        assert self.event.wait(TIMEOUT), "gate never opened"


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
    lock = threading.Lock()

    def drive(name, region=REGION):
        return drive_cls(Drive(metadata=Metadata(name=name), spec=DriveSpec(region=region)))

    def mount(drive_name, mount_path, drive_path, read_only):
        with lock:
            mounted.append(
                DriveMountInfo(drive_name, drive_path, mount_path=mount_path, read_only=read_only)
            )

    h = SimpleNamespace(
        is_async=is_async,
        cls=sandbox_cls,
        drive=drive,
        response=response,
        gate=lambda: Gate(is_async),
        lock=lock,
        create_sandbox=mock(return_value=response),
        get=mock(side_effect=drive),
        create=mock(side_effect=lambda config: drive(config.name, config.region)),
        real_mount=mount,
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
    h.delete_sandbox.assert_not_called()
    h.unmount.assert_not_called()


def effect(h, produce, gate_for=lambda *args: None, counter=None):
    """A mock side effect: wait for `gate_for(*args)` if it names a gate, then `produce(*args)`."""

    def enter(args):
        if counter:
            counter.enter()
        return gate_for(*args)

    def leave():
        if counter:
            counter.exit()

    if h.is_async:

        async def side_effect(*args, **kwargs):
            gate = enter(args)
            try:
                if gate:
                    await gate.wait()
            finally:
                leave()
            return produce(*args)

    else:

        def side_effect(*args, **kwargs):
            gate = enter(args)
            try:
                if gate:
                    gate.wait()
            finally:
                leave()
            return produce(*args)

    return side_effect


def raising(error):
    def produce(*args):
        raise error

    return produce


class Counter:
    """Calls started, and the most in flight at once."""

    def __init__(self):
        self.lock = threading.Lock()
        self.started = self.active = self.most = 0

    def enter(self):
        with self.lock:
            self.started += 1
            self.active += 1
            self.most = max(self.most, self.active)

    def exit(self):
        with self.lock:
            self.active -= 1


class Running:
    """A create call in progress, driven from the test (a task or a thread)."""

    def __init__(self, h, *args, **kwargs):
        self.h = h
        self.outcome = None
        if h.is_async:
            self.task = asyncio.ensure_future(self._run_async(args, kwargs))
        else:
            self.task = threading.Thread(target=self._run_sync, args=(args, kwargs), daemon=True)
            self.task.start()

    async def _run_async(self, args, kwargs):
        try:
            self.outcome = await self.h.cls.create(*args, **kwargs)
        except BaseException as error:
            self.outcome = error

    def _run_sync(self, args, kwargs):
        try:
            self.outcome = self.h.cls.create(*args, **kwargs)
        except BaseException as error:
            self.outcome = error

    async def until(self, condition):
        deadline = time.monotonic() + TIMEOUT
        while not condition():
            assert time.monotonic() < deadline, "condition never became true"
            await asyncio.sleep(0.005)

    async def settle(self):
        await asyncio.sleep(0.05)

    async def result(self):
        if self.h.is_async:
            await asyncio.wait_for(self.task, TIMEOUT)
        else:
            self.task.join(TIMEOUT)
            assert not self.task.is_alive()
        return self.outcome


async def test_sandbox_and_drive_creation_start_before_either_finishes(h):
    sandbox = h.gate()
    gates = {"a": h.gate(), "b": h.gate()}
    h.create_sandbox.side_effect = effect(h, lambda *a: h.response, lambda *a: sandbox)
    h.create.side_effect = effect(
        h, lambda config: h.drive(config.name), lambda config: gates[config.name]
    )

    run = Running(h, dict(CONFIG), mount_drives=[entry("a"), entry("b")])
    await run.until(lambda: h.create_sandbox.call_count == 1 and h.create.call_count == 2)
    assert {c.args[0].name: c.args[0].region for c in h.create.call_args_list} == {
        "a": REGION,
        "b": REGION,
    }
    h.mount.assert_not_called()

    # A drive that is ready waits for the sandbox: mounting needs both.
    for gate in gates.values():
        gate.open()
    await run.settle()
    h.mount.assert_not_called()

    sandbox.open()
    created = await run.result()
    assert not isinstance(created, BaseException), created
    assert h.mount.call_count == 2
    h.list.assert_called_once_with()


async def test_a_ready_drive_is_mounted_without_waiting_for_a_slower_one(h):
    slow = h.gate()
    h.create.side_effect = effect(
        h,
        lambda config: h.drive(config.name),
        lambda config: slow if config.name == "slow" else None,
    )
    run = Running(h, dict(CONFIG), mount_drives=[entry("slow"), entry("fast")])
    await run.until(lambda: h.mount.call_count == 1)
    h.mount.assert_called_once_with("fast", "/mnt/fast", "/", False)
    slow.open()
    created = await run.result()
    assert not isinstance(created, BaseException), created
    assert h.mount.call_count == 2


async def test_existing_drive_is_looked_up_while_the_sandbox_is_created(h):
    sandbox = h.gate()
    h.create_sandbox.side_effect = effect(h, lambda *a: h.response, lambda *a: sandbox)
    run = Running(h, dict(CONFIG), mount_drives=[{"drive_name": "data", "mount_path": "/mnt/data"}])
    await run.until(lambda: h.get.call_count == 1)
    h.get.assert_called_once_with("data")
    await run.settle()
    h.mount.assert_not_called()
    sandbox.open()
    assert not isinstance(await run.result(), BaseException)
    h.mount.assert_called_once_with("data", "/mnt/data", "/", False)


async def test_drives_are_created_and_mounted_a_few_at_a_time(h):
    total = MOUNT_DRIVES_CONCURRENCY * 2 + 1
    creating, mounting = Counter(), Counter()
    create_gate, mount_gate = h.gate(), h.gate()
    h.create.side_effect = effect(
        h, lambda config: h.drive(config.name), lambda config: create_gate, counter=creating
    )
    h.mount.side_effect = effect(h, h.real_mount, lambda *a: mount_gate, counter=mounting)

    run = Running(h, dict(CONFIG), mount_drives=[entry(f"d{i}") for i in range(total)])
    await run.until(lambda: creating.started == MOUNT_DRIVES_CONCURRENCY)
    await run.settle()
    assert creating.started == creating.most == MOUNT_DRIVES_CONCURRENCY
    create_gate.open()
    await run.until(lambda: mounting.started == MOUNT_DRIVES_CONCURRENCY)
    await run.settle()
    assert mounting.most == MOUNT_DRIVES_CONCURRENCY
    mount_gate.open()
    created = await run.result()
    assert not isinstance(created, BaseException), created
    assert h.create.call_count == total
    assert h.mount.call_count == total
    assert creating.most == mounting.most == MOUNT_DRIVES_CONCURRENCY


@pytest.mark.filterwarnings("ignore::FutureWarning")
async def test_without_a_known_region_new_drives_wait_for_the_sandbox_and_use_its_region(
    h, monkeypatch
):
    monkeypatch.delenv("BL_REGION", raising=False)
    sandbox = h.gate()
    h.create_sandbox.side_effect = effect(h, lambda *a: h.response, lambda *a: sandbox)
    mounts = [entry("a"), {"drive_name": "data", "mount_path": "/mnt/data"}]
    run = Running(h, {"name": "sandbox"}, mount_drives=mounts)
    await run.until(lambda: h.get.call_count == 1)
    await run.settle()
    h.create.assert_not_called()
    sandbox.open()
    assert not isinstance(await run.result(), BaseException)
    assert h.create.call_args.args[0].region == REGION


@pytest.mark.filterwarnings("ignore::FutureWarning")
async def test_drives_waiting_for_the_sandbox_region_do_not_hold_a_slot(h, monkeypatch):
    monkeypatch.delenv("BL_REGION", raising=False)
    sandbox = h.gate()
    h.create_sandbox.side_effect = effect(h, lambda *a: h.response, lambda *a: sandbox)
    waiting = [entry(f"d{i}") for i in range(MOUNT_DRIVES_CONCURRENCY)]
    mounts = waiting + [{"drive_name": "data", "mount_path": "/mnt/data"}]
    run = Running(h, {"name": "sandbox"}, mount_drives=mounts)
    await run.until(lambda: h.get.call_count == 1)
    h.create.assert_not_called()
    sandbox.open()
    assert not isinstance(await run.result(), BaseException)
    assert h.create.call_count == MOUNT_DRIVES_CONCURRENCY


async def test_failed_sandbox_deletes_the_drives_this_call_named_and_created_and_only_those(h):
    failure = RuntimeError("quota exceeded")
    sandbox, new = h.gate(), h.gate()
    h.create_sandbox.side_effect = effect(h, raising(failure), lambda *a: sandbox)

    def create(config):
        if config.name == "old":
            raise DriveAPIError("exists", status_code=409)
        return h.drive(config.name)

    h.create.side_effect = effect(h, create, lambda c: new if id_of(c) == "new" else None)
    mounts = [unnamed("new"), entry("old"), {"drive_name": "data", "mount_path": "/mnt/data"}]
    run = Running(h, dict(CONFIG), mount_drives=mounts)
    await run.until(lambda: h.create.call_count == 2 and h.get.call_count == 2)
    sandbox.open()
    # The drive still being created is waited for, then deleted.
    await run.settle()
    h.delete_drive.assert_not_called()
    new.open()
    assert await run.result() is failure
    assert deleted_ids(h) == ["new"]
    h.mount.assert_not_called()


async def test_failed_sandbox_never_deletes_a_drive_created_under_the_callers_name(h):
    # A concurrent call may have reused it (409, then get) and mounted it.
    failure = RuntimeError("quota exceeded")
    sandbox = h.gate()
    h.create_sandbox.side_effect = effect(h, raising(failure), lambda *a: sandbox)
    run = Running(h, dict(CONFIG), mount_drives=[entry("app-data")])
    await run.until(lambda: h.create.call_count == 1)
    await run.settle()
    sandbox.open()
    error = await run.result()
    assert isinstance(error, SandboxDriveSetupError)
    assert error.sandbox is None
    assert error.__cause__ is failure
    h.delete_drive.assert_not_called()
    assert error.created_drives == ["app-data"]
    assert str(error) == (
        "Sandbox creation failed: quota exceeded. "
        "Drives this call created (or may have created) are left in place: app-data."
    )


@pytest.mark.filterwarnings("ignore::FutureWarning")
async def test_failed_sandbox_never_creates_drives_still_waiting_for_its_region(h, monkeypatch):
    monkeypatch.delenv("BL_REGION", raising=False)
    failure = RuntimeError("boom")
    h.create_sandbox.side_effect = failure
    run = Running(h, {"name": "sandbox"}, mount_drives=[entry("a")])
    assert await run.result() is failure
    h.create.assert_not_called()
    h.delete_drive.assert_not_called()


async def test_failed_drive_deletes_new_drives_it_did_not_mount_and_starts_no_more(h):
    total = MOUNT_DRIVES_CONCURRENCY + 3
    cause = DriveAPIError("drive quota", status_code=429)
    sandbox, fail, rest = h.gate(), h.gate(), h.gate()
    h.create_sandbox.side_effect = effect(h, lambda *a: h.response, lambda *a: sandbox)

    def create(config):
        if id_of(config) == "d1":
            raise cause
        return h.drive(config.name)

    h.create.side_effect = effect(h, create, lambda c: fail if id_of(c) == "d1" else rest)
    mounts = [unnamed(f"d{i}") for i in range(total)] + [{"drive_name": "data", "mount_path": "/m"}]
    run = Running(h, dict(CONFIG), mount_drives=mounts)
    await run.until(lambda: h.create.call_count == MOUNT_DRIVES_CONCURRENCY)
    fail.open()
    await run.settle()
    rest.open()
    sandbox.open()
    error = await run.result()
    assert isinstance(error, SandboxDriveSetupError)
    assert error.__cause__ is cause
    assert error.sandbox.metadata.name == "sandbox"
    # Drives in flight when d1 failed finished; the queued ones were never started.
    assert h.create.call_count == MOUNT_DRIVES_CONCURRENCY
    h.mount.assert_not_called()
    assert deleted_ids(h) == ["d0", "d2", "d3", "d4"]
    h.get.assert_not_called()
    assert error.drive_names == error.created_drives == []


async def test_failed_mount_keeps_the_sandbox_and_mounted_drives_and_deletes_the_rest(h):
    cause = RuntimeError("409 mount path already in use")

    def mount(name, mount_path, *args):
        if mount_path == "/mnt/b":
            raise cause
        return h.real_mount(name, mount_path, *args)

    h.mount.side_effect = mount
    run = Running(h, dict(CONFIG), mount_drives=[unnamed("a"), unnamed("b"), unnamed("c")])
    error = await run.result()
    assert isinstance(error, SandboxDriveSetupError)
    assert error.__cause__ is cause
    assert error.sandbox.metadata.name == "sandbox"
    # The sandbox's mount list, not the failed call, says what is mounted.
    kept = sorted(c.args[0] for c in h.mount.call_args_list if c.args[1] != "/mnt/b")
    deleted = deleted_ids(h)
    # A drive whose creation had not started when b failed is never created.
    created = sorted(id_of(c.args[0]) for c in h.create.call_args_list)
    assert "b" in deleted and sorted([id_of_name(h, n) for n in kept] + deleted) == created
    assert sorted(error.drive_names) == sorted(error.created_drives) == kept
    assert h.list.call_count == 1


async def test_new_drive_whose_failed_mount_went_through_is_kept(h):
    def mount(*args):
        h.real_mount(*args)
        raise TimeoutError("read timed out")

    h.mount.side_effect = mount
    error = await Running(h, dict(CONFIG), mount_drives=[unnamed("a")]).result()
    assert isinstance(error, SandboxDriveSetupError)
    h.delete_drive.assert_not_called()
    assert [id_of_name(h, n) for n in error.created_drives] == ["a"]
    assert f"left in place: {error.created_drives[0]}." in str(error)


async def test_new_drive_is_kept_when_the_mount_list_cannot_be_read(h):
    h.mount.side_effect = TimeoutError("read timed out")
    h.list.side_effect = TimeoutError("read timed out")
    error = await Running(h, dict(CONFIG), mount_drives=[unnamed("a")]).result()
    assert isinstance(error, SandboxDriveSetupError)
    h.delete_drive.assert_not_called()
    assert [id_of_name(h, n) for n in error.created_drives] == ["a"]


async def test_new_drive_the_sandbox_does_not_list_after_a_successful_mount_is_deleted(h):
    # e.g. the path was already mounted with another drive.
    h.mount.side_effect = lambda name, *args: h.real_mount("other", *args)
    error = await Running(h, dict(CONFIG), mount_drives=[unnamed("a")]).result()
    assert isinstance(error, SandboxDriveSetupError)
    assert "/mnt/a is not mounted as requested" in str(error)
    assert deleted_ids(h) == ["a"]
    assert error.created_drives == []


async def test_drive_created_under_the_callers_name_and_not_mounted_is_kept_and_named(h):
    cause = DriveAPIError("drive quota", status_code=429)
    sandbox = h.gate()
    h.create_sandbox.side_effect = effect(h, lambda *a: h.response, lambda *a: sandbox)

    def create(config):
        if config.name == "b":
            raise cause
        return h.drive(config.name)

    h.create.side_effect = create
    run = Running(h, dict(CONFIG), mount_drives=[entry("a"), entry("b")])
    await run.until(lambda: h.create.call_count == 2)
    await run.settle()
    sandbox.open()
    error = await run.result()
    assert isinstance(error, SandboxDriveSetupError)
    assert error.__cause__ is cause
    h.mount.assert_not_called()
    h.delete_drive.assert_not_called()
    assert error.drive_names == error.created_drives == ["a"]
    assert "left in place: a." in str(error)


async def test_failed_sandbox_names_the_drives_it_could_not_delete(h):
    failure = RuntimeError("quota exceeded")
    sandbox = h.gate()
    h.create_sandbox.side_effect = effect(h, raising(failure), lambda *a: sandbox)

    def delete(name):
        if id_of_name(h, name) == "b":
            raise TimeoutError("read timed out")

    h.delete_drive.side_effect = delete
    run = Running(h, dict(CONFIG), mount_drives=[unnamed("a"), unnamed("b")])
    await run.until(lambda: h.create.call_count == 2)
    sandbox.open()
    error = await run.result()
    assert isinstance(error, SandboxDriveSetupError)
    assert error.sandbox is None
    assert error.__cause__ is failure
    assert h.delete_drive.call_count == 2
    assert [id_of_name(h, n) for n in error.created_drives] == ["b"]
    assert str(error) == (
        "Sandbox creation failed: quota exceeded. "
        f"Drives this call created (or may have created) are left in place: {error.created_drives[0]}."
    )


@pytest.mark.filterwarnings("ignore::FutureWarning")
async def test_drives_use_the_region_the_request_sends_not_bl_region(h, monkeypatch):
    # A Sandbox model is sent as is: no region, so the control plane picks one (here us-was-1).
    monkeypatch.setenv("BL_REGION", "eu-lon-1")
    sandbox = h.gate()
    h.create_sandbox.side_effect = effect(h, lambda *a: h.response, lambda *a: sandbox)
    body = Sandbox(metadata=Metadata(name="sandbox"), spec=SandboxSpec())
    run = Running(h, body, mount_drives=[entry("a")])
    await run.until(lambda: h.create_sandbox.call_count == 1)
    await run.settle()
    h.create.assert_not_called()
    sandbox.open()
    assert not isinstance(await run.result(), BaseException)
    assert h.create.call_args.args[0].region == REGION


async def test_named_drive_in_the_requested_region_is_kept_when_the_sandbox_is_elsewhere(h):
    # create_if_not_exist returns an existing sandbox as is, whatever region was requested.
    elsewhere = Sandbox(metadata=Metadata(name="sandbox"), spec=SandboxSpec(region="eu-lon-1"))
    sandbox = h.gate()
    h.create_sandbox.side_effect = effect(h, lambda *a: elsewhere, lambda *a: sandbox)

    def create(config):
        if config.name == "old":
            raise DriveAPIError("exists", status_code=409)
        return h.drive(config.name)

    h.create.side_effect = create
    mounts = [entry("new"), entry("old")]
    run = Running(h, dict(CONFIG), create_if_not_exist=True, mount_drives=mounts)
    await run.until(lambda: h.create.call_count == 2 and h.get.call_count == 1)
    await run.settle()
    sandbox.open()
    error = await run.result()
    assert isinstance(error, SandboxDriveSetupError)
    assert "is in us-was-1, but the sandbox is in eu-lon-1" in str(error)
    h.delete_drive.assert_not_called()
    assert error.drive_names == ["new", "old"]
    assert error.created_drives == ["new"]
    h.mount.assert_not_called()


async def test_drive_it_named_in_the_requested_region_is_deleted_when_the_sandbox_is_elsewhere(h):
    elsewhere = Sandbox(metadata=Metadata(name="sandbox"), spec=SandboxSpec(region="eu-lon-1"))
    h.create_sandbox.return_value = elsewhere
    error = await Running(h, dict(CONFIG), mount_drives=[unnamed("new")]).result()
    assert isinstance(error, SandboxDriveSetupError)
    assert "but the sandbox is in eu-lon-1" in str(error)
    assert deleted_ids(h) == ["new"]
    assert error.created_drives == []


@pytest.mark.filterwarnings("ignore::FutureWarning")
async def test_no_drive_is_created_when_the_sandbox_reports_no_region(h, monkeypatch):
    monkeypatch.delenv("BL_REGION", raising=False)
    h.create_sandbox.return_value = Sandbox(metadata=Metadata(name="sandbox"), spec=SandboxSpec())
    error = await Running(h, {"name": "sandbox"}, mount_drives=[entry("a")]).result()
    assert isinstance(error, SandboxDriveSetupError)
    assert "reports no region" in str(error)
    h.create.assert_not_called()


def lost():
    return TimeoutError("read timed out")


async def test_lost_create_of_an_unnamed_drive_is_looked_up_and_treated_as_its_own(h):
    h.create.side_effect = lost()
    sandbox = h.gate()
    h.create_sandbox.side_effect = effect(h, raising(RuntimeError("boom")), lambda *a: sandbox)
    run = Running(h, dict(CONFIG), mount_drives=[{"create": {}, "mount_path": "/a"}])
    await run.until(lambda: h.get.call_count == 1)
    await run.settle()
    sandbox.open()
    error = await run.result()
    assert isinstance(error, RuntimeError) and str(error) == "boom"
    name = h.create.call_args.args[0].name
    h.get.assert_called_once_with(name)
    # Found under its generated name, so it is this call's drive: deleted with the failed sandbox.
    h.delete_drive.assert_called_once_with(name)


async def test_drive_found_after_a_lost_create_is_mounted(h):
    h.create.side_effect = DriveAPIError("Bad Gateway", status_code=502)
    created = await Running(h, dict(CONFIG), mount_drives=[entry("a")]).result()
    assert not isinstance(created, BaseException), created
    h.get.assert_called_once_with("a")
    h.mount.assert_called_once()


async def test_named_drive_found_after_a_lost_create_is_never_deleted(h):
    # A chosen name may belong to a drive that existed before this call.
    h.create.side_effect = lost()
    h.mount.side_effect = RuntimeError("Mount drive failed: bad request")
    error = await Running(h, dict(CONFIG), mount_drives=[entry("a")]).result()
    assert isinstance(error, SandboxDriveSetupError)
    h.delete_drive.assert_not_called()
    assert error.drive_names == ["a"]
    assert error.created_drives == []


async def test_drive_that_may_exist_after_a_lost_create_is_named(h):
    failure = lost()
    h.create.side_effect = failure
    h.get.side_effect = DriveAPIError("Drive not found", status_code=404)
    error = await Running(h, dict(CONFIG), mount_drives=[entry("a")]).result()
    assert isinstance(error, SandboxDriveSetupError)
    assert error.__cause__ is failure
    assert error.created_drives == ["a"]
    h.delete_drive.assert_not_called()


async def test_drive_the_server_refused_to_create_is_not_looked_up(h):
    h.create.side_effect = DriveAPIError("Drives feature is not enabled", status_code=403)
    error = await Running(h, dict(CONFIG), mount_drives=[entry("a")]).result()
    assert isinstance(error, SandboxDriveSetupError)
    h.get.assert_not_called()
    assert error.created_drives == []


async def test_a_drive_whose_name_collides_with_a_generated_one_is_not_taken_over(h):
    h.create.side_effect = DriveAPIError("exists", status_code=409)
    error = await Running(
        h, dict(CONFIG), mount_drives=[{"create": {}, "mount_path": "/a"}]
    ).result()
    assert isinstance(error, SandboxDriveSetupError)
    h.get.assert_not_called()
    h.delete_drive.assert_not_called()

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


async def test_failed_sandbox_deletes_the_drives_this_call_created_and_only_those(h):
    failure = RuntimeError("quota exceeded")
    sandbox, new = h.gate(), h.gate()
    h.create_sandbox.side_effect = effect(h, raising(failure), lambda *a: sandbox)

    def create(config):
        if config.name == "old":
            raise DriveAPIError("exists", status_code=409)
        return h.drive(config.name)

    h.create.side_effect = effect(h, create, lambda config: new if config.name == "new" else None)
    mounts = [entry("new"), entry("old"), {"drive_name": "data", "mount_path": "/mnt/data"}]
    run = Running(h, dict(CONFIG), mount_drives=mounts)
    await run.until(lambda: h.create.call_count == 2 and h.get.call_count == 2)
    sandbox.open()
    # The drive still being created is waited for, then deleted.
    await run.settle()
    h.delete_drive.assert_not_called()
    new.open()
    assert await run.result() is failure
    h.delete_drive.assert_called_once_with("new")
    h.mount.assert_not_called()


@pytest.mark.filterwarnings("ignore::FutureWarning")
async def test_failed_sandbox_never_creates_drives_still_waiting_for_its_region(h, monkeypatch):
    monkeypatch.delenv("BL_REGION", raising=False)
    failure = RuntimeError("boom")
    h.create_sandbox.side_effect = failure
    run = Running(h, {"name": "sandbox"}, mount_drives=[entry("a")])
    assert await run.result() is failure
    h.create.assert_not_called()
    h.delete_drive.assert_not_called()


async def test_failed_drive_keeps_the_sandbox_starts_no_more_drives_and_reports_the_cause(h):
    total = MOUNT_DRIVES_CONCURRENCY + 3
    cause = RuntimeError("drive quota")
    sandbox, fail, rest = h.gate(), h.gate(), h.gate()
    h.create_sandbox.side_effect = effect(h, lambda *a: h.response, lambda *a: sandbox)

    def create(config):
        if config.name == "d1":
            raise cause
        return h.drive(config.name)

    h.create.side_effect = effect(h, create, lambda config: fail if config.name == "d1" else rest)
    run = Running(h, dict(CONFIG), mount_drives=[entry(f"d{i}") for i in range(total)])
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
    assert sorted(error.drive_names) == ["d0", "d2", "d3", "d4"]
    h.mount.assert_not_called()
    h.delete_drive.assert_not_called()


async def test_failed_mount_keeps_the_sandbox_and_the_other_mounts(h):
    cause = RuntimeError("409 mount path already in use")

    def mount(name, *args):
        if name == "b":
            raise cause
        return h.real_mount(name, *args)

    h.mount.side_effect = mount
    run = Running(h, dict(CONFIG), mount_drives=[entry("a"), entry("b"), entry("c")])
    error = await run.result()
    assert isinstance(error, SandboxDriveSetupError)
    assert error.__cause__ is cause
    assert sorted(error.drive_names) == ["a", "b", "c"]
    assert error.sandbox.metadata.name == "sandbox"
    h.list.assert_not_called()
    h.delete_drive.assert_not_called()

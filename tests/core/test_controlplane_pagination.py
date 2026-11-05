from types import SimpleNamespace

import pytest

from blaxel.core.client.client import Client
from blaxel.core.client.models import Drive, DriveSpec, Metadata, Sandbox, SandboxSpec
from blaxel.core.client.models.drive_list import DriveList
from blaxel.core.client.models.error import Error
from blaxel.core.client.models.job_execution import JobExecution
from blaxel.core.client.models.job_execution_list import JobExecutionList
from blaxel.core.client.models.job_execution_metadata import JobExecutionMetadata
from blaxel.core.client.models.job_execution_spec import JobExecutionSpec
from blaxel.core.client.models.lite_volume import LiteVolume
from blaxel.core.client.models.lite_volume_metadata import LiteVolumeMetadata
from blaxel.core.client.models.lite_volume_spec import LiteVolumeSpec
from blaxel.core.client.models.pagination_meta import PaginationMeta
from blaxel.core.client.models.sandbox_list import SandboxList
from blaxel.core.client.models.volume_list import VolumeList
from blaxel.core.client.types import UNSET
from blaxel.core.drive.drive import DriveAPIError, DriveInstance, SyncDriveInstance
from blaxel.core.jobs import bl_job
from blaxel.core.sandbox.default.sandbox import SandboxInstance
from blaxel.core.volume.volume import SyncVolumeInstance, VolumeAPIError, VolumeInstance


@pytest.mark.asyncio
async def test_sandbox_list_returns_page_with_next_page(monkeypatch):
    pages = [
        SandboxList(
            data=[Sandbox(metadata=Metadata(name="sandbox-a"), spec=SandboxSpec())],
            meta=PaginationMeta(has_more=True, next_cursor="cursor-2"),
        ),
        SandboxList(
            data=[Sandbox(metadata=Metadata(name="sandbox-b"), spec=SandboxSpec())],
            meta=PaginationMeta(has_more=False),
        ),
    ]
    calls = []

    async def fake_list_sandboxes(*, client, cursor=UNSET, limit=50):
        calls.append((cursor, limit))
        return pages.pop(0)

    monkeypatch.setattr("blaxel.core.sandbox.default.sandbox.list_sandboxes", fake_list_sandboxes)

    page = await SandboxInstance.list(limit=1)
    next_page = await page.next_page()

    assert [sandbox.metadata.name for sandbox in page.data] == ["sandbox-a"]
    assert page.has_more is True
    assert page.next_cursor == "cursor-2"
    assert [sandbox.metadata.name for sandbox in next_page.data] == ["sandbox-b"]
    assert next_page.has_more is False
    assert calls == [(UNSET, 1), ("cursor-2", 1)]


def test_drive_list_returns_page_with_next_page(monkeypatch):
    pages = [
        DriveList(
            data=[Drive(metadata=Metadata(name="drive-a"), spec=DriveSpec())],
            meta=PaginationMeta(has_more=True, next_cursor="cursor-2"),
        ),
        DriveList(
            data=[Drive(metadata=Metadata(name="drive-b"), spec=DriveSpec())],
            meta=PaginationMeta(has_more=False),
        ),
    ]
    calls = []

    def fake_list_drives(*, client, cursor=UNSET, limit=50):
        calls.append((cursor, limit))
        return pages.pop(0)

    monkeypatch.setattr("blaxel.core.drive.drive.list_drives_sync", fake_list_drives)

    page = SyncDriveInstance.list(limit=1)
    next_page = page.next_page()

    assert [drive.name for drive in page.data] == ["drive-a"]
    assert page.has_more is True
    assert page.next_cursor == "cursor-2"
    assert [drive.name for drive in next_page.data] == ["drive-b"]
    assert next_page.has_more is False
    assert calls == [(UNSET, 1), ("cursor-2", 1)]


def test_drive_list_raises_api_errors(monkeypatch):
    def fake_list_drives(*, client, cursor=UNSET, limit=50):
        return Error(error="boom", code=500, message="drive failed")

    monkeypatch.setattr("blaxel.core.drive.drive.list_drives_sync", fake_list_drives)

    with pytest.raises(DriveAPIError) as exc_info:
        SyncDriveInstance.list()

    assert str(exc_info.value) == "drive failed"
    assert exc_info.value.status_code == 500
    assert exc_info.value.code == "boom"


@pytest.mark.asyncio
async def test_async_drive_list_raises_api_errors(monkeypatch):
    async def fake_list_drives(*, client, cursor=UNSET, limit=50):
        return Error(error="boom", code=401, message="async drive failed")

    monkeypatch.setattr("blaxel.core.drive.drive.list_drives", fake_list_drives)

    with pytest.raises(DriveAPIError) as exc_info:
        await DriveInstance.list()

    assert str(exc_info.value) == "async drive failed"
    assert exc_info.value.status_code == 401
    assert exc_info.value.code == "boom"


def test_volume_list_raises_api_errors(monkeypatch):
    def fake_list_volumes(*, client, cursor=UNSET, limit=50):
        return Error(error="boom", code=403, message="volume failed")

    monkeypatch.setattr("blaxel.core.volume.volume.list_volumes_sync", fake_list_volumes)

    with pytest.raises(VolumeAPIError) as exc_info:
        SyncVolumeInstance.list()

    assert str(exc_info.value) == "volume failed"
    assert exc_info.value.status_code == 403
    assert exc_info.value.code == "boom"


@pytest.mark.asyncio
async def test_async_volume_list_raises_api_errors(monkeypatch):
    async def fake_list_volumes(*, client, cursor=UNSET, limit=50):
        return Error(error="boom", code=401, message="async volume failed")

    monkeypatch.setattr("blaxel.core.volume.volume.list_volumes", fake_list_volumes)

    with pytest.raises(VolumeAPIError) as exc_info:
        await VolumeInstance.list()

    assert str(exc_info.value) == "async volume failed"
    assert exc_info.value.status_code == 401
    assert exc_info.value.code == "boom"


def test_generated_list_models_accept_legacy_array_responses():
    sandbox_page = SandboxList.from_dict(
        [Sandbox(metadata=Metadata(name="sandbox-a"), spec=SandboxSpec()).to_dict()]
    )
    drive_page = DriveList.from_dict(
        [Drive(metadata=Metadata(name="drive-a"), spec=DriveSpec()).to_dict()]
    )
    volume_page = VolumeList.from_dict(
        [
            LiteVolume(
                metadata=LiteVolumeMetadata(name="volume-a"),
                spec=LiteVolumeSpec(size=10),
            ).to_dict()
        ]
    )
    execution_page = JobExecutionList.from_dict(
        [
            JobExecution(
                metadata=JobExecutionMetadata(id="execution-a"),
                spec=JobExecutionSpec(),
            ).to_dict()
        ]
    )

    assert sandbox_page is not None
    assert sandbox_page.meta is UNSET
    assert [sandbox.metadata.name for sandbox in sandbox_page.data] == ["sandbox-a"]

    assert drive_page is not None
    assert drive_page.meta is UNSET
    assert [drive.metadata.name for drive in drive_page.data] == ["drive-a"]

    assert volume_page is not None
    assert volume_page.meta is UNSET
    assert [volume.metadata.name for volume in volume_page.data] == ["volume-a"]

    assert execution_page is not None
    assert execution_page.meta is UNSET
    assert [execution.metadata.id for execution in execution_page.data] == ["execution-a"]


def test_generated_list_models_are_iterable_like_a_list():
    """Regression for SDK-PYTHON-11R.

    Iterating or index-accessing a raw ``*List`` model used to fall back to the
    ``additional_properties`` mapping and raise ``KeyError(0)`` because the model
    exposed ``__getitem__`` without ``__iter__``/``__len__``. It must now behave
    like the list of items it represents.
    """
    drive_a = Drive(metadata=Metadata(name="drive-a"), spec=DriveSpec())
    drive_b = Drive(metadata=Metadata(name="drive-b"), spec=DriveSpec())
    drive_list = DriveList(
        data=[drive_a, drive_b],
        meta=PaginationMeta(has_more=False),
    )

    # Iteration (the exact operation that raised KeyError in production).
    assert [drive.metadata.name for drive in drive_list] == ["drive-a", "drive-b"]
    # list() and unpacking rely on the same protocol.
    assert list(drive_list) == [drive_a, drive_b]
    # Integer and slice indexing.
    assert drive_list[0] is drive_a
    assert drive_list[-1] is drive_b
    assert drive_list[0:1] == [drive_a]
    # Length / truthiness.
    assert len(drive_list) == 2
    assert bool(drive_list) is True

    # String keys still address additional_properties (unchanged behaviour).
    drive_list["extra"] = "value"
    assert drive_list["extra"] == "value"
    with pytest.raises(KeyError):
        _ = drive_list["missing"]


def test_generated_list_models_iterate_empty_when_data_unset():
    """An unset/None ``data`` iterates as empty instead of raising."""
    empty_drive_list = DriveList()
    assert list(empty_drive_list) == []
    assert len(empty_drive_list) == 0
    assert bool(empty_drive_list) is False

    sandbox_list = SandboxList(data=UNSET, meta=PaginationMeta(has_more=False))
    assert list(sandbox_list) == []
    assert len(sandbox_list) == 0


def test_multiple_generated_list_models_share_iteration_fix():
    """The template-driven fix applies to every paginated ``*List`` model."""
    sandbox_list = SandboxList(
        data=[Sandbox(metadata=Metadata(name="sandbox-a"), spec=SandboxSpec())],
        meta=PaginationMeta(has_more=False),
    )
    volume_list = VolumeList(
        data=[
            LiteVolume(
                metadata=LiteVolumeMetadata(name="volume-a"),
                spec=LiteVolumeSpec(size=10),
            )
        ],
        meta=PaginationMeta(has_more=False),
    )
    execution_list = JobExecutionList(
        data=[
            JobExecution(
                metadata=JobExecutionMetadata(id="execution-a"),
                spec=JobExecutionSpec(),
            )
        ],
        meta=PaginationMeta(has_more=False),
    )

    assert [item.metadata.name for item in sandbox_list] == ["sandbox-a"]
    assert [item.metadata.name for item in volume_list] == ["volume-a"]
    assert [item.metadata.id for item in execution_list] == ["execution-a"]
    assert len(sandbox_list) == len(volume_list) == len(execution_list) == 1


def test_job_execution_list_supports_explicit_next_page(monkeypatch):
    first_execution = JobExecution(
        metadata=JobExecutionMetadata(id="execution-a"),
        spec=JobExecutionSpec(),
    )
    second_execution = JobExecution(
        metadata=JobExecutionMetadata(id="execution-b"),
        spec=JobExecutionSpec(),
    )
    pages = [
        JobExecutionList(
            data=[first_execution],
            meta=PaginationMeta(has_more=True, next_cursor="cursor-2"),
        ),
        JobExecutionList(
            data=[second_execution],
            meta=PaginationMeta(has_more=False),
        ),
    ]
    calls = []

    def fake_list_job_executions(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(
            status_code=200,
            parsed=pages.pop(0),
        )

    monkeypatch.setattr(
        "blaxel.core.jobs.list_job_executions.sync_detailed",
        fake_list_job_executions,
    )

    executions = bl_job("job-a").list_executions(limit=10, cursor="cursor-1")
    next_executions = executions.next_page()

    assert executions.data == [first_execution]
    assert executions.has_more is True
    assert executions.next_cursor == "cursor-2"
    assert next_executions.data == [second_execution]
    assert next_executions.has_more is False
    assert calls[0]["job_id"] == "job-a"
    assert calls[0]["limit"] == 10
    assert calls[0]["cursor"] == "cursor-1"
    assert calls[0]["offset"] == 0
    assert calls[1]["cursor"] == "cursor-2"
    assert calls[1]["offset"] == 0


def test_job_execution_auto_paging_iter_is_explicit(monkeypatch):
    first_execution = JobExecution(
        metadata=JobExecutionMetadata(id="execution-a"),
        spec=JobExecutionSpec(),
    )
    second_execution = JobExecution(
        metadata=JobExecutionMetadata(id="execution-b"),
        spec=JobExecutionSpec(),
    )
    pages = [
        JobExecutionList(
            data=[first_execution],
            meta=PaginationMeta(has_more=True, next_cursor="cursor-2"),
        ),
        JobExecutionList(
            data=[second_execution],
            meta=PaginationMeta(has_more=False),
        ),
    ]

    def fake_list_job_executions(**kwargs):
        return SimpleNamespace(
            status_code=200,
            parsed=pages.pop(0),
        )

    monkeypatch.setattr(
        "blaxel.core.jobs.list_job_executions.sync_detailed",
        fake_list_job_executions,
    )

    executions = list(bl_job("job-a").list_executions(limit=10).auto_paging_iter())

    assert executions == [first_execution, second_execution]


def test_job_execution_offset_is_only_sent_on_first_page(monkeypatch):
    pages = [
        JobExecutionList(
            data=[
                JobExecution(
                    metadata=JobExecutionMetadata(id="execution-a"),
                    spec=JobExecutionSpec(),
                )
            ],
            meta=PaginationMeta(has_more=True, next_cursor="cursor-2"),
        ),
        JobExecutionList(
            data=[
                JobExecution(
                    metadata=JobExecutionMetadata(id="execution-b"),
                    spec=JobExecutionSpec(),
                )
            ],
            meta=PaginationMeta(has_more=False),
        ),
    ]
    calls = []

    def fake_list_job_executions(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(
            status_code=200,
            parsed=pages.pop(0),
        )

    monkeypatch.setattr(
        "blaxel.core.jobs.list_job_executions.sync_detailed",
        fake_list_job_executions,
    )

    page = bl_job("job-a").list_executions(limit=10, offset=25)
    page.next_page()

    assert calls[0]["offset"] == 25
    assert calls[1]["offset"] == 0


@pytest.mark.asyncio
async def test_sandbox_schedules_list_returns_page_with_next_page(monkeypatch):
    from blaxel.core.client.models.sandbox_schedule_entry import SandboxScheduleEntry
    from blaxel.core.client.models.sandbox_schedule_entry_list import (
        SandboxScheduleEntryList,
    )
    from blaxel.core.sandbox.default.schedule import SandboxSchedules

    pages = [
        SandboxScheduleEntryList(
            data=[SandboxScheduleEntry(id="schedule-0")],
            meta=PaginationMeta(has_more=True, next_cursor="cursor-2"),
        ),
        SandboxScheduleEntryList(
            data=[SandboxScheduleEntry(id="schedule-1")],
            meta=PaginationMeta(has_more=False),
        ),
    ]
    calls = []

    async def fake_list(sandbox_name, *, client, cursor=UNSET, limit=UNSET, **kwargs):
        calls.append((sandbox_name, cursor, limit))
        return pages.pop(0)

    monkeypatch.setattr(
        "blaxel.core.sandbox.default.schedule.list_sandbox_schedules", fake_list
    )

    schedules = SandboxSchedules(Sandbox(metadata=Metadata(name="sbx"), spec=SandboxSpec()))
    page = await schedules.list(limit=1)
    next_page = await page.next_page()

    assert [s.id for s in page.data] == ["schedule-0"]
    assert page.has_more is True
    assert page.next_cursor == "cursor-2"
    assert [s.id for s in next_page.data] == ["schedule-1"]
    assert next_page.has_more is False
    assert calls == [("sbx", UNSET, 1), ("sbx", "cursor-2", 1)]


def test_sandbox_schedule_executions_auto_paging_iter(monkeypatch):
    from blaxel.core.client.models.sandbox_schedule_execution import (
        SandboxScheduleExecution,
    )
    from blaxel.core.client.models.sandbox_schedule_execution_list import (
        SandboxScheduleExecutionList,
    )
    from blaxel.core.sandbox.sync.schedule import SyncSandboxSchedules

    pages = [
        SandboxScheduleExecutionList(
            data=[SandboxScheduleExecution(id="exec-a")],
            meta=PaginationMeta(has_more=True, next_cursor="cursor-2"),
        ),
        SandboxScheduleExecutionList(
            data=[SandboxScheduleExecution(id="exec-b")],
            meta=PaginationMeta(has_more=False),
        ),
    ]

    def fake_list(sandbox_name, *, client, cursor=UNSET, limit=UNSET, **kwargs):
        return pages.pop(0)

    monkeypatch.setattr(
        "blaxel.core.sandbox.sync.schedule.list_sandbox_schedule_executions", fake_list
    )

    schedules = SyncSandboxSchedules(Sandbox(metadata=Metadata(name="sbx"), spec=SandboxSpec()))
    executions = list(schedules.executions(limit=1).auto_paging_iter())

    assert [e.id for e in executions] == ["exec-a", "exec-b"]


def test_client_with_headers_merges_existing_headers():
    client = Client(headers={"Blaxel-Version": "2026-04-28"})

    updated = client.with_headers({"X-Test": "yes"})

    assert client._headers == {"Blaxel-Version": "2026-04-28", "X-Test": "yes"}
    assert updated._headers == {"Blaxel-Version": "2026-04-28", "X-Test": "yes"}

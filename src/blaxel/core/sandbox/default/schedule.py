from typing import Any, Dict, List, Union

from ...client import errors
from ...client.api.compute.create_sandbox_schedule import (
    asyncio as create_sandbox_schedule,
)
from ...client.api.compute.delete_sandbox_schedule import (
    asyncio as delete_sandbox_schedule,
)
from ...client.api.compute.get_sandbox_schedule import (
    asyncio as get_sandbox_schedule,
)
from ...client.api.compute.list_sandbox_schedule_executions import (
    asyncio as list_sandbox_schedule_executions,
)
from ...client.api.compute.list_sandbox_schedules import (
    asyncio as list_sandbox_schedules,
)
from ...client.api.compute.update_sandbox_schedule import (
    asyncio as update_sandbox_schedule,
)
from ...client.client import client
from ...client.models import (
    ListSandboxSchedulesType,
    Sandbox,
    SandboxScheduleEntry,
    SandboxScheduleExecution,
)
from ...client.types import Unset


# A schedule entry is a flat record (id/type/value/input) with no sub-resource
# of its own, so methods return the raw SandboxScheduleEntry rather than a
# wrapper class. Executions are sandbox-scoped (across all schedules); filter by
# `schedule_id` on the returned records to isolate a single schedule's runs.
class SandboxSchedules:
    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    @property
    def sandbox_name(self) -> str:
        return (
            self.sandbox.metadata.name
            if self.sandbox.metadata and self.sandbox.metadata.name
            else ""
        )

    async def list(
        self,
        *,
        q: str | None = None,
        type_: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> List[SandboxScheduleEntry]:
        kwargs: Dict[str, Any] = {}
        if q is not None:
            kwargs["q"] = q
        if type_ is not None:
            kwargs["type_"] = ListSandboxSchedulesType(type_)
        if limit is not None:
            kwargs["limit"] = limit
        if cursor is not None:
            kwargs["cursor"] = cursor
        response = await list_sandbox_schedules(self.sandbox_name, client=client, **kwargs)
        if response is None:
            raise errors.UnexpectedStatus(400, b"Failed to list schedules")
        return [] if isinstance(response.data, Unset) else (response.data or [])

    async def create(
        self, schedule: Union[SandboxScheduleEntry, Dict[str, Any]]
    ) -> SandboxScheduleEntry:
        if isinstance(schedule, dict):
            schedule = SandboxScheduleEntry.from_dict(schedule)
        response = await create_sandbox_schedule(self.sandbox_name, body=schedule, client=client)
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to create schedule")

    async def get(self, schedule_id: str) -> SandboxScheduleEntry:
        response = await get_sandbox_schedule(self.sandbox_name, schedule_id, client=client)
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to get schedule")

    async def update(
        self, schedule_id: str, schedule: Union[SandboxScheduleEntry, Dict[str, Any]]
    ) -> SandboxScheduleEntry:
        if isinstance(schedule, dict):
            schedule = SandboxScheduleEntry.from_dict(schedule)
        response = await update_sandbox_schedule(
            self.sandbox_name, schedule_id, body=schedule, client=client
        )
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to update schedule")

    async def delete(self, schedule_id: str) -> SandboxScheduleEntry:
        response = await delete_sandbox_schedule(self.sandbox_name, schedule_id, client=client)
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to delete schedule")

    async def executions(
        self,
        *,
        q: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> List[SandboxScheduleExecution]:
        kwargs: Dict[str, Any] = {}
        if q is not None:
            kwargs["q"] = q
        if limit is not None:
            kwargs["limit"] = limit
        if cursor is not None:
            kwargs["cursor"] = cursor
        response = await list_sandbox_schedule_executions(
            self.sandbox_name, client=client, **kwargs
        )
        if response is None:
            raise errors.UnexpectedStatus(400, b"Failed to list schedule executions")
        return [] if isinstance(response.data, Unset) else (response.data or [])

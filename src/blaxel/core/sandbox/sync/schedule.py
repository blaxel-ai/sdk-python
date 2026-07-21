from typing import Any, Dict, Union

from ...client import errors
from ...client.api.compute.create_sandbox_schedule import sync as create_sandbox_schedule
from ...client.api.compute.delete_sandbox_schedule import sync as delete_sandbox_schedule
from ...client.api.compute.get_sandbox_schedule import sync as get_sandbox_schedule
from ...client.api.compute.list_sandbox_schedule_executions import (
    sync as list_sandbox_schedule_executions,
)
from ...client.api.compute.list_sandbox_schedules import sync as list_sandbox_schedules
from ...client.api.compute.update_sandbox_schedule import sync as update_sandbox_schedule
from ...client.client import client
from ...client.models import (
    ListSandboxSchedulesType,
    Sandbox,
    SandboxScheduleEntry,
    SandboxScheduleExecution,
)
from ...client.pagination import (
    PaginatedList,
    make_paginated_list,
    normalize_cursor,
)


# A schedule entry is a flat record (id/type/value/input) with no sub-resource
# of its own, so methods return the raw SandboxScheduleEntry rather than a
# wrapper class. Executions are sandbox-scoped (across all schedules); filter by
# `schedule_id` on the returned records to isolate a single schedule's runs.
class SyncSandboxSchedules:
    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    @property
    def sandbox_name(self) -> str:
        return (
            self.sandbox.metadata.name
            if self.sandbox.metadata and self.sandbox.metadata.name
            else ""
        )

    def list(
        self,
        *,
        q: str | None = None,
        type_: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> PaginatedList[SandboxScheduleEntry]:
        """List one page of the sandbox's schedules.

        Returns a ``PaginatedList`` exposing ``.data``, ``.meta``,
        ``.has_more``, ``.next_cursor``, ``.next_page()`` and
        ``.auto_paging_iter()``. Filters (``q``, ``type_``, ``limit``) are kept
        when advancing to the next page.
        """
        filters: Dict[str, Any] = {}
        if q is not None:
            filters["q"] = q
        if type_ is not None:
            filters["type_"] = ListSandboxSchedulesType(type_)
        if limit is not None:
            filters["limit"] = limit

        def fetch_page(page_cursor: str | None):
            response = list_sandbox_schedules(
                self.sandbox_name,
                client=client,
                cursor=normalize_cursor(page_cursor),
                **filters,
            )
            if response is None:
                raise errors.UnexpectedStatus(400, b"Failed to list schedules")
            return make_paginated_list(
                response, mapper=lambda item: item, fetch_next=fetch_page
            )

        return fetch_page(cursor)

    def create(self, schedule: Union[SandboxScheduleEntry, Dict[str, Any]]) -> SandboxScheduleEntry:
        if isinstance(schedule, dict):
            schedule = SandboxScheduleEntry.from_dict(schedule)
        response = create_sandbox_schedule(self.sandbox_name, body=schedule, client=client)
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to create schedule")

    def get(self, schedule_id: str) -> SandboxScheduleEntry:
        response = get_sandbox_schedule(self.sandbox_name, schedule_id, client=client)
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to get schedule")

    def update(
        self, schedule_id: str, schedule: Union[SandboxScheduleEntry, Dict[str, Any]]
    ) -> SandboxScheduleEntry:
        if isinstance(schedule, dict):
            schedule = SandboxScheduleEntry.from_dict(schedule)
        response = update_sandbox_schedule(
            self.sandbox_name, schedule_id, body=schedule, client=client
        )
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to update schedule")

    def delete(self, schedule_id: str) -> SandboxScheduleEntry:
        response = delete_sandbox_schedule(self.sandbox_name, schedule_id, client=client)
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to delete schedule")

    def executions(
        self,
        *,
        q: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> PaginatedList[SandboxScheduleExecution]:
        """List one page of schedule executions, newest first.

        Returns a ``PaginatedList`` exposing ``.data``, ``.meta``,
        ``.has_more``, ``.next_cursor``, ``.next_page()`` and
        ``.auto_paging_iter()``. Executions are sandbox-scoped across all
        schedules; filter by ``schedule_id`` on the records to isolate one.
        """
        filters: Dict[str, Any] = {}
        if q is not None:
            filters["q"] = q
        if limit is not None:
            filters["limit"] = limit

        def fetch_page(page_cursor: str | None):
            response = list_sandbox_schedule_executions(
                self.sandbox_name,
                client=client,
                cursor=normalize_cursor(page_cursor),
                **filters,
            )
            if response is None:
                raise errors.UnexpectedStatus(400, b"Failed to list schedule executions")
            return make_paginated_list(
                response, mapper=lambda item: item, fetch_next=fetch_page
            )

        return fetch_page(cursor)

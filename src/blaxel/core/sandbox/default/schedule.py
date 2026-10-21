from typing import Any, Dict, Union

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
from ...client.pagination import (
    AsyncPaginatedList,
    make_async_paginated_list,
    normalize_cursor,
)


# A schedule entry is a flat record (id/type/value/input) with no sub-resource
# of its own, so methods return the raw SandboxScheduleEntry rather than a
# wrapper class. Executions are sandbox-scoped (across all schedules); filter by
# `schedule_id` on the returned records to isolate a single schedule's runs.
class SandboxSchedules:
    """Run commands in a sandbox on a schedule.

    Reach it as ``sandbox.schedules``. Each schedule has a ``type`` and a
    ``value``: ``"cron"`` with a 5-field cron expression (``"0 8 * * 1-5"``),
    ``"at"`` with an RFC 3339 datetime, or ``"sleep"`` with a duration from
    now (``"30m"``, ``"2h"``), turned into ``"at"`` on creation. ``input``
    holds the process to run: ``command``, ``name``, ``working_dir``,
    ``env``, ``timeout`` (seconds, default 600, 0 for none) and
    ``keep_alive`` (default True). Every call goes to the control plane. An
    error status raises ``blaxel.core.client.errors.UnexpectedStatus``, and
    so does an empty response, with status 400.

    Example:
        ```python
        entry = await sandbox.schedules.create(
            {"type": "cron", "value": "0 8 * * 1-5", "input": {"command": "python report.py"}}
        )
        runs = await sandbox.schedules.executions()
        ```
    """

    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    @property
    def sandbox_name(self) -> str:
        """Name of the sandbox these schedules belong to."""
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
    ) -> AsyncPaginatedList[SandboxScheduleEntry]:
        """List one page of the sandbox's schedules.

        Returns an ``AsyncPaginatedList`` exposing ``.data``, ``.meta``,
        ``.has_more``, ``.next_cursor``, ``.next_page()`` and
        ``.auto_paging_iter()``. Filters (``q``, ``type_``, ``limit``) are kept
        when advancing to the next page.

        Args:
            q: Optional text filter.
            type_: Optional schedule type: ``"cron"``, ``"at"`` or ``"sleep"``.
            limit: Maximum number of schedules in this page.
            cursor: Cursor from a previous page. Leave unset for the first page.
        """
        filters: Dict[str, Any] = {}
        if q is not None:
            filters["q"] = q
        if type_ is not None:
            filters["type_"] = ListSandboxSchedulesType(type_)
        if limit is not None:
            filters["limit"] = limit

        async def fetch_page(page_cursor: str | None):
            response = await list_sandbox_schedules(
                self.sandbox_name,
                client=client,
                cursor=normalize_cursor(page_cursor),
                **filters,
            )
            if response is None:
                raise errors.UnexpectedStatus(400, b"Failed to list schedules")
            return make_async_paginated_list(
                response, mapper=lambda item: item, fetch_next=fetch_page
            )

        return await fetch_page(cursor)

    async def create(
        self, schedule: Union[SandboxScheduleEntry, Dict[str, Any]]
    ) -> SandboxScheduleEntry:
        """Create a schedule.

        Args:
            schedule: A ``SandboxScheduleEntry`` or a dict with ``type``,
                ``value``, ``input`` and optional ``id`` (generated when
                omitted) and ``max_executions`` (execution records kept,
                default 100).

        Returns:
            The created ``SandboxScheduleEntry``, with its ``id``.
        """
        if isinstance(schedule, dict):
            schedule = SandboxScheduleEntry.from_dict(schedule)
        response = await create_sandbox_schedule(self.sandbox_name, body=schedule, client=client)
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to create schedule")

    async def get(self, schedule_id: str) -> SandboxScheduleEntry:
        """Get a schedule by ID.

        Environment values in ``input.env`` are masked in the response.
        """
        response = await get_sandbox_schedule(self.sandbox_name, schedule_id, client=client)
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to get schedule")

    async def update(
        self, schedule_id: str, schedule: Union[SandboxScheduleEntry, Dict[str, Any]]
    ) -> SandboxScheduleEntry:
        """Replace a schedule's timing and input.

        Send the whole entry: fields left out are not kept. The ID stays
        the same. An ``env`` value still holding the mask from a read keeps
        its stored secret.

        Args:
            schedule_id: ID of the schedule to update.
            schedule: The new entry, in any form :meth:`create` accepts.

        Returns:
            The updated ``SandboxScheduleEntry``.
        """
        if isinstance(schedule, dict):
            schedule = SandboxScheduleEntry.from_dict(schedule)
        response = await update_sandbox_schedule(
            self.sandbox_name, schedule_id, body=schedule, client=client
        )
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to update schedule")

    async def delete(self, schedule_id: str) -> SandboxScheduleEntry:
        """Delete a schedule; it stops running.

        Returns:
            The deleted ``SandboxScheduleEntry``.
        """
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
    ) -> AsyncPaginatedList[SandboxScheduleExecution]:
        """List one page of schedule executions, newest first.

        Returns an ``AsyncPaginatedList`` exposing ``.data``, ``.meta``,
        ``.has_more``, ``.next_cursor``, ``.next_page()`` and
        ``.auto_paging_iter()``. Executions are sandbox-scoped across all
        schedules; filter by ``schedule_id`` on the records to isolate one.

        Args:
            q: Optional text filter.
            limit: Maximum number of executions in this page.
            cursor: Cursor from a previous page. Leave unset for the first page.
        """
        filters: Dict[str, Any] = {}
        if q is not None:
            filters["q"] = q
        if limit is not None:
            filters["limit"] = limit

        async def fetch_page(page_cursor: str | None):
            response = await list_sandbox_schedule_executions(
                self.sandbox_name,
                client=client,
                cursor=normalize_cursor(page_cursor),
                **filters,
            )
            if response is None:
                raise errors.UnexpectedStatus(400, b"Failed to list schedule executions")
            return make_async_paginated_list(
                response, mapper=lambda item: item, fetch_next=fetch_page
            )

        return await fetch_page(cursor)

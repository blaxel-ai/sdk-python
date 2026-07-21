"""Integration test for the sandbox schedules sub-resource.

Exercises the full SDK surface against a real control plane:
create / list / get / update / delete plus executions(), and the one backend
behavior that is synchronous (so checkable without waiting): a "sleep" schedule
is resolved to an absolute "at" at creation time.

It deliberately does NOT wait for schedules to fire. Firing is driven by AWS
EventBridge Scheduler whose granularity is 1 minute, so observing a real firing
(let alone a recurring cron, which needs two ticks) cannot be done in a short,
non-flaky test. That end-to-end firing check lives in the controlplane
`e2e-sandbox-scheduling` skill. This test stays under ~1 minute.

    BL_WORKSPACE=main uv run pytest \
        tests/integration/core/sandbox/test_schedules.py -v -s
"""

from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, default_region, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestScheduleCrud:
    """Full schedule CRUD surface against a deployed control plane."""

    sandbox: SandboxInstance

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": unique_name("sched-test"),
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        yield
        try:
            await self.sandbox.delete()
        except Exception:
            pass

    async def test_schedule_crud_surface(self):
        schedules = self.sandbox.schedules
        at_iso = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

        # --- create the three timing types -----------------------------------
        cron = await schedules.create(
            {
                "type": "cron",
                "value": "0 8 * * 1-5",
                "input": {"command": "echo cron", "keep_alive": True, "timeout": 60},
            }
        )
        assert cron.id
        assert cron.type_.value == "cron"
        assert cron.value == "0 8 * * 1-5"
        cron_id = cron.id

        at = await schedules.create(
            {
                "type": "at",
                "value": at_iso,
                "input": {"command": "echo at", "keep_alive": True, "timeout": 60},
            }
        )
        assert at.id
        at_id = at.id

        sleep_entry = await schedules.create(
            {
                "type": "sleep",
                "value": "30s",
                "input": {"command": "echo sleep", "keep_alive": True, "timeout": 60},
            }
        )
        assert sleep_entry.id
        sleep_id = sleep_entry.id
        # Backend resolves "sleep" to an absolute "at" synchronously at creation.
        assert sleep_entry.type_.value == "at", (
            f"sleep should resolve to 'at', got {sleep_entry.type_.value}"
        )
        assert datetime.fromisoformat(sleep_entry.value.replace("Z", "+00:00"))

        # --- list shows all three --------------------------------------------
        ids = {s.id for s in await schedules.list()}
        assert {cron_id, at_id, sleep_id} <= ids

        # --- get round-trips --------------------------------------------------
        fetched = await schedules.get(cron_id)
        assert fetched.id == cron_id
        assert fetched.value == "0 8 * * 1-5"

        # --- update reflected -------------------------------------------------
        updated = await schedules.update(
            cron_id,
            {
                "type": "cron",
                "value": "30 9 * * 1-5",
                "input": {"command": "echo cron-updated", "keep_alive": True, "timeout": 60},
            },
        )
        assert updated.value == "30 9 * * 1-5"
        assert updated.input_.command == "echo cron-updated"

        # --- executions endpoint reachable (empty before any firing) ---------
        executions = await schedules.executions()
        assert isinstance(executions, list)

        # --- delete empties the list -----------------------------------------
        for s in await schedules.list():
            await schedules.delete(s.id)
        remaining = {s.id for s in await schedules.list()}
        assert not ({cron_id, at_id, sleep_id} & remaining)

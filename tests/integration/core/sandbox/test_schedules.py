"""End-to-end test for sandbox schedules.

Mirrors the controlplane `e2e-sandbox-scheduling` skill (standard suite, no
stress): it does not just exercise CRUD, it verifies the AWS EventBridge
Scheduler actually fires the scheduled process inside the sandbox for all three
timing types:

  cron   - "* * * * *" must fire MORE THAN ONCE (recurring)
  at     - one-off at now+~30s, fires once
  sleep  - "30s", resolved by the backend to an absolute "at", fires once

Firing is counted from the sandbox PROCESS API: each schedule runs
`echo <unique-marker>`, so one process per firing carries that marker. No shell,
filesystem, or keep-awake dependency.

Requires a real environment (dev or prod) -- the local stack does not implement
EventBridge. Run with, e.g.:

    BL_ENV=dev BL_WORKSPACE=chris uv run pytest \
        tests/integration/core/sandbox/test_schedules.py -v -s

Runtime ~3-4 min (EventBridge cron granularity is 1 minute, so two ticks need
~2 minutes plus SQS/lambda latency).
"""

import asyncio
import json
import time
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, default_region, unique_name

ONESHOT_TIMEOUT_S = 150
CRON_TIMEOUT_S = 210
DELETE_CHECK_WAIT_S = 130


@pytest.mark.asyncio(loop_scope="class")
class TestScheduleFiring:
    """Full schedule lifecycle + real firing against a deployed control plane."""

    sandbox: SandboxInstance
    run_id: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.run_id = unique_name("")[-8:]
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": unique_name("sched-e2e"),
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        await request.cls.sandbox.wait(max_wait=120000, interval=2000)
        yield
        try:
            await self.sandbox.delete()
        except Exception:
            pass

    async def _find_firings(self, marker: str) -> list:
        """Processes whose command carries the marker (one per firing)."""
        for attempt in range(3):
            try:
                procs = await self.sandbox.process.list()
                return [p for p in procs if marker in json.dumps(p.to_dict())]
            except Exception:
                if attempt == 2:
                    return []
                await asyncio.sleep(2)
        return []

    async def _wait_for_firings(
        self, marker: str, minimum: int, timeout_s: int, label: str
    ) -> list:
        deadline = time.monotonic() + timeout_s
        procs: list = []
        while time.monotonic() < deadline:
            procs = await self._find_firings(marker)
            if len(procs) >= minimum:
                return procs
            await asyncio.sleep(5)
        raise AssertionError(
            f"{label}: expected >= {minimum} firing(s), saw {len(procs)} after {timeout_s}s"
        )

    @staticmethod
    def _assert_went_through(procs: list, label: str):
        bad = next((p for p in procs if p.exit_code not in (None, 0)), None)
        assert bad is None, f"{label}: process exited {bad.exit_code} (status={bad.status})"

    async def test_schedule_firing_lifecycle(self):
        run = self.run_id
        cron_mark = f"SCHEDMARK-CRON-{run}"
        at_mark = f"SCHEDMARK-AT-{run}"
        sleep_mark = f"SCHEDMARK-SLEEP-{run}"
        schedules = self.sandbox.schedules

        # Align to ~10s before the next minute boundary so the two cron ticks
        # land close together (cap the wait so we never burn a whole minute).
        ms_into_minute = (time.time() % 60) * 1000
        wait_ms = (50000 - ms_into_minute + 60000) % 60000
        if 0 < wait_ms <= 50000:
            await asyncio.sleep(wait_ms / 1000)

        at_iso = (datetime.now(timezone.utc) + timedelta(seconds=30)).strftime("%Y-%m-%dT%H:%M:%SZ")

        # --- create the three timing types -----------------------------------
        cron = await schedules.create(
            {
                "type": "cron",
                "value": "* * * * *",
                "input": {"command": f"echo {cron_mark}", "keep_alive": True, "timeout": 60},
            }
        )
        assert cron.id
        cron_id = cron.id

        at = await schedules.create(
            {
                "type": "at",
                "value": at_iso,
                "input": {"command": f"echo {at_mark}", "keep_alive": True, "timeout": 60},
            }
        )
        assert at.id
        at_id = at.id

        sleep_entry = await schedules.create(
            {
                "type": "sleep",
                "value": "30s",
                "input": {"command": f"echo {sleep_mark}", "keep_alive": True, "timeout": 60},
            }
        )
        assert sleep_entry.id
        sleep_id = sleep_entry.id
        # Backend resolves "sleep" to an absolute "at".
        assert sleep_entry.type_.value == "at", (
            f"sleep should resolve to 'at', got {sleep_entry.type_.value}"
        )
        assert datetime.fromisoformat(sleep_entry.value.replace("Z", "+00:00"))

        # --- list shows all three --------------------------------------------
        listed = await schedules.list()
        assert len(listed) == 3, f"expected 3 schedules, got {len(listed)}"

        # --- verify real firing ----------------------------------------------
        self._assert_went_through(
            await self._wait_for_firings(at_mark, 1, ONESHOT_TIMEOUT_S, "at"), "at"
        )
        self._assert_went_through(
            await self._wait_for_firings(sleep_mark, 1, ONESHOT_TIMEOUT_S, "sleep"), "sleep"
        )
        cron_procs = await self._wait_for_firings(cron_mark, 2, CRON_TIMEOUT_S, "cron")
        self._assert_went_through(cron_procs, "cron")

        # --- execution history ------------------------------------------------
        execs = await schedules.executions()
        assert len(execs) >= 3, f"expected >= 3 executions, got {len(execs)}"
        assert all(200 <= e.status_code < 400 for e in execs), "execution with non-2xx status"
        assert cron_id in {e.schedule_id for e in execs}, "no execution recorded for cron"

        # --- one-off schedules auto-delete after firing, cron remains ---------
        ids_after_fire = {s.id for s in await schedules.list()}
        assert at_id not in ids_after_fire, "at schedule should be deleted after firing"
        assert sleep_id not in ids_after_fire, "sleep schedule should be deleted after firing"
        assert cron_id in ids_after_fire, "cron schedule should still exist"

        # --- update the cron --------------------------------------------------
        updated = await schedules.update(
            cron_id,
            {
                "type": "cron",
                "value": "* * * * *",
                "input": {
                    "command": f"echo {cron_mark}-updated",
                    "keep_alive": True,
                    "timeout": 60,
                },
            },
        )
        assert updated.input_.command == f"echo {cron_mark}-updated"

        # --- deleting the cron stops further firings --------------------------
        before = len(await self._find_firings(cron_mark))
        await schedules.delete(cron_id)
        await asyncio.sleep(DELETE_CHECK_WAIT_S)  # ~2 cron ticks
        after = len(await self._find_firings(cron_mark))
        # Tolerate at most one SQS message that was already in flight.
        assert after <= before + 1, (
            f"cron still firing after delete: {before} -> {after} (not removed from AWS)"
        )

        # --- list empties -----------------------------------------------------
        for s in await schedules.list():
            await schedules.delete(s.id)
        assert len(await schedules.list()) == 0

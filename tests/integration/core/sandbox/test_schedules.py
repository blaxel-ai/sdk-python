import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestScheduleOperations:
    """Test sandbox schedule CRUD operations against a real control plane."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.sandbox_name = unique_name("schedule-test")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": default_image,
                "memory": 2048,
                "labels": default_labels,
            }
        )

        yield

        try:
            await self.sandbox.delete()
        except Exception:
            pass

    async def test_schedule_crud_lifecycle(self):
        """create -> list -> get -> update -> delete round-trip."""
        created = await self.sandbox.schedules.create(
            {
                "type": "cron",
                "value": "0 8 * * 1-5",
                "input": {"command": "echo hello", "working_dir": "/blaxel"},
            }
        )
        assert created.id
        assert created.type_.value == "cron"
        assert created.value == "0 8 * * 1-5"
        schedule_id = created.id

        listed = await self.sandbox.schedules.list()
        assert any(s.id == schedule_id for s in listed)

        fetched = await self.sandbox.schedules.get(schedule_id)
        assert fetched.id == schedule_id
        assert fetched.value == "0 8 * * 1-5"

        updated = await self.sandbox.schedules.update(
            schedule_id,
            {
                "type": "cron",
                "value": "30 9 * * 1-5",
                "input": {"command": "echo updated", "working_dir": "/blaxel"},
            },
        )
        assert updated.value == "30 9 * * 1-5"

        await self.sandbox.schedules.delete(schedule_id)
        remaining = await self.sandbox.schedules.list()
        assert all(s.id != schedule_id for s in remaining)

    async def test_executions_returns_list(self):
        """executions() is sandbox-scoped and returns a list (empty is fine)."""
        executions = await self.sandbox.schedules.executions()
        assert isinstance(executions, list)

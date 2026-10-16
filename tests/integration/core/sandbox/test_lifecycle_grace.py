import pytest

from blaxel.core import SandboxInstance
from tests.helpers import (
    default_image,
    default_labels,
    unique_name,
)


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxLifecycleGrace:
    """Test the termination and standby grace periods of a sandbox."""

    async def test_creates_sandbox_with_grace_periods(self):
        name = unique_name("lifecycle-grace")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "termination_grace_period_seconds": 30,
                "standby_grace_period_seconds": 30,
                "labels": default_labels,
            }
        )

        try:
            retrieved = await SandboxInstance.get(name)
            assert retrieved.spec.runtime.termination_grace_period_seconds == 30
            assert retrieved.spec.runtime.standby_grace_period_seconds == 30
        finally:
            await SandboxInstance.delete(name)

    async def test_rejects_standby_grace_above_limit(self):
        name = unique_name("lifecycle-grace-too-long")
        with pytest.raises(Exception, match="standbyGracePeriodSeconds"):
            await SandboxInstance.create(
                {
                    "name": name,
                    "image": default_image,
                    "standby_grace_period_seconds": 301,
                    "labels": default_labels,
                }
            )

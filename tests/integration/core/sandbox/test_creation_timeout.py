"""Integration tests for the per-request creation timeout on sandbox creation.

``timeout`` is forwarded to the control plane as ``X-Blaxel-Creation-Timeout``;
when the sandbox is not ready in time the creation is cancelled with a 408 that
the SDK raises as ``SandboxCreationTimeoutError``. A healthy creation is well
within the cap, so what is exercised here is that a creation carrying the header
succeeds end to end and that the cap is enforced before any request is made.
"""

import pytest

from blaxel.core import SandboxInstance
from blaxel.core.sandbox import MAX_CREATION_TIMEOUT_SECONDS
from tests.helpers import default_image, default_labels, default_region, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestCreationTimeout:
    """Test creating a sandbox with a per-request creation timeout."""

    async def test_creates_with_a_creation_timeout(self):
        name = unique_name("create-timeout")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            },
            timeout=MAX_CREATION_TIMEOUT_SECONDS,
        )
        try:
            assert sandbox.metadata.name == name
            assert str(sandbox.status) == "DEPLOYED"
            result = await sandbox.process.exec({"command": "echo ok", "waitForCompletion": True})
            assert (result.logs or "").strip() == "ok"
        finally:
            await SandboxInstance.delete(name)

    async def test_rejects_a_timeout_above_the_cap_before_calling_the_api(self):
        with pytest.raises(ValueError, match="between 1 and 50"):
            await SandboxInstance.create(
                {
                    "name": unique_name("create-timeout-cap"),
                    "image": default_image,
                    "region": default_region,
                    "labels": default_labels,
                },
                timeout=MAX_CREATION_TIMEOUT_SECONDS + 1,
            )

    async def test_creates_with_a_retry_budget(self):
        """A healthy creation succeeds on the first attempt even with retries allowed."""
        name = unique_name("create-retry")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            },
            timeout=MAX_CREATION_TIMEOUT_SECONDS,
            retry=1,
        )
        try:
            assert sandbox.metadata.name == name
            assert str(sandbox.status) == "DEPLOYED"
        finally:
            await SandboxInstance.delete(name)

    async def test_rejects_retry_without_timeout_before_calling_the_api(self):
        with pytest.raises(ValueError, match="requires 'timeout'"):
            await SandboxInstance.create(
                {"name": unique_name("create-retry-cap"), "labels": default_labels},
                retry=1,
            )

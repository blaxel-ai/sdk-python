import asyncio
from datetime import datetime, timedelta, timezone

import pytest

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import async_sleep, default_image, default_labels, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxLifecycleAndExpiration:
    """Test sandbox lifecycle and expiration."""

    created_sandboxes: list[str] = []

    @pytest.fixture(autouse=True)
    async def cleanup(self):
        """Clean up all sandboxes after each test class."""
        yield
        # Clean up all sandboxes in parallel
        await asyncio.gather(
            *[
                self._safe_delete(name)
                for name in TestSandboxLifecycleAndExpiration.created_sandboxes
            ],
            return_exceptions=True,
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.clear()

    async def _safe_delete(self, name: str) -> None:
        """Safely delete a sandbox, ignoring errors."""
        try:
            await SandboxInstance.delete(name)
        except Exception:
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestTTL(TestSandboxLifecycleAndExpiration):
    """Test TTL (time-to-live) configuration."""

    async def test_creates_sandbox_with_ttl_string(self):
        """Test creating a sandbox with TTL string."""
        name = unique_name("ttl-string")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "ttl": "5m",
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        assert sandbox.metadata.name == name

        await async_sleep(0.1)

        # Verify sandbox is running
        status = await SandboxInstance.get(name)
        assert status.status != "TERMINATED"

    async def test_creates_sandbox_with_expires_date(self):
        """Test creating a sandbox with expires date."""
        name = unique_name("expires-date")
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "expires": expires_at,
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        assert sandbox.metadata.name == name


@pytest.mark.asyncio(loop_scope="class")
class TestExpirationPolicies(TestSandboxLifecycleAndExpiration):
    """Test expiration policies configuration."""

    async def test_creates_sandbox_with_ttl_max_age_policy(self):
        """Test creating a sandbox with ttl-max-age policy."""
        name = unique_name("maxage-policy")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "lifecycle": {
                    "expiration_policies": [
                        {"type": "ttl-max-age", "value": "10m", "action": "delete"},
                    ],
                },
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        assert sandbox.metadata.name == name

    async def test_creates_sandbox_with_date_expiration_policy(self):
        """Test creating a sandbox with date expiration policy."""
        name = unique_name("date-policy")
        expiration_date = datetime.now(timezone.utc) + timedelta(minutes=10)

        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "lifecycle": {
                    "expiration_policies": [
                        {"type": "date", "value": expiration_date.isoformat(), "action": "delete"},
                    ],
                },
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        assert sandbox.metadata.name == name

    async def test_creates_sandbox_with_ttl_idle_policy(self):
        """Test creating a sandbox with ttl-idle policy."""
        name = unique_name("idle-policy")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "lifecycle": {
                    "expiration_policies": [
                        {"type": "ttl-idle", "value": "5m", "action": "delete"},
                    ],
                },
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        assert sandbox.metadata.name == name

    async def test_creates_sandbox_with_multiple_policies(self):
        """Test creating a sandbox with multiple policies."""
        name = unique_name("multi-policy")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "lifecycle": {
                    "expiration_policies": [
                        {"type": "ttl-idle", "value": "5m", "action": "delete"},
                        {"type": "ttl-max-age", "value": "30m", "action": "delete"},
                    ],
                },
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        assert sandbox.metadata.name == name

    async def test_supports_various_duration_formats(self):
        """Test that various duration formats are supported."""
        durations = ["30s", "5m", "1h"]

        for duration in durations:
            # Extract numeric part for unique name
            numeric_part = "".join(c for c in duration if c.isdigit())
            name = unique_name(f"dur-{numeric_part}")
            sandbox = await SandboxInstance.create(
                {
                    "name": name,
                    "image": default_image,
                    "lifecycle": {
                        "expiration_policies": [
                            {"type": "ttl-max-age", "value": duration, "action": "delete"},
                        ],
                    },
                    "labels": default_labels,
                }
            )
            TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

            assert sandbox.metadata.name == name


@pytest.mark.asyncio(loop_scope="class")
class TestTTLExpirationBehavior(TestSandboxLifecycleAndExpiration):
    """Test TTL expiration behavior."""

    async def test_sandbox_terminates_after_ttl_expires(self):
        """Test that sandbox terminates after TTL expires."""
        name = unique_name("ttl-expire")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "ttl": "1s",
                "labels": default_labels,
            }
        )
        # Don't add to created_sandboxes - we expect it to auto-delete

        # Wait for TTL + buffer (cron runs every minute)
        await async_sleep(1.1)

        # This should not fail - create a new sandbox with the same name
        sbx = await SandboxInstance.create({"name": name, "labels": default_labels})
        assert sbx.metadata.name == name
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)


@pytest.mark.asyncio(loop_scope="class")
class TestSnapshotConfiguration(TestSandboxLifecycleAndExpiration):
    """Test snapshot configuration."""

    async def test_creates_sandbox_with_snapshots_enabled(self):
        """Test creating a sandbox with snapshots enabled."""
        name = unique_name("snapshot-on")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "snapshot_enabled": True,
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        assert sandbox.metadata.name == name

    async def test_creates_sandbox_with_snapshots_disabled(self):
        """Test creating a sandbox with snapshots disabled."""
        name = unique_name("snapshot-off")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "snapshot_enabled": False,
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        assert sandbox.metadata.name == name

import asyncio
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio

from blaxel.core.client.models import (
    ExpirationPolicy,
    ExpirationPolicyAction,
    ExpirationPolicyType,
    SandboxLifecycle,
)
from blaxel.core.sandbox import SandboxInstance
from tests.helpers import (
    async_sleep,
    default_image,
    default_labels,
    unique_name,
    wait_for_sandbox_deployed,
)


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxLifecycleAndExpiration:
    """Test sandbox lifecycle and expiration."""

    created_sandboxes: list[str] = []

    @pytest_asyncio.fixture(autouse=True)
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


@pytest.mark.asyncio(loop_scope="class")
class TestUpdateTTLPreservesState(TestSandboxLifecycleAndExpiration):
    """Test that updateTTL preserves sandbox state (files)."""

    async def test_update_ttl_does_not_recreate_sandbox_files_preserved(self):
        """Test that updateTTL does not recreate sandbox - files are preserved."""
        name = unique_name("update-ttl")
        test_file_path = "/tmp/ttl-test-file.txt"
        test_content = f"unique-content-{datetime.now().timestamp()}"

        # Create sandbox with initial TTL
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "ttl": "10m",
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        assert sandbox.metadata.name == name

        # Write a file to the sandbox
        await sandbox.fs.write(test_file_path, test_content)

        # Verify file was written
        content_before = await sandbox.fs.read(test_file_path)
        assert content_before == test_content

        # Update TTL to a new value
        await SandboxInstance.update_ttl(name, "30m")

        # Wait for sandbox to be deployed after update
        await async_sleep(0.2)
        await wait_for_sandbox_deployed(name)
        updated_sandbox = await SandboxInstance.get(name)

        # Verify sandbox still exists and has same name
        assert updated_sandbox.metadata.name == name

        # CRITICAL: Verify the file still exists with same content
        # If the sandbox was recreated, this file would not exist
        content_after = await updated_sandbox.fs.read(test_file_path)
        assert content_after == test_content

    async def test_update_ttl_multiple_times_preserves_files(self):
        """Test that updating TTL multiple times preserves files."""
        name = unique_name("multi-ttl")
        test_file_path = "/tmp/multi-ttl-test.txt"
        test_content = f"multi-update-content-{datetime.now().timestamp()}"

        # Create sandbox
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "ttl": "5m",
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        # Write a file
        await sandbox.fs.write(test_file_path, test_content)

        # Update TTL multiple times
        await SandboxInstance.update_ttl(name, "10m")
        await wait_for_sandbox_deployed(name)

        await SandboxInstance.update_ttl(name, "15m")
        await wait_for_sandbox_deployed(name)

        await SandboxInstance.update_ttl(name, "20m")
        await wait_for_sandbox_deployed(name)
        final_sandbox = await SandboxInstance.get(name)

        # File should still be there
        content = await final_sandbox.fs.read(test_file_path)
        assert content == test_content


@pytest.mark.asyncio(loop_scope="class")
class TestUpdateLifecyclePreservesState(TestSandboxLifecycleAndExpiration):
    """Test that updateLifecycle preserves sandbox state (files)."""

    async def test_update_lifecycle_does_not_recreate_sandbox_files_preserved(self):
        """Test that updateLifecycle does not recreate sandbox - files are preserved."""
        name = unique_name("update-lifecycle")
        test_file_path = "/tmp/lifecycle-test-file.txt"
        test_content = f"lifecycle-content-{datetime.now().timestamp()}"

        # Create sandbox with initial lifecycle policy
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "lifecycle": {
                    "expiration_policies": [
                        {"type": "ttl-max-age", "value": "10m", "action": "delete"}
                    ]
                },
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        assert sandbox.metadata.name == name

        # Write a file to the sandbox
        await sandbox.fs.write(test_file_path, test_content)

        # Verify file was written
        content_before = await sandbox.fs.read(test_file_path)
        assert content_before == test_content

        # Update lifecycle to a new policy
        new_lifecycle = SandboxLifecycle(
            expiration_policies=[{"type": "ttl-max-age", "value": "30m", "action": "delete"}]
        )
        await SandboxInstance.update_lifecycle(name, new_lifecycle)

        # Wait for sandbox to be deployed after update
        await async_sleep(0.2)
        await wait_for_sandbox_deployed(name)
        updated_sandbox = await SandboxInstance.get(name)

        # Verify sandbox still exists and has same name
        assert updated_sandbox.metadata.name == name

        # CRITICAL: Verify the file still exists with same content
        # If the sandbox was recreated, this file would not exist
        content_after = await updated_sandbox.fs.read(test_file_path)
        assert content_after == test_content

    async def test_update_lifecycle_with_different_policy_types_preserves_files(self):
        """Test that changing lifecycle policy types preserves files."""
        name = unique_name("lifecycle-change")
        test_file_path = "/tmp/lifecycle-change-test.txt"
        test_content = f"policy-change-content-{datetime.now().timestamp()}"

        # Create sandbox with ttl-idle policy
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "lifecycle": {
                    "expiration_policies": [{"type": "ttl-idle", "value": "5m", "action": "delete"}]
                },
                "labels": default_labels,
            }
        )
        TestSandboxLifecycleAndExpiration.created_sandboxes.append(name)

        # Write a file
        await sandbox.fs.write(test_file_path, test_content)

        # Change to a different policy type
        new_lifecycle = SandboxLifecycle(
            expiration_policies=[
                ExpirationPolicy(
                    type_=ExpirationPolicyType.TTL_MAX_AGE,
                    value="20m",
                    action=ExpirationPolicyAction.DELETE,
                ),
                ExpirationPolicy(
                    type_=ExpirationPolicyType.TTL_IDLE,
                    value="10m",
                    action=ExpirationPolicyAction.DELETE,
                ),
                ExpirationPolicy(
                    type_=ExpirationPolicyType.TTL_IDLE,
                    value="10m",
                    action=ExpirationPolicyAction.DELETE,
                ),
            ]
        )
        await SandboxInstance.update_lifecycle(name, new_lifecycle)

        # Wait for sandbox to be deployed after update
        await async_sleep(0.2)
        await wait_for_sandbox_deployed(name)
        updated_sandbox = await SandboxInstance.get(name)

        # File should still be there
        content = await updated_sandbox.fs.read(test_file_path)
        assert content == test_content

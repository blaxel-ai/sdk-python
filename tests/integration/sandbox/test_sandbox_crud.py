import asyncio

import pytest

from blaxel.core import SandboxInstance
from blaxel.core.sandbox.types import SandboxUpdateMetadata
from tests.helpers import (
    default_image,
    default_labels,
    default_region,
    unique_name,
    wait_for_sandbox_deletion,
)

# =============================================================================
# Sandbox Create Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxCreate:
    """Test sandbox creation operations."""

    async def test_creates_sandbox_with_default_settings(self):
        """Test creating a sandbox with default settings."""
        sandbox = await SandboxInstance.create({"labels": default_labels})

        try:
            assert sandbox.metadata.name is not None
            assert sandbox.metadata.name.startswith("sandbox-")
        finally:
            await SandboxInstance.delete(sandbox.metadata.name)

    async def test_creates_sandbox_with_custom_name(self):
        """Test creating a sandbox with a custom name."""
        name = unique_name("custom")
        sandbox = await SandboxInstance.create({"name": name, "labels": default_labels})

        try:
            assert sandbox.metadata.name == name
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_specific_image(self):
        """Test creating a sandbox with a specific image."""
        name = unique_name("image-test")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "labels": default_labels,
            }
        )

        try:
            assert sandbox.metadata.name == name
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_memory_configuration(self):
        """Test creating a sandbox with memory configuration."""
        name = unique_name("memory-test")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "memory": 2048,
                "labels": default_labels,
            }
        )

        try:
            retrieved = await SandboxInstance.get(name)
            assert retrieved.spec.runtime.memory == 2048
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_labels(self):
        """Test creating a sandbox with labels."""
        name = unique_name("labels-test")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "labels": {**default_labels, "env": "test", "purpose": "integration"},
            }
        )

        try:
            assert sandbox.metadata.labels["env"] == "test"
            assert sandbox.metadata.labels["purpose"] == "integration"
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_ports(self):
        """Test creating a sandbox with ports."""
        name = unique_name("ports-test")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "memory": 2048,
                "ports": [
                    {"name": "web", "target": 3000},
                    {"name": "api", "target": 8080, "protocol": "TCP"},
                ],
                "labels": default_labels,
            }
        )

        try:
            retrieved = await SandboxInstance.get(name)
            assert len(retrieved.spec.runtime.ports) == 2
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_environment_variables(self):
        """Test creating a sandbox with environment variables."""
        name = unique_name("envs-test")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "envs": [
                    {"name": "NODE_ENV", "value": "test"},
                    {"name": "DEBUG", "value": "true"},
                ],
                "labels": default_labels,
            }
        )

        try:
            retrieved = await SandboxInstance.get(name)
            assert len(retrieved.spec.runtime.envs) == 2
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_region(self):
        """Test creating a sandbox with a region."""
        name = unique_name("region-test")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "region": default_region,
                "labels": default_labels,
            }
        )

        try:
            retrieved = await SandboxInstance.get(name)
            assert retrieved.spec.region == default_region
        finally:
            await SandboxInstance.delete(name)


# =============================================================================
# Sandbox CreateIfNotExists Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxCreateIfNotExists:
    """Test createIfNotExists operations."""

    async def test_creates_new_sandbox_if_not_exists(self):
        """Test creating a new sandbox if it doesn't exist."""
        name = unique_name("cine")
        sandbox = await SandboxInstance.create_if_not_exists(
            {"name": name, "labels": default_labels}
        )

        try:
            assert sandbox.metadata.name == name
        finally:
            await SandboxInstance.delete(name)

    async def test_returns_existing_sandbox_if_exists(self):
        """Test returning existing sandbox if it already exists."""
        name = unique_name("cine-existing")

        # Create first
        first = await SandboxInstance.create({"name": name, "labels": default_labels})

        try:
            # create_if_not_exists should return the same sandbox
            second = await SandboxInstance.create_if_not_exists(
                {"name": name, "labels": default_labels}
            )
            assert second.metadata.name == first.metadata.name
        finally:
            await SandboxInstance.delete(name)

    async def test_handles_concurrent_create_if_not_exists_calls(self):
        """Test handling concurrent createIfNotExists calls."""
        name = unique_name("cine-race")
        concurrent_calls = 5

        async def create_task():
            try:
                sb = await SandboxInstance.create_if_not_exists(
                    {"name": name, "labels": default_labels}
                )
                return {"sandbox": sb, "error": None}
            except Exception as e:
                return {"sandbox": None, "error": e}

        results = await asyncio.gather(
            *[create_task() for _ in range(concurrent_calls)],
            return_exceptions=True,
        )

        try:
            successes = [r for r in results if isinstance(r, dict) and r.get("sandbox") is not None]
            unique_names = set(r["sandbox"].metadata.name for r in successes)

            assert len(unique_names) == 1
            assert len(successes) >= 2

            sandbox = await SandboxInstance.get(name)
            result = await sandbox.process.exec(
                {"command": "echo 'test'", "wait_for_completion": True}
            )
            assert result.logs == "test\n"
        finally:
            await SandboxInstance.delete(name)


# =============================================================================
# Sandbox Get Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxGet:
    """Test sandbox get operations."""

    async def test_retrieves_existing_sandbox(self):
        """Test retrieving an existing sandbox."""
        name = unique_name("get-test")
        await SandboxInstance.create({"name": name, "labels": default_labels})

        try:
            retrieved = await SandboxInstance.get(name)
            assert retrieved.metadata.name == name
        finally:
            await SandboxInstance.delete(name)

    async def test_throws_error_for_non_existent_sandbox(self):
        """Test that getting a non-existent sandbox raises an error."""
        with pytest.raises(Exception):
            await SandboxInstance.get("non-existent-sandbox-xyz")


# =============================================================================
# Sandbox List Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxList:
    """Test sandbox list operations."""

    async def test_lists_all_sandboxes(self):
        """Test listing all sandboxes."""
        name = unique_name("list-test")
        await SandboxInstance.create({"name": name, "labels": default_labels})

        try:
            sandboxes = await SandboxInstance.list()
            assert isinstance(sandboxes, list)

            found = next((s for s in sandboxes if s.metadata.name == name), None)
            assert found is not None
        finally:
            await SandboxInstance.delete(name)


# =============================================================================
# Sandbox Delete Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxDelete:
    """Test sandbox delete operations."""

    async def test_deletes_existing_sandbox(self):
        """Test deleting an existing sandbox."""
        name = unique_name("delete-test")
        await SandboxInstance.create({"name": name, "labels": default_labels})

        await SandboxInstance.delete(name)

        # Wait for deletion to fully complete
        deleted = await wait_for_sandbox_deletion(name)
        assert deleted is True

    async def test_can_delete_using_instance_method(self):
        """Test deleting using instance method."""
        name = unique_name("delete-instance")
        sandbox = await SandboxInstance.create({"name": name, "labels": default_labels})

        await sandbox.delete()

        # Wait for deletion to fully complete
        deleted = await wait_for_sandbox_deletion(name)
        assert deleted is True


# =============================================================================
# Sandbox UpdateMetadata Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxUpdateMetadata:
    """Test sandbox updateMetadata operations."""

    async def test_updates_sandbox_labels(self):
        """Test updating sandbox labels."""
        name = unique_name("update-meta")
        await SandboxInstance.create({"name": name, "labels": default_labels})

        try:
            updated = await SandboxInstance.update_metadata(
                name,
                SandboxUpdateMetadata(labels={**default_labels, "updated": "true"}),
            )
            assert updated.metadata.labels["updated"] == "true"
        finally:
            await SandboxInstance.delete(name)

    async def test_updates_sandbox_display_name(self):
        """Test updating sandbox displayName."""
        name = unique_name("update-display")
        await SandboxInstance.create({"name": name, "labels": default_labels})

        try:
            updated = await SandboxInstance.update_metadata(
                name,
                SandboxUpdateMetadata(display_name="My Test Sandbox"),
            )
            assert updated.metadata.display_name == "My Test Sandbox"
        finally:
            await SandboxInstance.delete(name)


# =============================================================================
# Sandbox Wait Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxWait:
    """Test sandbox wait operations."""

    async def test_waits_for_sandbox_to_be_ready(self):
        """Test waiting for sandbox to be ready."""
        name = unique_name("wait-test")
        sandbox = await SandboxInstance.create({"name": name, "labels": default_labels})

        try:
            # After wait, sandbox should be ready and we can run commands
            result = await sandbox.process.exec(
                {"command": "echo 'ready'", "wait_for_completion": True}
            )
            assert "ready" in result.logs
        finally:
            await SandboxInstance.delete(name)

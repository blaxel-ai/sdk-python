"""Pytest configuration for integration tests."""

import asyncio

import pytest
import pytest_asyncio


@pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
async def reset_client():
    """Reset the global client's async httpx client before each test class.

    This is needed because the SDK uses a global client singleton that caches
    the httpx.AsyncClient. When tests run in sequence with different event loops,
    the cached client becomes stale and causes "Event loop is closed" errors.
    """
    # Reset the async client before each test class
    from blaxel.core.client.client import client

    client._async_client = None

    yield

    # Optionally close and reset after test class
    if client._async_client is not None:
        try:
            await client._async_client.aclose()
        except Exception:
            pass
        client._async_client = None


def pytest_sessionfinish(session, exitstatus):
    """Clean up all test sandboxes after the test session ends.

    With pytest-xdist, this only runs on the master node after all workers finish.
    """
    # Skip cleanup on worker nodes (pytest-xdist)
    # Workers have workerinput attribute, master doesn't
    if hasattr(session.config, "workerinput"):
        return

    from blaxel.core.client.client import client
    from blaxel.core.sandbox import SandboxInstance
    from blaxel.core.volume import VolumeInstance

    async def cleanup_test_resources():
        """Delete all sandboxes and volumes with test labels."""
        # Reset client for cleanup
        client._async_client = None

        print("\n🧹 Cleaning up test resources...")

        # Clean up sandboxes with test labels
        try:
            sandboxes = await SandboxInstance.list()
            for sb in sandboxes:
                labels = sb.metadata.labels
                # Labels are stored in additional_properties of MetadataLabels object
                if labels is not None:
                    props = getattr(labels, "additional_properties", {}) or {}
                    if props.get("env") == "integration-test":
                        try:
                            await SandboxInstance.delete(sb.metadata.name)
                        except Exception:
                            pass
        except Exception as e:
            print(f"  Error listing sandboxes: {e}")

        # Clean up volumes with test labels
        try:
            volumes = await VolumeInstance.list()
            for vol in volumes:
                labels = vol.metadata.labels if hasattr(vol, "metadata") and vol.metadata else None
                # Labels are stored in additional_properties of MetadataLabels object
                if labels is not None:
                    props = getattr(labels, "additional_properties", {}) or {}
                    if props.get("env") == "integration-test":
                        try:
                            await VolumeInstance.delete(vol.name)
                        except Exception:
                            pass
        except Exception as e:
            print(f"  Error listing volumes: {e}")

        # Close the client
        if client._async_client is not None:
            try:
                await client._async_client.aclose()
            except Exception:
                pass
            client._async_client = None

        print("✅ Cleanup complete!")

    # Run cleanup in a new event loop
    try:
        asyncio.run(cleanup_test_resources())
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")


# Mark all tests in this module as integration tests
def pytest_collection_modifyitems(config, items):
    """Add integration marker to all tests in this directory."""
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

"""Pytest configuration for core integration tests."""

import asyncio


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
                            await sb.delete()
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
                            await vol.delete()  # type: ignore[attr-defined]
                        except Exception:
                            pass
        except Exception as e:
            print(f"  Error listing volumes: {e}")

        # Close the client
        if client._async_client is not None:
            client._async_client = None

        print("✅ Cleanup complete!")

    # Run cleanup in a new event loop
    try:
        asyncio.run(cleanup_test_resources())
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")

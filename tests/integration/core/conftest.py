"""Pytest configuration for core integration tests."""

import asyncio


def pytest_sessionfinish(session, exitstatus):
    """Clean up the sandboxes this run created.

    With pytest-xdist, this only runs on the master node after all workers finish.

    Only sandboxes tagged with this run's ``run-id`` are deleted, plus stale
    orphans from runs that crashed. CI runs several pull requests against the
    same workspace: deleting every ``env=integration-test`` sandbox would tear
    down sandboxes a concurrent run is still using.
    """
    # Skip cleanup on worker nodes (pytest-xdist)
    # Workers have workerinput attribute, master doesn't
    if hasattr(session.config, "workerinput"):
        return

    from blaxel.core.client.client import client
    from blaxel.core.sandbox import SandboxInstance
    from tests.helpers import is_stale_orphan, resource_labels, run_id

    def is_ours(resource) -> bool:
        labels = resource_labels(resource)
        if labels.get("run-id") == run_id:
            return True
        return labels.get("created-by") == "pytest" and is_stale_orphan(resource)

    async def cleanup_test_resources():
        """Delete this run's sandboxes, plus stale orphans."""
        # Reset client for cleanup
        client._async_client = None

        print("\n🧹 Cleaning up test resources...")

        # Volumes are not swept here: the list endpoint returns LiteVolumeMetadata,
        # which carries no labels, so there is no way to tell ours apart without a
        # GET per volume. Volume tests delete what they create in their own
        # class-level fixtures.
        try:
            page = await SandboxInstance.list()
            # Walk every page: one page holds 50 sandboxes and the shared
            # workspace routinely holds more than that.
            ours = [sb async for sb in page.auto_paging_iter() if is_ours(sb)]
        except Exception as e:
            print(f"  Error listing sandboxes: {e}")
            ours = []
        await asyncio.gather(
            *(sb.delete() for sb in ours),
            return_exceptions=True,
        )

        # Close the client
        if client._async_client is not None:
            client._async_client = None

        print("✅ Cleanup complete!")

    # Run cleanup in a new event loop
    try:
        asyncio.run(cleanup_test_resources())
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")

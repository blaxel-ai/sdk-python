"""Pytest configuration for core integration tests."""

import asyncio
from datetime import datetime, timedelta, timezone

# Orphans older than this were left behind by a crashed run, never by a live one.
ORPHAN_MAX_AGE = timedelta(hours=2)


def _labels(resource) -> dict:
    metadata = getattr(resource, "metadata", None)
    labels = getattr(metadata, "labels", None) if metadata else None
    return getattr(labels, "additional_properties", {}) or {}


def _is_stale_orphan(resource) -> bool:
    """True for a pytest resource old enough that no live run still needs it."""
    created_at = getattr(getattr(resource, "metadata", None), "created_at", None)
    if not isinstance(created_at, str):
        return False
    try:
        # Timestamps come back with nanosecond precision, which fromisoformat
        # rejects on older Pythons -- truncate to microseconds.
        head, _, tail = created_at.partition(".")
        created = datetime.fromisoformat(f"{head}.{tail[:6]}+00:00" if tail else f"{head}+00:00")
    except ValueError:
        return False
    return datetime.now(timezone.utc) - created > ORPHAN_MAX_AGE


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
    from tests.helpers import run_id

    def is_ours(resource) -> bool:
        labels = _labels(resource)
        if labels.get("run-id") == run_id:
            return True
        return labels.get("created-by") == "pytest" and _is_stale_orphan(resource)

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
            sandboxes = await SandboxInstance.list()
        except Exception as e:
            print(f"  Error listing sandboxes: {e}")
            sandboxes = []
        await asyncio.gather(
            *(sb.delete() for sb in sandboxes if is_ours(sb)),
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

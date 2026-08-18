"""Test utility functions."""

import asyncio
import os
import time
import uuid
from datetime import datetime, timedelta, timezone

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.volume import VolumeInstance

# Environment-aware configuration
env = os.environ.get("BL_ENV", "prod")
default_region = "eu-dub-1" if env == "dev" else "us-pdx-1"
default_image = "blaxel/base-image:latest"

# Unique per pytest run. CI runs of several PRs share one workspace, so the
# end-of-session cleanup must only delete what *this* run created -- deleting by
# ``env=integration-test`` alone tears down sandboxes a concurrent run is still
# using, which is a large part of the suite's cross-run flakiness.
#
# Kept in the environment rather than in module state so that pytest-xdist
# workers, which import this module in their own process, share the master's id
# instead of minting one each. Otherwise the master's teardown -- the only one
# that runs -- would match nothing the workers created.
run_id = os.environ.setdefault("BL_TEST_RUN_ID", uuid.uuid4().hex[:12])

# Default labels to identify test sandboxes in the UI
default_labels = {
    "env": "integration-test",
    "created-by": "pytest",
    "run-id": run_id,
}


def unique_name(prefix: str = "test") -> str:
    """Generate a unique sandbox/volume name for testing."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


async def wait_for_sandbox_deployed(sandbox_name: str, max_attempts: int = 30) -> bool:
    """
    Wait for a sandbox to be deployed by polling until status is DEPLOYED.

    Args:
        sandbox_name: The name of the sandbox to wait for
        max_attempts: Maximum number of attempts to wait (default: 30 seconds)

    Returns:
        True if deployed, False if timeout
    """
    attempts = 0

    while attempts < max_attempts:
        sandbox = await SandboxInstance.get(sandbox_name)
        if sandbox.status == "DEPLOYED":
            return True
        await async_sleep(1)
        attempts += 1

    print(f"Timeout waiting for {sandbox_name} to be deployed")
    return False


async def wait_for_sandbox_deletion(sandbox_name: str, max_attempts: int = 30) -> bool:
    """
    Wait for a sandbox deletion to complete by polling until the sandbox either
    (a) no longer exists (GET raises) or (b) has transitioned to the
    ``TERMINATED`` status — which the SDK itself treats as "not existing"
    (see ``SandboxInstance.create_if_not_exists``). This avoids waiting for the
    backend tombstone after the sandbox is already semantically gone.

    Args:
        sandbox_name: The name of the sandbox to wait for deletion
        max_attempts: Maximum number of attempts to wait (default: 30 seconds)

    Returns:
        True if deletion completed, False if timeout
    """
    attempts = 0

    while attempts < max_attempts:
        try:
            sandbox = await SandboxInstance.get(sandbox_name)
            if getattr(sandbox, "status", None) == "TERMINATED":
                return True
            await async_sleep(1)
            attempts += 1
        except Exception:
            return True

    print(f"Timeout waiting for {sandbox_name} deletion to complete")
    return False


async def wait_for_volume_deletion(volume_name: str, max_attempts: int = 30) -> bool:
    """
    Wait for a volume deletion to fully complete by polling until the volume no longer exists.

    Args:
        volume_name: The name of the volume to wait for deletion
        max_attempts: Maximum number of attempts to wait (default: 30 seconds)

    Returns:
        True if deletion completed, False if timeout
    """
    attempts = 0

    while attempts < max_attempts:
        try:
            await VolumeInstance.get(volume_name)
            # If we get here, volume still exists, wait and try again
            await async_sleep(1)
            attempts += 1
        except Exception:
            # If get throws an error, the volume no longer exists
            return True

    print(f"Timeout waiting for {volume_name} deletion to complete")
    return False


# Orphans older than this were left behind by a crashed run, never by a live one.
ORPHAN_MAX_AGE = timedelta(hours=2)


def resource_labels(resource) -> dict:
    """Labels of a sandbox/volume, or an empty dict when the API omits them."""
    metadata = getattr(resource, "metadata", None)
    labels = getattr(metadata, "labels", None) if metadata else None
    return getattr(labels, "additional_properties", {}) or {}


def is_stale_orphan(resource, now: datetime | None = None) -> bool:
    """True for a pytest resource old enough that no live run still needs it."""
    created_at = getattr(getattr(resource, "metadata", None), "created_at", None)
    if not isinstance(created_at, str):
        return False
    try:
        # Timestamps arrive as RFC3339 with a trailing Z and up to nanosecond
        # precision, both of which fromisoformat rejects on Python 3.10: drop
        # the Z and truncate the fraction to microseconds.
        head, _, tail = created_at.rstrip("Zz").partition(".")
        created = datetime.fromisoformat(f"{head}.{tail[:6]}+00:00" if tail else f"{head}+00:00")
    except ValueError:
        return False
    return (now or datetime.now(timezone.utc)) - created > ORPHAN_MAX_AGE


async def wait_until(predicate, timeout: float = 10.0, interval: float = 0.1) -> bool:
    """Poll ``predicate`` until it is true or ``timeout`` elapses.

    Callbacks (watch events, log streams) usually fire in well under a second,
    but a fixed sleep turns a slow round-trip into a test failure. Polling keeps
    the fast path fast and the slow path green.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        await asyncio.sleep(interval)
    return predicate()


def sleep(seconds: float) -> None:
    """Synchronous sleep helper."""
    time.sleep(seconds)


async def async_sleep(seconds: float) -> None:
    """Async sleep helper."""
    await asyncio.sleep(seconds)

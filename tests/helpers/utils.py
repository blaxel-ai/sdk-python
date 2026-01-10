"""Test utility functions."""

import asyncio
import os
import time
import uuid

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.volume import VolumeInstance

# Environment-aware configuration
env = os.environ.get("BL_ENV", "prod")
default_region = "eu-dub-1" if env == "dev" else "us-pdx-1"
default_image = "blaxel/base-image:latest"

# Default labels to identify test sandboxes in the UI
default_labels = {
    "env": "integration-test",
    "created-by": "pytest",
}


def unique_name(prefix: str = "test") -> str:
    """Generate a unique sandbox/volume name for testing."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


async def wait_for_sandbox_deletion(sandbox_name: str, max_attempts: int = 30) -> bool:
    """
    Wait for a sandbox deletion to fully complete by polling until the sandbox no longer exists.

    Args:
        sandbox_name: The name of the sandbox to wait for deletion
        max_attempts: Maximum number of attempts to wait (default: 30 seconds)

    Returns:
        True if deletion completed, False if timeout
    """
    attempts = 0

    while attempts < max_attempts:
        try:
            await SandboxInstance.get(sandbox_name)
            # If we get here, sandbox still exists, wait and try again
            await async_sleep(1)
            attempts += 1
        except Exception:
            # If get throws an error, the sandbox no longer exists
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


def sleep(seconds: float) -> None:
    """Synchronous sleep helper."""
    time.sleep(seconds)


async def async_sleep(seconds: float) -> None:
    """Async sleep helper."""
    await asyncio.sleep(seconds)

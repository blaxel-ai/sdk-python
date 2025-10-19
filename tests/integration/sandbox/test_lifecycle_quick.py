#!/usr/bin/env python3
"""Quick test to verify lifecycle configuration works correctly."""

import asyncio
import os

from blaxel.core import SandboxInstance
from blaxel.core.client.models import ExpirationPolicy, SandboxLifecycle

# Determine the base image based on environment
BL_ENV = os.environ.get("BL_ENV", "prod")
BASE_IMAGE = "blaxel/base:latest"


async def test_basic_lifecycle():
    """Test basic lifecycle creation without waiting for expiration."""
    print(f"Testing basic lifecycle creation with {BASE_IMAGE} (BL_ENV={BL_ENV})")

    # Create a simple lifecycle with ttl-max-age
    ttl_policy = ExpirationPolicy(
        type_="ttl-max-age",
        value="5m",
        action="delete"
    )
    lifecycle = SandboxLifecycle(
        expiration_policies=[ttl_policy]
    )

    print(f"Creating sandbox with lifecycle: {lifecycle.to_dict()}")

    try:
        # Create sandbox with lifecycle
        sandbox = await SandboxInstance.create({
            "lifecycle": lifecycle,
            "image": BASE_IMAGE,
            "name": "test-lifecycle-quick"
        })

        print(f"✅ Sandbox created successfully: {sandbox.metadata.name}")
        print(f"   Status: {sandbox.status}")
        print(f"   Spec: {sandbox.spec.to_dict() if sandbox.spec else 'None'}")

        # Test process exec to activate idle monitoring (if ttl-idle was used)
        result = await sandbox.process.exec({"command": "echo 'Hello from sandbox!'"})
        print(f"✅ Process exec successful: pid={result.pid}, exit_code={result.exit_code}")

        # Clean up
        await SandboxInstance.delete(sandbox.metadata.name)
        print(f"✅ Sandbox cleaned up: {sandbox.metadata.name}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_multiple_policies():
    """Test creating sandbox with multiple expiration policies."""
    print("\nTesting multiple expiration policies...")

    policies = [
        ExpirationPolicy(type_="ttl-idle", value="5m", action="delete"),
        ExpirationPolicy(type_="ttl-max-age", value="10m", action="delete"),
    ]
    lifecycle = SandboxLifecycle(expiration_policies=policies)

    try:
        sandbox = await SandboxInstance.create({
            "lifecycle": lifecycle,
            "image": BASE_IMAGE,
            "name": "test-multiple-policies"
        })

        print(f"✅ Sandbox with multiple policies created: {sandbox.metadata.name}")

        # Activate idle monitoring with a process exec
        result = await sandbox.process.exec({"command": "ls /"})
        print(f"✅ Idle monitoring activated: pid={result.pid}")

        # Clean up
        await SandboxInstance.delete(sandbox.metadata.name)
        print(f"✅ Sandbox cleaned up: {sandbox.metadata.name}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    print("=== Quick Lifecycle Test for Python SDK ===\n")

    success_count = 0

    # Test 1: Basic lifecycle
    if await test_basic_lifecycle():
        success_count += 1

    # Test 2: Multiple policies
    if await test_multiple_policies():
        success_count += 1

    print(f"\n=== Results: {success_count}/2 tests passed ===")

    if success_count == 2:
        print("✅ All tests passed!")
        exit(0)
    else:
        print("❌ Some tests failed")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())

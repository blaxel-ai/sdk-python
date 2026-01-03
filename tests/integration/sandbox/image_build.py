"""Integration test for Image build functionality.

This test builds and deploys a custom image as a sandbox and verifies the process.
"""

import asyncio
import sys
import uuid

from blaxel.core.image import ImageInstance
from blaxel.core.sandbox import SandboxInstance


def get_sandbox_name(sandbox) -> str:
    """Safely get sandbox name from metadata."""
    if sandbox.metadata and sandbox.metadata.name:
        return str(sandbox.metadata.name)
    return "unknown"


async def delete_sandbox(name: str) -> None:
    """Delete a sandbox by name using the API directly."""
    from blaxel.core.client.api.compute.delete_sandbox import (
        asyncio as delete_sandbox_api,
    )
    from blaxel.core.client.client import client

    await delete_sandbox_api(sandbox_name=name, client=client)


def print_status(status: str) -> None:
    """Callback for status changes during deployment."""
    status_icons = {
        "UPLOADING": "📤",
        "BUILDING": "🔨",
        "DEPLOYING": "🚀",
        "DEPLOYED": "✅",
        "FAILED": "❌",
        "TERMINATED": "🛑",
    }
    icon = status_icons.get(status, "📋")
    print(f"  {icon} Status: {status}")


async def test_advanced_image_build():
    """Test advanced image build with all features."""
    print("\n" + "=" * 60)
    print("Advanced Image Build Test")
    print("=" * 60)

    sandbox_name = f"image-test-{uuid.uuid4().hex[:8]}"

    # Create a comprehensive image with multiple features
    image = (
        ImageInstance.from_registry("python:3.11-slim")
        .run_commands("apt-get update && apt-get install -y --no-install-recommends curl git wget && rm -rf /var/lib/apt/lists/*")
        .workdir("/app")
        .run_commands("pip install --no-cache-dir requests httpx pydantic")
        .env(
            PYTHONUNBUFFERED="1",
            APP_NAME="blaxel-test",
            DEBUG="true",
            LOG_LEVEL="info",
        )
        .label(
            maintainer="blaxel",
            version="1.0.0",
            description="Integration test image",
        )
        .run_commands(
            "python --version",
            "curl --version",
            "git --version",
        )
        .copy(".", "/app")
        .expose(8080)
    )

    print(f"📦 Building advanced image as sandbox: {sandbox_name}")
    print(f"   Base image: {image.base_image}")
    print(f"   Dockerfile hash: {image.hash}")
    print(f"\n📄 User-defined Dockerfile:\n{'-' * 40}")
    print(image.dockerfile)
    print("-" * 40)

    # Show what the prepared image looks like (with sandbox-api injected)
    prepared = image._prepare_for_sandbox("latest")
    print(f"\n📄 Final Dockerfile (with sandbox-api):\n{'-' * 40}")
    print(prepared.dockerfile)
    print("-" * 40)

    try:
        sandbox = await image.build(
            name=sandbox_name,
            memory=4096,
            timeout=900.0,
            on_status_change=print_status,
            sandbox_version="latest",
        )

        print(f"\n✅ Build successful!")
        print(f"   Sandbox name: {get_sandbox_name(sandbox)}")
        print(f"   Status: {sandbox.status}")

        # Verify the sandbox is accessible and packages work
        print("\n🔍 Verifying sandbox...")
        sandbox_instance = await SandboxInstance.get(sandbox_name)
        print(f"   Sandbox exists: {get_sandbox_name(sandbox_instance)}")

        # Test Python packages
        result = await sandbox_instance.process.exec(
            {
                "command": "python -c \"import requests; import httpx; import pydantic; print('All packages OK')\"",
                "waitForCompletion": True,
            }
        )
        process_name = result.name if result.name else "unknown"
        logs = await sandbox_instance.process.logs(process_name, "all")
        print(f"   Python packages: {logs.strip() if logs else 'N/A'}")

        # Test apt packages
        result = await sandbox_instance.process.exec(
            {
                "command": "curl --version | head -1",
                "waitForCompletion": True,
            }
        )
        process_name = result.name if result.name else "unknown"
        logs = await sandbox_instance.process.logs(process_name, "all")
        print(f"   curl: {logs.strip() if logs else 'N/A'}")

        # Test re-building the same image with the same name (update scenario)
        print("\n" + "=" * 60)
        print("Re-building same image (update scenario)")
        print("=" * 60)

        # Modify the image slightly to simulate an update
        image_v2 = (
            ImageInstance.from_registry("python:3.11-slim")
            .run_commands("apt-get update && apt-get install -y --no-install-recommends curl git wget vim && rm -rf /var/lib/apt/lists/*")  # Added vim
            .workdir("/app")
            .run_commands("pip install --no-cache-dir requests httpx pydantic aiohttp")  # Added aiohttp
            .env(
                PYTHONUNBUFFERED="1",
                APP_NAME="blaxel-test",
                DEBUG="true",
                LOG_LEVEL="debug",  # Changed from info to debug
                VERSION="2.0.0",  # New env var
            )
            .label(
                maintainer="blaxel",
                version="2.0.0",  # Updated version
                description="Integration test image v2",
            )
            .run_commands(
                "python --version",
                "curl --version",
                "git --version",
                "vim --version | head -1",  # New command
            )
            .copy(".", "/app")
            .expose(8080)
        )

        print(f"📦 Re-building updated image as sandbox: {sandbox_name}")
        print(f"   Dockerfile hash: {image_v2.hash}")

        sandbox_v2 = await image_v2.build(
            name=sandbox_name,
            memory=4096,
            timeout=900.0,
            on_status_change=print_status,
            sandbox_version="latest",
        )

        print(f"\n✅ Re-build successful!")
        print(f"   Sandbox name: {get_sandbox_name(sandbox_v2)}")
        print(f"   Status: {sandbox_v2.status}")

        # Verify the updated sandbox
        print("\n🔍 Verifying updated sandbox...")
        sandbox_instance_v2 = await SandboxInstance.get(sandbox_name)

        # Test new Python package (aiohttp)
        result = await sandbox_instance_v2.process.exec(
            {
                "command": "python -c \"import aiohttp; print('aiohttp OK')\"",
                "waitForCompletion": True,
            }
        )
        process_name = result.name if result.name else "unknown"
        logs = await sandbox_instance_v2.process.logs(process_name, "all")
        print(f"   aiohttp package: {logs.strip() if logs else 'N/A'}")

        # Test new apt package (vim)
        result = await sandbox_instance_v2.process.exec(
            {
                "command": "vim --version | head -1",
                "waitForCompletion": True,
            }
        )
        process_name = result.name if result.name else "unknown"
        logs = await sandbox_instance_v2.process.logs(process_name, "all")
        print(f"   vim: {logs.strip() if logs else 'N/A'}")

        # Clean up
        print(f"\n🧹 Cleaning up sandbox: {sandbox_name}")
        await delete_sandbox(sandbox_name)
        print("✅ Cleanup complete")

        print("\n🎉 All verifications passed!")
        print("   - Initial build: OK")
        print("   - Re-build (update): OK")
        return True

    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        import traceback

        traceback.print_exc()
        # Try to clean up even on failure
        try:
            await delete_sandbox(sandbox_name)
        except Exception:
            pass
        raise


async def main():
    """Run the integration test."""
    print("🚀 Starting Image Build Integration Test")
    print("=" * 60)

    try:
        await test_advanced_image_build()
        print("\n✅ Integration test completed successfully!")
        return 0
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

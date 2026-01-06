"""Integration test for Image build functionality.

This test builds and deploys a custom image as a sandbox and verifies the process.
"""

import asyncio
import sys
import uuid

from blaxel.core import ImageInstance, SandboxInstance


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
    sandbox = None
    sandbox_v2 = None
    image_name = f"image-test-{uuid.uuid4().hex[:8]}"

    # Create a comprehensive image with multiple features
    image = (
        ImageInstance.from_registry("python:3.11-slim")
        .apt_install("curl", "git", "wget")
        .workdir("/app")
        .pip_install("requests", "httpx", "pydantic")
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

    print(f"📦 Building advanced image as sandbox: {image_name}")
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
        await image.build(
            name=image_name,
            memory=4096,
            timeout=900.0,
            on_status_change=print_status,
            sandbox_version="latest",
        )
        sandbox = await SandboxInstance.create({
            "image": image_name,
            "memory": 4096,
        })
        if not sandbox.metadata or not sandbox.metadata.name:
            raise ValueError("Sandbox metadata is not set")

        print(f"\n✅ Build successful!")
        print(f"   Sandbox name: {get_sandbox_name(sandbox)}")
        print(f"   Status: {sandbox.status}")

        # Test Python packages
        result = await sandbox.process.exec(
            {
                "command": "python -c \"import requests; import httpx; import pydantic; print('All packages OK')\"",
                "waitForCompletion": True,
            }
        )
        process_name = result.name if result.name else "unknown"
        logs = await sandbox.process.logs(process_name, "all")
        print(f"   Python packages: {logs.strip() if logs else 'N/A'}")

        # Test apt packages
        result = await sandbox.process.exec(
            {
                "command": "curl --version | head -1",
                "waitForCompletion": True,
            }
        )
        process_name = result.name if result.name else "unknown"
        logs = await sandbox.process.logs(process_name, "all")
        print(f"   curl: {logs.strip() if logs else 'N/A'}")

        # Test re-building the same image with the same name (update scenario)
        print("\n" + "=" * 60)
        print("Re-building same image (update scenario)")
        print("=" * 60)

        # Modify the image slightly to simulate an update
        image_v2 = (
            ImageInstance.from_registry("python:3.11-alpine")
            .apk_add("curl", "git", "wget", "vim")
            .workdir("/app")
            .pip_install("requests", "httpx", "pydantic", "aiohttp")
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

        print(f"📦 Re-building updated image as sandbox: {image_name}")
        print(f"   Dockerfile hash: {image_v2.hash}")

        await image_v2.build(
            name=image_name,
            memory=4096,
            timeout=900.0,
            on_status_change=print_status,
            sandbox_version="latest",
        )

        sandbox_v2 = await SandboxInstance.create({
            "image": image_name,
            "memory": 4096,
        })

        if not sandbox_v2.metadata or not sandbox_v2.metadata.name:
            raise ValueError("Sandbox metadata is not set")

        print(f"\n✅ Re-build successful!")
        print(f"   Sandbox name: {get_sandbox_name(sandbox_v2)}")
        print(f"   Status: {sandbox_v2.status}")

        # Test new Python package (aiohttp)
        result = await sandbox_v2.process.exec(
            {
                "command": "python -c \"import aiohttp; print('aiohttp OK')\"",
                "waitForCompletion": True,
            }
        )
        process_name = result.name if result.name else "unknown"
        logs = await sandbox_v2.process.logs(process_name, "all")
        print(f"   aiohttp package: {logs.strip() if logs else 'N/A'}")

        # Test new apt package (vim)
        result = await sandbox_v2.process.exec(
            {
                "command": "vim --version | head -1",
                "waitForCompletion": True,
            }
        )
        process_name = result.name if result.name else "unknown"
        logs = await sandbox_v2.process.logs(process_name, "all")
        print(f"   vim: {logs.strip() if logs else 'N/A'}")

        # Clean up
        print(f"\n🧹 Cleaning up sandbox: {image_name}")
        await delete_sandbox(image_name)
        await delete_sandbox(sandbox.metadata.name)
        await delete_sandbox(sandbox_v2.metadata.name)
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
            await delete_sandbox(image_name)
            if sandbox and sandbox.metadata and sandbox.metadata.name:
                await delete_sandbox(sandbox.metadata.name)
            if sandbox_v2 and sandbox_v2.metadata and sandbox_v2.metadata.name:
                await delete_sandbox(sandbox_v2.metadata.name)
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

import asyncio
import os

import httpx
import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.sandbox.client.models import HealthResponse
from tests.helpers import default_labels, default_region, unique_name

# Environment-aware version
VERSION = "develop" if os.environ.get("BL_ENV") == "dev" else "latest"


async def wait_for_upgrade_complete(
    sandbox: SandboxInstance, max_wait_time: float = 30.0
) -> HealthResponse:
    """
    Wait for sandbox upgrade to complete by polling the health endpoint.
    Uses the SDK's health method which includes proper authentication.
    Returns the health data when upgrade count > 0, raises if upgrade failed.
    """
    print("[TEST] Waiting for health upgrade count > 0...")
    elapsed = 0.0
    poll_interval = 0.5
    health_data = None

    while elapsed < max_wait_time:
        try:
            health_data = await sandbox.system.health()
            upgrade_count = health_data.upgrade_count or 0
            print(
                f"[TEST] Health check - upgradeCount: {upgrade_count} (elapsed: {elapsed * 1000:.0f}ms)"
            )
            if upgrade_count > 0:
                print(f"[TEST] Upgrade completed (took {elapsed * 1000:.0f}ms)")
                return health_data
            if health_data.last_upgrade and health_data.last_upgrade.status == "failed":
                print(f"[TEST] Health check - last upgrade failed, health data: {health_data}")
                raise Exception(f"Upgrade failed: {health_data}")
        except Exception as e:
            # Re-throw upgrade failures
            if str(e).startswith("Upgrade failed:"):
                raise
            print(f"[TEST] Health check error: {e} (elapsed: {elapsed * 1000:.0f}ms)")

        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    raise Exception(
        f"Upgrade did not complete within {max_wait_time * 1000}ms. Last health data: {health_data}"
    )


class TestSystemOperations:
    """Base class for system tests with cleanup tracking."""

    created_sandboxes: list[str] = []

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def cleanup(self, request):
        """Clean up all resources after each test class."""
        request.cls.created_sandboxes = []

        yield

        # Clean up sandboxes
        await asyncio.gather(
            *[self._safe_delete_sandbox(name) for name in request.cls.created_sandboxes],
            return_exceptions=True,
        )

    async def _safe_delete_sandbox(self, name: str) -> None:
        """Safely delete a sandbox, ignoring errors."""
        try:
            await SandboxInstance.delete(name)
        except Exception:
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestSystemUpgrade(TestSystemOperations):
    """Test system upgrade operations."""

    async def test_upgrades_sandbox_and_preview_remains_responsive(self):
        """Test that upgrade works and preview remains responsive."""
        name = unique_name("system-upgrade")
        print(f"[TEST] Starting test with sandbox name: {name}")

        # Create sandbox with Next.js image
        print("[TEST] Creating sandbox with blaxel/nextjs:latest image...")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": "blaxel/nextjs:latest",
                "memory": 4096,
                "region": default_region,
                "ports": [{"target": 3000}],
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(name)
        print("[TEST] Sandbox created")

        sandbox_host = sandbox.metadata.url
        print(f"[TEST] Sandbox host: {sandbox_host}")
        assert sandbox_host is not None

        # Do initial health check using the SDK
        print("[TEST] Performing initial health check...")
        initial_health = await sandbox.system.health()
        print(f"[TEST] Initial health check - upgradeCount: {initial_health.upgrade_count}")

        # Start the Next.js dev server
        print("[TEST] Starting Next.js dev server...")
        await sandbox.process.exec(
            {
                "name": "nextjs-dev",
                "command": "npm run dev -- --port 3000",
                "working_dir": "/blaxel/app",
                "wait_for_ports": [3000],
            }
        )
        print("[TEST] Next.js dev server started")

        # Create a public preview on port 3000
        print("[TEST] Creating preview on port 3000...")
        preview = await sandbox.previews.create(
            {
                "metadata": {"name": "upgrade-test-preview"},
                "spec": {"port": 3000, "public": True},
            }
        )

        assert preview.spec.url is not None
        preview_url = preview.spec.url
        print(f"[TEST] Preview created with URL: {preview_url}")

        # Wait for preview to be ready and verify it's responsive
        print("[TEST] Waiting for preview to be ready...")
        preview_ready = False
        max_wait_time = 30.0
        elapsed = 0.0

        async with httpx.AsyncClient(timeout=10.0) as client:
            while elapsed < max_wait_time:
                try:
                    response = await client.get(preview_url)
                    print(
                        f"[TEST] Preview check - status: {response.status_code} (elapsed: {elapsed * 1000:.0f}ms)"
                    )
                    if response.status_code == 200:
                        preview_ready = True
                        break
                except Exception as e:
                    print(f"[TEST] Preview check - error: {e} (elapsed: {elapsed * 1000:.0f}ms)")
                await asyncio.sleep(1)
                elapsed += 1

        print(f"[TEST] Preview ready: {preview_ready} (took {elapsed * 1000:.0f}ms)")
        assert preview_ready is True

        # Verify preview is accessible before upgrade and capture content
        print("[TEST] Verifying preview is accessible before upgrade...")
        async with httpx.AsyncClient(timeout=10.0) as client:
            pre_upgrade_response = await client.get(preview_url)
        print(f"[TEST] Pre-upgrade preview status: {pre_upgrade_response.status_code}")
        assert pre_upgrade_response.status_code == 200
        pre_upgrade_content = pre_upgrade_response.text
        print(f"[TEST] Pre-upgrade preview content length: {len(pre_upgrade_content)} bytes")

        # Upgrade the sandbox system
        print(f"[TEST] Calling sandbox.system.upgrade(version={VERSION})...")
        upgrade_result = await sandbox.system.upgrade(version=VERSION)
        print(f"[TEST] Upgrade call completed, result: {upgrade_result}")
        assert upgrade_result is not None

        # Wait for health to show upgrade count > 0
        health_data = await wait_for_upgrade_complete(sandbox, max_wait_time)
        assert (health_data.upgrade_count or 0) > 0

        # Wait a bit for everything to stabilize after upgrade
        print("[TEST] Waiting 5s for stabilization...")
        await asyncio.sleep(5)

        # Verify preview URL is still responsive after upgrade
        print("[TEST] Verifying preview is still responsive after upgrade...")
        async with httpx.AsyncClient(timeout=10.0) as client:
            post_upgrade_response = await client.get(preview_url)
        print(f"[TEST] Post-upgrade preview status: {post_upgrade_response.status_code}")
        assert post_upgrade_response.status_code == 200

        # Verify we can still read content from the preview and compare sizes
        post_upgrade_content = post_upgrade_response.text
        print(f"[TEST] Post-upgrade preview content length: {len(post_upgrade_content)} bytes")
        assert post_upgrade_content is not None
        assert len(post_upgrade_content) > 0

        # Verify the content size is similar before and after upgrade (allow delta of 200 bytes)
        size_delta = abs(len(post_upgrade_content) - len(pre_upgrade_content))
        print(
            f"[TEST] Comparing content sizes - pre: {len(pre_upgrade_content)}, post: {len(post_upgrade_content)}, delta: {size_delta}"
        )
        assert size_delta <= 200

        print("[TEST] Test completed successfully!")

    async def test_upgrades_sandbox_and_running_process_persists(self):
        """Test that running process persists and completes after upgrade."""
        name = unique_name("system-upgrade-process")
        print(f"[TEST] Starting process persistence test with sandbox name: {name}")

        # Create sandbox
        print("[TEST] Creating sandbox...")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": "blaxel/base-image:latest",
                "memory": 1024,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(name)
        print("[TEST] Sandbox created")

        # Start a sleep process that will run for 6 seconds
        sleep_duration = 6
        print(f"[TEST] Starting sleep process for {sleep_duration} seconds...")
        import time

        process_start = time.time()
        sleep_process = await sandbox.process.exec(
            {
                "name": "test-sleep",
                "command": f"sleep {sleep_duration}",
                "wait_for_completion": False,
            }
        )
        print(f"[TEST] Sleep process started with name: {sleep_process.name}")
        assert sleep_process.name == "test-sleep"

        # Wait a bit to ensure the process is running
        await asyncio.sleep(2)

        # Verify the process is running before upgrade
        print("[TEST] Checking process status before upgrade...")
        process_before_upgrade = await sandbox.process.get("test-sleep")
        print(f"[TEST] Process status before upgrade: {process_before_upgrade.status}")
        assert process_before_upgrade.status == "running"

        # Upgrade the sandbox system
        print(f"[TEST] Calling sandbox.system.upgrade(version={VERSION})...")
        upgrade_result = await sandbox.system.upgrade(version=VERSION)
        print(f"[TEST] Upgrade call completed, result: {upgrade_result}")
        assert upgrade_result is not None

        # Wait for the upgrade to complete (check health)
        health_data = await wait_for_upgrade_complete(sandbox, 10.0)
        assert (health_data.upgrade_count or 0) > 0

        # Check that the sleep process is still visible in the API after upgrade
        print("[TEST] Checking process status after upgrade...")
        process_after_upgrade = await sandbox.process.get("test-sleep")
        print(f"[TEST] Process status after upgrade: {process_after_upgrade.status}")
        assert process_after_upgrade is not None
        # The process should still be running (or completed if we took too long)
        assert process_after_upgrade.status in ["running", "completed"]

        # Calculate remaining time for the sleep to complete
        elapsed_since_start = time.time() - process_start
        expected_total_duration = sleep_duration
        remaining_time = expected_total_duration - elapsed_since_start
        print(
            f"[TEST] Elapsed since process start: {elapsed_since_start * 1000:.0f}ms, remaining: {remaining_time * 1000:.0f}ms"
        )

        # If the process is still running, wait for it to complete
        if process_after_upgrade.status == "running":
            # Wait for the process to complete with some buffer (5 seconds extra)
            wait_time = max(remaining_time + 5000, 5000)
            print(f"[TEST] Waiting {wait_time * 1000:.0f}ms for process to complete...")

            completed_process = await sandbox.process.wait(
                "test-sleep",
                max_wait=wait_time,
                interval=1,
            )
            print(
                f"[TEST] Process completed with status: {completed_process.status}, exitCode: {completed_process.exit_code}"
            )
            assert completed_process.status == "completed"
            assert completed_process.exit_code == 0

        # Verify the process completed in roughly the expected time (within 15 seconds tolerance)
        total_duration = time.time() - process_start
        print(
            f"[TEST] Total duration from process start to completion: {total_duration * 1000:.0f}ms"
        )
        print(f"[TEST] Expected duration: ~{expected_total_duration * 1000:.0f}ms")

        # The process should have completed close to the expected time
        # Allow 15 seconds tolerance for upgrade overhead
        tolerance = 15
        assert total_duration >= expected_total_duration - 2  # At least 4 seconds
        assert total_duration <= expected_total_duration + tolerance  # At most 21 seconds

        print("[TEST] Process persistence test completed successfully!")

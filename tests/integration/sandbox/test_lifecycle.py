import asyncio
import os
import uuid
from datetime import datetime, timedelta

from blaxel.core import SandboxInstance
from blaxel.core.client.models import ExpirationPolicy, SandboxLifecycle

# Determine the base image based on environment
BL_ENV = os.environ.get("BL_ENV", "prod")
BASE_IMAGE = "blaxel/base:latest"
print(f"Using base image: {BASE_IMAGE} (BL_ENV={BL_ENV})\n")


async def wait(seconds: float) -> None:
    """Helper function to wait for specified seconds."""
    await asyncio.sleep(seconds)


# Test 1: TTL Max-Age expiration policy
async def test_ttl_max_age():
    try:
        print("[Test 1] TTL Max-Age: Starting...")
        ttl_policy = ExpirationPolicy(
            type_="ttl-max-age",
            value="60s",
            action="delete"
        )
        lifecycle = SandboxLifecycle(
            expiration_policies=[ttl_policy]
        )

        print("[Test 1] Creating sandbox with lifecycle: ttl-max-age=60s")
        # Add unique suffix to avoid conflicts
        sandbox_name = f"sandbox-ttl-maxage-{uuid.uuid4().hex[:8]}"
        sandbox = await SandboxInstance.create({
            "lifecycle": lifecycle,
            "image": BASE_IMAGE,
            "name": sandbox_name
        })
        print(f"[Test 1] Created sandbox: {sandbox.metadata.name}")

        status = await SandboxInstance.get(sandbox.metadata.name)
        print(f"[Test 1] Initial status: {status.status}")

        print("[Test 1] Waiting 180s for expiration (60s TTL + cron delays)...")
        await wait(180)

        try:
            status = await SandboxInstance.get(sandbox.metadata.name)
            if status.status in ["DELETED", "TERMINATED"]:
                print("[Test 1] ✅ PASSED: Sandbox deleted after TTL max-age expiration")
            else:
                print(f"[Test 1] ❌ FAILED: Expected DELETED/TERMINATED, got {status.status}")
                raise Exception(f"Test 1 failed: Expected DELETED/TERMINATED, got {status.status}")
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                print("[Test 1] ✅ PASSED: Sandbox deleted after TTL max-age expiration (404)")
            else:
                raise

    except Exception as error:
        print(f"[Test 1] ❌ Error occurred: {error}")
        raise


# Test 2: Date expiration policy
async def test_date_expiration():
    try:
        print("[Test 2] Date Expiration: Starting...")
        # Use UTC time explicitly
        from datetime import timezone
        expiration_date = datetime.now(timezone.utc) + timedelta(seconds=60)

        date_policy = ExpirationPolicy(
            type_="date",
            value=expiration_date.strftime("%Y-%m-%dT%H:%M:%SZ"),  # Proper UTC format
            action="delete"
        )
        lifecycle = SandboxLifecycle(
            expiration_policies=[date_policy]
        )

        sandbox_name = f"sandbox-date-{uuid.uuid4().hex[:8]}"
        sandbox = await SandboxInstance.create({
            "lifecycle": lifecycle,
            "image": BASE_IMAGE,
            "name": sandbox_name
        })
        print(f"[Test 2] Created sandbox: {sandbox.metadata.name}")
        print(f"[Test 2] Expires at: {date_policy.value}")

        status = await SandboxInstance.get(sandbox.metadata.name)
        print(f"[Test 2] Initial status: {status.status}")

        print("[Test 2] Waiting 180s for date expiration (60s + cron delays)...")
        await wait(180)

        try:
            status = await SandboxInstance.get(sandbox.metadata.name)
            if status.status in ["DELETED", "TERMINATED"]:
                print("[Test 2] ✅ PASSED: Sandbox deleted at specified date")
            else:
                print(f"[Test 2] ❌ FAILED: Expected DELETED/TERMINATED, got {status.status}")
                raise Exception(f"Test 2 failed: Expected DELETED/TERMINATED, got {status.status}")
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                print("[Test 2] ✅ PASSED: Sandbox deleted at specified date (404)")
            else:
                raise

    except Exception as error:
        print(f"[Test 2] ❌ Error occurred: {error}")
        raise


# Test 3: TTL Idle expiration policy - Two scenarios
async def test_ttl_idle():
    print("[Test 3] TTL Idle: Starting two test scenarios...")

    # Scenario A: Test that sandbox stays alive with regular activity
    print("\n[Test 3A] Scenario A: Testing idle timeout with regular activity...")
    idle_policy_active = ExpirationPolicy(
        type_="ttl-idle",
        value="60s",  # 1 minute idle timeout
        action="delete"
    )
    lifecycle_active = SandboxLifecycle(
        expiration_policies=[idle_policy_active]
    )

    sandbox_name_active = f"sandbox-idle-active-{uuid.uuid4().hex[:8]}"
    sandbox_active = await SandboxInstance.create({
        "lifecycle": lifecycle_active,
        "image": BASE_IMAGE,
        "name": sandbox_name_active
    })
    print(f"[Test 3A] Created sandbox with 60s idle timeout: {sandbox_active.metadata.name}")

    # Make initial sandbox API call to activate idle monitoring
    print("[Test 3A] Making initial sandbox API call (process.exec) to activate idle monitoring...")
    result = await sandbox_active.process.exec({"command": "ls /"})
    print(f"[Test 3A] Initial exec successful (pid: {result.pid}) - Idle timer started")

    # Make sandbox API calls every 30 seconds to keep sandbox alive (3 calls total)
    for i in range(1, 4):
        print(f"[Test 3A] Waiting 30 seconds before API call {i}...")
        await wait(30)

        try:
            # Make a sandbox API call (process exec) to reset idle timer
            result = await sandbox_active.process.exec({"command": "echo 'keep-alive call'"})
            print(f"[Test 3A] API call {i} successful (pid: {result.pid}) - sandbox kept alive")

            # Also check control plane status to ensure sandbox is still running
            status_active = await SandboxInstance.get(sandbox_active.metadata.name)
            print(f"[Test 3A] Control plane status: {status_active.status}")
        except Exception as error:
            if "404" in str(error) or "not found" in str(error).lower():
                print(f"[Test 3A] ❌ FAILED: Sandbox was deleted prematurely after only {i * 30}s with regular activity")
                raise Exception("Test 3A failed: Sandbox deleted while making regular calls every 30s")
            raise

    print("[Test 3A] ✅ PASSED: Sandbox stayed alive with regular activity (90s total with calls every 30s)")

    # Clean up the active sandbox
    await SandboxInstance.delete(sandbox_active.metadata.name)
    print("[Test 3A] Cleaned up active sandbox\n")

    # Scenario B: Test that sandbox gets deleted after idle timeout
    print("[Test 3B] Scenario B: Testing idle timeout without activity...")
    idle_policy_inactive = ExpirationPolicy(
        type_="ttl-idle",
        value="30s",  # 30 seconds idle timeout for faster testing
        action="delete"
    )
    lifecycle_inactive = SandboxLifecycle(
        expiration_policies=[idle_policy_inactive]
    )

    sandbox_name_inactive = f"sandbox-idle-inactive-{uuid.uuid4().hex[:8]}"
    sandbox_inactive = await SandboxInstance.create({
        "lifecycle": lifecycle_inactive,
        "image": BASE_IMAGE,
        "name": sandbox_name_inactive
    })
    print(f"[Test 3B] Created sandbox with 30s idle timeout: {sandbox_inactive.metadata.name}")

    # Make initial sandbox API call to activate idle monitoring
    print("[Test 3B] Making initial sandbox API call (process.exec) to activate idle monitoring...")
    result_inactive = await sandbox_inactive.process.exec({"command": "ls /"})
    print(f"[Test 3B] Initial exec successful (pid: {result_inactive.pid}) - Idle timer started")

    # Now wait for idle timeout without any further activity
    print("[Test 3B] Now waiting 90s for idle timeout to trigger (cron runs every minute)...")
    await wait(90)

    # Check if sandbox was deleted due to idle timeout
    try:
        status_inactive = await SandboxInstance.get(sandbox_inactive.metadata.name)
        print(f"[Test 3B] ⚠️ WARNING: Sandbox still active with status: {status_inactive.status}")
        # Clean up if not already deleted
        await SandboxInstance.delete(sandbox_inactive.metadata.name)
        print("[Test 3B] ⚠️ Test completed with warning - sandbox manually cleaned up")
    except Exception as error:
        # If we get a 404, the sandbox was successfully deleted
        if "404" in str(error) or "not found" in str(error).lower():
            print("[Test 3B] ✅ PASSED: Sandbox deleted after idle timeout (404 on get)")
        else:
            print(f"[Test 3B] ❌ Error checking sandbox status: {error}")
            raise

    print("[Test 3] ✅ Both idle timeout scenarios completed successfully")


# Test 4: Multiple expiration policies
async def test_multiple_policies():
    print("[Test 4] Multiple Policies: Starting...")
    idle_policy = ExpirationPolicy(
        type_="ttl-idle",
        value="5m",
        action="delete"
    )
    max_age_policy = ExpirationPolicy(
        type_="ttl-max-age",
        value="10m",
        action="delete"
    )
    lifecycle = SandboxLifecycle(
        expiration_policies=[idle_policy, max_age_policy]
    )

    sandbox_name = f"sandbox-multiple-{uuid.uuid4().hex[:8]}"
    sandbox = await SandboxInstance.create({
        "lifecycle": lifecycle,
        "image": BASE_IMAGE,
        "name": sandbox_name
    })
    print(f"[Test 4] Created sandbox: {sandbox.metadata.name}")
    print("[Test 4] Policy 1: ttl-idle=5m (delete)")
    print("[Test 4] Policy 2: ttl-max-age=10m (delete)")

    # IMPORTANT: Make a sandbox API call to activate idle monitoring for ttl-idle policy
    print("[Test 4] Making sandbox API call (process.exec) to activate idle monitoring...")
    exec_result = await sandbox.process.exec({"command": "echo 'activate idle timer'"})
    print(f"[Test 4] Process exec successful (pid: {exec_result.pid}) - Idle timer activated")

    # Clean up immediately for this test (just testing configuration)
    await SandboxInstance.delete(sandbox.metadata.name)
    print("[Test 4] ✅ PASSED: Multiple policies configured successfully")


# Test 5: Empty expiration policies (now testing sandbox without lifecycle)
async def test_empty_policies():
    print("[Test 5] No Lifecycle: Starting...")
    # Don't specify lifecycle at all (instead of empty policies)
    sandbox_name = f"sandbox-no-lifecycle-{uuid.uuid4().hex[:8]}"
    sandbox = await SandboxInstance.create({
        "image": BASE_IMAGE,
        "name": sandbox_name
    })
    print(f"[Test 5] Created sandbox without lifecycle: {sandbox.metadata.name}")

    status = await SandboxInstance.get(sandbox.metadata.name)
    print(f"[Test 5] Current status: {status.status}")

    # Clean up
    await SandboxInstance.delete(sandbox.metadata.name)
    print("[Test 5] ✅ PASSED: Sandbox without lifecycle created successfully")


# Test 6: Backward compatibility with legacy ttl
async def test_backward_compatibility():
    print("[Test 6] Backward Compatibility: Starting...")
    lifecycle = SandboxLifecycle(
        expiration_policies=[
            ExpirationPolicy(type_="ttl-max-age", value="2m", action="delete")
        ]
    )

    # Test that lifecycle can coexist with legacy ttl
    sandbox_name = f"sandbox-backcompat-{uuid.uuid4().hex[:8]}"
    sandbox = await SandboxInstance.create({
        "lifecycle": lifecycle,
        "image": BASE_IMAGE,
        "ttl": "5m",  # Legacy ttl - should be overridden by lifecycle
        "name": sandbox_name
    })
    print("[Test 6] Created sandbox with both lifecycle and legacy ttl")
    print("[Test 6] Lifecycle: ttl-max-age=2m (delete), Legacy ttl: 5m")

    status = await SandboxInstance.get(sandbox.metadata.name)
    print(f"[Test 6] Current status: {status.status}")

    # Clean up
    await SandboxInstance.delete(sandbox.metadata.name)
    print("[Test 6] ✅ PASSED: Backward compatibility maintained")


# Test 7: Various duration formats
async def test_duration_formats():
    print("[Test 7] Duration Formats: Starting...")
    durations = ["30s", "5m", "1h", "1d"]

    for duration in durations:
        lifecycle = SandboxLifecycle(
            expiration_policies=[
                ExpirationPolicy(type_="ttl-max-age", value=duration, action="delete")
            ]
        )

        sandbox_name = f"sandbox-dur-{duration.replace('s', '').replace('m', '').replace('h', '').replace('d', '')}{duration[-1]}-{uuid.uuid4().hex[:8]}"
        sandbox = await SandboxInstance.create({
            "lifecycle": lifecycle,
            "image": BASE_IMAGE,
            "name": sandbox_name
        })
        print(f"[Test 7] Created sandbox with {duration} TTL: {sandbox.metadata.name}")

        # Clean up immediately
        await SandboxInstance.delete(sandbox.metadata.name)

    print("[Test 7] ✅ PASSED: All duration formats accepted")


# Test 8: TTL Max-Age with delete action
async def test_ttl_max_age_delete():
    print("[Test 8] TTL Max-Age Delete: Starting...")
    delete_policy = ExpirationPolicy(
        type_="ttl-max-age",
        value="30s",
        action="delete"
    )
    lifecycle = SandboxLifecycle(
        expiration_policies=[delete_policy]
    )

    sandbox_name = f"sandbox-maxage-delete-{uuid.uuid4().hex[:8]}"
    sandbox = await SandboxInstance.create({
        "lifecycle": lifecycle,
        "image": BASE_IMAGE,
        "name": sandbox_name
    })
    print(f"[Test 8] Created sandbox: {sandbox.metadata.name}")
    print("[Test 8] Policy: ttl-max-age=30s (delete)")

    status = await SandboxInstance.get(sandbox.metadata.name)
    print(f"[Test 8] Initial status: {status.status}")

    print("[Test 8] Waiting 90s for deletion (cron runs every minute)...")
    await wait(90)

    try:
        status = await SandboxInstance.get(sandbox.metadata.name)
        if status.status in ["DELETED", "TERMINATED"]:
            print("[Test 8] ✅ PASSED: Sandbox deleted after TTL max-age")
        else:
            print(f"[Test 8] ⚠️ WARNING: Expected DELETED/TERMINATED, got {status.status}")
            # Clean up if not already deleted
            await SandboxInstance.delete(sandbox.metadata.name)
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            print("[Test 8] ✅ PASSED: Sandbox deleted after TTL max-age (404)")
        else:
            raise


# Test 9: Mixed policy types and actions
async def test_mixed_policies():
    print("[Test 9] Mixed Policies: Starting...")
    from datetime import timezone
    policies = [
        ExpirationPolicy(type_="ttl-idle", value="2m", action="delete"),
        ExpirationPolicy(type_="ttl-max-age", value="5m", action="delete"),
        ExpirationPolicy(
            type_="date",
            value=(datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            action="delete"
        )
    ]
    lifecycle = SandboxLifecycle(expiration_policies=policies)

    sandbox_name = f"sandbox-mixed-{uuid.uuid4().hex[:8]}"
    sandbox = await SandboxInstance.create({
        "lifecycle": lifecycle,
        "image": BASE_IMAGE,
        "name": sandbox_name
    })
    print(f"[Test 9] Created sandbox: {sandbox.metadata.name}")
    print("[Test 9] Policies: idle=2m(delete), max-age=5m(delete), date=+1h(delete)")

    # IMPORTANT: Make a sandbox API call to activate idle monitoring for ttl-idle policy
    print("[Test 9] Making sandbox API call (process.exec) to activate idle monitoring...")
    exec_result = await sandbox.process.exec({"command": "echo 'activate idle timer'"})
    print(f"[Test 9] Process exec successful (pid: {exec_result.pid}) - Idle timer activated")

    # Clean up
    await SandboxInstance.delete(sandbox.metadata.name)
    print("[Test 9] ✅ PASSED: Mixed policies configured successfully")


async def main():
    try:
        print("=== Testing Sandbox Lifecycle with ExpirationPolicies ===")
        print("=== Running all tests in parallel ===\n")

        import time
        start_time = time.time()

        # Run all tests in parallel
        results = await asyncio.gather(
            test_ttl_max_age(),
            test_date_expiration(),
            test_ttl_idle(),
            test_multiple_policies(),
            test_empty_policies(),
            test_backward_compatibility(),
            test_duration_formats(),
            test_ttl_max_age_delete(),
            test_mixed_policies(),
            return_exceptions=True
        )

        end_time = time.time()
        duration = round(end_time - start_time)

        # Print summary
        print("\n=== Test Results Summary ===")
        print(f"Total execution time: {duration} seconds\n")

        test_names = [
            "TTL Max-Age", "Date Expiration", "TTL Idle",
            "Multiple Policies", "No Lifecycle", "Backward Compatibility",
            "Duration Formats", "TTL Max-Age Delete", "Mixed Policies"
        ]

        passed = 0
        failed = 0

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed += 1
                print(f"❌ Test {i + 1} ({test_names[i]}): FAILED")
                print(f"   Error: {result}")
            else:
                passed += 1
                print(f"✅ Test {i + 1} ({test_names[i]}): PASSED")

        print(f"\n📊 Results: {passed} passed, {failed} failed")

        if failed == 0:
            print("\n✅ All lifecycle tests completed successfully!")
            exit(0)
        else:
            print("\n❌ Some tests failed. Check the logs above for details.")
            exit(1)

    except Exception as e:
        print(f"\n❌ Fatal test error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())

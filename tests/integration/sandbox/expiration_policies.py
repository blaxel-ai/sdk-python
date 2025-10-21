import asyncio
import os
import sys

from blaxel.core.sandbox import SandboxInstance

# Determine base image based on environment
base_image = "blaxel/vite:latest" if os.getenv("BL_ENV") == "dev" else "blaxel/prod-base:latest"
print(f"Using base image: {base_image} (BL_ENV={os.getenv('BL_ENV', 'not set')})\n")


async def wait_for_termination(sandbox_name: str, max_minutes: int = 10) -> bool:
    """Wait for sandbox to be terminated, checking every minute."""
    print(f"Checking sandbox status every minute for up to {max_minutes} minutes...")

    for minute in range(1, max_minutes + 1):
        # Wait 1 minute
        await asyncio.sleep(60)

        # Check sandbox status
        sandbox_status = await SandboxInstance.get(sandbox_name)
        print(f"  Minute {minute}: Status = {sandbox_status.status}")

        if sandbox_status.status in ["TERMINATED", "DELETED"]:
            print(f"✅ Sandbox terminated after {minute} minute(s)")
            return True

    return False


async def main():
    """Test expiration policies with ttl-idle and createIfNotExists."""
    try:
        sandbox_name = "sandbox-ttl-idle"

        print("=== Test 1: Create sandbox with ttl-idle expiration policy ===")

        # Create sandbox with ttl-idle expiration policy of 20 seconds
        sandbox = await SandboxInstance.create_if_not_exists({
            "name": sandbox_name,
            "image": base_image,
            "lifecycle": {
                "expirationPolicies": [
                    {
                        "type": "ttl-idle",
                        "value": "20s",
                        "action": "delete",
                    },
                ],
            },
        })

        print(f"✅ Created sandbox with ttl-idle policy: {sandbox.metadata.name}")

        # IMPORTANT: Make a sandbox API call to activate idle monitoring for ttl-idle policy
        print("Making sandbox API call to activate idle monitoring...")
        exec_result = await sandbox.process.exec({"command": "echo 'activate idle timer'"})
        print(f"Process exec successful (pid: {exec_result.pid}) - Idle timer activated")

        # Test 1.5: Try to create_if_not_exists with same name while running
        print("\n=== Test 1.5: Attempt to create_if_not_exists with same name while running ===")
        print("Attempting to create_if_not_exists with duplicate name (should return existing sandbox)...")

        duplicate_sandbox = await SandboxInstance.create_if_not_exists({
            "name": sandbox_name,
            "image": base_image,
            "lifecycle": {
                "expirationPolicies": [
                    {
                        "type": "ttl-idle",
                        "value": "20s",
                        "action": "delete",
                    },
                ],
            },
        })

        # With create_if_not_exists, we should get the existing active sandbox
        if duplicate_sandbox.metadata.name == sandbox_name and duplicate_sandbox.status in ["RUNNING", "DEPLOYED"]:
            print("✅ Test 1.5 PASSED: create_if_not_exists correctly returned the existing active sandbox")
            print(f"  Returned sandbox: {duplicate_sandbox.metadata.name}, Status: {duplicate_sandbox.status}")
        else:
            print("❌ Test 1.5 FAILED: create_if_not_exists did not return the expected active sandbox")
            print(f"  Got: {duplicate_sandbox.metadata.name}, Status: {duplicate_sandbox.status}")
            sys.exit(1)

        print("\nContinuing with original sandbox termination test...")

        # Wait for termination (checking every minute for up to 10 minutes)
        terminated1 = await wait_for_termination(sandbox_name, 10)

        if terminated1:
            print("✅ Test 1 PASSED: Sandbox was terminated due to idle timeout.")
        else:
            print("❌ Test 1 FAILED: Sandbox was not terminated within 10 minutes.")

            # Clean up if not terminated
            final_status = await SandboxInstance.get(sandbox_name)
            if final_status.status in ["RUNNING", "DEPLOYED"]:
                await SandboxInstance.delete(sandbox_name)
                print("Cleaned up sandbox manually.")
            sys.exit(1)

        print("\n=== Test 2: Use create_if_not_exists with same name after termination ===")
        print("Using create_if_not_exists with the same name - should automatically recreate since previous is TERMINATED...")

        # Create another sandbox with the same name
        sandbox = await SandboxInstance.create_if_not_exists({
            "name": sandbox_name,
            "image": base_image,
            "lifecycle": {
                "expirationPolicies": [
                    {
                        "type": "ttl-idle",
                        "value": "20s",
                        "action": "delete",
                    },
                ],
            },
        })

        print(f"✅ Successfully created new sandbox with same name: {sandbox.metadata.name}")

        # Activate idle monitoring again
        print("Making sandbox API call to activate idle monitoring...")
        exec_result = await sandbox.process.exec({"command": "echo 'activate idle timer for second sandbox'"})
        print(f"Process exec successful (pid: {exec_result.pid}) - Idle timer activated")

        # Wait for second sandbox termination
        terminated2 = await wait_for_termination(sandbox_name, 10)

        if terminated2:
            print("✅ Test 2 PASSED: Second sandbox was also terminated due to idle timeout.")
            print("\n✅✅✅ ALL TESTS PASSED ✅✅✅")
        else:
            print("❌ Test 2 FAILED: Second sandbox was not terminated within 10 minutes.")

            # Clean up if not terminated
            final_status = await SandboxInstance.get(sandbox_name)
            if final_status.status in ["RUNNING", "DEPLOYED"]:
                await SandboxInstance.delete(sandbox_name)
                print("Cleaned up sandbox manually.")
            sys.exit(1)

    except Exception as e:
        print(f"❌ There was an error => {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        sys.exit(0)
    except Exception as err:
        print(f"❌ There was an error => {err}")
        sys.exit(1)


import asyncio
import sys
from datetime import datetime, timedelta

from blaxel.core.sandbox import SandboxInstance


async def main():
    """Test TTL and expires functionality for sandboxes."""
    try:
        # Test 1: Create sandbox with ttl
        print("Test 1: Create sandbox with ttl...")
        sandbox = await SandboxInstance.create({"ttl": "60s", "name": "sandbox-ttl"})
        print(f"✅ Created sandbox with default name: {sandbox.metadata.name}")
        await asyncio.sleep(120)  # Wait 120 seconds (2 minutes)
        sandbox_status = await SandboxInstance.get(sandbox.metadata.name)
        if sandbox_status.status == "TERMINATED":
            print(f"✅ Sandbox status: {sandbox_status.status}")
        else:
            print(f"❌ Sandbox status: {sandbox_status.status}")

        # Test 2: Create sandbox with expires
        print("\nTest 2: Create sandbox with expires...")
        expires_date = datetime.now() + timedelta(seconds=60)
        sandbox = await SandboxInstance.create({"expires": expires_date, "name": "sandbox-expires"})
        print(f"✅ Created sandbox with default name: {sandbox.metadata.name}")
        await asyncio.sleep(120)  # Wait 120 seconds (2 minutes)
        sandbox_status = await SandboxInstance.get(sandbox.metadata.name)
        if sandbox_status.status == "TERMINATED":
            print(f"✅ Sandbox status: {sandbox_status.status}")
        else:
            print(f"❌ Sandbox status: {sandbox_status.status}")

    except Exception as e:
        print(f"❌ There was an error => {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("✅ All tests completed successfully")
        sys.exit(0)
    except Exception as err:
        print(f"❌ There was an error => {err}")
        sys.exit(1)

import asyncio
import sys

from blaxel.core.sandbox import SandboxCreateConfiguration, SandboxInstance


async def main():
    """Test sandbox snapshot feature."""
    try:
        # Test 1: Create sandbox with snapshot disabled using dict
        print("Test 1: Create sandbox with snapshot disabled (dict syntax)...")
        sandbox = await SandboxInstance.create({"snapshot_enabled": False})
        print(f"✅ Created sandbox with snapshot disabled: {sandbox.metadata.name}")
        print(f"   Snapshot enabled: {sandbox.spec.runtime.snapshot_enabled}")
        await asyncio.sleep(2)
        await sandbox.fs.ls("/")
        print("Waiting 20 seconds...")
        await asyncio.sleep(20)
        await sandbox.fs.ls("/")
        print("✅ Sandbox with snapshot disabled completed operations")

        # Test 2: Create sandbox with default snapshot settings (enabled by default)
        print("\nTest 2: Create sandbox with default snapshot settings...")
        sandbox2 = await SandboxInstance.create()
        print(f"✅ Created sandbox with default settings: {sandbox2.metadata.name}")
        print(f"   Snapshot enabled: {sandbox2.spec.runtime.snapshot_enabled}")
        await sandbox2.fs.ls("/")
        await sandbox2.fs.write("/test.txt", "Hello, world!")
        print("Waiting 30 seconds...")
        await asyncio.sleep(30)
        result = await sandbox2.fs.read("/test.txt")
        assert result == "Hello, world!", "File content mismatch"
        print("✅ Sandbox with default settings completed operations")
        print(f"   Directory contents: {result}")

        # Test 3: Create sandbox with snapshot disabled using SandboxCreateConfiguration
        print("\nTest 3: Create sandbox with snapshot disabled (config syntax)...")
        config = SandboxCreateConfiguration(
            name="sandbox-snapshot-disabled-config", snapshot_enabled=False
        )
        sandbox3 = await SandboxInstance.create(config)
        print(f"✅ Created sandbox with config: {sandbox3.metadata.name}")
        print(f"   Snapshot enabled: {sandbox3.spec.runtime.snapshot_enabled}")
        await sandbox3.fs.ls("/")
        print("✅ Config sandbox completed operations")

        # Cleanup
        print("\nCleaning up sandboxes...")
        await SandboxInstance.delete(sandbox.metadata.name)
        print(f"✅ Deleted sandbox: {sandbox.metadata.name}")
        await SandboxInstance.delete(sandbox2.metadata.name)
        print(f"✅ Deleted sandbox: {sandbox2.metadata.name}")
        await SandboxInstance.delete(sandbox3.metadata.name)
        print(f"✅ Deleted sandbox: {sandbox3.metadata.name}")

        print("\n🎉 All snapshot tests passed!")

    except Exception as e:
        print(f"❌ There was an error => {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("✅ Tests completed successfully")
        sys.exit(0)
    except Exception as err:
        print(f"❌ There was an error => {err}")
        sys.exit(1)


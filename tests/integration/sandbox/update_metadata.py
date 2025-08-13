import asyncio
import logging

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.sandbox.types import SandboxUpdateMetadata

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main():
    try:
        print("Test 1: Create default sandbox...")
        sandbox = await SandboxInstance.create()

        print("Metadata:")
        print(f"  labels: {sandbox.metadata.labels if sandbox.metadata else None}")
        print(f"  displayName: {sandbox.metadata.display_name if sandbox.metadata else None}")
        print(f"  name: {sandbox.metadata.name if sandbox.metadata else None}")
        print(f"  createdAt: {sandbox.metadata.created_at if sandbox.metadata else None}")
        print(f"  updatedAt: {sandbox.metadata.updated_at if sandbox.metadata else None}")
        print(f"  createdBy: {sandbox.metadata.created_by if sandbox.metadata else None}")
        print(f"  updatedBy: {sandbox.metadata.updated_by if sandbox.metadata else None}")

        print("\nTest 2: Update metadata...")

        sandbox = await SandboxInstance.update_metadata(
            sandbox.metadata.name,
            SandboxUpdateMetadata(labels={"test": "test"}, display_name="test"),
        )

        print("Updated Metadata:")
        print(f"  labels: {sandbox.metadata.labels if sandbox.metadata else None}")
        print(f"  displayName: {sandbox.metadata.display_name if sandbox.metadata else None}")
        print(f"  name: {sandbox.metadata.name if sandbox.metadata else None}")
        print(f"  createdAt: {sandbox.metadata.created_at if sandbox.metadata else None}")
        print(f"  updatedAt: {sandbox.metadata.updated_at if sandbox.metadata else None}")
        print(f"  createdBy: {sandbox.metadata.created_by if sandbox.metadata else None}")
        print(f"  updatedBy: {sandbox.metadata.updated_by if sandbox.metadata else None}")

        await sandbox.fs.ls("/asdasdas")
        print("\nSandbox filesystem is accessible after metadata update ✅")

    except Exception as e:
        print(f"❌ There was an error => {e}")
        import traceback

        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())

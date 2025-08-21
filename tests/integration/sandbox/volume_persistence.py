"""
Volume Persistence Test

This test verifies that volume data persists across sandbox recreations by:
1. Creating a volume
2. Creating a sandbox with that volume attached
3. Writing a file to the volume
4. Deleting the sandbox
5. Creating a new sandbox with the same volume
6. Verifying the file persisted
"""

import asyncio
import os

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.volume import VolumeInstance


async def wait_for_sandbox_deletion(sandbox_name: str, max_attempts: int = 30) -> bool:
    """
    Waits for a sandbox deletion to fully complete by polling until the sandbox no longer exists.
    
    Args:
        sandbox_name: The name of the sandbox to wait for deletion
        max_attempts: Maximum number of attempts to wait (default: 30 seconds)
        
    Returns:
        bool: True if deletion completed, False if timeout
    """
    print(f"⏳ Waiting for {sandbox_name} deletion to fully complete...")
    attempts = 0

    while attempts < max_attempts:
        try:
            await SandboxInstance.get(sandbox_name)
            # If we get here, sandbox still exists, wait and try again
            await asyncio.sleep(1)
            attempts += 1
            print(f"   Still exists, waiting... ({attempts}/{max_attempts})")
        except Exception:
            # If getSandbox throws an error, the sandbox no longer exists
            print(f"✅ {sandbox_name} fully deleted")
            return True

    print(f"⚠️ Timeout waiting for {sandbox_name} deletion to complete")
    return False


async def main():
    """Main test function for volume persistence."""
    
    # Cleanup function
    async def cleanup():
        try:
            await SandboxInstance.delete("first-sandbox")
        except Exception:
            pass
        try:
            await SandboxInstance.delete("second-sandbox")
            await wait_for_sandbox_deletion("second-sandbox")
        except Exception as e:
            print(f"❌ Sandbox not found: {e}")

        try:
            await VolumeInstance.delete("test-persistence-volume")
        except Exception as e:
            print(f"❌ Volume not found: {e}")

    try:
        print("🗄️  Simple Volume Persistence Test")
        print("=" * 40)

        # Choose image based on BL_ENV
        bl_env = os.getenv("BL_ENV", "prod")
        is_dev = bl_env == "dev"
        image_base = "dev-base" if is_dev else "prod-base"
        image = f"blaxel/{image_base}:latest"
        file_content = "Hello from sandbox!"

        print(f"Using image: {image} (BL_ENV={bl_env})")

        # Step 1: Create a volume
        print("\n1. Creating a volume...")
        volume = await VolumeInstance.create({
            "name": "test-persistence-volume",
            "display_name": "Test Persistence Volume",
            "size": 1024  # 1GB
        })
        print(f"✅ Volume created: {volume.name}")

        # Step 2: Create a sandbox with that volume
        print("\n2. Creating sandbox with volume...")
        sandbox = await SandboxInstance.create({
            "name": "first-sandbox",
            "image": image,
            "memory": 2048,
            "volumes": [
                {
                    "name": "test-persistence-volume",
                    "mount_path": "/persistent-data",
                    "read_only": False
                }
            ]
        })
        print(f"✅ Sandbox created: {sandbox.metadata.name}")

        # Step 3: Put a file in that volume
        print("\n3. Writing file to volume...")
        await sandbox.process.exec({
            "command": f"echo '{file_content}' > /persistent-data/test-file.txt",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        print("✅ File written to volume")

        # Step 4: Retrieve the file in that volume
        print("\n4. Reading file from volume in first sandbox...")

        # Debug: Check mount points
        print("🔍 Debug: Checking mount points...")
        mount_check = await sandbox.process.exec({
            "command": "mount | grep persistent-data",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        mount_info = mount_check.logs.strip() if mount_check.logs else 'No mount found'
        print(f"Mount info: {mount_info}")

        # Debug: Check directory structure and file existence
        print("🔍 Debug: Checking directory structure...")
        dir_check = await sandbox.process.exec({
            "command": "ls -la /persistent-data/",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        dir_listing = dir_check.logs.strip() if dir_check.logs else 'No listing'
        print(f"Directory listing: {dir_listing}")

        # Debug: Check if specific file exists
        print("🔍 Debug: Checking if test-file.txt exists...")
        file_exists = await sandbox.process.exec({
            "command": "test -f /persistent-data/test-file.txt && echo 'File exists' || echo 'File does not exist'",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        existence_check = file_exists.logs.strip() if file_exists.logs else 'No response'
        print(f"File existence check: {existence_check}")

        # Debug: Check file ownership and permissions
        print("🔍 Debug: Checking file details...")
        file_details = await sandbox.process.exec({
            "command": "ls -la /persistent-data/test-file.txt 2>/dev/null || echo 'Cannot access file'",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        details = file_details.logs.strip() if file_details.logs else 'No details'
        print(f"File details: {details}")

        # Try to read the file content
        first_read = await sandbox.process.exec({
            "command": "cat /persistent-data/test-file.txt",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        first_content = first_read.logs.strip() if first_read.logs else ''
        print(f"✅ File content: {first_content}")

        # Step 5: Delete the sandbox
        print("\n5. Deleting first sandbox...")
        await SandboxInstance.delete("first-sandbox")
        print("✅ First sandbox deleted")

        # Wait for deletion to fully complete
        deletion_completed = await wait_for_sandbox_deletion("first-sandbox")
        if not deletion_completed:
            raise Exception("Timeout waiting for sandbox deletion to complete")

        # Step 6: Create a new sandbox with previous volume
        print("\n6. Creating new sandbox with same volume...")
        new_sandbox = await SandboxInstance.create({
            "name": "second-sandbox",
            "image": image,
            "memory": 2048,
            "volumes": [
                {
                    "name": "test-persistence-volume",
                    "mount_path": "/data",  # Different mount path to show flexibility
                    "read_only": False
                }
            ]
        })
        print(f"✅ New sandbox created: {new_sandbox.metadata.name}")

        # Step 7: Retrieve the file in that volume
        print("\n7. Reading file from volume in second sandbox...")

        # Debug: Check mount points in new sandbox
        print("🔍 Debug: Checking mount points in new sandbox...")
        new_mount_check = await new_sandbox.process.exec({
            "command": "mount | grep data",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        new_mount_info = new_mount_check.logs.strip() if new_mount_check.logs else 'No mount found'
        print(f"Mount info: {new_mount_info}")

        # Debug: Check directory structure and file existence in new sandbox
        print("🔍 Debug: Checking directory structure in new sandbox...")
        new_dir_check = await new_sandbox.process.exec({
            "command": "ls -la /data/",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        new_dir_listing = new_dir_check.logs.strip() if new_dir_check.logs else 'No listing'
        print(f"Directory listing (/data): {new_dir_listing}")

        # Debug: Check if specific file exists in new sandbox
        print("🔍 Debug: Checking if test-file.txt exists in new sandbox...")
        new_file_exists = await new_sandbox.process.exec({
            "command": "test -f /data/test-file.txt && echo 'File exists' || echo 'File does not exist'",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        new_existence_check = new_file_exists.logs.strip() if new_file_exists.logs else 'No response'
        print(f"File existence check: {new_existence_check}")

        # Debug: Check file ownership and permissions in new sandbox
        print("🔍 Debug: Checking file details in new sandbox...")
        new_file_details = await new_sandbox.process.exec({
            "command": "ls -la /data/test-file.txt 2>/dev/null || echo 'Cannot access file'",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        new_details = new_file_details.logs.strip() if new_file_details.logs else 'No details'
        print(f"File details: {new_details}")

        # Debug: Check current user and groups
        print("🔍 Debug: Checking current user and groups...")
        user_info = await new_sandbox.process.exec({
            "command": "whoami && groups",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        user_details = user_info.logs.strip() if user_info.logs else 'No user info'
        print(f"Current user and groups: {user_details}")

        # Try to read the file content
        second_read = await new_sandbox.process.exec({
            "command": "cat /data/test-file.txt",
            "waitForCompletion": True,
            "on_log": lambda log: None  # Dummy callback to force waiting
        })
        second_content = second_read.logs.strip() if second_read.logs else ''
        print(f"✅ File content from new sandbox: {second_content}")

        # Verify persistence worked
        persisted_content = second_content

        if file_content == persisted_content:
            print("\n🎉 SUCCESS: Volume data persisted across sandbox recreations!")
            print(f'   Original: "{file_content}"')
            print(f'   Persisted: "{persisted_content}"')
        else:
            print("\n❌ FAILURE: Volume data did not persist correctly")
            print(f'   Expected: "{file_content}"')
            print(f'   Got: "{persisted_content}"')

        print("\n✨ Test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    finally:
        # Cleanup
        await cleanup()


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)

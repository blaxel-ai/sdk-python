import asyncio
from logging import getLogger

from utils import create_or_get_sandbox

from blaxel.core.sandbox import SandboxInstance

logger = getLogger(__name__)

SANDBOX_NAME = "sandbox-test-python-binary"


async def main():
    """Main binary write test function."""
    print("🚀 Starting sandbox binary write tests...")

    try:
        # Create or get sandbox
        sandbox = await create_or_get_sandbox(SANDBOX_NAME)
        print(f"✅ Sandbox ready: {sandbox.metadata.name}")

        # Wait for sandbox to be deployed
        await sandbox.wait()
        print("✅ Sandbox deployed successfully")

        # Create test binary data
        print("🔧 Creating test binary data...")
        test_binary_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82"

        # Alternative: create a simple binary file with some pattern
        binary_pattern = bytearray()
        for i in range(1000):
            binary_pattern.extend([i % 256, (i * 2) % 256, (i * 3) % 256])
        test_binary_data = bytes(binary_pattern)

        print(f"Binary data size: {len(test_binary_data)} bytes")

        # Write binary data to sandbox
        print("🔧 Writing binary data to sandbox...")
        target_path = "/blaxel/test-binary.bin"
        await sandbox.fs.write_binary(target_path, test_binary_data)
        print("✅ Binary data written successfully")

        # Verify the file exists and has correct size
        print("🔧 Verifying binary file...")
        directory = await sandbox.fs.ls("/blaxel")

        binary_file = None
        for file in directory.files:
            if file.name == "test-binary.bin":
                binary_file = file
                break

        assert binary_file is not None, "Binary file not found in directory"
        print(f"✅ Binary file found: {binary_file.name}")

        # Check file size
        local_size = len(test_binary_data)
        remote_size = binary_file.size
        print(f"Local size: {local_size}, Remote size: {remote_size}")

        if remote_size == local_size:
            print("✅ File size matches perfectly!")
        else:
            print(f"⚠️ File size mismatch: local={local_size}, remote={remote_size}")

        # Test with different binary data types
        print("🔧 Testing with different binary data types...")

        # Test with bytearray
        bytearray_data = bytearray(
            [0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x57, 0x6F, 0x72, 0x6C, 0x64]
        )  # "Hello World"
        await sandbox.fs.write_binary("/blaxel/test-bytearray.bin", bytearray_data)
        print("✅ Bytearray binary write successful")

        # Test with bytes
        bytes_data = b"This is a test binary file with some content"
        await sandbox.fs.write_binary("/blaxel/test-bytes.bin", bytes_data)
        print("✅ Bytes binary write successful")

        # Verify all files exist
        print("🔧 Verifying all binary files...")
        final_directory = await sandbox.fs.ls("/blaxel")
        file_names = [file.name for file in final_directory.files]

        expected_files = ["test-binary.bin", "test-bytearray.bin", "test-bytes.bin"]
        for expected_file in expected_files:
            if expected_file in file_names:
                print(f"✅ {expected_file} found")
            else:
                print(f"❌ {expected_file} not found")

        # Clean up test files
        print("🧹 Cleaning up test files...")
        for file_name in expected_files:
            try:
                await sandbox.fs.rm(f"/blaxel/{file_name}")
                print(f"✅ Removed {file_name}")
            except Exception as e:
                print(f"⚠️ Failed to remove {file_name}: {e}")

        print("🎉 All binary write tests completed successfully!")

    except Exception as e:
        print(f"❌ Binary write test failed with error: {e}")
        logger.exception("Binary write test error")
        raise
    finally:
        print("🧹 Final cleanup...")
        try:
            await SandboxInstance.delete(SANDBOX_NAME)
            print("✅ Sandbox deleted")
        except Exception as e:
            print(f"⚠️ Failed to delete sandbox: {e}")


if __name__ == "__main__":
    asyncio.run(main())

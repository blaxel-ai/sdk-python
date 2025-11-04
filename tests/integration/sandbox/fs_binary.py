import asyncio
import hashlib
import sys
import time
from pathlib import Path

from utils import create_or_get_sandbox, info, sep

from blaxel.core.sandbox import SandboxInstance

SANDBOX_NAME = "sandbox-test-fsbinary"


def create_repeating_pattern(total_size: int) -> bytes:
    """Helper function to create a repeating pattern for large files."""
    chunk_size = 1024 * 1024  # 1MB chunks
    pattern = bytes(i % 256 for i in range(chunk_size))

    chunks = []
    remaining = total_size
    while remaining > 0:
        to_write = min(remaining, chunk_size)
        chunks.append(pattern[:to_write])
        remaining -= to_write

    return b"".join(chunks)


def calculate_hash(data: bytes) -> str:
    """Helper function to calculate SHA256 hash of bytes."""
    return hashlib.sha256(data).hexdigest()


async def test_binary_file_upload(sandbox: SandboxInstance):
    """Test 1: Binary File Upload."""
    print(sep)
    info("Test 1: Binary File Upload")

    timestamp = int(time.time() * 1000)
    test_file_path = f"/tmp/binary-file-{timestamp}.bin"

    # Create binary test data with various byte values including null bytes
    binary_data = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0xFF, 0xFE, 0xFD, 0x8A, 0x8B, 0x8C])

    info(f"Uploading binary file to {test_file_path}...")
    upload_resp = await sandbox.fs.write_binary(test_file_path, binary_data)
    print(f"Upload response: {upload_resp}")

    info("Verifying file exists and reading it back...")
    downloaded_bytes = await sandbox.fs.read_binary(test_file_path)

    print(f"Original size: {len(binary_data)} bytes")
    print(f"Downloaded size: {len(downloaded_bytes)} bytes")
    print(f"Original data: {binary_data.hex()}")
    print(f"Downloaded data: {downloaded_bytes.hex()}")

    # Verify data integrity
    if len(binary_data) != len(downloaded_bytes):
        raise Exception(f"Size mismatch! Expected {len(binary_data)}, got {len(downloaded_bytes)}")

    if binary_data != downloaded_bytes:
        raise Exception("Binary data mismatch! Downloaded content doesn't match uploaded content")

    info("✅ Binary data verified successfully!")

    # Clean up
    info("Cleaning up test file...")
    await sandbox.fs.rm(test_file_path)
    info("✅ Test 1 passed: Binary File Upload")


async def test_streaming_large_file(sandbox: SandboxInstance):
    """Test 2: Streaming Large File (5MB)."""
    print(sep)
    info("Test 2: Streaming Large File (5MB)")

    timestamp = int(time.time() * 1000)
    source_file = f"/tmp/streaming-test-source-{timestamp}.bin"
    target_file = f"/tmp/streaming-test-target-{timestamp}.bin"

    file_size = 5 * 1024 * 1024  # 5MB

    try:
        info("Creating 5MB test file for streaming test...")
        test_data = create_repeating_pattern(file_size)
        upload_hash = calculate_hash(test_data)
        print(f"Upload hash: {upload_hash}")

        # Upload the file
        info(f"Uploading 5MB file to {source_file}...")
        start_upload = time.time()
        await sandbox.fs.write_binary(source_file, test_data)
        upload_duration = (time.time() - start_upload) * 1000
        upload_mbps = (file_size / (1024 * 1024)) / (upload_duration / 1000)
        info(f"Upload completed in {upload_duration:.0f}ms ({upload_mbps:.2f} MB/s)")

        # Download the file
        info(f"Downloading 5MB file from {source_file}...")
        start_download = time.time()
        downloaded_bytes = await sandbox.fs.read_binary(source_file)
        download_duration = (time.time() - start_download) * 1000
        download_mbps = (file_size / (1024 * 1024)) / (download_duration / 1000)
        info(f"Download completed in {download_duration:.0f}ms ({download_mbps:.2f} MB/s)")

        # Verify download hash
        download_hash = calculate_hash(downloaded_bytes)
        print(f"Download hash: {download_hash}")

        if len(downloaded_bytes) != file_size:
            raise Exception(f"Size mismatch! Expected {file_size}, got {len(downloaded_bytes)}")

        if upload_hash != download_hash:
            raise Exception(f"Hash mismatch! Upload: {upload_hash}, Download: {download_hash}")

        info("✅ File size and hash verified successfully!")

        # Test simultaneous read/write: stream from source to target
        info("Test 3: Simultaneous read/write by streaming copy...")
        start_copy = time.time()

        # Download source file and upload to target
        source_bytes = await sandbox.fs.read_binary(source_file)
        await sandbox.fs.write_binary(target_file, source_bytes)

        copy_duration = (time.time() - start_copy) * 1000
        copy_mbps = (file_size / (1024 * 1024)) / (copy_duration / 1000)
        info(f"Streaming copy completed in {copy_duration:.0f}ms ({copy_mbps:.2f} MB/s)")

        copy_hash = calculate_hash(source_bytes)
        print(f"Copy hash: {copy_hash}")

        if upload_hash != copy_hash:
            raise Exception(f"Copy hash mismatch! Expected: {upload_hash}, Got: {copy_hash}")

        # Verify target file by reading it back
        info("Verifying copied file integrity...")
        verify_bytes = await sandbox.fs.read_binary(target_file)
        verify_hash = calculate_hash(verify_bytes)
        print(f"Verify hash: {verify_hash}")

        if len(verify_bytes) != file_size:
            raise Exception(f"Verified file size mismatch! Expected {file_size}, got {len(verify_bytes)}")

        if upload_hash != verify_hash:
            raise Exception(f"Verified hash mismatch! Expected: {upload_hash}, Got: {verify_hash}")

        info("✅ Copied file verified successfully!")
        info("✅ Test 2 passed: Streaming Large File")

    finally:
        # Clean up
        info("Cleaning up test files...")
        try:
            await sandbox.fs.rm(source_file)
            info(f"Deleted source file: {source_file}")
        except Exception as e:
            print(f"Failed to delete source file: {e}")

        try:
            await sandbox.fs.rm(target_file)
            info(f"Deleted target file: {target_file}")
        except Exception as e:
            print(f"Failed to delete target file: {e}")


async def test_various_binary_types(sandbox: SandboxInstance):
    """Test 3: Various Binary Content Types."""
    print(sep)
    info("Test 3: Various Binary Content Types")

    timestamp = int(time.time() * 1000)

    # Test with different binary patterns
    test_cases = [
        {"name": "All zeros", "data": bytes([0x00] * 1024)},
        {"name": "All ones", "data": bytes([0xFF] * 1024)},
        {"name": "Sequential", "data": bytes(range(256))},
        {"name": "Random pattern", "data": bytes((i * 137) % 256 for i in range(1024))},
    ]

    for test_case in test_cases:
        info(f"Testing: {test_case['name']} ({len(test_case['data'])} bytes)")
        file_path = f"/tmp/binary-test-{test_case['name'].replace(' ', '-')}-{timestamp}.bin"

        original_hash = calculate_hash(test_case["data"])

        # Upload
        await sandbox.fs.write_binary(file_path, test_case["data"])

        # Download
        downloaded_bytes = await sandbox.fs.read_binary(file_path)
        downloaded_hash = calculate_hash(downloaded_bytes)

        # Verify
        if original_hash != downloaded_hash:
            raise Exception(
                f"{test_case['name']}: Hash mismatch! Original: {original_hash}, Downloaded: {downloaded_hash}"
            )

        if test_case["data"] != downloaded_bytes:
            raise Exception(f"{test_case['name']}: Binary data mismatch!")

        # Clean up
        await sandbox.fs.rm(file_path)
        info(f"✅ {test_case['name']} verified")

    info("✅ Test 3 passed: Various Binary Content Types")


async def test_binary_from_local_file(sandbox: SandboxInstance):
    """Test 4: Upload Binary File from Local Filesystem."""
    print(sep)
    info("Test 4: Upload Binary File from Local Filesystem")

    timestamp = int(time.time() * 1000)
    local_file_path = f"/tmp/local-test-{timestamp}.bin"
    remote_file_path = f"/tmp/remote-test-{timestamp}.bin"

    # Create a local binary file
    test_data = bytes((i % 256) for i in range(10240))
    Path(local_file_path).write_bytes(test_data)

    try:
        info(f"Uploading local file: {local_file_path} -> {remote_file_path}")

        # Upload using string path (filesystem path)
        await sandbox.fs.write_binary(remote_file_path, local_file_path)

        # Download and verify
        downloaded_bytes = await sandbox.fs.read_binary(remote_file_path)

        original_hash = calculate_hash(test_data)
        downloaded_hash = calculate_hash(downloaded_bytes)

        if original_hash != downloaded_hash:
            raise Exception(f"Hash mismatch! Original: {original_hash}, Downloaded: {downloaded_hash}")

        info("✅ Local file uploaded and verified successfully!")

        # Clean up remote
        await sandbox.fs.rm(remote_file_path)

    finally:
        # Clean up local
        try:
            Path(local_file_path).unlink()
        except Exception as e:
            print(f"Failed to delete local file: {e}")

    info("✅ Test 4 passed: Binary File from Local Filesystem")


async def run_tests():
    """Main test runner."""
    try:
        sandbox = await create_or_get_sandbox(
            sandbox_name=SANDBOX_NAME,
            image="blaxel/base-image:latest",
            memory=8192  # 8GB for handling large files
        )

        print(sep)
        info("Starting Binary Filesystem Tests")
        print(sep)

        # Ensure tmp directory exists
        try:
            await sandbox.fs.mkdir("/tmp")
        except Exception:
            # Directory might already exist
            pass

        # Run all tests
        await test_binary_file_upload(sandbox)
        await test_various_binary_types(sandbox)
        await test_binary_from_local_file(sandbox)
        await test_streaming_large_file(sandbox)  # Run this last as it's the most intensive

        print(sep)
        info("✅ All binary filesystem tests passed!")
        print(sep)

    except Exception as e:
        print(sep)
        print("❌ Test failed with error:")
        print(e)
        import traceback
        traceback.print_exc()
        print(sep)
        sys.exit(1)
    finally:
        info("Cleaning up sandbox...")
        await SandboxInstance.delete(SANDBOX_NAME)
        info("✅ Cleanup complete")


if __name__ == "__main__":
    asyncio.run(run_tests())


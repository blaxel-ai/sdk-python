import asyncio
import hashlib
import sys
import time
from pathlib import Path

from utils import create_or_get_sandbox, info, sep

from blaxel.core.sandbox import SandboxInstance

SANDBOX_NAME = "sandbox-test-multipart"


def calculate_hash(data: bytes) -> str:
    """Helper function to calculate SHA256 hash of bytes."""
    return hashlib.sha256(data).hexdigest()


async def test_small_file_regular_upload(sandbox: SandboxInstance):
    """Test 1: Small file (should use regular upload, not multipart)."""
    print(sep)
    info("Test 1: Small File Upload (< 5MB)")

    small_content = "Hello, world! " * 1000  # ~14KB
    content_bytes = small_content.encode('utf-8')
    file_size_kb = len(content_bytes) / 1024

    info(f"File size: {file_size_kb:.2f} KB")

    await sandbox.fs.write("/tmp/small-file.txt", small_content)
    info("✓ Small file uploaded successfully")

    read_content = await sandbox.fs.read("/tmp/small-file.txt")
    assert read_content == small_content, "Small file content should match"
    info("✓ Small file content verified")

    # Clean up
    await sandbox.fs.rm("/tmp/small-file.txt")
    info("✅ Test 1 passed: Small File Upload")


async def test_large_text_file_multipart(sandbox: SandboxInstance):
    """Test 2: Large text file (should use multipart upload)."""
    print(sep)
    info("Test 2: Large Text File Upload (> 5MB, multipart)")

    # Create content > 5MB
    large_content = "Large file content line. " * 250000  # ~6MB
    content_bytes = large_content.encode('utf-8')
    file_size_mb = len(content_bytes) / (1024 * 1024)

    info(f"File size: {file_size_mb:.2f} MB")

    start_time = time.time()
    await sandbox.fs.write("/tmp/large-file.txt", large_content)
    upload_duration = time.time() - start_time
    info(f"✓ Large text file uploaded with multipart in {upload_duration:.2f}s")

    read_content = await sandbox.fs.read("/tmp/large-file.txt")
    assert read_content == large_content, "Large file content should match"
    assert len(read_content) == len(large_content), "Large file size should match"
    info("✓ Large file content verified")

    # Clean up
    await sandbox.fs.rm("/tmp/large-file.txt")
    info("✅ Test 2 passed: Large Text File Multipart Upload")


async def test_large_binary_file_multipart(sandbox: SandboxInstance):
    """Test 3: Large binary file (should use multipart upload)."""
    print(sep)
    info("Test 3: Large Binary File Upload (> 5MB, multipart)")

    binary_size = 6 * 1024 * 1024  # 6MB
    # Create binary content with pattern for verification
    binary_content = bytes((i % 256) for i in range(binary_size))
    file_size_mb = binary_size / (1024 * 1024)

    info(f"File size: {file_size_mb:.2f} MB")

    original_hash = calculate_hash(binary_content)
    info(f"Original hash: {original_hash}")

    start_time = time.time()
    await sandbox.fs.write_binary("/tmp/large-binary.bin", binary_content)
    upload_duration = time.time() - start_time
    info(f"✓ Large binary file uploaded with multipart in {upload_duration:.2f}s")

    read_binary = await sandbox.fs.read_binary("/tmp/large-binary.bin")
    downloaded_hash = calculate_hash(read_binary)
    info(f"Downloaded hash: {downloaded_hash}")

    assert len(read_binary) == binary_size, "Binary file size should match"
    assert original_hash == downloaded_hash, "Binary file hash should match"
    # Verify pattern integrity
    assert all(read_binary[i] == i % 256 for i in range(min(1000, binary_size))), "Binary content pattern should match"
    info("✓ Large binary file content verified")

    # Clean up
    await sandbox.fs.rm("/tmp/large-binary.bin")
    info("✅ Test 3 passed: Large Binary File Multipart Upload")


async def test_very_large_file_multiple_parts(sandbox: SandboxInstance):
    """Test 4: Very large file (multiple parts, > 10MB)."""
    print(sep)
    info("Test 4: Very Large File Upload (> 10MB, multiple parts)")

    # Create content > 10MB to test multiple parts
    very_large_content = "X" * (12 * 1024 * 1024)  # 12MB (will be split into 3 parts)
    content_bytes = very_large_content.encode('utf-8')
    file_size_mb = len(content_bytes) / (1024 * 1024)

    info(f"File size: {file_size_mb:.2f} MB (will be split into ~3 parts)")

    start_time = time.time()
    await sandbox.fs.write("/tmp/very-large-file.txt", very_large_content)
    upload_duration = time.time() - start_time
    upload_speed = file_size_mb / upload_duration
    info(f"✓ Very large file uploaded with multipart in {upload_duration:.2f}s ({upload_speed:.2f} MB/s)")

    start_time = time.time()
    read_content = await sandbox.fs.read("/tmp/very-large-file.txt")
    download_duration = time.time() - start_time
    download_speed = file_size_mb / download_duration
    info(f"✓ Very large file downloaded in {download_duration:.2f}s ({download_speed:.2f} MB/s)")

    assert len(read_content) == len(very_large_content), "Very large file size should match"
    info("✓ Very large file content verified")

    # Clean up
    await sandbox.fs.rm("/tmp/very-large-file.txt")
    info("✅ Test 4 passed: Very Large File Multipart Upload")


async def test_upload_and_download_real_file(sandbox: SandboxInstance):
    """Test 5: Upload and download real file from local filesystem."""
    print(sep)
    info("Test 5: Upload and Download Real File")

    # Create a temporary large file locally
    test_dir = Path(__file__).parent
    local_file_path = test_dir / "test-large-file.bin"
    downloaded_file_path = test_dir / "downloaded-large-file.bin"

    try:
        # Create a 7MB test file
        file_size = 7 * 1024 * 1024
        test_data = bytes((i % 256) for i in range(file_size))
        local_file_path.write_bytes(test_data)

        original_hash = calculate_hash(test_data)
        file_size_mb = file_size / (1024 * 1024)
        info(f"Created local test file: {file_size_mb:.2f} MB")
        info(f"Original hash: {original_hash}")

        # Upload the file using file path
        start_time = time.time()
        await sandbox.fs.write_binary("/tmp/uploaded-file.bin", str(local_file_path))
        upload_duration = time.time() - start_time
        info(f"✓ File uploaded to sandbox in {upload_duration:.2f}s")

        # Download the file back
        start_time = time.time()
        await sandbox.fs.download("/tmp/uploaded-file.bin", str(downloaded_file_path))
        download_duration = time.time() - start_time
        info(f"✓ File downloaded from sandbox in {download_duration:.2f}s")

        # Verify downloaded file
        downloaded_data = downloaded_file_path.read_bytes()
        downloaded_hash = calculate_hash(downloaded_data)
        info(f"Downloaded hash: {downloaded_hash}")

        assert len(downloaded_data) == file_size, "Downloaded file size should match original"
        assert original_hash == downloaded_hash, "Downloaded file hash should match original"
        info("✓ Downloaded file verified (byte-perfect match)")

        # Clean up remote file
        await sandbox.fs.rm("/tmp/uploaded-file.bin")
        info("✅ Test 5 passed: Upload and Download Real File")

    finally:
        # Clean up local files
        if local_file_path.exists():
            local_file_path.unlink()
        if downloaded_file_path.exists():
            downloaded_file_path.unlink()


async def test_verify_all_uploaded_files(sandbox: SandboxInstance):
    """Test 6: Verify all files can be listed."""
    print(sep)
    info("Test 6: Verify Files List")

    # Upload multiple files of different sizes
    test_files = {
        "small-1.txt": "Small content 1",
        "small-2.txt": "Small content 2",
        "large-1.txt": "X" * (6 * 1024 * 1024),  # 6MB
    }

    for filename, content in test_files.items():
        await sandbox.fs.write(f"/tmp/multipart-test-{filename}", content)
        info(f"✓ Uploaded {filename}")

    # List files
    listing = await sandbox.fs.ls("/tmp")
    uploaded_filenames = [f.name for f in listing.files]
    info(f"Files in /tmp: {', '.join(uploaded_filenames)}")

    # Verify all files exist
    for filename in test_files.keys():
        full_name = f"multipart-test-{filename}"
        assert full_name in uploaded_filenames, f"Should find {full_name}"
        info(f"✓ Found {full_name}")

    # Clean up
    for filename in test_files.keys():
        await sandbox.fs.rm(f"/tmp/multipart-test-{filename}")

    info("✅ Test 6 passed: Verify Files List")


async def test_edge_case_exactly_threshold(sandbox: SandboxInstance):
    """Test 7: File exactly at threshold size (5MB)."""
    print(sep)
    info("Test 7: Edge Case - File Exactly 5MB")

    # Create content exactly 5MB (at threshold)
    exact_size = 5 * 1024 * 1024
    exact_content = "A" * exact_size
    content_bytes = exact_content.encode('utf-8')
    file_size_mb = len(content_bytes) / (1024 * 1024)

    info(f"File size: {file_size_mb:.2f} MB (exactly at threshold)")

    await sandbox.fs.write("/tmp/exact-threshold.txt", exact_content)
    info("✓ File at exact threshold uploaded")

    read_content = await sandbox.fs.read("/tmp/exact-threshold.txt")
    assert len(read_content) == len(exact_content), "File size should match"
    info("✓ File content verified")

    # Clean up
    await sandbox.fs.rm("/tmp/exact-threshold.txt")
    info("✅ Test 7 passed: Edge Case File")


async def run_tests():
    """Main test runner."""
    try:
        sandbox = await create_or_get_sandbox(
            sandbox_name=SANDBOX_NAME,
            image="blaxel/base-image:latest",
            memory=8192  # 8GB for handling large files
        )

        print(sep)
        info("Starting Multipart Upload Tests")
        print(sep)

        # Ensure tmp directory exists
        try:
            await sandbox.fs.mkdir("/tmp")
        except Exception:
            # Directory might already exist
            pass

        # Run all tests
        await test_small_file_regular_upload(sandbox)
        await test_large_text_file_multipart(sandbox)
        await test_large_binary_file_multipart(sandbox)
        await test_very_large_file_multiple_parts(sandbox)
        await test_upload_and_download_real_file(sandbox)
        await test_verify_all_uploaded_files(sandbox)
        await test_edge_case_exactly_threshold(sandbox)

        print(sep)
        info("✅ All multipart upload tests passed!")
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


import asyncio
import sys
from pathlib import Path

from blaxel.core.sandbox import SandboxInstance


async def main():
    """Test file read and download operations."""
    try:
        # Get the directory where this test file is located
        test_dir = Path(__file__).parent
        archive_path = test_dir / "archive.zip"
        downloaded_path = test_dir / "archive.downloaded.zip"

        # Ensure archive exists
        if not archive_path.exists():
            print(f"❌ Test archive not found at {archive_path}")
            sys.exit(1)

        sandbox = await SandboxInstance.create()
        print("✓ Sandbox created")

        # Test text file write
        await sandbox.fs.write("/tmp/test.txt", "Hello world")
        print("✓ Text file written")

        # Test binary file write from local path
        await sandbox.fs.write_binary("/tmp/archive.zip", str(archive_path))
        print("✓ Binary file written")

        # Test ls
        listing = await sandbox.fs.ls("/tmp")
        assert any(f.name == "test.txt" for f in listing.files), "test.txt should exist in /tmp"
        assert any(f.name == "archive.zip" for f in listing.files), "archive.zip should exist in /tmp"
        print("✓ Files listed correctly")

        # Test read text file
        text_content = await sandbox.fs.read("/tmp/test.txt")
        assert text_content == "Hello world", "Text content should match"
        print("✓ Text file read correctly")

        # Test read_binary
        binary_bytes = await sandbox.fs.read_binary("/tmp/archive.zip")
        assert isinstance(binary_bytes, bytes), "read_binary should return bytes"
        print("✓ Binary file read correctly")

        text_content_binary = await sandbox.fs.read_binary("/tmp/test.txt")
        assert isinstance(text_content_binary, bytes), "read_binary should return bytes"
        print("✓ Text file read as binary correctly")

        # Test download
        await sandbox.fs.download("/tmp/archive.zip", str(downloaded_path))
        print("✓ Binary file downloaded")

        # Compare file sizes
        original_size = archive_path.stat().st_size
        downloaded_size = downloaded_path.stat().st_size

        print(f"Original file size: {original_size} bytes")
        print(f"Downloaded file size: {downloaded_size} bytes")
        assert downloaded_size == original_size, "Downloaded file size should match original"
        print("✓ File sizes match")

        # Cleanup
        await SandboxInstance.delete(sandbox.metadata.name)
        print("✓ Sandbox deleted")

        # Clean up downloaded file
        if downloaded_path.exists():
            downloaded_path.unlink()
            print("✓ Downloaded file cleaned up")

        print("\n✅ All tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())


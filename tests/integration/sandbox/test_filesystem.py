import asyncio

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import async_sleep, default_image, default_labels, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestFilesystemOperations:
    """Test sandbox filesystem operations."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("fs-test")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": default_image,
                "memory": 2048,
                "labels": default_labels,
            }
        )

        yield

        # Cleanup
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestWriteAndRead(TestFilesystemOperations):
    """Test write and read operations."""

    async def test_writes_and_reads_text_file(self):
        """Test writing and reading a text file."""
        content = "Hello, World!"
        path = "/tmp/test-write.txt"

        await self.sandbox.fs.write(path, content)
        result = await self.sandbox.fs.read(path)

        assert result == content

    async def test_writes_and_reads_unicode_content(self):
        """Test writing and reading unicode content."""
        content = "Hello 世界 🌍 émojis"
        path = "/tmp/test-unicode.txt"

        await self.sandbox.fs.write(path, content)
        result = await self.sandbox.fs.read(path)

        assert result == content

    async def test_writes_and_reads_multiline_content(self):
        """Test writing and reading multiline content."""
        content = "Line 1\nLine 2\nLine 3"
        path = "/tmp/test-multiline.txt"

        await self.sandbox.fs.write(path, content)
        result = await self.sandbox.fs.read(path)

        assert result == content

    async def test_overwrites_existing_file(self):
        """Test overwriting an existing file."""
        path = "/tmp/test-overwrite.txt"

        await self.sandbox.fs.write(path, "original")
        await self.sandbox.fs.write(path, "updated")

        result = await self.sandbox.fs.read(path)
        assert result == "updated"


@pytest.mark.asyncio(loop_scope="class")
class TestBinaryOperations(TestFilesystemOperations):
    """Test binary write and read operations."""

    async def test_read_binary_works_on_text_files(self):
        """Test that readBinary works on text files too."""
        path = "/tmp/test-binary-text.txt"
        await self.sandbox.fs.write(path, "text content")

        blob = await self.sandbox.fs.read_binary(path)
        assert isinstance(blob, bytes)

        text = blob.decode("utf-8")
        assert text == "text content"


@pytest.mark.asyncio(loop_scope="class")
class TestListDirectory(TestFilesystemOperations):
    """Test ls (list directory) operations."""

    async def test_lists_files_in_directory(self):
        """Test listing files in a directory."""
        # Create some test files
        await self.sandbox.fs.write("/tmp/ls-test/file1.txt", "content1")
        await self.sandbox.fs.write("/tmp/ls-test/file2.txt", "content2")

        listing = await self.sandbox.fs.ls("/tmp/ls-test")

        assert listing.files is not None
        assert len(listing.files) >= 2

        names = [f.name for f in listing.files]
        assert "file1.txt" in names
        assert "file2.txt" in names

    async def test_lists_subdirectories(self):
        """Test listing subdirectories."""
        await self.sandbox.fs.mkdir("/tmp/ls-subdir-test/subdir1")
        await self.sandbox.fs.mkdir("/tmp/ls-subdir-test/subdir2")

        listing = await self.sandbox.fs.ls("/tmp/ls-subdir-test")

        assert listing.subdirectories is not None
        names = [d.name for d in listing.subdirectories]
        assert "subdir1" in names
        assert "subdir2" in names

    async def test_returns_file_metadata(self):
        """Test that file metadata is returned."""
        await self.sandbox.fs.write("/tmp/meta-test.txt", "some content")
        listing = await self.sandbox.fs.ls("/tmp")

        file = next((f for f in listing.files if f.name == "meta-test.txt"), None)
        assert file is not None
        assert file.path == "/tmp/meta-test.txt"


@pytest.mark.asyncio(loop_scope="class")
class TestMkdir(TestFilesystemOperations):
    """Test mkdir operations."""

    async def test_creates_directory(self):
        """Test creating a directory."""
        import time

        path = f"/tmp/new-dir-{int(time.time() * 1000)}"
        await self.sandbox.fs.mkdir(path)

        listing = await self.sandbox.fs.ls(path)
        assert listing is not None

    async def test_creates_nested_directories(self):
        """Test creating nested directories."""
        import time

        path = f"/tmp/nested-{int(time.time() * 1000)}/level1/level2"
        await self.sandbox.fs.mkdir(path)

        listing = await self.sandbox.fs.ls(path)
        assert listing is not None


@pytest.mark.asyncio(loop_scope="class")
class TestCopy(TestFilesystemOperations):
    """Test cp (copy) operations."""

    async def test_copies_file(self):
        """Test copying a file."""
        src = "/tmp/cp-src.txt"
        dst = "/tmp/cp-dst.txt"

        await self.sandbox.fs.write(src, "copy me")
        await self.sandbox.fs.cp(src, dst)

        content = await self.sandbox.fs.read(dst)
        assert content == "copy me"

    async def test_copies_directory(self):
        """Test copying a directory."""
        src_dir = "/tmp/cp-dir-src"
        dst_dir = "/tmp/cp-dir-dst"

        await self.sandbox.fs.write(f"{src_dir}/file.txt", "content")
        await self.sandbox.fs.cp(src_dir, dst_dir)

        content = await self.sandbox.fs.read(f"{dst_dir}/file.txt")
        assert content == "content"


@pytest.mark.asyncio(loop_scope="class")
class TestRemove(TestFilesystemOperations):
    """Test rm (remove) operations."""

    async def test_removes_file(self):
        """Test removing a file."""
        path = "/tmp/rm-file.txt"
        await self.sandbox.fs.write(path, "delete me")

        await self.sandbox.fs.rm(path)

        # File should no longer exist
        with pytest.raises(Exception):
            await self.sandbox.fs.read(path)

    async def test_removes_directory_recursively(self):
        """Test removing a directory recursively."""
        dir_path = "/tmp/rm-dir"
        await self.sandbox.fs.write(f"{dir_path}/file.txt", "content")
        await self.sandbox.fs.mkdir(f"{dir_path}/subdir")

        await self.sandbox.fs.rm(dir_path, recursive=True)

        with pytest.raises(Exception):
            await self.sandbox.fs.ls(dir_path)


@pytest.mark.asyncio(loop_scope="class")
class TestWatch(TestFilesystemOperations):
    """Test watch operations."""

    async def test_watches_for_file_changes(self):
        """Test watching for file changes."""
        import time

        dir_path = f"/tmp/watch-test-{int(time.time() * 1000)}"
        await self.sandbox.fs.mkdir(dir_path)

        change_detected = False

        def on_change(event):
            nonlocal change_detected
            if event.name == "watched-file.txt":
                change_detected = True

        handle = self.sandbox.fs.watch(dir_path, on_change)

        await async_sleep(0.5)
        # Trigger a file change
        await self.sandbox.fs.write(f"{dir_path}/watched-file.txt", "new content")

        # Wait for callback
        await async_sleep(0.5)
        handle["close"]()

        assert change_detected is True


@pytest.mark.asyncio(loop_scope="class")
class TestMultipartUpload(TestFilesystemOperations):
    """Test multipart upload for large files."""

    async def test_uploads_small_file(self):
        """Test uploading a small file (< 1MB) via regular upload."""
        content = "Hello, world! " * 1000  # ~14KB
        path = "/tmp/small-upload.txt"

        await self.sandbox.fs.write(path, content)

        result = await self.sandbox.fs.read(path)
        assert result == content

    async def test_uploads_large_text_file(self):
        """Test uploading a large text file (> 1MB) via multipart."""
        content = "Large file content line. " * 50000  # ~1.2MB
        path = "/tmp/large-upload.txt"

        await self.sandbox.fs.write(path, content)

        result = await self.sandbox.fs.read(path)
        assert len(result) == len(content)
        assert result == content


@pytest.mark.asyncio(loop_scope="class")
class TestParallelOperations(TestFilesystemOperations):
    """Test parallel operations."""

    async def test_handles_100_parallel_file_reads(self):
        """Test handling 100 parallel file reads."""
        # Create a test file
        content = "A" * (200 * 1024)  # 200KB
        path = "/tmp/parallel-read.txt"
        await self.sandbox.fs.write(path, content)

        # Make 100 parallel read calls
        async def read_and_get_length():
            file_content = await self.sandbox.fs.read(path)
            return len(file_content)

        results = await asyncio.gather(*[read_and_get_length() for _ in range(100)])

        # All reads should return the same size
        assert all(size == len(content) for size in results)

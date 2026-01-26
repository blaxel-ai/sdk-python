import asyncio

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import async_sleep, default_image, default_labels, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestFilesystemOperations:
    """Test sandbox filesystem operations."""

    sandbox: SandboxInstance
    sandbox_name: str

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
            await self.sandbox.delete()
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
class TestWriteBinary(TestFilesystemOperations):
    """Test write_binary operations."""

    async def test_writes_and_reads_binary_content(self):
        """Test writing and reading binary content."""
        import time

        path = f"/tmp/binary-test-{int(time.time() * 1000)}.bin"
        # Create binary content with various byte values
        binary_content = bytes([0, 1, 2, 127, 128, 255, 0, 100, 200])

        await self.sandbox.fs.write_binary(path, binary_content)
        result = await self.sandbox.fs.read_binary(path)

        assert result == binary_content

    async def test_writes_binary_from_bytearray(self):
        """Test writing binary content from bytearray."""
        import time

        path = f"/tmp/bytearray-test-{int(time.time() * 1000)}.bin"
        binary_content = bytearray([10, 20, 30, 40, 50])

        await self.sandbox.fs.write_binary(path, binary_content)
        result = await self.sandbox.fs.read_binary(path)

        assert result == bytes(binary_content)

    async def test_writes_large_binary_file(self):
        """Test writing a large binary file."""
        import time

        path = f"/tmp/large-binary-{int(time.time() * 1000)}.bin"
        # Create ~500KB of binary data
        binary_content = bytes(range(256)) * 2000

        await self.sandbox.fs.write_binary(path, binary_content)
        result = await self.sandbox.fs.read_binary(path)

        assert len(result) == len(binary_content)
        assert result == binary_content


@pytest.mark.asyncio(loop_scope="class")
class TestWriteTree(TestFilesystemOperations):
    """Test write_tree operations."""

    async def test_writes_multiple_files(self):
        """Test writing multiple files in a tree structure."""
        import time

        base_dir = f"/tmp/tree-test-{int(time.time() * 1000)}"
        files = [
            {"path": f"{base_dir}/file1.txt", "content": "content1"},
            {"path": f"{base_dir}/file2.txt", "content": "content2"},
            {"path": f"{base_dir}/subdir/file3.txt", "content": "content3"},
        ]

        result = await self.sandbox.fs.write_tree(files)
        assert result is not None

        # Verify files were created
        content1 = await self.sandbox.fs.read(f"{base_dir}/file1.txt")
        content2 = await self.sandbox.fs.read(f"{base_dir}/file2.txt")
        content3 = await self.sandbox.fs.read(f"{base_dir}/subdir/file3.txt")

        assert content1 == "content1"
        assert content2 == "content2"
        assert content3 == "content3"

    async def test_writes_tree_with_destination_path(self):
        """Test writing files with a destination path prefix."""
        import time

        base_dir = f"/tmp/tree-dest-{int(time.time() * 1000)}"
        files = [
            {"path": "a.txt", "content": "file a"},
            {"path": "b.txt", "content": "file b"},
        ]

        result = await self.sandbox.fs.write_tree(files, destination_path=base_dir)
        assert result is not None

        # Verify files were created at destination
        content_a = await self.sandbox.fs.read(f"{base_dir}/a.txt")
        content_b = await self.sandbox.fs.read(f"{base_dir}/b.txt")

        assert content_a == "file a"
        assert content_b == "file b"


@pytest.mark.asyncio(loop_scope="class")
class TestDownload(TestFilesystemOperations):
    """Test download operations."""

    async def test_downloads_file_to_local(self):
        """Test downloading a file from sandbox to local filesystem."""
        import os
        import tempfile
        import time

        # Create a file in the sandbox
        sandbox_path = f"/tmp/download-test-{int(time.time() * 1000)}.txt"
        content = "Download me!"
        await self.sandbox.fs.write(sandbox_path, content)

        # Download to local temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            local_path = tmp.name

        try:
            await self.sandbox.fs.download(sandbox_path, local_path)

            # Verify local file content
            with open(local_path, "r") as f:
                local_content = f.read()

            assert local_content == content
        finally:
            # Cleanup
            if os.path.exists(local_path):
                os.remove(local_path)

    async def test_downloads_binary_file_to_local(self):
        """Test downloading a binary file from sandbox to local filesystem."""
        import os
        import tempfile
        import time

        # Create a binary file in the sandbox
        sandbox_path = f"/tmp/download-binary-{int(time.time() * 1000)}.bin"
        binary_content = bytes([0, 1, 2, 127, 128, 255])
        await self.sandbox.fs.write_binary(sandbox_path, binary_content)

        # Download to local temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as tmp:
            local_path = tmp.name

        try:
            await self.sandbox.fs.download(sandbox_path, local_path)

            # Verify local file content
            with open(local_path, "rb") as f:
                local_content = f.read()

            assert local_content == binary_content
        finally:
            # Cleanup
            if os.path.exists(local_path):
                os.remove(local_path)


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
class TestFind(TestFilesystemOperations):
    """Test find operations."""

    async def test_finds_files_by_pattern(self):
        """Test finding files by pattern."""
        import time

        base_dir = f"/tmp/find-test-{int(time.time() * 1000)}"
        await self.sandbox.fs.write(f"{base_dir}/file1.txt", "content1")
        await self.sandbox.fs.write(f"{base_dir}/file2.txt", "content2")
        await self.sandbox.fs.write(f"{base_dir}/file3.py", "content3")

        result = await self.sandbox.fs.find(base_dir, patterns=["*.txt"])
        assert result is not None

        assert result.total >= 2
        paths = [m.path for m in result.matches]
        assert any("file1.txt" in p for p in paths)
        assert any("file2.txt" in p for p in paths)
        assert not any("file3.py" in p for p in paths)

    async def test_finds_directories(self):
        """Test finding directories only."""
        import time

        base_dir = f"/tmp/find-dir-test-{int(time.time() * 1000)}"
        await self.sandbox.fs.mkdir(f"{base_dir}/subdir1")
        await self.sandbox.fs.mkdir(f"{base_dir}/subdir2")
        await self.sandbox.fs.write(f"{base_dir}/file.txt", "content")

        result = await self.sandbox.fs.find(base_dir, type="directory")
        assert result is not None

        types = [m.type_ for m in result.matches]
        assert all(t == "directory" for t in types)

    async def test_finds_files_only(self):
        """Test finding files only."""
        import time

        base_dir = f"/tmp/find-files-only-{int(time.time() * 1000)}"
        await self.sandbox.fs.mkdir(f"{base_dir}/subdir")
        await self.sandbox.fs.write(f"{base_dir}/file1.txt", "content1")
        await self.sandbox.fs.write(f"{base_dir}/file2.txt", "content2")

        result = await self.sandbox.fs.find(base_dir, type="file")
        assert result is not None

        assert result.matches is not None
        types = [m.type_ for m in result.matches]
        assert all(t == "file" for t in types)

    async def test_respects_max_results(self):
        """Test that max_results limits the results."""
        import time

        base_dir = f"/tmp/find-max-{int(time.time() * 1000)}"
        for i in range(5):
            await self.sandbox.fs.write(f"{base_dir}/file{i}.txt", f"content{i}")

        result = await self.sandbox.fs.find(base_dir, max_results=2)
        assert result is not None

        assert result.matches is not None
        assert len(result.matches) <= 2

    async def test_finds_nested_files(self):
        """Test finding files in nested directories."""
        import time

        base_dir = f"/tmp/find-nested-{int(time.time() * 1000)}"
        await self.sandbox.fs.write(f"{base_dir}/level1/level2/deep.txt", "deep content")
        await self.sandbox.fs.write(f"{base_dir}/shallow.txt", "shallow content")

        result = await self.sandbox.fs.find(base_dir, patterns=["*.txt"])
        assert result is not None

        assert result.matches is not None
        paths = [m.path for m in result.matches]
        assert any("deep.txt" in p for p in paths)
        assert any("shallow.txt" in p for p in paths)

    async def test_find_with_all_options(self):
        """Test find with all options set."""
        import time

        base_dir = f"/tmp/find-all-opts-{int(time.time() * 1000)}"
        # Create visible files
        await self.sandbox.fs.write(f"{base_dir}/visible1.txt", "content1")
        await self.sandbox.fs.write(f"{base_dir}/visible2.txt", "content2")
        await self.sandbox.fs.write(f"{base_dir}/visible3.py", "content3")
        # Create hidden file
        await self.sandbox.fs.write(f"{base_dir}/.hidden.txt", "hidden content")
        # Create file in excluded directory
        await self.sandbox.fs.write(f"{base_dir}/node_modules/dep.txt", "dep content")
        # Create nested file
        await self.sandbox.fs.write(f"{base_dir}/src/nested.txt", "nested content")

        result = await self.sandbox.fs.find(
            base_dir,
            type="file",
            patterns=["*.txt"],
            max_results=10,
            exclude_dirs=["node_modules"],
            exclude_hidden=True,
        )
        assert result is not None

        assert result.matches is not None
        paths = [m.path for m in result.matches]
        types = [m.type_ for m in result.matches]

        # Should find visible .txt files
        assert any("visible1.txt" in p for p in paths)
        assert any("visible2.txt" in p for p in paths)
        assert any("nested.txt" in p for p in paths)
        # Should not find .py file (pattern filter)
        assert not any("visible3.py" in p for p in paths)
        # Should not find hidden file (exclude_hidden)
        assert not any(".hidden.txt" in p for p in paths)
        # Should not find file in excluded directory
        assert not any("node_modules" in p for p in paths)
        # All should be files
        assert all(t == "file" for t in types)


@pytest.mark.asyncio(loop_scope="class")
class TestGrep(TestFilesystemOperations):
    """Test grep (content search) operations."""

    async def test_searches_text_in_files(self):
        """Test basic text search."""
        import time

        base_dir = f"/tmp/grep-test-{int(time.time() * 1000)}"
        await self.sandbox.fs.write(f"{base_dir}/file1.txt", "Hello World")
        await self.sandbox.fs.write(f"{base_dir}/file2.txt", "Goodbye World")
        await self.sandbox.fs.write(f"{base_dir}/file3.txt", "No match here")

        result = await self.sandbox.fs.grep("World", base_dir)
        assert result is not None

        assert result.matches is not None
        assert result.total >= 2
        assert result.query == "World"
        paths = [m.path for m in result.matches]
        assert any("file1.txt" in p for p in paths)
        assert any("file2.txt" in p for p in paths)

    async def test_case_sensitive_search(self):
        """Test case sensitive search."""
        import time

        base_dir = f"/tmp/grep-case-{int(time.time() * 1000)}"
        await self.sandbox.fs.write(f"{base_dir}/upper.txt", "HELLO")
        await self.sandbox.fs.write(f"{base_dir}/lower.txt", "hello")

        result = await self.sandbox.fs.grep("HELLO", base_dir, case_sensitive=True)
        assert result is not None

        assert result.matches is not None
        paths = [m.path for m in result.matches]
        assert any("upper.txt" in p for p in paths)
        # In case sensitive mode, lowercase should not match
        assert len([p for p in paths if "lower.txt" in p]) == 0

    async def test_case_insensitive_search(self):
        """Test case insensitive search."""
        import time

        base_dir = f"/tmp/grep-icase-{int(time.time() * 1000)}"
        await self.sandbox.fs.write(f"{base_dir}/upper.txt", "HELLO")
        await self.sandbox.fs.write(f"{base_dir}/lower.txt", "hello")

        result = await self.sandbox.fs.grep("hello", base_dir, case_sensitive=False)
        assert result is not None

        assert result.matches is not None
        paths = [m.path for m in result.matches]
        assert any("upper.txt" in p for p in paths)
        assert any("lower.txt" in p for p in paths)

    async def test_returns_line_information(self):
        """Test that search returns line and column info."""
        import time

        base_dir = f"/tmp/grep-line-{int(time.time() * 1000)}"
        content = "first line\nsecond line with match\nthird line"
        await self.sandbox.fs.write(f"{base_dir}/file.txt", content)

        result = await self.sandbox.fs.grep("match", base_dir)
        assert result is not None

        assert result.matches is not None
        assert len(result.matches) >= 1
        match = result.matches[0]
        assert match.line is not None
        assert match.text is not None
        assert "match" in match.text

    async def test_respects_file_pattern(self):
        """Test searching only in files matching pattern."""
        import time

        base_dir = f"/tmp/grep-pattern-{int(time.time() * 1000)}"
        await self.sandbox.fs.write(f"{base_dir}/code.py", "search_term here")
        await self.sandbox.fs.write(f"{base_dir}/data.txt", "search_term here too")

        result = await self.sandbox.fs.grep("search_term", base_dir, file_pattern="*.py")
        assert result is not None

        assert result.matches is not None
        paths = [m.path for m in result.matches]
        assert any("code.py" in p for p in paths)
        assert not any("data.txt" in p for p in paths)

    async def test_respects_max_results(self):
        """Test that max_results limits the search results."""
        import time

        base_dir = f"/tmp/grep-max-{int(time.time() * 1000)}"
        for i in range(5):
            await self.sandbox.fs.write(f"{base_dir}/file{i}.txt", "findme content")

        result = await self.sandbox.fs.grep("findme", base_dir, max_results=2)
        assert result is not None

        assert result.matches is not None
        assert len(result.matches) <= 2

    async def test_searches_nested_directories(self):
        """Test searching in nested directories."""
        import time

        base_dir = f"/tmp/grep-nested-{int(time.time() * 1000)}"
        await self.sandbox.fs.write(f"{base_dir}/level1/level2/deep.txt", "unique_string")
        await self.sandbox.fs.write(f"{base_dir}/shallow.txt", "unique_string")

        result = await self.sandbox.fs.grep("unique_string", base_dir)
        assert result is not None

        assert result.matches is not None
        assert result.total >= 2
        paths = [m.path for m in result.matches]
        assert any("deep.txt" in p for p in paths)
        assert any("shallow.txt" in p for p in paths)

    async def test_grep_with_all_options(self):
        """Test grep with all options set."""
        import time

        base_dir = f"/tmp/grep-all-opts-{int(time.time() * 1000)}"
        # Create files with target content
        content_with_context = "line one\nline two\nSEARCH_TARGET here\nline four\nline five"
        await self.sandbox.fs.write(f"{base_dir}/main.py", content_with_context)
        await self.sandbox.fs.write(f"{base_dir}/other.txt", "SEARCH_TARGET in txt")
        await self.sandbox.fs.write(f"{base_dir}/lowercase.py", "search_target lowercase")
        # Create file in excluded directory
        await self.sandbox.fs.write(
            f"{base_dir}/node_modules/dep.py", "SEARCH_TARGET in excluded"
        )

        result = await self.sandbox.fs.grep(
            "SEARCH_TARGET",
            base_dir,
            case_sensitive=True,
            context_lines=2,
            max_results=10,
            file_pattern="*.py",
            exclude_dirs=["node_modules"],
        )
        assert result is not None

        assert result.matches is not None
        assert result.query == "SEARCH_TARGET"
        paths = [m.path for m in result.matches]

        # Should find .py files with exact case match
        assert any("main.py" in p for p in paths)
        # Should not find .txt file (file_pattern filter)
        assert not any("other.txt" in p for p in paths)
        # Should not find lowercase version (case_sensitive)
        assert not any("lowercase.py" in p for p in paths)
        # Should not find file in excluded directory
        assert not any("node_modules" in p for p in paths)

        # Check context lines are included for main.py match
        main_match = next((m for m in result.matches if "main.py" in m.path), None)
        assert main_match is not None
        # With context_lines=2, we should have context around the match
        if main_match.context:
            assert "line" in main_match.context or "SEARCH_TARGET" in main_match.context


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

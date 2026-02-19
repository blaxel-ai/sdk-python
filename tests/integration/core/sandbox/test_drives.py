import asyncio
import time

import pytest
import pytest_asyncio

from blaxel.core.drive import DriveInstance
from blaxel.core.sandbox import SandboxInstance
from tests.helpers import (
    default_image,
    default_labels,
    default_region,
    unique_name,
    wait_for_sandbox_deletion,
)


class TestDriveOperations:
    """Base class for drive tests with cleanup tracking."""

    created_sandboxes: list[str] = []
    created_drives: list[str] = []

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def cleanup(self, request):
        """Clean up all resources after each test class."""
        # Reset lists for this class
        request.cls.created_sandboxes = []
        request.cls.created_drives = []

        yield

        # Clean up sandboxes first (they depend on drives)
        await asyncio.gather(
            *[self._safe_delete_sandbox(name) for name in request.cls.created_sandboxes],
            return_exceptions=True,
        )

        # Then clean up drives
        await asyncio.gather(
            *[self._safe_delete_drive(name) for name in request.cls.created_drives],
            return_exceptions=True,
        )

    async def _safe_delete_sandbox(self, name: str) -> None:
        """Safely delete a sandbox, ignoring errors."""
        try:
            await SandboxInstance.delete(name)
            await wait_for_sandbox_deletion(name)
        except Exception:
            pass

    async def _safe_delete_drive(self, name: str) -> None:
        """Safely delete a drive, ignoring errors."""
        try:
            await DriveInstance.delete(name)
        except Exception:
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestDriveInstanceCRUD(TestDriveOperations):
    """Test DriveInstance CRUD operations."""

    async def test_creates_a_drive(self):
        """Test creating a drive."""
        name = unique_name("drive")
        drive = await DriveInstance.create(
            {
                "name": name,
                "size": 10,  # 10GB
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(name)

        assert drive.name == name
        assert drive.size == 10
        assert drive.region == default_region

    async def test_creates_a_drive_with_display_name(self):
        """Test creating a drive with display name."""
        name = unique_name("drive-display")
        drive = await DriveInstance.create(
            {
                "name": name,
                "display_name": "My Test Drive",
                "size": 20,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(name)

        assert drive.display_name == "My Test Drive"

    async def test_gets_a_drive(self):
        """Test getting a drive."""
        name = unique_name("drive-get")
        await DriveInstance.create(
            {
                "name": name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(name)

        drive = await DriveInstance.get(name)
        assert drive.name == name

    async def test_lists_drives(self):
        """Test listing drives."""
        name = unique_name("drive-list")
        await DriveInstance.create(
            {
                "name": name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(name)

        drives = await DriveInstance.list()
        assert isinstance(drives, list)

        found = next((d for d in drives if d.name == name), None)
        assert found is not None

    async def test_updates_a_drive(self):
        """Test updating a drive."""
        name = unique_name("drive-update")
        drive = await DriveInstance.create(
            {
                "name": name,
                "display_name": "Original Name",
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(name)

        updated = await drive.update(
            {
                "display_name": "Updated Name",
                "labels": {
                    **default_labels,
                    "updated": "true",
                },
            }
        )

        assert updated.display_name == "Updated Name"
        assert updated.metadata.labels["updated"] == "true"

    async def test_deletes_a_drive(self):
        """Test deleting a drive."""
        name = unique_name("drive-delete")
        drive = await DriveInstance.create(
            {
                "name": name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        await drive.delete()

        # Drive should no longer exist
        with pytest.raises(Exception):
            await DriveInstance.get(name)

    async def test_creates_drive_if_not_exists(self):
        """Test creating a drive with idempotency."""
        name = unique_name("drive-idempotent")

        # Create the first time
        drive1 = await DriveInstance.create_if_not_exists(
            {
                "name": name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(name)

        # Create again - should return existing drive
        drive2 = await DriveInstance.create_if_not_exists(
            {
                "name": name,
                "size": 10,
                "region": default_region,
            }
        )

        assert drive1.name == drive2.name


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxDriveMounting(TestDriveOperations):
    """Test sandbox drive mounting operations."""

    async def test_attaches_a_drive_to_a_sandbox(self):
        """Test attaching a drive to a sandbox."""
        drive_name = unique_name("mount-drive")
        sandbox_name = unique_name("mount-sandbox")

        # Create drive
        await DriveInstance.create(
            {
                "name": drive_name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(drive_name)

        # Create sandbox
        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox_name)

        # Attach drive
        result = await sandbox.drive.attach(
            drive_name=drive_name,
            mount_path="/mnt/test",
            drive_path="/",
        )

        assert result["success"] is True
        assert result["driveName"] == drive_name
        assert result["mountPath"] == "/mnt/test"

    async def test_lists_mounted_drives(self):
        """Test listing mounted drives."""
        drive_name = unique_name("list-drive")
        sandbox_name = unique_name("list-sandbox")

        await DriveInstance.create(
            {
                "name": drive_name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(drive_name)

        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox_name)

        # Attach drive
        await sandbox.drive.attach(
            drive_name=drive_name,
            mount_path="/mnt/data",
        )

        # List mounts
        mounts = await sandbox.drive.list()
        assert isinstance(mounts, list)

        found = next((m for m in mounts if m["driveName"] == drive_name), None)
        assert found is not None
        assert found["mountPath"] == "/mnt/data"
        assert found["drivePath"] == "/"

    async def test_writes_and_reads_from_mounted_drive(self):
        """Test writing and reading from a mounted drive."""
        drive_name = unique_name("rw-drive")
        sandbox_name = unique_name("rw-sandbox")

        await DriveInstance.create(
            {
                "name": drive_name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(drive_name)

        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox_name)

        # Attach drive
        await sandbox.drive.attach(
            drive_name=drive_name,
            mount_path="/mnt/storage",
        )

        # Write to the drive
        await sandbox.process.exec(
            {
                "command": "echo 'Hello from Drive' > /mnt/storage/test.txt",
                "wait_for_completion": True,
            }
        )

        # Read from the drive
        result = await sandbox.process.exec(
            {
                "command": "cat /mnt/storage/test.txt",
                "wait_for_completion": True,
            }
        )

        assert "Hello from Drive" in result.logs

    async def test_detaches_a_drive_from_sandbox(self):
        """Test detaching a drive from a sandbox."""
        drive_name = unique_name("detach-drive")
        sandbox_name = unique_name("detach-sandbox")

        await DriveInstance.create(
            {
                "name": drive_name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(drive_name)

        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox_name)

        # Attach drive
        await sandbox.drive.attach(
            drive_name=drive_name,
            mount_path="/mnt/temp",
        )

        # Verify it's mounted
        mounts_before = await sandbox.drive.list()
        found_before = next((m for m in mounts_before if m["driveName"] == drive_name), None)
        assert found_before is not None

        # Detach drive
        detach_result = await sandbox.drive.detach("/mnt/temp")
        assert detach_result["success"] is True
        assert detach_result["mountPath"] == "/mnt/temp"

        # Verify it's unmounted
        mounts_after = await sandbox.drive.list()
        found_after = next((m for m in mounts_after if m["driveName"] == drive_name), None)
        assert found_after is None

    async def test_mounts_drive_subdirectory(self):
        """Test mounting a subdirectory of a drive."""
        drive_name = unique_name("subdir-drive")
        sandbox_name = unique_name("subdir-sandbox")

        await DriveInstance.create(
            {
                "name": drive_name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(drive_name)

        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox_name)

        # First, mount the root and create a subdirectory
        await sandbox.drive.attach(
            drive_name=drive_name,
            mount_path="/mnt/root",
        )

        await sandbox.process.exec(
            {
                "command": "mkdir -p /mnt/root/subdir && echo 'data in subdir' > /mnt/root/subdir/file.txt",
                "wait_for_completion": True,
            }
        )

        await sandbox.drive.detach("/mnt/root")

        # Now mount only the subdirectory
        mount_result = await sandbox.drive.attach(
            drive_name=drive_name,
            mount_path="/mnt/sub",
            drive_path="/subdir",
        )

        assert mount_result["drivePath"] == "/subdir"

        # Verify we can access the file from the subdirectory mount
        result = await sandbox.process.exec(
            {
                "command": "cat /mnt/sub/file.txt",
                "wait_for_completion": True,
            }
        )

        assert "data in subdir" in result.logs


@pytest.mark.asyncio(loop_scope="class")
class TestDrivePersistence(TestDriveOperations):
    """Test drive persistence across sandboxes."""

    async def test_data_persists_when_drive_is_attached_to_different_sandboxes(self):
        """Test that data persists when a drive is attached to different sandboxes."""
        drive_name = unique_name("persist-drive")
        file_content = f"persistent data {time.time()}"

        await DriveInstance.create(
            {
                "name": drive_name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(drive_name)

        # First sandbox - write data
        sandbox1_name = unique_name("persist-1")
        sandbox1 = await SandboxInstance.create(
            {
                "name": sandbox1_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox1_name)

        await sandbox1.drive.attach(
            drive_name=drive_name,
            mount_path="/data",
        )

        await sandbox1.process.exec(
            {
                "command": f"echo '{file_content}' > /data/persistent.txt",
                "wait_for_completion": True,
            }
        )

        await sandbox1.drive.detach("/data")

        # Delete first sandbox
        await SandboxInstance.delete(sandbox1_name)
        await wait_for_sandbox_deletion(sandbox1_name)

        # Second sandbox - read data
        sandbox2_name = unique_name("persist-2")
        sandbox2 = await SandboxInstance.create(
            {
                "name": sandbox2_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox2_name)

        await sandbox2.drive.attach(
            drive_name=drive_name,
            mount_path="/data",
        )

        result = await sandbox2.process.exec(
            {
                "command": "cat /data/persistent.txt",
                "wait_for_completion": True,
            }
        )

        assert file_content in result.logs.strip()


@pytest.mark.asyncio(loop_scope="class")
class TestMultipleDrives(TestDriveOperations):
    """Test multiple drives mounted to a sandbox."""

    async def test_mounts_multiple_drives_to_a_sandbox(self):
        """Test mounting multiple drives to a single sandbox."""
        drive1_name = unique_name("multi-drive1")
        drive2_name = unique_name("multi-drive2")
        sandbox_name = unique_name("multi-sandbox")

        await DriveInstance.create(
            {
                "name": drive1_name,
                "size": 5,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(drive1_name)

        await DriveInstance.create(
            {
                "name": drive2_name,
                "size": 5,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(drive2_name)

        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox_name)

        # Attach both drives
        await sandbox.drive.attach(
            drive_name=drive1_name,
            mount_path="/mnt/drive1",
        )

        await sandbox.drive.attach(
            drive_name=drive2_name,
            mount_path="/mnt/drive2",
        )

        # Verify both are mounted
        mounts = await sandbox.drive.list()
        assert len(mounts) >= 2

        found1 = next((m for m in mounts if m["driveName"] == drive1_name), None)
        found2 = next((m for m in mounts if m["driveName"] == drive2_name), None)
        assert found1 is not None
        assert found2 is not None

        # Write to both drives
        await sandbox.process.exec(
            {
                "command": "echo 'drive1 data' > /mnt/drive1/file.txt && echo 'drive2 data' > /mnt/drive2/file.txt",
                "wait_for_completion": True,
            }
        )

        # Read from both
        result1 = await sandbox.process.exec(
            {
                "command": "cat /mnt/drive1/file.txt",
                "wait_for_completion": True,
            }
        )
        assert "drive1 data" in result1.logs

        result2 = await sandbox.process.exec(
            {
                "command": "cat /mnt/drive2/file.txt",
                "wait_for_completion": True,
            }
        )
        assert "drive2 data" in result2.logs


@pytest.mark.asyncio(loop_scope="class")
class TestDriveMountPathHandling(TestDriveOperations):
    """Test drive mount path handling."""

    async def test_handles_mount_path_without_leading_slash(self):
        """Test that mount paths without leading slash are handled correctly."""
        drive_name = unique_name("path-drive")
        sandbox_name = unique_name("path-sandbox")

        await DriveInstance.create(
            {
                "name": drive_name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(drive_name)

        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox_name)

        # Attach with path that will be normalized
        result = await sandbox.drive.attach(
            drive_name=drive_name,
            mount_path="/mnt/test",
        )

        assert result["success"] is True

        # Detach should also work without leading slash
        await sandbox.drive.detach("mnt/test")

        mounts = await sandbox.drive.list()
        found = next((m for m in mounts if m["driveName"] == drive_name), None)
        assert found is None


@pytest.mark.asyncio(loop_scope="class")
class TestDriveFileOperations(TestDriveOperations):
    """Test file operations on mounted drives."""

    async def test_creates_directory_structure_in_drive(self):
        """Test creating a directory structure in a drive."""
        drive_name = unique_name("fs-drive")
        sandbox_name = unique_name("fs-sandbox")

        await DriveInstance.create(
            {
                "name": drive_name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(drive_name)

        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox_name)

        await sandbox.drive.attach(
            drive_name=drive_name,
            mount_path="/mnt/files",
        )

        # Create directory structure
        await sandbox.process.exec(
            {
                "command": "mkdir -p /mnt/files/project/{src,tests,docs} && echo 'code' > /mnt/files/project/src/main.js",
                "wait_for_completion": True,
            }
        )

        # Verify structure
        result = await sandbox.process.exec(
            {
                "command": "ls -la /mnt/files/project/",
                "wait_for_completion": True,
            }
        )

        assert "src" in result.logs
        assert "tests" in result.logs
        assert "docs" in result.logs

        # Verify file content
        cat_result = await sandbox.process.exec(
            {
                "command": "cat /mnt/files/project/src/main.js",
                "wait_for_completion": True,
            }
        )
        assert "code" in cat_result.logs

    async def test_uses_filesystem_api_with_mounted_drive(self):
        """Test using filesystem API with a mounted drive."""
        drive_name = unique_name("fsapi-drive")
        sandbox_name = unique_name("fsapi-sandbox")

        await DriveInstance.create(
            {
                "name": drive_name,
                "size": 10,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_drives.append(drive_name)

        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox_name)

        await sandbox.drive.attach(
            drive_name=drive_name,
            mount_path="/mnt/fs",
        )

        # Use filesystem API to write
        await sandbox.fs.write("/mnt/fs/api-test.txt", "Written via FS API")

        # Read back
        content = await sandbox.fs.read("/mnt/fs/api-test.txt")
        assert content == "Written via FS API"

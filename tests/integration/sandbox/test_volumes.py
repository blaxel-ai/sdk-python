import asyncio
import time

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.volume import VolumeInstance
from tests.helpers import (
    default_image,
    default_labels,
    default_region,
    unique_name,
    wait_for_sandbox_deletion,
    wait_for_volume_deletion,
)


class TestVolumeOperations:
    """Base class for volume tests with cleanup tracking."""

    created_sandboxes: list[str] = []
    created_volumes: list[str] = []

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def cleanup(self, request):
        """Clean up all resources after each test class."""
        # Reset lists for this class
        request.cls.created_sandboxes = []
        request.cls.created_volumes = []

        yield

        # Clean up sandboxes first (they depend on volumes)
        await asyncio.gather(
            *[self._safe_delete_sandbox(name) for name in request.cls.created_sandboxes],
            return_exceptions=True,
        )

        # Then clean up volumes
        await asyncio.gather(
            *[self._safe_delete_volume(name) for name in request.cls.created_volumes],
            return_exceptions=True,
        )

    async def _safe_delete_sandbox(self, name: str) -> None:
        """Safely delete a sandbox, ignoring errors."""
        try:
            await SandboxInstance.delete(name)
            await wait_for_sandbox_deletion(name)
        except Exception:
            pass

    async def _safe_delete_volume(self, name: str) -> None:
        """Safely delete a volume, ignoring errors."""
        try:
            await VolumeInstance.delete(name)
        except Exception:
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestVolumeInstanceCRUD(TestVolumeOperations):
    """Test VolumeInstance CRUD operations."""

    async def test_creates_a_volume(self):
        """Test creating a volume."""
        name = unique_name("volume")
        volume = await VolumeInstance.create(
            {
                "name": name,
                "size": 1024,  # 1GB
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_volumes.append(name)

        assert volume.name == name

    async def test_creates_a_volume_with_display_name(self):
        """Test creating a volume with display name."""
        name = unique_name("volume-display")
        volume = await VolumeInstance.create(
            {
                "name": name,
                "display_name": "My Test Volume",
                "size": 1024,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_volumes.append(name)

        assert volume.name == name

    async def test_gets_a_volume(self):
        """Test getting a volume."""
        name = unique_name("volume-get")
        await VolumeInstance.create(
            {
                "name": name,
                "size": 1024,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_volumes.append(name)

        volume = await VolumeInstance.get(name)
        assert volume.name == name

    async def test_lists_volumes(self):
        """Test listing volumes."""
        name = unique_name("volume-list")
        await VolumeInstance.create(
            {
                "name": name,
                "size": 1024,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_volumes.append(name)

        volumes = await VolumeInstance.list()
        assert isinstance(volumes, list)

        found = next((v for v in volumes if v.name == name), None)
        assert found is not None

    async def test_deletes_a_volume(self):
        """Test deleting a volume."""
        name = unique_name("volume-delete")
        volume = await VolumeInstance.create(
            {
                "name": name,
                "size": 1024,
                "region": default_region,
                "labels": default_labels,
            }
        )
        await volume.delete()
        await wait_for_volume_deletion(name)

        # Volume should no longer exist
        with pytest.raises(Exception):
            await VolumeInstance.get(name)


@pytest.mark.asyncio(loop_scope="class")
class TestMountingVolumesToSandboxes(TestVolumeOperations):
    """Test mounting volumes to sandboxes."""

    async def test_mounts_a_volume_to_a_sandbox(self):
        """Test mounting a volume to a sandbox."""
        volume_name = unique_name("mount-vol")
        sandbox_name = unique_name("mount-sandbox")

        await VolumeInstance.create(
            {
                "name": volume_name,
                "size": 1024,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_volumes.append(volume_name)

        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "volumes": [
                    {
                        "name": volume_name,
                        "mount_path": "/data",
                        "read_only": False,
                    },
                ],
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox_name)

        # Verify mount by writing a file
        await sandbox.process.exec(
            {
                "command": "echo 'mounted' > /data/test.txt",
                "wait_for_completion": True,
            }
        )

        result = await sandbox.process.exec(
            {
                "command": "cat /data/test.txt",
                "wait_for_completion": True,
            }
        )

        assert "mounted" in result.logs


@pytest.mark.asyncio(loop_scope="class")
class TestVolumeResize(TestVolumeOperations):
    """Test volume resize operations."""

    async def test_resizes_volume_and_preserves_data(self):
        """Test resizing a volume and verifying data is preserved."""
        volume_name = unique_name("resize-vol")
        sandbox1_name = unique_name("resize-sandbox-1")
        sandbox2_name = unique_name("resize-sandbox-2")

        # Create a 512MB volume
        await VolumeInstance.create(
            {
                "name": volume_name,
                "size": 512,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_volumes.append(volume_name)

        # Create first sandbox with volume attached
        sandbox1 = await SandboxInstance.create(
            {
                "name": sandbox1_name,
                "image": default_image,
                "memory": 4096,
                "region": default_region,
                "volumes": [
                    {"name": volume_name, "mount_path": "/data", "read_only": False}
                ],
                "labels": default_labels,
            }
        )

        # Write ~400MB of data to the volume
        await sandbox1.process.exec(
            {
                "command": "dd if=/dev/urandom of=/data/large-file-1.bin bs=1M count=400",
                "wait_for_completion": True,
            }
        )

        # Verify file was created
        check_result1 = await sandbox1.process.exec(
            {
                "command": "ls -lh /data/large-file-1.bin",
                "wait_for_completion": True,
            }
        )
        assert "large-file-1.bin" in check_result1.logs

        # Delete first sandbox
        await SandboxInstance.delete(sandbox1_name)
        await wait_for_sandbox_deletion(sandbox1_name)

        # Resize volume to 1GB
        updated_volume = await VolumeInstance.update(volume_name, {"size": 1024})
        assert updated_volume.size == 1024

        # Create second sandbox with the resized volume
        sandbox2 = await SandboxInstance.create(
            {
                "name": sandbox2_name,
                "image": default_image,
                "memory": 4096,
                "region": default_region,
                "volumes": [
                    {"name": volume_name, "mount_path": "/data", "read_only": False}
                ],
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox2_name)

        # Verify previous data still exists
        check_result2 = await sandbox2.process.exec(
            {
                "command": "ls -lh /data/large-file-1.bin",
                "wait_for_completion": True,
            }
        )
        assert "large-file-1.bin" in check_result2.logs

        # Write another ~400MB file (would fail if volume wasn't resized)
        write_result = await sandbox2.process.exec(
            {
                "command": "dd if=/dev/urandom of=/data/large-file-2.bin bs=1M count=400 && echo 'WRITE_SUCCESS'",
                "wait_for_completion": True,
            }
        )
        assert "WRITE_SUCCESS" in write_result.logs

        # Verify both files exist
        final_check = await sandbox2.process.exec(
            {
                "command": "ls -lh /data/",
                "wait_for_completion": True,
            }
        )
        assert "large-file-1.bin" in final_check.logs
        assert "large-file-2.bin" in final_check.logs

    async def test_fails_when_writing_more_data_than_volume_capacity(self):
        """Test that writing more data than volume capacity fails."""
        volume_name = unique_name("overflow-vol")
        sandbox_name = unique_name("overflow-sandbox")

        # Create a small 512MB volume
        await VolumeInstance.create(
            {
                "name": volume_name,
                "size": 512,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_volumes.append(volume_name)

        # Create sandbox with volume attached
        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "image": default_image,
                "memory": 4096,
                "region": default_region,
                "volumes": [
                    {"name": volume_name, "mount_path": "/data", "read_only": False}
                ],
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox_name)

        # Try to write more data than the volume can hold (600MB > 512MB)
        # dd will fail when disk is full, so we check for failure
        write_result = await sandbox.process.exec(
            {
                "command": "(dd if=/dev/urandom of=/data/too-large.bin bs=1M count=600 2>&1 && echo 'WRITE_SUCCESS') || echo 'WRITE_FAILED'",
                "wait_for_completion": True,
            }
        )

        # The write should fail due to insufficient space
        assert "WRITE_FAILED" in write_result.logs or "No space left on device" in write_result.logs


@pytest.mark.asyncio(loop_scope="class")
class TestVolumePersistence(TestVolumeOperations):
    """Test volume persistence across sandbox recreations."""

    async def test_data_persists_across_sandbox_recreations(self):
        """Test that data persists across sandbox recreations."""
        volume_name = unique_name("persist-vol")
        file_content = f"persistent data {int(time.time() * 1000)}"

        await VolumeInstance.create(
            {
                "name": volume_name,
                "size": 1024,
                "region": default_region,
                "labels": default_labels,
            }
        )
        self.created_volumes.append(volume_name)

        # First sandbox - write data
        sandbox1_name = unique_name("persist-1")
        sandbox1 = await SandboxInstance.create(
            {
                "name": sandbox1_name,
                "image": default_image,
                "region": default_region,
                "volumes": [{"name": volume_name, "mount_path": "/persistent", "read_only": False}],
                "labels": default_labels,
            }
        )

        await sandbox1.process.exec(
            {
                "command": f"echo '{file_content}' > /persistent/data.txt",
                "wait_for_completion": True,
            }
        )

        # Delete first sandbox and wait for full deletion
        await SandboxInstance.delete(sandbox1_name)
        await wait_for_sandbox_deletion(sandbox1_name)

        # Second sandbox - read data
        sandbox2_name = unique_name("persist-2")
        sandbox2 = await SandboxInstance.create(
            {
                "name": sandbox2_name,
                "image": default_image,
                "region": default_region,
                "volumes": [{"name": volume_name, "mount_path": "/data", "read_only": False}],
                "labels": default_labels,
            }
        )
        self.created_sandboxes.append(sandbox2_name)

        result = await sandbox2.process.exec(
            {
                "command": "cat /data/data.txt",
                "wait_for_completion": True,
            }
        )

        assert result.logs.strip() == file_content

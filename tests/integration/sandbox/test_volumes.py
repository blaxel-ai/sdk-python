import asyncio
import time

import pytest

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


@pytest.mark.asyncio(loop_scope="class")
class TestVolumeOperations:
    """Test volume operations."""

    created_sandboxes: list[str] = []
    created_volumes: list[str] = []

    @pytest.fixture(autouse=True)
    async def cleanup(self):
        """Clean up all sandboxes and volumes after each test class."""
        yield
        # Clean up sandboxes first and wait for full deletion
        await asyncio.gather(
            *[
                self._safe_delete_sandbox_and_wait(name)
                for name in TestVolumeOperations.created_sandboxes
            ],
            return_exceptions=True,
        )
        TestVolumeOperations.created_sandboxes.clear()

        # Clean up volumes (now safe since sandboxes are fully deleted)
        await asyncio.gather(
            *[self._safe_delete_volume(name) for name in TestVolumeOperations.created_volumes],
            return_exceptions=True,
        )
        TestVolumeOperations.created_volumes.clear()

    async def _safe_delete_sandbox_and_wait(self, name: str) -> None:
        """Safely delete a sandbox and wait for deletion, ignoring errors."""
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
        TestVolumeOperations.created_volumes.append(name)

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
        TestVolumeOperations.created_volumes.append(name)

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
        TestVolumeOperations.created_volumes.append(name)

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
        TestVolumeOperations.created_volumes.append(name)

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
        TestVolumeOperations.created_volumes.append(volume_name)

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
        TestVolumeOperations.created_sandboxes.append(sandbox_name)

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
        TestVolumeOperations.created_volumes.append(volume_name)

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
        TestVolumeOperations.created_sandboxes.append(sandbox2_name)

        result = await sandbox2.process.exec(
            {
                "command": "cat /data/data.txt",
                "wait_for_completion": True,
            }
        )

        assert result.logs.strip() == file_content

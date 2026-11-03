from typing import List

from ...common.settings import settings
from ..client.api.drive.delete_drives_mount_mount_path import (
    asyncio as delete_drives_mount,
)
from ..client.api.drive.get_drives_mount import asyncio as get_drives_mount
from ..client.api.drive.post_drives_mount import asyncio as post_drives_mount
from ..client.client import Client
from ..client.models import (
    DriveMountInfo,
    DriveMountRequest,
    DriveMountResponse,
    DriveUnmountResponse,
    ErrorResponse,
)
from ..transient_retry import retry_on_transient_reset_async
from ..types import SandboxConfiguration
from .action import SandboxAction


class SandboxDrive(SandboxAction):
    """Asynchronous drive operations for mounting/unmounting drives to sandbox.

    Reached as ``sandbox.drives``. The drive itself is a separate resource:
    create it first with ``DriveInstance.create``. Mounting, unmounting and
    listing go to the sandbox, and a failure raises a plain ``Exception``
    whose message carries the sandbox API's error.

    Example:
        ```python
        await sandbox.drives.mount("shared-data", "/mnt/data")
        print(await sandbox.drives.list())
        await sandbox.drives.unmount("/mnt/data")
        ```
    """

    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    async def mount(
        self,
        drive_name: str,
        mount_path: str,
        drive_path: str = "/",
        read_only: bool = False,
    ) -> DriveMountResponse:
        """
        Mount a drive to the sandbox at the specified mount path.

        Args:
            drive_name: Name of the drive to mount
            mount_path: Path in the sandbox where the drive should be mounted
            drive_path: Path within the drive to mount (default: "/")
            read_only: If True, mount the drive as read-only (default: False)

        Returns:
            DriveMountResponse with success status and mount information

        Raises:
            Exception: "Mount drive failed: <error>" when the sandbox API
                rejects the mount.
        """
        if not mount_path.startswith("/"):
            mount_path = f"/{mount_path}"

        body = DriveMountRequest(
            drive_name=drive_name,
            mount_path=mount_path,
            drive_path=drive_path,
            read_only=read_only,
        )

        client = Client(
            base_url=self.url,
            headers={**settings.headers, **self.sandbox_config.headers},
        )

        async with client:
            response = await post_drives_mount(client=client, body=body)
            if response is None:
                raise Exception("Failed to mount drive")
            if isinstance(response, ErrorResponse):
                raise Exception(f"Mount drive failed: {response.error}")
            return response

    async def unmount(self, mount_path: str) -> DriveUnmountResponse:
        """
        Unmount a drive from the sandbox.

        Args:
            mount_path: Path where the drive is currently mounted

        Returns:
            DriveUnmountResponse with success status

        Raises:
            Exception: "Unmount drive failed: <error>" when the sandbox API
                rejects the request.
        """
        # Strip leading slash for the path parameter since the URL template
        # already includes the slash: /drives/mount/{mountPath}
        param_path = mount_path[1:] if mount_path.startswith("/") else mount_path

        client = Client(
            base_url=self.url,
            headers={**settings.headers, **self.sandbox_config.headers},
        )

        async with client:
            response = await delete_drives_mount(param_path, client=client)
            if response is None:
                raise Exception("Failed to unmount drive")
            if isinstance(response, ErrorResponse):
                raise Exception(f"Unmount drive failed: {response.error}")
            return response

    async def list(self) -> List[DriveMountInfo]:
        """
        List all currently mounted drives in the sandbox.

        Returns:
            List of DriveMountInfo for each mounted drive, empty when none is
            mounted.

        Raises:
            Exception: "List drives failed: <error>" when the sandbox API
                rejects the request.
        """

        async def list_once() -> List[DriveMountInfo]:
            client = Client(
                base_url=self.url,
                headers={**settings.headers, **self.sandbox_config.headers},
            )

            async with client:
                response = await get_drives_mount(client=client)
                if response is None:
                    raise Exception("Failed to list drives")
                if isinstance(response, ErrorResponse):
                    raise Exception(f"List drives failed: {response.error}")
                return list(response.mounts) if response.mounts else []

        return await retry_on_transient_reset_async(list_once)

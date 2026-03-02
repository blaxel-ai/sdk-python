from typing import Any, Dict, List

from ..types import SandboxConfiguration
from .action import SyncSandboxAction


class SyncSandboxDrive(SyncSandboxAction):
    """Synchronous drive operations for mounting/unmounting drives to sandbox."""

    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    def mount(
        self,
        drive_name: str,
        mount_path: str,
        drive_path: str = "/",
    ) -> Dict[str, Any]:
        """
        Mount a drive to the sandbox at the specified mount path.

        Args:
            drive_name: Name of the drive to mount
            mount_path: Path in the sandbox where the drive should be mounted
            drive_path: Path within the drive to mount (default: "/")

        Returns:
            Dictionary with success status and mount information
        """
        if not mount_path.startswith("/"):
            mount_path = f"/{mount_path}"

        payload = {
            "driveName": drive_name,
            "mountPath": mount_path,
            "drivePath": drive_path,
        }

        client = self.get_client()
        response = client.post("/drives/mount", json=payload)
        self.handle_response_error(response)
        return response.json()

    def unmount(self, mount_path: str) -> Dict[str, Any]:
        """
        Unmount a drive from the sandbox.

        Args:
            mount_path: Path where the drive is currently mounted

        Returns:
            Dictionary with success status
        """
        if not mount_path.startswith("/"):
            mount_path = f"/{mount_path}"

        url_path = mount_path[1:]

        client = self.get_client()
        response = client.delete(f"/drives/mount/{url_path}")
        self.handle_response_error(response)
        return response.json()

    def list(self) -> List[Dict[str, Any]]:
        """
        List all currently mounted drives in the sandbox.

        Returns:
            List of dictionaries containing mount information for each drive
        """
        client = self.get_client()
        response = client.get("/drives/mount")
        self.handle_response_error(response)

        result = response.json()
        if isinstance(result, dict) and "mounts" in result:
            return result["mounts"]
        return []

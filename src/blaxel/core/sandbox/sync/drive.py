from typing import Any, Dict, List

import httpx

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
        # Normalize mount_path to ensure it starts with /
        if not mount_path.startswith("/"):
            mount_path = f"/{mount_path}"

        url = f"{self.url}/drives/mount"
        headers = self.sandbox_config.headers

        payload = {
            "driveName": drive_name,
            "mountPath": mount_path,
            "drivePath": drive_path,
        }

        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=headers)
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
        # Normalize mount_path to ensure it starts with /
        if not mount_path.startswith("/"):
            mount_path = f"/{mount_path}"

        # URL encode the mount path for use in URL
        encoded_path = mount_path.replace("/", "%2F")
        url = f"{self.url}/drives/{encoded_path}"
        headers = self.sandbox_config.headers

        with httpx.Client() as client:
            response = client.delete(url, headers=headers)
            self.handle_response_error(response)

            return response.json()

    def list(self) -> List[Dict[str, Any]]:
        """
        List all currently mounted drives in the sandbox.

        Returns:
            List of dictionaries containing mount information for each drive
        """
        url = f"{self.url}/drives/mount"
        headers = self.sandbox_config.headers

        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            self.handle_response_error(response)

            result = response.json()
            # The API returns {"mounts": [...]}
            if isinstance(result, dict) and "mounts" in result:
                return result["mounts"]
            return []

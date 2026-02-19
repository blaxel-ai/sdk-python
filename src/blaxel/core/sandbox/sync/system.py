from ...common.settings import settings
from ..client.api.system.get_health import sync as get_health
from ..client.api.system.post_upgrade import sync as post_upgrade
from ..client.client import Client
from ..client.models import ErrorResponse, HealthResponse, SuccessResponse, UpgradeRequest
from ..types import SandboxConfiguration
from .action import SyncSandboxAction


class SyncSandboxSystem(SyncSandboxAction):
    """System operations for sandbox including upgrade functionality (sync version)."""

    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    def upgrade(
        self,
        version: str | None = None,
        base_url: str | None = None,
    ) -> SuccessResponse:
        """Upgrade the sandbox-api to a new version.

        Triggers an upgrade of the sandbox-api process. Returns immediately before upgrading.
        The upgrade will: download the specified binary from GitHub releases, validate it, and restart.
        All running processes will be preserved across the upgrade.

        Args:
            version: Version to upgrade to - "develop" (default), "main", "latest",
                     or specific tag like "v1.0.0"
            base_url: Base URL for releases (useful for forks, defaults to
                      https://github.com/blaxel-ai/sandbox/releases)

        Returns:
            SuccessResponse with status information
        """
        request = UpgradeRequest(version=version, base_url=base_url)

        client = Client(
            base_url=self.url,
            headers={**settings.headers, **self.sandbox_config.headers},
        )

        with client:
            response = post_upgrade(client=client, body=request)
            if response is None:
                raise Exception("Failed to upgrade sandbox")
            if isinstance(response, ErrorResponse):
                raise Exception(f"Upgrade failed: {response.error}")
            return response

    def health(self) -> HealthResponse:
        """Get health status and system information.

        Returns health status and system information including upgrade count and binary details.
        Also includes last upgrade attempt status with detailed error information if available.

        Returns:
            HealthResponse with system status information
        """
        client = Client(
            base_url=self.url,
            headers={**settings.headers, **self.sandbox_config.headers},
        )

        with client:
            response = get_health(client=client)
            if response is None:
                raise Exception("Failed to get health status")
            return response

import httpx

from ..types import SandboxConfiguration
from .action import SyncSandboxAction


class SyncSandboxNetwork(SyncSandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    def fetch(
        self, port: int, path: str = "/", method: str = "GET", **kwargs
    ) -> httpx.Response:
        """Fetch a resource served on a sandbox port.

        The request is proxied through the sandbox's /port/{port} endpoint.

        Args:
            port: The port number inside the sandbox
            path: Optional path appended after the port (default: "/")
            method: HTTP method (default: "GET")
            **kwargs: Additional arguments forwarded to httpx (e.g. headers, content)
        """
        normalized_path = path if path.startswith("/") else f"/{path}"
        url = f"/port/{port}{normalized_path}"
        client = self.get_client()
        return client.request(method, url, **kwargs)

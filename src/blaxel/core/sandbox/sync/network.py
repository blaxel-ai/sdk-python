import httpx

from ..transient_retry import retry_on_transient_sandbox_read
from ..types import SandboxConfiguration
from .action import SyncSandboxAction

IDEMPOTENT_READ_METHODS = {"GET", "HEAD", "OPTIONS"}


class SyncSandboxNetwork(SyncSandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    def fetch(self, port: int, path: str = "/", method: str = "GET", **kwargs) -> httpx.Response:
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
        with self.get_client() as client:
            fetch_once = lambda: client.request(method, url, **kwargs)
            if method.upper() in IDEMPOTENT_READ_METHODS:
                return retry_on_transient_sandbox_read(fetch_once)
            return fetch_once()

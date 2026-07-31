import httpx

from ..transient_retry import retry_on_transient_sandbox_read_async
from ..types import SandboxConfiguration
from .action import SandboxAction

IDEMPOTENT_READ_METHODS = {"GET", "HEAD", "OPTIONS"}


class SandboxNetwork(SandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    async def fetch(
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
        fetch_once = lambda: client.request(method, url, **kwargs)
        if method.upper() in IDEMPOTENT_READ_METHODS:
            return await retry_on_transient_sandbox_read_async(fetch_once)
        return await fetch_once()

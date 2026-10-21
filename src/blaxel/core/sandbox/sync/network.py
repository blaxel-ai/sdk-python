import httpx

from ..types import SandboxConfiguration
from .action import SyncSandboxAction


class SyncSandboxNetwork(SyncSandboxAction):
    """Send HTTP requests to servers listening on sandbox ports.

    Reach it as ``sandbox.network``; ``sandbox.fetch`` is a shortcut for
    :meth:`fetch`. Requests go through the sandbox API with the caller's
    credentials, so no preview is needed.

    Example:
        ```python
        response = sandbox.network.fetch(8000, "/health")
        print(response.status_code, response.text)
        ```
    """

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

        Returns:
            The ``httpx.Response``. HTTP error statuses are returned, not
            raised.
        """
        normalized_path = path if path.startswith("/") else f"/{path}"
        url = f"/port/{port}{normalized_path}"
        with self.get_client() as client:
            return client.request(method, url, **kwargs)

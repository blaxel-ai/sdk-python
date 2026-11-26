"""Shared helpers for sandbox port-proxied HTTP requests."""

SANDBOX_API_PORT = 8080


def build_port_fetch_url(port: int, path: str = "/") -> str:
    """Build the ``/port/{port}{path}`` proxy URL for ``sandbox.fetch``.

    Raises:
        ValueError: If ``port`` is ``SANDBOX_API_PORT`` (8080), which is reserved
            by ``sandbox-api`` itself and would self-proxy.
    """
    if port == SANDBOX_API_PORT:
        raise ValueError(
            f"sandbox.fetch(port={SANDBOX_API_PORT}) is not supported because port "
            f"{SANDBOX_API_PORT} is reserved by sandbox-api and /port/{SANDBOX_API_PORT} "
            "would self-proxy. Use sandbox.process, sandbox.fs, sandbox.system, or "
            "get_client() for sandbox-api routes, and run user servers on another port "
            "(such as 3000 or 8000)."
        )
    normalized_path = path if path.startswith("/") else f"/{path}"
    return f"/port/{port}{normalized_path}"

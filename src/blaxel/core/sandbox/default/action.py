
import httpx
from contextlib import asynccontextmanager

from ...common.internal import get_forced_url, get_global_unique_hash
from ...common.settings import settings
from ..types import ResponseError, SandboxConfiguration


class SandboxAction:
    _clients: dict[str, httpx.AsyncClient] = {}
    _clients_opened: dict[str, bool] = {}
    
    def __init__(self, sandbox_config: SandboxConfiguration):
        self.sandbox_config = sandbox_config

    @property
    def name(self) -> str:
        return self.sandbox_config.metadata.name if self.sandbox_config.metadata else ""

    @property
    def external_url(self) -> str:
        # Check if metadata has a URL first (like TypeScript implementation: metadata?.url)
        if (
            self.sandbox_config.metadata
            and self.sandbox_config.metadata.url is not None
            and self.sandbox_config.metadata.url != ""
        ):
            return self.sandbox_config.metadata.url

        return f"{settings.run_url}/{settings.workspace}/sandboxes/{self.name}"

    @property
    def internal_url(self) -> str:
        hash_value = get_global_unique_hash(settings.workspace, "sandbox", self.name)
        return f"{settings.run_internal_protocol}://bl-{settings.env}-{hash_value}.{settings.run_internal_hostname}"

    @property
    def forced_url(self) -> str | None:
        if self.sandbox_config.force_url:
            return self.sandbox_config.force_url
        return get_forced_url("sandbox", self.name)

    @property
    def url(self) -> str:
        if self.forced_url:
            url = self.forced_url
            return url[:-1] if url.endswith("/") else url
        # Uncomment when mk3 is fully available
        # if settings.run_internal_hostname:
        #     return self.internal_url
        return self.external_url

    @property
    def fallback_url(self) -> str | None:
        if self.external_url != self.url:
            return self.external_url
        return None

    @asynccontextmanager
    async def get_client(self):
        # Use persistent client per base URL for connection reuse
        base_url = self.sandbox_config.force_url or self.url
        
        if base_url not in SandboxAction._clients:
            # Optimized limits for bulk requests
            limits = httpx.Limits(
                max_keepalive_connections=10,  # Keep more connections alive
                max_connections=20,             # Allow more total connections
                keepalive_expiry=60.0,          # Keep connections alive longer
            )
            
            # Optimized timeouts for bulk operations
            timeout = httpx.Timeout(
                connect=10.0,   # Connection timeout
                read=60.0,      # Read timeout
                write=10.0,     # Write timeout  
                pool=5.0,       # Pool timeout (time to get connection from pool)
            )
            
            client = httpx.AsyncClient(
                base_url=base_url,
                headers=self.sandbox_config.headers if self.sandbox_config.force_url else {**settings.headers, **self.sandbox_config.headers},
                limits=limits,
                timeout=timeout,
                http2=True,
            )
            # Open the client once
            await client.__aenter__()
            SandboxAction._clients[base_url] = client
            SandboxAction._clients_opened[base_url] = True
        
        # Yield the client without closing it
        yield SandboxAction._clients[base_url]

    def handle_response_error(self, response: httpx.Response):
        if not response.is_success:
            raise ResponseError(response)

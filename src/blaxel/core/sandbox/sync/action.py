import httpx

from ...common.internal import get_forced_url, get_global_unique_hash
from ...common.settings import settings

try:
    import h2 as _h2  # noqa: F401

    HTTP2_AVAILABLE = True
except ImportError:
    HTTP2_AVAILABLE = False
from ..types import ResponseError, SandboxConfiguration


class SyncSandboxAction:
    def __init__(self, sandbox_config: SandboxConfiguration):
        self.sandbox_config = sandbox_config

    @property
    def name(self) -> str:
        return self.sandbox_config.metadata.name if self.sandbox_config.metadata else ""

    @property
    def external_url(self) -> str:
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
        return self.external_url

    @property
    def fallback_url(self) -> str | None:
        if self.external_url != self.url:
            return self.external_url
        return None

    def get_client(self) -> httpx.Client:
        """Get an HTTP client for this sandbox instance.

        Headers are injected via an event hook so that token refreshes are
        picked up automatically without recreating the client.
        """
        transport = getattr(self.sandbox_config, "h3_transport", None)
        kwargs: dict = {}
        if transport is not None:
            kwargs["transport"] = transport
        elif HTTP2_AVAILABLE:
            kwargs["http2"] = True

        sandbox_config = self.sandbox_config

        def _inject_headers(request: httpx.Request) -> None:
            """Inject fresh headers before every request."""
            if sandbox_config.force_url:
                fresh = sandbox_config.headers
            else:
                fresh = {**settings.headers, **sandbox_config.headers}
            for key, value in fresh.items():
                request.headers[key] = value

        base_url = self.sandbox_config.force_url or self.url
        return httpx.Client(
            base_url=base_url,
            event_hooks={"request": [_inject_headers]},
            **kwargs,
        )

    def handle_response_error(self, response: httpx.Response):
        if not response.is_success:
            raise ResponseError(response)

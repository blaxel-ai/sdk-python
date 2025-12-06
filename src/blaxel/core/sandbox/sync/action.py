import httpx

from ...common.internal import get_forced_url, get_global_unique_hash
from ...common.settings import settings
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
        if self.sandbox_config.force_url:
            return httpx.Client(
                base_url=self.sandbox_config.force_url,
                headers=self.sandbox_config.headers,
            )
        return httpx.Client(
            base_url=self.url,
            headers={**settings.headers, **self.sandbox_config.headers},
        )

    def handle_response_error(self, response: httpx.Response):
        if not response.is_success:
            raise ResponseError(response)

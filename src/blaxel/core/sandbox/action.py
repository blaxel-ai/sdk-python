from typing import Optional

import httpx

from ..common.internal import get_forced_url, get_global_unique_hash
from ..common.settings import settings
from .types import SandboxConfiguration


class ResponseError(Exception):
    def __init__(self, response: httpx.Response):
        data_error = {}
        data = None
        if response.content:
            try:
                data = response.json()
                data_error = data
            except Exception:
                data = response.text
                data_error["response"] = data
        if response.status_code:
            data_error["status"] = response.status_code
        if response.reason_phrase:
            data_error["statusText"] = response.reason_phrase

        super().__init__(str(data_error))
        self.response = response
        self.data = data
        self.error = None


class SandboxAction:
    def __init__(self, sandbox_config: SandboxConfiguration):
        self.sandbox_config = sandbox_config

    @property
    def name(self) -> str:
        return self.sandbox_config.metadata.name if self.sandbox_config.metadata else ""

    @property
    def external_url(self) -> str:
        return f"{settings.run_url}/{settings.workspace}/sandboxes/{self.name}"

    @property
    def internal_url(self) -> str:
        hash_value = get_global_unique_hash(settings.workspace, "sandbox", self.name)
        return f"{settings.run_internal_protocol}://bl-{settings.env}-{hash_value}.{settings.run_internal_hostname}"

    @property
    def forced_url(self) -> Optional[str]:
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
    def fallback_url(self) -> Optional[str]:
        if self.external_url != self.url:
            return self.external_url
        return None

    def get_client(self) -> httpx.AsyncClient:
        if self.sandbox_config.force_url:
            return httpx.AsyncClient(
                base_url=self.sandbox_config.force_url, headers=self.sandbox_config.headers
            )
        # Create a new client instance each time to avoid "Cannot open a client instance more than once" error
        return httpx.AsyncClient(
            base_url=self.url,
            headers={**settings.headers, **self.sandbox_config.headers},
        )

    def handle_response_error(self, response: httpx.Response):
        if not response.is_success:
            raise ResponseError(response)

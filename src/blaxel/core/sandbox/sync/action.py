import logging
import time
from collections.abc import Callable

import httpx

from ...common.internal import get_forced_url, get_global_unique_hash
from ...common.settings import settings
from ..types import ResponseError, SandboxConfiguration

logger = logging.getLogger(__name__)

# Retry parameters for WORKLOAD_UNAVAILABLE (sandbox cold start)
_INITIAL_BACKOFF = 0.5  # 500ms
_MAX_BACKOFF = 30.0  # 30s
_TOTAL_BUDGET = 60.0  # ~60s total retry budget


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

    def _request_with_retry(self, request_fn: Callable[[], httpx.Response]) -> httpx.Response:
        """Execute an HTTP request with retry on retryable errors (e.g. WORKLOAD_UNAVAILABLE).

        Retries with exponential backoff: 500ms → 30s, gives up after ~60s total.
        """
        elapsed = 0.0
        backoff = _INITIAL_BACKOFF

        while True:
            response = request_fn()
            response.read()  # Ensure body is loaded for inspection

            if response.is_success:
                return response

            if elapsed >= _TOTAL_BUDGET:
                return response

            # Check if the error response indicates retryability
            try:
                data = response.json()
                error = data.get("error", {})
                if isinstance(error, dict) and error.get("retryable", False):
                    logger.info(
                        "Sandbox not ready (%s), retrying in %.1fs...",
                        error.get("code", "UNKNOWN"),
                        backoff,
                    )
                    time.sleep(backoff)
                    elapsed += backoff
                    backoff = min(backoff * 2, _MAX_BACKOFF)
                    continue
            except Exception:
                pass

            return response  # Not retryable, return as-is for caller to handle

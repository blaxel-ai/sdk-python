import os

from httpx import Response

from ..client.models import Sandbox
from ..common.internal import get_global_unique_hash
from ..common.settings import settings
from .client.client import client
from .client.models import ErrorResponse


class ResponseError(Exception):
    def __init__(self, response: Response):
        self.status_code = response.status_code
        self.status_text = response.content
        self.error = None
        data_error = {
            "status": response.status_code,
            "statusText": response.content,
        }
        if hasattr(response, "parsed") and isinstance(response.parsed, ErrorResponse):
            data_error["error"] = response.parsed.error
            self.error = response.parsed.error
        super().__init__(str(data_error))


class SandboxHandleBase:
    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox
        self.client = client.with_base_url(self.url).with_headers(settings.headers)

    @property
    def name(self):
        return self.sandbox.metadata and self.sandbox.metadata.name

    @property
    def fallback_url(self):
        if self.external_url != self.url:
            return self.external_url
        return None

    @property
    def external_url(self):
        return f"{settings.run_url}/{settings.workspace}/sandboxes/{self.name}"

    @property
    def internal_url(self):
        hash_ = get_global_unique_hash(settings.workspace, "sandbox", self.name)
        return f"{settings.run_internal_protocol}://bl-{settings.env}-{hash_}.{settings.run_internal_hostname}"

    @property
    def forced_url(self):
        env_var = self.name.replace("-", "_").upper()
        env_name = f"BL_SANDBOX_{env_var}_URL"
        return os.environ.get(env_name)

    @property
    def url(self):
        if self.forced_url:
            return self.forced_url
        if settings.run_internal_hostname:
            return self.internal_url
        return self.external_url

    def handle_response(self, response: Response):
        if response.status_code >= 400:
            raise ResponseError(response)


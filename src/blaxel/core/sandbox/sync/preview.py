from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Union

from ...client import errors
from ...client.api.compute.create_sandbox_preview import sync as create_sandbox_preview
from ...client.api.compute.create_sandbox_preview_token import sync as create_sandbox_preview_token
from ...client.api.compute.delete_sandbox_preview import sync as delete_sandbox_preview
from ...client.api.compute.delete_sandbox_preview_token import sync as delete_sandbox_preview_token
from ...client.api.compute.get_sandbox_preview import sync as get_sandbox_preview
from ...client.api.compute.list_sandbox_preview_tokens import sync as list_sandbox_preview_tokens
from ...client.api.compute.list_sandbox_previews import sync as list_sandbox_previews
from ...client.client import client
from ...client.models import (
    Preview,
    PreviewSpec,
    PreviewToken,
    PreviewTokenSpec,
    Sandbox,
)


@dataclass
class SyncSandboxPreviewToken:
    preview_token: PreviewToken

    @property
    def value(self) -> str:
        return self.preview_token.spec.token if self.preview_token.spec else ""

    @property
    def expires_at(self) -> datetime:
        return self.preview_token.spec.expires_at if self.preview_token.spec else datetime.now()


class SyncSandboxPreviewTokens:
    def __init__(self, preview: Preview):
        self.preview = preview

    @property
    def preview_name(self) -> str:
        return self.preview.metadata.name if self.preview.metadata else ""

    @property
    def resource_name(self) -> str:
        return self.preview.metadata.resource_name if self.preview.metadata else ""

    def create(self, expires_at: datetime) -> SyncSandboxPreviewToken:
        response: PreviewToken = create_sandbox_preview_token(
            self.resource_name,
            self.preview_name,
            body=PreviewToken(
                spec=PreviewTokenSpec(
                    expires_at=to_utc_z(expires_at),
                )
            ),
            client=client,
        )
        return SyncSandboxPreviewToken(response)

    def list(self) -> List[SyncSandboxPreviewToken]:
        response: List[PreviewToken] = list_sandbox_preview_tokens(
            self.resource_name,
            self.preview_name,
            client=client,
        )
        return [SyncSandboxPreviewToken(token) for token in response]

    def delete(self, token_name: str) -> dict:
        response: PreviewToken = delete_sandbox_preview_token(
            self.resource_name,
            self.preview_name,
            token_name,
            client=client,
        )
        return response


class SyncSandboxPreview:
    def __init__(self, preview: Preview):
        self.preview = preview
        self.tokens = SyncSandboxPreviewTokens(preview)

    @property
    def name(self) -> str:
        return self.preview.metadata.name if self.preview.metadata else ""

    @property
    def metadata(self) -> dict | None:
        return self.preview.metadata

    @property
    def spec(self) -> PreviewSpec | None:
        return self.preview.spec


class SyncSandboxPreviews:
    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    @property
    def sandbox_name(self) -> str:
        return self.sandbox.metadata.name if self.sandbox.metadata else ""

    def list(self) -> List[SyncSandboxPreview]:
        response: List[Preview] = list_sandbox_previews(
            self.sandbox_name,
            client=client,
        )
        return [SyncSandboxPreview(preview) for preview in response]

    def create(self, preview: Union[Preview, Dict[str, Any]]) -> SyncSandboxPreview:
        if isinstance(preview, dict):
            preview = Preview.from_dict(preview)
        response: Preview = create_sandbox_preview(
            self.sandbox_name,
            body=preview,
            client=client,
        )
        return SyncSandboxPreview(response)

    def create_if_not_exists(self, preview: Union[Preview, Dict[str, Any]]) -> SyncSandboxPreview:
        if isinstance(preview, dict):
            preview = Preview.from_dict(preview)
        preview_name = preview.metadata.name if preview.metadata else ""
        try:
            existing_preview = self.get(preview_name)
            return existing_preview
        except errors.UnexpectedStatus as e:
            if e.status_code == 404:
                return self.create(preview)
            raise e

    def get(self, preview_name: str) -> SyncSandboxPreview:
        response: Preview = get_sandbox_preview(
            self.sandbox_name,
            preview_name,
            client=client,
        )
        return SyncSandboxPreview(response)

    def delete(self, preview_name: str) -> dict:
        response: Preview = delete_sandbox_preview(
            self.sandbox_name,
            preview_name,
            client=client,
        )
        return response


def to_utc_z(dt: datetime) -> str:
    iso_string = dt.isoformat()
    if iso_string.endswith("+00:00"):
        return iso_string.replace("+00:00", "Z")
    elif "T" in iso_string and not iso_string.endswith("Z"):
        return iso_string + "Z"
    return iso_string



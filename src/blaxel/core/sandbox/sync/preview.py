from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Union

from ...client import errors
from ...client.api.compute.create_sandbox_preview import sync as create_sandbox_preview
from ...client.api.compute.create_sandbox_preview_token import (
    sync as create_sandbox_preview_token,
)
from ...client.api.compute.delete_sandbox_preview import sync as delete_sandbox_preview
from ...client.api.compute.delete_sandbox_preview_token import (
    sync as delete_sandbox_preview_token,
)
from ...client.api.compute.get_sandbox_preview import sync as get_sandbox_preview
from ...client.api.compute.list_sandbox_preview_tokens import (
    sync as list_sandbox_preview_tokens,
)
from ...client.api.compute.list_sandbox_previews import sync as list_sandbox_previews
from ...client.client import client
from ...client.models import (
    Preview,
    PreviewMetadata,
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
        return (
            self.preview_token.spec.token
            if self.preview_token.spec and self.preview_token.spec.token
            else ""
        )

    @property
    def expires_at(self) -> datetime:
        return (
            datetime.fromisoformat(self.preview_token.spec.expires_at)
            if self.preview_token.spec and self.preview_token.spec.expires_at
            else datetime.now()
        )


class SyncSandboxPreviewTokens:
    def __init__(self, preview: Preview):
        self.preview = preview

    @property
    def preview_name(self) -> str:
        return (
            self.preview.metadata.name
            if self.preview.metadata and self.preview.metadata.name
            else ""
        )

    @property
    def resource_name(self) -> str:
        return (
            self.preview.metadata.resource_name
            if self.preview.metadata and self.preview.metadata.resource_name
            else ""
        )

    def create(self, expires_at: datetime):
        response = create_sandbox_preview_token(
            self.resource_name,
            self.preview_name,
            body=PreviewToken(
                spec=PreviewTokenSpec(
                    expires_at=to_utc_z(expires_at),
                )
            ),
            client=client,
        )
        if response:
            return SyncSandboxPreviewToken(response)
        raise errors.UnexpectedStatus(400, b"Failed to create preview token")

    def list(self):
        response = list_sandbox_preview_tokens(
            self.resource_name,
            self.preview_name,
            client=client,
        )
        if response:
            return [SyncSandboxPreviewToken(token) for token in response]
        raise errors.UnexpectedStatus(400, b"Failed to list preview tokens")

    def delete(self, token_name: str):
        response = delete_sandbox_preview_token(
            self.resource_name,
            self.preview_name,
            token_name,
            client=client,
        )
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to delete preview token")


class SyncSandboxPreview:
    def __init__(self, preview: Preview):
        self.preview = preview
        self.tokens = SyncSandboxPreviewTokens(preview)

    @property
    def name(self) -> str:
        return (
            self.preview.metadata.name
            if self.preview.metadata and self.preview.metadata.name
            else ""
        )

    @property
    def metadata(self) -> PreviewMetadata | None:
        return self.preview.metadata if self.preview.metadata else None

    @property
    def spec(self) -> PreviewSpec | None:
        return self.preview.spec if self.preview.spec else None


class SyncSandboxPreviews:
    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    @property
    def sandbox_name(self) -> str:
        return (
            self.sandbox.metadata.name
            if self.sandbox.metadata and self.sandbox.metadata.name
            else ""
        )

    def list(self) -> List[SyncSandboxPreview]:
        response = list_sandbox_previews(
            self.sandbox_name,
            client=client,
        )
        if response:
            return [SyncSandboxPreview(preview) for preview in response]
        raise errors.UnexpectedStatus(400, b"Failed to list previews")

    def create(self, preview: Union[Preview, Dict[str, Any]]) -> SyncSandboxPreview:
        if isinstance(preview, dict):
            preview = Preview.from_dict(preview)
        response = create_sandbox_preview(
            self.sandbox_name,
            body=preview,
            client=client,
        )
        if response:
            return SyncSandboxPreview(response)
        raise errors.UnexpectedStatus(400, b"Failed to create preview")

    def create_if_not_exists(self, preview: Union[Preview, Dict[str, Any]]) -> SyncSandboxPreview:
        if isinstance(preview, dict):
            preview = Preview.from_dict(preview)
        preview_name = preview.metadata.name if preview.metadata and preview.metadata.name else ""
        try:
            existing_preview = self.get(preview_name)
            return existing_preview
        except errors.UnexpectedStatus as e:
            if e.status_code == 404:
                return self.create(preview)
            raise e

    def get(self, preview_name: str) -> SyncSandboxPreview:
        response = get_sandbox_preview(
            self.sandbox_name,
            preview_name,
            client=client,
        )
        if response:
            return SyncSandboxPreview(response)
        raise errors.UnexpectedStatus(400, b"Failed to get preview")

    def delete(self, preview_name: str) -> Preview:
        response = delete_sandbox_preview(
            self.sandbox_name,
            preview_name,
            client=client,
        )
        if response:
            return response
        raise errors.UnexpectedStatus(400, b"Failed to delete preview")


def to_utc_z(dt: datetime) -> str:
    iso_string = dt.isoformat()
    if iso_string.endswith("+00:00"):
        return iso_string.replace("+00:00", "Z")
    elif "T" in iso_string and not iso_string.endswith("Z"):
        return iso_string + "Z"
    return iso_string

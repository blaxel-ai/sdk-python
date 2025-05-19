from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from ..client.api.compute.create_sandbox_preview import asyncio as create_sandbox_preview
from ..client.api.compute.create_sandbox_preview_token import (
    asyncio as create_sandbox_preview_token,
)
from ..client.api.compute.delete_sandbox_preview import asyncio as delete_sandbox_preview
from ..client.api.compute.delete_sandbox_preview_token import (
    asyncio as delete_sandbox_preview_token,
)
from ..client.api.compute.get_sandbox_preview import asyncio as get_sandbox_preview
from ..client.api.compute.list_sandbox_preview_tokens import asyncio as list_sandbox_preview_tokens
from ..client.api.compute.list_sandbox_previews import asyncio as list_sandbox_previews
from ..client.client import client
from ..client.models import Preview, PreviewSpec, PreviewToken, PreviewTokenSpec, Sandbox


@dataclass
class SandboxPreviewToken:
    """Represents a preview token with its value and expiration."""
    preview_token: PreviewToken

    @property
    def value(self) -> str:
        return self.preview_token.spec.token if self.preview_token.spec else ""

    @property
    def expires_at(self) -> datetime:
        return self.preview_token.spec.expires_at if self.preview_token.spec else datetime.now()

class SandboxPreviewTokens:
    """Manages preview tokens for a sandbox preview."""
    def __init__(self, preview: Preview):
        self.preview = preview

    @property
    def preview_name(self) -> str:
        return self.preview.metadata.name if self.preview.metadata else ""

    @property
    def resource_name(self) -> str:
        return self.preview.metadata.resource_name if self.preview.metadata else ""

    async def create(self, expires_at: datetime) -> SandboxPreviewToken:
        """Create a new preview token."""
        response: PreviewToken = await create_sandbox_preview_token(
            self.resource_name,
            self.preview_name,
            body=PreviewToken(
                spec=PreviewTokenSpec(
                    expires_at=to_utc_z(expires_at),
                )
            ),
            client=client,
        )
        return SandboxPreviewToken(response)

    async def list(self) -> List[SandboxPreviewToken]:
        """List all preview tokens."""
        response: List[PreviewToken] = await list_sandbox_preview_tokens(
            self.resource_name,
            self.preview_name,
            client=client,
        )
        return [SandboxPreviewToken(token) for token in response]

    async def delete(self, token_name: str) -> dict:
        """Delete a preview token."""
        response: PreviewToken = await delete_sandbox_preview_token(
            self.resource_name,
            self.preview_name,
            token_name,
            client=client,
        )
        return response

class SandboxPreview:
    """Represents a sandbox preview with its metadata and tokens."""
    def __init__(self, preview: Preview):
        self.preview = preview
        self.tokens = SandboxPreviewTokens(self)

    @property
    def name(self) -> str:
        return self.preview.metadata.name if self.preview.metadata else ""

    @property
    def metadata(self) -> Optional[dict]:
        return self.preview.metadata

    @property
    def spec(self) -> Optional[PreviewSpec]:
        return self.preview.spec

class SandboxPreviews:
    """Manages sandbox previews."""
    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    @property
    def sandbox_name(self) -> str:
        return self.sandbox.metadata.name if self.sandbox.metadata else ""

    async def list(self) -> List[SandboxPreview]:
        """List all previews for the sandbox."""
        response: List[Preview] = await list_sandbox_previews(
            self.sandbox_name,
            client=client,
        )
        return [SandboxPreview(preview) for preview in response]

    async def create(self, preview: Preview) -> SandboxPreview:
        """Create a new preview."""
        response: Preview = await create_sandbox_preview(
            self.sandbox_name,
            body=preview,
            client=client,
        )
        return SandboxPreview(response)

    async def get(self, preview_name: str) -> SandboxPreview:
        """Get a specific preview by name."""
        response: Preview = await get_sandbox_preview(
            self.sandbox_name,
            preview_name,
            client=client,
        )
        return SandboxPreview(response)

    async def delete(self, preview_name: str) -> dict:
        """Delete a preview."""
        response: Preview = await delete_sandbox_preview(
            self.sandbox_name,
            preview_name,
            client=client,
        )
        return response

def to_utc_z(dt: datetime) -> str:
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")
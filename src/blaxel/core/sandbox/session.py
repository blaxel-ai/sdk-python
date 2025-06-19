from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from ..client.api.compute import (
    create_sandbox_preview,
    delete_sandbox_preview,
    get_sandbox_preview,
    list_sandbox_preview_tokens,
    list_sandbox_previews,
)
from ..client.client import client
from ..client.models import Metadata, Preview, PreviewSpec
from .preview import SandboxPreview
from .types import SandboxConfiguration, SessionCreateOptions, SessionWithToken


class SandboxSessions:
    def __init__(self, sandbox_config: SandboxConfiguration):
        self.sandbox_config = sandbox_config

    @property
    def sandbox_name(self) -> str:
        return self.sandbox_config.metadata.name if self.sandbox_config.metadata else ""

    async def create(
        self, options: Optional[Union[SessionCreateOptions, Dict[str, Any]]] = None
    ) -> SessionWithToken:
        if options is None:
            options = SessionCreateOptions()
        elif isinstance(options, dict):
            options = SessionCreateOptions.from_dict(options)

        expires_at = options.expires_at or datetime.now() + timedelta(days=1)

        preview_body = Preview(
            metadata=Metadata(name=f"session-{int(datetime.now().timestamp() * 1000)}"),
            spec=PreviewSpec(
                port=443,
                public=False,
                request_headers=options.request_headers,
                response_headers=options.response_headers,
            ),
        )

        preview_response = await create_sandbox_preview.asyncio(
            self.sandbox_name, client=client, body=preview_body
        )

        preview = SandboxPreview(preview_response, self.sandbox_name)
        token_obj = await preview.tokens.create(expires_at)

        return SessionWithToken(
            name=preview_body.metadata.name,
            url=preview.spec.url or "",
            token=token_obj.value,
            expires_at=token_obj.expires_at,
        )

    async def create_if_expired(
        self,
        options: Optional[Union[SessionCreateOptions, Dict[str, Any]]] = None,
        delta_seconds: int = 3600,  # 1 hour
    ) -> SessionWithToken:
        if options is None:
            options = SessionCreateOptions()
        elif isinstance(options, dict):
            options = SessionCreateOptions.from_dict(options)

        all_sessions = await self.list()
        now = datetime.now()
        threshold = now + timedelta(seconds=delta_seconds)

        if all_sessions:
            session_data = all_sessions[0]
            if session_data.expires_at < threshold:
                await self.delete(session_data.name)
                session_data = await self.create(options)
        else:
            session_data = await self.create(options)

        return session_data

    async def list(self) -> List[SessionWithToken]:
        previews_response = await list_sandbox_previews.asyncio(self.sandbox_name, client=client)

        sessions = []
        for preview in previews_response:
            if preview.metadata and preview.metadata.name and "session-" in preview.metadata.name:
                token = await self.get_token(preview.metadata.name)
                if token:
                    sessions.append(
                        SessionWithToken(
                            name=preview.metadata.name,
                            url=preview.spec.url or "",
                            token=token.spec.token or "",
                            expires_at=token.spec.expires_at or datetime.now(),
                        )
                    )

        return sessions

    async def get(self, name: str) -> SessionWithToken:
        preview_response = await get_sandbox_preview.asyncio(self.sandbox_name, name, client=client)

        token = await self.get_token(name)

        return SessionWithToken(
            name=name,
            url=preview_response.spec.url or "",
            token=token.spec.token or "" if token else "",
            expires_at=token.spec.expires_at or datetime.now() if token else datetime.now(),
        )

    async def delete(self, name: str):
        return await delete_sandbox_preview.asyncio(self.sandbox_name, name, client=client)

    async def get_token(self, preview_name: str):
        tokens_response = await list_sandbox_preview_tokens.asyncio(
            self.sandbox_name, preview_name, client=client
        )

        if not tokens_response:
            return None
        return tokens_response[0]

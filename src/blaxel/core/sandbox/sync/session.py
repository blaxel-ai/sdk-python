from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

from ...client.api.compute import (
    create_sandbox_preview,
    delete_sandbox_preview,
    get_sandbox_preview,
    list_sandbox_preview_tokens,
    list_sandbox_previews,
)
from ...client.client import client
from ...client.models import Metadata, Preview, PreviewSpec
from ..types import SandboxConfiguration, SessionCreateOptions, SessionWithToken
from .preview import SyncSandboxPreview


class SyncSandboxSessions:
    def __init__(self, sandbox_config: SandboxConfiguration):
        self.sandbox_config = sandbox_config

    @property
    def sandbox_name(self) -> str:
        return self.sandbox_config.metadata.name if self.sandbox_config.metadata else ""

    def create(
        self, options: Union[SessionCreateOptions, Dict[str, Any]] | None = None
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
                expires=expires_at.isoformat(),
                request_headers=options.request_headers,
                response_headers=options.response_headers,
            ),
        )
        preview_response = create_sandbox_preview.sync(
            self.sandbox_name, client=client, body=preview_body
        )
        preview = SyncSandboxPreview(preview_response)
        token_obj = preview.tokens.create(expires_at)
        return SessionWithToken(
            name=preview_body.metadata.name,
            url=preview.spec.url or "",
            token=token_obj.value,
            expires_at=token_obj.expires_at,
        )

    def create_if_expired(
        self,
        options: Union[SessionCreateOptions, Dict[str, Any]] | None = None,
        delta_seconds: int = 3600,
    ) -> SessionWithToken:
        if options is None:
            options = SessionCreateOptions()
        elif isinstance(options, dict):
            options = SessionCreateOptions.from_dict(options)
        all_sessions = self.list()
        now = datetime.now()
        threshold = now + timedelta(seconds=delta_seconds)
        if all_sessions:
            all_sessions.sort(
                key=lambda s: datetime.fromisoformat(s.expires_at)
                if isinstance(s.expires_at, str)
                else s.expires_at
            )
            session_data = all_sessions[0]
            expires_at = datetime.fromisoformat(session_data.expires_at)
            if expires_at.tzinfo is not None and threshold.tzinfo is None:
                threshold = threshold.replace(tzinfo=expires_at.tzinfo)
            elif expires_at.tzinfo is None and threshold.tzinfo is not None:
                expires_at = expires_at.replace(tzinfo=threshold.tzinfo)
            if expires_at < threshold:
                self.delete(session_data.name)
                session_data = self.create(options)
        else:
            session_data = self.create(options)
        return session_data

    def list(self) -> List[SessionWithToken]:
        previews_response = list_sandbox_previews.sync(self.sandbox_name, client=client)
        sessions = []
        for preview in previews_response:
            if preview.metadata and preview.metadata.name and "session-" in preview.metadata.name:
                token = self.get_token(preview.metadata.name)
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

    def get(self, name: str) -> SessionWithToken:
        preview_response = get_sandbox_preview.sync(self.sandbox_name, name, client=client)
        token = self.get_token(name)
        return SessionWithToken(
            name=name,
            url=preview_response.spec.url or "",
            token=token.spec.token or "" if token else "",
            expires_at=token.spec.expires_at or datetime.now() if token else datetime.now(),
        )

    def delete(self, name: str):
        return delete_sandbox_preview.sync(self.sandbox_name, name, client=client)

    def get_token(self, preview_name: str):
        tokens_response = list_sandbox_preview_tokens.sync(
            self.sandbox_name, preview_name, client=client
        )
        if not tokens_response:
            return None
        return tokens_response[0]

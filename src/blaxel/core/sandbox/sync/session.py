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
    """Manage sessions: short-lived access to one sandbox without an API key.

    Reach it as ``sandbox.sessions``. A session is a private preview named
    ``session-<timestamp>`` on the sandbox API port plus a preview token. Give
    the session (name, URL, token and expiry) to code that must not hold an
    API key, such as a browser or another service, and open it there with
    ``SyncSandboxInstance.from_session``. Every call here goes to the control
    plane and needs an API key; an error status raises
    ``blaxel.core.client.errors.UnexpectedStatus``.

    Example:
        ```python
        session = sandbox.sessions.create_if_expired()
        # Hand session.name, .url, .token and .expires_at to the client side.
        ```
    """

    def __init__(self, sandbox_config: SandboxConfiguration):
        self.sandbox_config = sandbox_config

    @property
    def sandbox_name(self) -> str:
        """Name of the sandbox these sessions belong to."""
        return self.sandbox_config.metadata.name if self.sandbox_config.metadata else ""

    def create(
        self, options: Union[SessionCreateOptions, Dict[str, Any]] | None = None
    ) -> SessionWithToken:
        """Create a session: a private preview and a token for it.

        Args:
            options: ``SessionCreateOptions`` or a dict with ``expires_at``,
                ``request_headers`` and ``response_headers`` (headers the
                preview adds to requests and responses). ``expires_at``
                defaults to 24 hours from now on the local clock. A naive
                datetime, including that default, is sent as if it were UTC,
                so pass an aware UTC datetime for an exact expiry.

        Returns:
            ``SessionWithToken`` with ``name``, ``url``, ``token`` and
            ``expires_at``.

        Example:
            ```python
            from datetime import datetime, timedelta, timezone

            session = sandbox.sessions.create(
                {"expires_at": datetime.now(timezone.utc) + timedelta(hours=2)}
            )
            ```
        """
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
        """Return a session that stays valid long enough, creating one if needed.

        Looks at the session that expires first. When it expires within
        ``delta_seconds``, it is deleted and a new one is created with
        ``options``; otherwise it is returned as is. Without any session, one
        is created.

        Args:
            options: Options for a new session, as in :meth:`create`.
            delta_seconds: Minimum remaining validity, in seconds, for reuse.

        Returns:
            The reused or new ``SessionWithToken``.
        """
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
        """List the sessions of this sandbox.

        Sessions are the previews whose name contains ``session-``, each with
        its first token. A session without a token is left out. This makes
        one token request per session.

        Returns:
            A list of ``SessionWithToken``.
        """
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
        """Get a session by name.

        Args:
            name: Session name, such as ``session-1718000000000``.

        Returns:
            ``SessionWithToken``. ``token`` is ``""`` when the session has no
            token.

        Raises:
            blaxel.core.client.errors.UnexpectedStatus: With status 404 when the
                session does not exist.
        """
        preview_response = get_sandbox_preview.sync(self.sandbox_name, name, client=client)
        token = self.get_token(name)
        return SessionWithToken(
            name=name,
            url=preview_response.spec.url or "",
            token=token.spec.token or "" if token else "",
            expires_at=token.spec.expires_at or datetime.now() if token else datetime.now(),
        )

    def delete(self, name: str):
        """Delete a session; its URL and token stop working.

        Args:
            name: Session name.

        Returns:
            The deleted ``Preview`` record.
        """
        return delete_sandbox_preview.sync(self.sandbox_name, name, client=client)

    def get_token(self, preview_name: str):
        """Return the first token of a session preview, or None when it has none.

        Args:
            preview_name: Session name.

        Returns:
            A ``PreviewToken`` or None.
        """
        tokens_response = list_sandbox_preview_tokens.sync(
            self.sandbox_name, preview_name, client=client
        )
        if not tokens_response:
            return None
        return tokens_response[0]

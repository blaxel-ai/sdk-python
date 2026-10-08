import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Union, cast

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
from ...client.api.compute.get_sandbox_preview import (
    sync_detailed as get_sandbox_preview_detailed,
)
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
    PreviewTokenMetadata,
    PreviewTokenSpec,
    Sandbox,
)
from ..types import SandboxPreviewCreateConfiguration


def _is_shorthand(
    preview: Union[Preview, SandboxPreviewCreateConfiguration, Dict[str, Any]],
) -> bool:
    return isinstance(preview, SandboxPreviewCreateConfiguration) or (
        isinstance(preview, dict) and "metadata" not in preview and "spec" not in preview
    )


def _normalize_preview(
    preview: Union[Preview, SandboxPreviewCreateConfiguration, Dict[str, Any]],
) -> Preview:
    if isinstance(preview, Preview):
        return preview
    if isinstance(preview, dict) and ("metadata" in preview or "spec" in preview):
        return cast(Preview, Preview.from_dict(preview))
    config = (
        SandboxPreviewCreateConfiguration.from_dict(preview)
        if isinstance(preview, dict)
        else preview
    )
    port, name, public = config.port, config.name, config.public
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("Preview port must be an integer between 1 and 65535")
    if name is not None and (not isinstance(name, str) or not name):
        raise ValueError("Preview name must be a nonempty string")
    if not isinstance(public, bool):
        raise ValueError("Preview public must be a boolean")
    return Preview(
        metadata=PreviewMetadata(name=name if name is not None else f"preview-{port}"),
        spec=PreviewSpec(port=port, public=public),
    )


def _utc_datetime(value: datetime) -> datetime:
    return (
        value.replace(tzinfo=timezone.utc)
        if value.tzinfo is None
        else value.astimezone(timezone.utc)
    )


def _token_bounds(
    expires_at: datetime | None,
    min_validity: timedelta,
    now: datetime,
) -> tuple[datetime, datetime]:
    if not isinstance(min_validity, timedelta) or min_validity.total_seconds() < 0:
        raise ValueError("min_validity must be a non-negative timedelta")
    try:
        if expires_at is not None and not isinstance(expires_at, datetime):
            raise ValueError
        minimum = now + min_validity
        expiry = now + timedelta(hours=24) if expires_at is None else _utc_datetime(expires_at)
        if expiry <= now or expiry < minimum:
            raise ValueError
    except (AttributeError, TypeError, ValueError, OverflowError):
        raise ValueError(
            "expires_at must be a valid future datetime at least min_validity from now"
        ) from None
    return expiry, minimum


def _select_token(
    response: Any,
    now: datetime,
    minimum: datetime,
    ceiling: datetime,
) -> PreviewToken | None:
    if not isinstance(response, list):
        raise RuntimeError("Failed to list preview tokens")
    selected = None
    latest = now
    for token in response:
        spec = getattr(token, "spec", None)
        value = getattr(spec, "token", None)
        raw_expiry = getattr(spec, "expires_at", None)
        if (
            not isinstance(value, str)
            or not value
            or getattr(spec, "expired", None) is True
            or not isinstance(raw_expiry, str)
        ):
            continue
        try:
            expiry = _utc_datetime(datetime.fromisoformat(raw_expiry.replace("Z", "+00:00")))
        except (ValueError, OverflowError):
            continue
        if expiry <= now or expiry < minimum or expiry > ceiling:
            continue
        if expiry > latest:
            selected, latest = token, expiry
    return selected


@dataclass
class SyncSandboxPreviewToken:
    preview_token: PreviewToken

    @property
    def name(self) -> str:
        name = getattr(getattr(self.preview_token, "metadata", None), "name", None)
        return name if isinstance(name, str) else ""

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
                metadata=PreviewTokenMetadata(name=""),
                spec=PreviewTokenSpec(
                    expires_at=to_utc_z(expires_at),
                ),
            ),
            client=client,
        )
        if response:
            return SyncSandboxPreviewToken(response)
        raise errors.UnexpectedStatus(400, b"Failed to create preview token")

    def create_if_expired(
        self,
        expires_at: datetime | None = None,
        min_validity: timedelta = timedelta(hours=1),
    ) -> SyncSandboxPreviewToken:
        """Reuse the latest eligible token, or create one. Naive datetimes mean UTC.

        The requested expiry caps reuse. Concurrent calls can mint separate tokens;
        no existing credentials are deleted.
        """
        now = datetime.now(timezone.utc)
        expiry, minimum = _token_bounds(expires_at, min_validity, now)
        if getattr(getattr(self.preview, "spec", None), "public", None) is True:
            raise ValueError("Cannot create or reuse a token for a public preview")
        response = list_sandbox_preview_tokens(
            self.resource_name,
            self.preview_name,
            client=client,
        )
        selected = _select_token(response, now, minimum, expiry)
        if selected is not None:
            return SyncSandboxPreviewToken(selected)
        return self.create(expiry)

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
    def url(self) -> str:
        url = getattr(getattr(self.preview, "spec", None), "url", None)
        return url if isinstance(url, str) else ""

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

    def create(
        self,
        preview: Union[Preview, SandboxPreviewCreateConfiguration, Dict[str, Any]],
    ) -> SyncSandboxPreview:
        """Create a preview; shorthand defaults to a private preview-<port>."""
        preview = _normalize_preview(preview)
        response = create_sandbox_preview(
            self.sandbox_name,
            body=preview,
            client=client,
        )
        if response:
            return SyncSandboxPreview(response)
        raise errors.UnexpectedStatus(400, b"Failed to create preview")

    def create_if_not_exists(
        self,
        preview: Union[Preview, SandboxPreviewCreateConfiguration, Dict[str, Any]],
    ) -> SyncSandboxPreview:
        """Return existing previews as-is; the private default applies only on creation."""
        if _is_shorthand(preview):
            normalized = _normalize_preview(preview)
            try:
                return self.get(normalized.metadata.name)
            except errors.UnexpectedStatus as e:
                if e.status_code != 404:
                    raise
            try:
                return self.create(normalized)
            except errors.UnexpectedStatus as e:
                if e.status_code != 409:
                    raise
                return self.get(normalized.metadata.name)
        preview = _normalize_preview(preview)
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
        if not response:
            raise errors.UnexpectedStatus(400, b"Failed to delete preview")

        # If the preview is in DELETING state, wait for it to be fully deleted
        if response.status == "DELETING":
            self._wait_for_deletion(preview_name)

        return response

    def _wait_for_deletion(self, preview_name: str, timeout_ms: int = 10000) -> None:
        """Wait for a preview to be fully deleted.

        Args:
            preview_name: Name of the preview to wait for
            timeout_ms: Timeout in milliseconds (default: 10000)

        Raises:
            Exception: If the preview is still in DELETING state after timeout
        """
        print(f"Waiting for preview deletion: {preview_name}")
        poll_interval = 0.5  # Poll every 500ms
        elapsed = 0.0
        timeout_seconds = timeout_ms / 1000.0

        while elapsed < timeout_seconds:
            try:
                response = get_sandbox_preview_detailed(
                    self.sandbox_name,
                    preview_name,
                    client=client,
                )
                if response.status_code == 404:
                    return
            except errors.UnexpectedStatus as e:
                # 404 means the preview is deleted
                if e.status_code == 404:
                    return
                raise
            # Preview still exists, wait and retry
            time.sleep(poll_interval)
            elapsed += poll_interval

        # Timeout reached, but deletion was initiated
        raise Exception(
            f"Preview deletion timeout: {preview_name} is still in DELETING state after {timeout_ms}ms"
        )


def to_utc_z(dt: datetime) -> str:
    iso_string = dt.isoformat()
    if iso_string.endswith("+00:00"):
        return iso_string.replace("+00:00", "Z")
    elif "T" in iso_string and not iso_string.endswith("Z"):
        return iso_string + "Z"
    return iso_string

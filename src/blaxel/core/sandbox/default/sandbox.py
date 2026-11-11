import asyncio
import json
import logging
import math
import time
import warnings
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import TYPE_CHECKING, Any, Callable, Dict, Union

from attrs import evolve

if TYPE_CHECKING:
    import httpx

from ...client import errors as client_errors
from ...client.api.compute.archive_sandbox import asyncio as archive_sandbox
from ...client.api.compute.create_sandbox import asyncio as create_sandbox
from ...client.api.compute.create_sandbox_snapshot import asyncio as create_sandbox_snapshot
from ...client.api.compute.delete_sandbox import asyncio as delete_sandbox
from ...client.api.compute.delete_sandbox_snapshot import asyncio as delete_sandbox_snapshot
from ...client.api.compute.fork_sandbox import asyncio as fork_sandbox
from ...client.api.compute.get_sandbox import asyncio as get_sandbox
from ...client.api.compute.list_sandbox_snapshots import asyncio as list_sandbox_snapshots
from ...client.api.compute.list_sandboxes import asyncio as list_sandboxes
from ...client.api.compute.restore_sandbox_snapshot import asyncio as restore_sandbox_snapshot
from ...client.api.compute.unarchive_sandbox import asyncio as unarchive_sandbox
from ...client.api.compute.update_sandbox import asyncio as update_sandbox
from ...client.client import Client, client
from ...client.models import (
    Env,
    Metadata,
    MetadataLabels,
    Sandbox,
    SandboxForkRequest,
    SandboxForkResponse,
    SandboxInfrastructureError,
    SandboxLifecycle,
    SandboxRestoreResponse,
    SandboxRuntime,
    SandboxRuntimeExtraArgs,
    SandboxSnapshot,
    SandboxSnapshotRequest,
    SandboxSpec,
)
from ...client.models import (
    SandboxNetwork as SandboxNetworkModel,
)
from ...client.models.error import Error
from ...client.models.sandbox_error import SandboxError
from ...client.pagination import AsyncPaginatedList, make_async_paginated_list, normalize_cursor
from ...client.types import UNSET, Unset
from ...common.polling import poll_delay_seconds
from ...common.settings import settings
from ...errors import _APIError
from ..drift import RequestedSandbox, caller_stacklevel, drift_message, requested_from_model
from ..drive_setup import _AsyncDriveSetup, _normalize_mount_drives, _requested_region
from ..names import _invalid_name_hint
from ..transient_retry import _backoff_delay_seconds
from ..types import (
    SandboxConfiguration,
    SandboxCreateConfiguration,
    SandboxDriveMountConfiguration,
    SandboxUpdateMetadata,
    SandboxUpdateNetwork,
    SessionWithToken,
)
from .codegen import SandboxCodegen
from .drive import SandboxDrive
from .filesystem import SandboxFileSystem
from .network import SandboxNetwork
from .preview import SandboxPreviews
from .process import SandboxProcess
from .schedule import SandboxSchedules
from .session import SandboxSessions
from .snapshot import SandboxSnapshots
from .system import SandboxSystem


class SandboxAPIError(_APIError):
    """Exception raised when sandbox API returns an error."""


CREATION_TIMEOUT_HEADER = "X-Blaxel-Creation-Timeout"
CREATION_TIMEOUT_CODE = "CREATION_TIMEOUT"
MAX_CREATION_TIMEOUT_SECONDS = 50


class SandboxCreationTimeoutError(SandboxAPIError):
    """Raised when the sandbox was not ready within the creation deadline.

    The control plane cancels the creation and releases the sandbox, so the same
    name can be used by a later creation attempt.
    """

    def __init__(
        self,
        sandbox_name: str | None,
        timeout: int | None,
        data: Any = None,
        *,
        response: "httpx.Response | None" = None,
    ):
        detail = data.get("message") if isinstance(data, dict) else None
        target = f"Sandbox {sandbox_name}" if sandbox_name else "Sandbox"
        deadline = f" within {timeout}s" if timeout is not None else " within the creation deadline"
        message = f"{target} was not ready{deadline}; the creation was cancelled."
        if isinstance(detail, str) and detail:
            message = f"{message} {detail}"
        super().__init__(
            message, status_code=408, code=CREATION_TIMEOUT_CODE, body=data, response=response
        )
        self.sandbox_name = sandbox_name
        self.timeout = timeout
        self.data = data


def is_creation_timeout_error(err: object) -> bool:
    """Return True when ``err`` is a sandbox creation timeout."""
    return isinstance(err, SandboxCreationTimeoutError)


def _validate_creation_timeout(timeout: int | None) -> int | None:
    if timeout is None:
        return None
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, int)
        or timeout < 1
        or timeout > MAX_CREATION_TIMEOUT_SECONDS
    ):
        raise ValueError(
            "SandboxInstance.create: 'timeout' must be a whole number of seconds"
            f" between 1 and {MAX_CREATION_TIMEOUT_SECONDS}, got {timeout!r}."
        )
    return timeout


def _creation_client(timeout: int | None) -> Client:
    """Return the control-plane client to use for a creation request.

    With a timeout, a copy of the shared client carrying the creation-timeout
    header is returned so the shared client is left untouched.
    """
    if timeout is None:
        return client
    return evolve(client, headers={**client._headers, CREATION_TIMEOUT_HEADER: str(timeout)})


def _decode_error_content(content: bytes) -> Any:
    try:
        return json.loads(content)
    except (UnicodeDecodeError, ValueError):
        return content.decode("utf-8", errors="replace")


def _raise_if_creation_timeout(
    error: SandboxError | client_errors.UnexpectedStatus,
    sandbox_name: str | None,
    timeout: int | None,
) -> None:
    if isinstance(error, client_errors.UnexpectedStatus):
        if error.status_code != 408:
            return
        raise SandboxCreationTimeoutError(
            sandbox_name, timeout, _decode_error_content(error.content), response=error.response
        ) from error
    status_code = error.status_code if error.status_code is not UNSET else None
    if status_code == 408 or error.code == CREATION_TIMEOUT_CODE:
        raise SandboxCreationTimeoutError(
            sandbox_name, timeout, error.to_dict(), response=error._response
        )


# A creation the control plane rejects at its credential check, in a way a new
# attempt can fix: a generic 403 "Authorization failed" (code UNAUTHORIZED) when
# it could not resolve the credentials, or a 503 AUTHENTICATION_UNAVAILABLE when
# its credential store is unreachable. Both are answered before anything is
# created, so sending the same request again is safe. A revoked token (401
# TOKEN_REVOKED) or a missing workspace permission (UNAUTHORIZED_WORKSPACE) is
# final and is not retried. A key the API does not recognize gets the same
# 403, so the retries stay few and the final message asks to check the key.
CREATE_AUTH_RETRIES = 2
CREATE_AUTH_RETRY_BASE_DELAY_SECONDS = 0.5
CREATE_AUTH_RETRY_MAX_DELAY_SECONDS = 2.0


def _error_status(error: SandboxError) -> int | None:
    if isinstance(error.status_code, int):
        return error.status_code
    return error._response.status_code if error._response is not None else None


def _is_transient_create_auth_failure(error: object) -> bool:
    if isinstance(error, SandboxError):
        return _error_status(error) == 403 and error.code == "UNAUTHORIZED"
    if isinstance(error, client_errors.UnexpectedStatus):
        return error.status_code == 503 and error.code == "AUTHENTICATION_UNAVAILABLE"
    return False


def _create_auth_retry_delay(attempt: int) -> float:
    return _backoff_delay_seconds(
        attempt, CREATE_AUTH_RETRY_BASE_DELAY_SECONDS, CREATE_AUTH_RETRY_MAX_DELAY_SECONDS
    )


def _create_error_message(error: SandboxError, sandbox_name: str | None, attempts: int) -> str:
    """Message of the SandboxAPIError raised for a rejected creation."""
    message = error.message if error.message else str(error)
    if _is_transient_create_auth_failure(error):
        try:
            workspace = settings.workspace
        except Exception:
            workspace = None
        current = f"; current workspace: '{workspace}'" if workspace else ""
        return (
            f"{message} (HTTP 403 {error.code}, after {attempts} attempts). The API answers"
            " this way both for a key it does not recognize and when its credential check"
            " fails for a moment. Check the credentials and workspace the SDK uses"
            f" (BL_API_KEY and BL_WORKSPACE, or `bl login`{current}); if they are right,"
            " retry in a few seconds."
        )
    explained = _limit_explanation(_error_status(error), error.code, error.message, None)
    if explained is not None:
        return explained[0]
    if _error_status(error) == 400:
        hint = _invalid_name_hint(sandbox_name)
        if hint and message and not message.endswith((".", "!", "?")):
            message += "."
        return message + hint
    return message


QUOTAS_DOC_URL = "https://docs.blaxel.ai/Security/Quotas"
EDGE_BLOCKED_MESSAGE = (
    "HTTP 403 without a JSON error body: likely an edge rate limit or firewall block"
    " in front of the API. If you send many requests, slow down and retry after about"
    " 60 s. Blaxel quota and permission errors carry a JSON error code"
)
_RATE_LIMIT_REASONS = {
    "WORKSPACE_RATE_LIMIT_EXCEEDED": "too many creations in flight in this workspace",
    "RATE_LIMIT_EXCEEDED": "the region's creation rate limit was reached",
}


def _retry_after_seconds(error: client_errors.UnexpectedStatus) -> int | None:
    """Seconds to wait from the server's retry_after (Retry-After header or body)."""
    seconds = getattr(error, "retry_after_seconds", None)
    if seconds is not None:
        return seconds
    value = getattr(error, "retry_after", None)  # an HTTP date, already normalized
    if not value:
        return None
    try:
        retry_at = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    return max(0, math.ceil((retry_at - datetime.now(timezone.utc)).total_seconds()))


def _server_message(body: Any) -> str | None:
    if not isinstance(body, dict):
        return None
    nested = body.get("error")
    for source in (nested, body) if isinstance(nested, dict) else (body,):
        message = source.get("message")
        if isinstance(message, str) and message:
            return message
    return None


def _has_json_error_body(content: bytes) -> bool:
    try:
        return isinstance(json.loads(content), dict)
    except (UnicodeDecodeError, ValueError, RecursionError):
        return False


def _limit_explanation(
    status: int | None, code: Any, server_message: str | None, wait: int | None
) -> tuple[str, bool] | None:
    """Message and retryable flag for a creation rejected by a quota or rate limit.

    QUOTA_EXCEEDED (HTTP 429 for a workspace quota, 400 for one ephemeral volume
    over the per-volume maximum) stays until quota is freed or raised. The rate
    limit codes clear on their own. The SDK itself retries none of them.
    """
    if code == "QUOTA_EXCEEDED" and status in (400, 429):
        if status == 400:
            advice = "not retryable as is; request a smaller volume or raise the quota"
        else:
            advice = "not retryable until quota is freed or raised"
        message = server_message or "Quota exceeded"
        return f"{message} (HTTP {status} QUOTA_EXCEEDED: {advice}: {QUOTAS_DOC_URL})", False
    if status == 429 and code in _RATE_LIMIT_REASONS:
        advice = f"retry after {wait} s" if wait is not None else "retry with backoff"
        message = server_message or "Rate limit exceeded"
        return f"{message} (HTTP 429 {code}: {_RATE_LIMIT_REASONS[code]}; {advice})", True
    return None


def _explain_create_error(error: client_errors.UnexpectedStatus) -> None:
    """Say in the message whether a rejected creation can be retried.

    Quota and rate-limit errors share HTTP 429 but need opposite handling;
    ``retryable`` says which. A 403 without a JSON error body did not come from
    the API's own checks.
    """
    if error.status_code == 403 and not _has_json_error_body(error.content):
        message = EDGE_BLOCKED_MESSAGE
    else:
        wait = _retry_after_seconds(error)
        explained = _limit_explanation(
            error.status_code, error.code, _server_message(error.body), wait
        )
        if explained is None:
            return
        message, error.retryable = explained
        if error.retryable:
            error.retry_after_seconds = wait
    error.message = message
    error.args = (message,)


def _create_error(
    error: SandboxError, sandbox_name: str | None, attempts: int
) -> client_errors.UnexpectedStatus | SandboxAPIError:
    """Exception for a creation the API rejected with a modeled error body.

    A 429 raises what it raised before CreateSandbox modeled 429:
    QuotaExceededError for QUOTA_EXCEEDED, RateLimitError for the rate limits.
    Everything else is SandboxAPIError.
    """
    status_code = _error_status(error)
    if status_code == 429:
        response = error._response
        if response is not None:
            limit_error = client_errors.from_response(
                429, response.content, response.headers, response=response
            )
        else:
            limit_error = client_errors.from_response(429, json.dumps(error.to_dict()).encode())
        _explain_create_error(limit_error)
        return limit_error
    code = error.code if error.code else None
    api_error = SandboxAPIError(
        _create_error_message(error, sandbox_name, attempts),
        status_code=status_code,
        code=code,
        error=error,
    )
    if _limit_explanation(status_code, code, None, None) is not None:
        api_error.retryable = False
    return api_error


_region_notice_shown = False


def _notify_region_unset(class_name: str = "SandboxInstance") -> None:
    """Say once per process that the platform picks the region when none is set."""
    global _region_notice_shown
    if _region_notice_shown:
        return
    _region_notice_shown = True
    warnings.warn(
        f"{class_name}.create: no region set, so the platform picks one for the sandbox."
        " Set 'region' in the sandbox configuration or the BL_REGION environment variable"
        " (e.g. 'us-pdx-1', 'eu-lon-1', 'us-was-1') to choose it; 'region' will become"
        " required in a future version. This notice is shown once per process.",
        FutureWarning,
        stacklevel=3,
    )


logger = logging.getLogger(__name__)

# Archiving a filesystem, and restoring it, take as long as that filesystem is
# big — minutes for a few gigabytes.
# Waits are expressed in milliseconds, like every other wait option of this SDK
# (e.g. ``process.wait(max_wait=..., interval=...)``).
ARCHIVE_MAX_WAIT_MS = 1_800_000
ARCHIVE_WAIT_POLL_MS = 2_000
# An archive is done when the sandbox is ARCHIVED; it is still under way while
# the record holds one of these.
ARCHIVING_STATUSES = {"ARCHIVING"}
# A restore is done when the sandbox is DEPLOYED again; the instance is recreated
# before the archived filesystem is written back over its image.
UNARCHIVING_STATUSES = {"UNARCHIVING", "DEPLOYING", "BUILDING", "UPLOADING"}
# The status the sandbox holds before the operation moves it, tolerated only
# while the operation is starting: an archive that fails hands the sandbox back
# as DEPLOYED, and a restore that fails leaves it ARCHIVED, so reading the entry
# status again once the operation has begun means it is over, not still running.
ARCHIVE_ENTRY_STATUS = "DEPLOYED"
UNARCHIVE_ENTRY_STATUS = "ARCHIVED"
ARCHIVE_ENTRY_MAX_WAIT_MS = 30_000


def _unwrap_response(response, action: str, *, allow_none: bool = False):
    """Raise a SandboxAPIError for error/empty responses, else return the payload.

    Every generated control-plane API function returns ``Union[Error, T] | None``,
    so an error status is a *return value*, not an exception. Callers must route
    the response through here; handing it straight to ``cls(...)`` builds an
    instance wrapping an ``Error`` and turns a failed write into a silent no-op.
    Void endpoints (e.g. delete, which returns 204 No Content) legitimately return
    ``None`` — pass ``allow_none=True`` for those.
    """
    if isinstance(response, Error):
        status_code = response.code if response.code is not UNSET else None
        message = response.message if response.message is not UNSET else response.error
        raise SandboxAPIError(message, status_code=status_code, code=response.error, error=response)
    if response is None and not allow_none:
        raise SandboxAPIError(f"Failed to {action}")
    return response


def _create_body(sandbox: Sandbox) -> Union[Sandbox, Dict[str, Any]]:
    """Build the create request body, omitting metadata.name when unnamed.

    Unnamed creations are sent without ``metadata.name`` so the server assigns
    a name and the request becomes eligible for warm sandbox pools (ENG-3931).
    """
    if sandbox.metadata and sandbox.metadata.name:
        return sandbox
    body = sandbox.to_dict()
    metadata = body.get("metadata")
    if isinstance(metadata, dict):
        metadata.pop("name", None)
    return body


class _AsyncDeleteDescriptor:
    """Descriptor that provides both class-level and instance-level delete functionality."""

    def __init__(self, delete_func: Callable):
        self._delete_func = delete_func

    def __get__(self, instance, owner):
        if instance is None:
            # Called on the class: SandboxInstance.delete("name")
            return self._delete_func
        else:
            # Called on an instance: instance.delete()
            async def instance_delete() -> Sandbox:
                """Delete this sandbox; see ``SandboxInstance.delete("name")`` for details."""
                return await self._delete_func(instance.metadata.name)

            return instance_delete


def _sandbox_name(
    sandbox: Union[Sandbox, SandboxCreateConfiguration, Dict[str, Any]],
) -> str | None:
    if isinstance(sandbox, SandboxCreateConfiguration):
        return sandbox.name
    if isinstance(sandbox, dict):
        if "name" in sandbox:
            return sandbox["name"]
        metadata = sandbox.get("metadata")
        if isinstance(metadata, dict):
            return metadata.get("name")
        return getattr(metadata, "name", None)
    if isinstance(sandbox, Sandbox):
        return sandbox.metadata.name if sandbox.metadata else None
    return None


def _status_of(sandbox: Sandbox) -> str | None:
    status = sandbox.status
    return None if isinstance(status, Unset) else str(status) if status else None


class _AsyncSandboxCallDescriptor:
    """Expose an operation as both ``SandboxInstance.op("name")`` and ``instance.op()``.

    Both forms answer a ``SandboxInstance``; the instance form refreshes the
    record it was called on. The archive of a filesystem and its restore run in
    the background, so both forms wait for the sandbox to reach ``target`` unless
    ``wait=False``.
    """

    def __init__(
        self,
        api_call: Callable,
        action: str,
        target: str,
        pending: set[str],
        entry: str,
        doc: str,
    ):
        self._api_call = api_call
        self._action = action
        self._target = target
        self._pending = pending
        self._entry = entry
        self.__doc__ = doc

    async def _call(self, sandbox_name: str, wait: bool, max_wait: int, interval: int) -> Sandbox:
        response = await self._api_call(sandbox_name)
        sandbox = _unwrap_response(response, f"{self._action} sandbox {sandbox_name}")
        if not wait or _status_of(sandbox) == self._target:
            return sandbox
        return await self._wait(sandbox_name, max_wait, interval)

    async def _wait(self, sandbox_name: str, max_wait: int, interval: int) -> Sandbox:
        deadline = time.monotonic() + max_wait / 1000
        entry_deadline = time.monotonic() + min(ARCHIVE_ENTRY_MAX_WAIT_MS, max_wait) / 1000
        started = False
        attempt = 0
        while True:
            # Until the operation is seen pending, read at the first interval:
            # a backed-off sleep could pass the entry grace window or miss a
            # short pending status.
            if started:
                attempt += 1
            remaining = max(deadline - time.monotonic(), 0.0)
            await asyncio.sleep(
                min(poll_delay_seconds(max(attempt, 1), interval / 1000), remaining)
            )
            response = await get_sandbox(sandbox_name, client=client)
            sandbox = _unwrap_response(response, f"read sandbox {sandbox_name}")
            status = _status_of(sandbox)
            if status == self._target:
                return sandbox
            if status in self._pending:
                started = True
            elif status == self._entry and not started and time.monotonic() < entry_deadline:
                continue
            if status not in self._pending:
                raise SandboxAPIError(
                    f"Sandbox {sandbox_name} is {status} while it should {self._action}"
                )
            if time.monotonic() >= deadline:
                raise SandboxAPIError(
                    f"Sandbox {sandbox_name} is still {status} "
                    f"after waiting {max_wait / 1000:.0f}s for it to {self._action}"
                )

    def __get__(self, instance, owner):
        if instance is None:

            async def class_call(
                sandbox_name: str,
                *,
                wait: bool = True,
                max_wait: int = ARCHIVE_MAX_WAIT_MS,
                interval: int = ARCHIVE_WAIT_POLL_MS,
            ) -> "SandboxInstance":
                return SandboxInstance(await self._call(sandbox_name, wait, max_wait, interval))

            class_call.__doc__ = self.__doc__
            return class_call

        async def instance_call(
            *,
            wait: bool = True,
            max_wait: int = ARCHIVE_MAX_WAIT_MS,
            interval: int = ARCHIVE_WAIT_POLL_MS,
        ) -> "SandboxInstance":
            instance.sandbox = await self._call(instance.metadata.name, wait, max_wait, interval)
            instance.config.sandbox = instance.sandbox
            return instance

        instance_call.__doc__ = self.__doc__
        return instance_call


class SandboxInstance:
    """A Blaxel sandbox and the async clients that work inside it.

    Get an instance from :meth:`create`, :meth:`create_if_not_exists`,
    :meth:`get`, :meth:`list` or :meth:`from_session` rather than calling the
    constructor. The instance holds the sandbox record as it was when it was
    read; it is not refreshed on its own, so call :meth:`get` again to read the
    current status. For blocking code, use ``SyncSandboxInstance``, which has
    the same methods without ``await``.

    Attributes:
        sandbox: The ``Sandbox`` record returned by the API.
        config: The record plus the URL and headers used to reach the sandbox.
        process: Runs commands and reads their output (``SandboxProcess``).
        fs: Reads, writes, searches and watches files (``SandboxFileSystem``).
        previews: Exposes sandbox ports on public or private URLs
            (``SandboxPreviews``).
        sessions: Creates short-lived URLs and tokens for clients that must not
            hold an API key (``SandboxSessions``).
        schedules: Manages the sandbox's schedules (``SandboxSchedules``).
        network: Sends HTTP requests to ports inside the sandbox
            (``SandboxNetwork``).
        codegen: Applies code edits and ranks files (``SandboxCodegen``).
        system: Reads health and upgrades the sandbox API (``SandboxSystem``).
        drives: Mounts and unmounts drives (``SandboxDrive``).
        snapshots: Creates and restores snapshots (``SandboxSnapshots``).

    Example:
        ```python
        from blaxel.core import SandboxInstance

        sandbox = await SandboxInstance.create_if_not_exists(
            {"name": "my-sandbox", "image": "blaxel/base-image:latest", "region": "us-pdx-1"}
        )
        result = await sandbox.process.exec({"command": "echo hello", "wait_for_completion": True})
        print(result.status, result.exit_code, result.stdout)
        ```
    """

    delete: "_AsyncDeleteDescriptor"
    archive: "_AsyncSandboxCallDescriptor"
    unarchive: "_AsyncSandboxCallDescriptor"

    def __init__(
        self,
        sandbox: Union[Sandbox, SandboxConfiguration],
        force_url: str | None = None,
        headers: Dict[str, str] | None = None,
        params: Dict[str, str] | None = None,
    ):
        # Handle both Sandbox and SandboxConfiguration inputs
        if isinstance(sandbox, SandboxConfiguration):
            self.config = sandbox
            self.sandbox = sandbox.sandbox
        else:
            # Create SandboxConfiguration with optional parameters
            self.sandbox = sandbox
            self.config = SandboxConfiguration(
                sandbox=sandbox,
                force_url=force_url,
                headers=headers,
                params=params,
            )

        self.process = SandboxProcess(self.config)
        self.fs = SandboxFileSystem(self.config, self.process)
        self.previews = SandboxPreviews(self.sandbox)
        self.schedules = SandboxSchedules(self.sandbox)
        self.sessions = SandboxSessions(self.config)
        self.network = SandboxNetwork(self.config)
        self.codegen = SandboxCodegen(self.config)
        self.system = SandboxSystem(self.config)
        self.drives = SandboxDrive(self.config)
        self.snapshots = SandboxSnapshots(self.sandbox, _unwrap_response)

    @property
    def metadata(self):
        """The sandbox metadata: ``name``, ``display_name``, ``labels``, ``url`` and more."""
        return self.sandbox.metadata

    @property
    def status(self):
        """The sandbox status when the record was read, such as ``DEPLOYED`` or ``FAILED``.

        It is not refreshed on its own: call :meth:`get` to read the current status.
        """
        return self.sandbox.status

    @property
    def events(self):
        """The events the platform recorded for this sandbox."""
        return self.sandbox.events

    @property
    def spec(self):
        """The sandbox spec as last read.

        It holds ``runtime`` (image, memory, ports, envs, ttl), ``region``,
        ``lifecycle``, ``network`` and ``volumes``.
        """
        return self.sandbox.spec

    @property
    def errors(self) -> list[SandboxInfrastructureError]:
        """Infrastructure failures the compute plane recorded for this sandbox, oldest first.

        Entries with ``fatal`` set are the ones that moved the sandbox to FAILED; the
        others (e.g. a microVM that exited and restarted) are informational. Only
        returned when a single sandbox is read, never in listings.
        """
        errors = self.sandbox.errors
        return list(errors) if not isinstance(errors, Unset) and errors else []

    @property
    def last_used_at(self):
        """When the sandbox was last used, as reported by the API."""
        return self.sandbox.last_used_at

    @property
    def expires_in(self):
        """Time left before a lifecycle or TTL rule deletes the sandbox, as reported by the API."""
        return self.sandbox.expires_in

    async def fetch(
        self, port: int, path: str = "/", method: str = "GET", **kwargs
    ) -> "httpx.Response":
        """Fetch a resource served on a sandbox port.

        The request goes through the sandbox API (``/port/{port}``) with this
        instance's credentials, so the port does not need a preview. HTTP error
        statuses are returned in the response, not raised.

        Args:
            port: The port number inside the sandbox
            path: Optional path appended after the port (default: "/")
            method: HTTP method (default: "GET")
            **kwargs: Additional arguments forwarded to httpx (e.g. headers, content)

        Returns:
            The ``httpx.Response`` from the service listening on the port.

        Example:
            ```python
            response = await sandbox.fetch(3000, "/health")
            print(response.status_code, response.text)
            ```
        """
        return await self.network.fetch(port, path, method, **kwargs)

    async def snapshot(self, name: str | None = None) -> SandboxSnapshot:
        """Create a point-in-time snapshot of this sandbox.

        Snapshots capture the sandbox state and can be forked into new sandboxes
        or applications.

        Args:
            name: Optional human-readable name for the snapshot.

        .. deprecated:: Use ``sandbox.snapshots.create(name)``.
        """
        body = SandboxSnapshotRequest(name=name) if name is not None else SandboxSnapshotRequest()
        response = await create_sandbox_snapshot(
            self.metadata.name,
            client=client,
            body=body,
        )
        return _unwrap_response(response, "create snapshot")

    async def list_snapshots(self) -> list[SandboxSnapshot]:
        """List the snapshots of this sandbox.

        .. deprecated:: Use ``sandbox.snapshots.list()``.
        """
        response = await list_sandbox_snapshots(
            self.metadata.name,
            client=client,
        )
        return _unwrap_response(response, "list snapshots")

    async def delete_snapshot(self, snapshot_id: str) -> None:
        """Delete a snapshot of this sandbox by its ID.

        .. deprecated:: Use ``sandbox.snapshots.delete(name)``.
        """
        response = await delete_sandbox_snapshot(
            self.metadata.name,
            snapshot_id,
            client=client,
        )
        _unwrap_response(response, "delete snapshot", allow_none=True)

    async def restore(self, snapshot_id: str) -> SandboxRestoreResponse:
        """Restore this sandbox to one of its own snapshots.

        The sandbox keeps its name, its URLs and its previews: the running
        instance is torn down and rebuilt from the snapshot, so everything
        written since the snapshot was taken is lost unless it was snapshotted
        too.

        The restore is asked for without waiting on the instance, the same way a
        fork is: connections to a sandbox still resuming are retried.

        Args:
            snapshot_id: ID of the snapshot to restore this sandbox to.

        .. deprecated:: Use ``sandbox.snapshots.restore(name)``.
        """
        response = await restore_sandbox_snapshot(
            self.metadata.name,
            snapshot_id,
            client=client,
        )
        return _unwrap_response(response, "restore snapshot")

    async def fork(
        self,
        target_name: str,
        *,
        target_type: str = "sandbox",
        port: int | None = None,
        traffic: int | None = None,
        custom_domain: str | None = None,
        prefix: str | None = None,
        snapshot_id: str | None = None,
        envs: list[Env] | None = None,
        lifecycle: SandboxLifecycle | Dict[str, Any] | None = None,
    ) -> SandboxForkResponse:
        """Fork this sandbox into a new sandbox or application.

        Forking into a sandbox copies this sandbox's live state straight into
        the fork: no snapshot is created, persisted, or listed under this
        sandbox. Pass ``snapshot_id`` to fork from a snapshot taken earlier
        instead. Forking into an application still goes through a snapshot,
        which the application's revision references so that revision can be
        re-activated later.

        Args:
            target_name: Name of the sandbox/application to create.
            target_type: Resource type to fork into ("sandbox" or "application").
            port: Port to expose from the fork.
            traffic: Canary traffic percentage (0-100) for an application fork.
            custom_domain: Custom domain for an application fork.
            prefix: URL prefix for an application fork.
            snapshot_id: Snapshot ID to fork from, instead of this sandbox's
                live state.
            envs: Environment variables the fork runs with, on top of the ones
                the source has: a variable the source already carries takes this
                value in the fork, one it does not is added, and every other
                variable of the source is kept.
            lifecycle: Lifecycle the fork runs with, replacing the source's.
                When omitted, a sandbox fork keeps the source's lifecycle and
                its runtime ttl and expires. Only valid for a sandbox fork.

        Returns:
            The ``SandboxForkResponse`` describing the new resource. Call
            ``SandboxInstance.get(target_name)`` to work with a sandbox fork.

        Raises:
            SandboxAPIError: When the API rejects the fork.
        """
        body = SandboxForkRequest(target_name=target_name, target_type=target_type)
        if port is not None:
            body.port = port
        if traffic is not None:
            body.traffic = traffic
        if custom_domain is not None:
            body.custom_domain = custom_domain
        if prefix is not None:
            body.prefix = prefix
        if snapshot_id is not None:
            body.snapshot_id = snapshot_id
        if envs is not None:
            body.envs = envs
        if lifecycle is not None:
            if isinstance(lifecycle, dict):
                lifecycle = SandboxLifecycle.from_dict(lifecycle) or SandboxLifecycle()
            body.additional_properties["lifecycle"] = lifecycle.to_dict()
        response = await fork_sandbox(
            self.metadata.name,
            client=client,
            body=body,
        )
        return _unwrap_response(response, "fork sandbox")

    async def wait(self, max_wait: int = 60000, interval: int = 1000) -> "SandboxInstance":
        """Return this instance right away; kept for compatibility.

        A sandbox returned by :meth:`create` is ready to use, so there is
        nothing to wait for. Both arguments are ignored and a deprecation
        warning is logged.

        .. deprecated:: Remove the call.
        """
        logger.warning(
            "⚠️  Warning: sandbox.wait() is deprecated. You don't need to wait for the sandbox to be deployed anymore."
        )
        return self

    @classmethod
    async def create(
        cls,
        sandbox: Union[Sandbox, SandboxCreateConfiguration, Dict[str, Any], None] = None,
        safe: bool = False,
        create_if_not_exist: bool = False,
        timeout: int | None = None,
        *,
        mount_drives: "list[SandboxDriveMountConfiguration | dict] | None" = None,
    ) -> "SandboxInstance":
        """Create a sandbox and return it once it is ready to use.

        Missing settings get defaults: image ``blaxel/base-image:latest`` and
        4096 MB of memory. Creating a name that is already taken fails with
        HTTP 409; use :meth:`create_if_not_exists` to reuse the sandbox instead.

        Lifetime: ``ttl`` deletes the sandbox that long after it is created, and
        ``lifecycle`` holds expiration policies of type ``ttl-idle`` (after that
        long without activity), ``ttl-max-age`` (after that long in total) or
        ``date`` (at an ISO 8601 date), each with action ``"delete"``. Durations
        are a number followed by ``s``, ``m``, ``h``, ``d`` or ``w``, such as
        ``"30m"`` or ``"7d"``. ``ttl`` and ``ttl-max-age`` must be at least
        ``5m`` and ``ttl-idle`` at least ``60s``; shorter values get HTTP 400.
        Recipes: https://docs.blaxel.ai/Sandboxes/Lifecycle-recipe

        A creation rejected by a transient authentication failure (403
        ``UNAUTHORIZED`` or 503 ``AUTHENTICATION_UNAVAILABLE``, both answered
        before anything is created) is sent again up to ``CREATE_AUTH_RETRIES``
        times with a short backoff.

        Args:
            sandbox: The sandbox to create: a ``SandboxCreateConfiguration``, a
                dict with the same keys (``name``, ``image``, ``memory`` in MB,
                ``ports``, ``envs``, ``volumes``, ``ttl``, ``expires``,
                ``region``, ``lifecycle``, ``network``, ``labels``, ...), or a
                full ``Sandbox`` model. Its name must use lowercase letters,
                digits and single hyphens, at most ``SANDBOX_NAME_MAX_LENGTH``
                (49) characters, like ``my-sandbox-1``. The API rejects any other
                name with a 400, and the SDK never renames it for you: to name a
                sandbox after an external id such as ``sesn_01AbC``, pass the id
                through ``sanitize_sandbox_name`` first (``is_valid_sandbox_name``
                checks a name). Omit the name to let the platform assign one.
                Without a region (here or in ``BL_REGION``) the platform picks
                one and a ``FutureWarning`` is shown once per process.
            safe: When True, make one filesystem call after creation so the
                sandbox API answers before this returns. Errors from that call
                are ignored.
            create_if_not_exist: Prefer :meth:`create_if_not_exists`, which sets
                this flag.
            mount_drives: Drives to mount on the sandbox. Drives are looked up or created
                while the sandbox is being created (a few at a time) and each is mounted
                as soon as the sandbox and that drive are ready. New drives go in the region
                the request sends (or, without one, the region the sandbox gets). On failure
                (cancellation included), unnamed drives this call created and did not mount
                are deleted; named ones are kept (a concurrent call may be using them) and
                listed in the error. If drive setup fails the sandbox is kept and
                SandboxDriveSetupError is raised; if the sandbox cannot be created, its
                error is raised (wrapped in a SandboxDriveSetupError only if a drive
                created for it is left in place).
            timeout: Optional creation deadline in whole seconds (1 to
                ``MAX_CREATION_TIMEOUT_SECONDS``). When the sandbox is not ready
                in time the control plane cancels the creation, releases the
                sandbox and ``SandboxCreationTimeoutError`` is raised. Omitted, the
                platform default deadline applies; an explicit value can only
                shorten it.

        Returns:
            The new ``SandboxInstance``.

        Raises:
            ValueError: When ``timeout`` is out of range, or ``lifecycle`` has an
                unknown policy type or action (checked before any request).
            SandboxCreationTimeoutError: When the sandbox was not ready before
                the deadline.
            SandboxAPIError: When the API rejects the creation, for example
                HTTP 400 for an invalid name or lifecycle value, or HTTP 409 for
                a name already in use. ``status_code`` and ``code`` carry the
                details.
            blaxel.core.client.errors.QuotaExceededError: HTTP 429
                QUOTA_EXCEEDED. Not retryable until usage drops or the quota is
                raised; it is not a RateLimitError.
            blaxel.core.client.errors.RateLimitError: HTTP 429 rate limit
                (WORKSPACE_RATE_LIMIT_EXCEEDED or RATE_LIMIT_EXCEEDED).
                ``retryable`` is True; ``retry_after_seconds`` says how long
                to wait when the server says.
            blaxel.core.client.errors.UnexpectedStatus: For a status the API
                does not document for this call.

        Example:
            ```python
            sandbox = await SandboxInstance.create(
                {
                    "name": "my-sandbox",
                    "image": "blaxel/base-image:latest",
                    "memory": 4096,
                    "region": "us-pdx-1",
                    "lifecycle": {
                        "expiration_policies": [
                            {"type": "ttl-idle", "value": "30m", "action": "delete"}
                        ]
                    },
                }
            )
            ```
        """
        mounts = _normalize_mount_drives(mount_drives, create_if_not_exist)
        timeout = _validate_creation_timeout(timeout)
        # No client-side default name: when the caller omits a name we send the
        # creation without metadata.name so the server can assign one and unnamed
        # creations become eligible for warm sandbox pools (ENG-3931).
        default_image = "blaxel/base-image:latest"
        default_memory = 4096

        # Handle SandboxCreateConfiguration or simple dict with name/image/memory/ports/envs/volumes keys
        if (
            sandbox is None
            or isinstance(sandbox, SandboxCreateConfiguration | dict)
            and (
                not isinstance(sandbox, Sandbox)
                and (
                    sandbox is None
                    or "name" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "image" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "memory" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "ports" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "envs" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "volumes" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "ttl" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "expires" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "region" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "lifecycle" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "network" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "snapshot_enabled"
                    in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "labels" in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "termination_grace_period_seconds"
                    in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                    or "standby_grace_period_seconds"
                    in (sandbox if isinstance(sandbox, dict) else sandbox.__dict__)
                )
            )
        ):
            config: SandboxCreateConfiguration
            if sandbox is None:
                config = SandboxCreateConfiguration()
            elif isinstance(sandbox, dict) and not isinstance(sandbox, Sandbox):
                config = SandboxCreateConfiguration.from_dict(sandbox)
            elif isinstance(sandbox, SandboxCreateConfiguration):
                config = sandbox
            else:
                raise ValueError(f"Unexpected sandbox type: {type(sandbox)}")

            # Set defaults if not provided
            name = config.name
            image = config.image or default_image
            memory = config.memory or default_memory
            ports = config._normalize_ports() or UNSET
            envs = config._normalize_envs() or UNSET
            volumes = config._normalize_volumes() or UNSET
            ttl = config.ttl
            expires = config.expires
            region = config.region or settings.region
            # What the caller asked for, read before the defaults above fill the gaps:
            # create_if_not_exists compares only these with the sandbox it gets back.
            requested = RequestedSandbox(
                image=config.image,
                memory=config.memory,
                region=config.region,
                envs=config._normalize_envs(),
            )
            if not region:
                _notify_region_unset()
            lifecycle = config.lifecycle
            network = config.network
            snapshot_enabled = config.snapshot_enabled
            extra_args = config.extra_args

            labels = MetadataLabels.from_dict(config.labels) if config.labels else UNSET
            if labels is None:
                labels = UNSET

            # Create full Sandbox object
            sandbox = Sandbox(
                metadata=Metadata(name=name, labels=labels),
                spec=SandboxSpec(
                    runtime=SandboxRuntime(
                        image=image,
                        memory=memory,
                        ports=ports,
                        envs=envs,
                    ),
                    volumes=volumes,
                ),
            )

            # Set ttl and expires if provided
            if ttl and sandbox.spec.runtime:
                sandbox.spec.runtime.ttl = ttl
            if expires and sandbox.spec.runtime:
                sandbox.spec.runtime.expires = expires.isoformat()
            if config.termination_grace_period_seconds is not None and sandbox.spec.runtime:
                sandbox.spec.runtime.termination_grace_period_seconds = (
                    config.termination_grace_period_seconds
                )
            if config.standby_grace_period_seconds is not None and sandbox.spec.runtime:
                sandbox.spec.runtime.standby_grace_period_seconds = (
                    config.standby_grace_period_seconds
                )
            if region:
                sandbox.spec.region = region
            if lifecycle:
                if type(lifecycle) is dict:
                    lifecycle = SandboxLifecycle.from_dict(lifecycle)
                    assert lifecycle is not None
                    sandbox.spec.lifecycle = lifecycle
                elif type(lifecycle) is SandboxLifecycle:
                    sandbox.spec.lifecycle = lifecycle
                else:
                    raise ValueError(f"Invalid lifecycle type: {type(lifecycle)}")
            if network:
                if isinstance(network, dict):
                    network = SandboxNetworkModel.from_dict(network)
                    assert network is not None
                sandbox.spec.network = network
            if snapshot_enabled is not None and sandbox.spec.runtime:
                sandbox.spec.runtime["snapshotEnabled"] = snapshot_enabled
            if extra_args and sandbox.spec.runtime:
                ea = SandboxRuntimeExtraArgs()
                ea.additional_properties = extra_args
                sandbox.spec.runtime.extra_args = ea
            if config.docker_config and sandbox.spec.runtime:
                # Not in the generated model: sent as an additional property.
                sandbox.spec.runtime["dockerConfig"] = config.docker_config
        else:
            # Handle existing Sandbox object or dict conversion
            if isinstance(sandbox, dict):
                sandbox = Sandbox.from_dict(sandbox)
                assert sandbox is not None

            assert isinstance(sandbox, Sandbox)
            requested = requested_from_model(sandbox)
            # Set defaults for missing fields
            if not sandbox.metadata:
                sandbox.metadata = Metadata(name=None)
            if not sandbox.spec:
                sandbox.spec = SandboxSpec(
                    runtime=SandboxRuntime(image=default_image, memory=default_memory)
                )
            if not sandbox.spec.runtime:
                sandbox.spec.runtime = SandboxRuntime(image=default_image, memory=default_memory)

            sandbox.spec.runtime.image = sandbox.spec.runtime.image or default_image
            sandbox.spec.runtime.memory = sandbox.spec.runtime.memory or default_memory

        drives = None
        if mounts:
            # Drives are set up alongside the sandbox, in the region this request sends (if it
            # sends none, the control plane picks one and new drives wait for the sandbox).
            drives = _AsyncDriveSetup(mounts, _requested_region(sandbox.spec.region))
            drives.start()
        try:
            body = _create_body(sandbox)
            attempts = 0
            while True:
                attempts += 1
                try:
                    if timeout is None:
                        response = await create_sandbox(
                            client=client, body=body, create_if_not_exist=create_if_not_exist
                        )
                    else:
                        async with _creation_client(timeout) as creation_client:
                            response = await create_sandbox(
                                client=creation_client,
                                body=body,
                                create_if_not_exist=create_if_not_exist,
                            )
                except client_errors.UnexpectedStatus as e:
                    _raise_if_creation_timeout(e, _sandbox_name(sandbox), timeout)
                    if attempts > CREATE_AUTH_RETRIES or not _is_transient_create_auth_failure(e):
                        _explain_create_error(e)
                        raise
                else:
                    if attempts > CREATE_AUTH_RETRIES or not _is_transient_create_auth_failure(
                        response
                    ):
                        break
                logger.debug("Sandbox creation hit a transient authentication failure, retrying")
                await asyncio.sleep(_create_auth_retry_delay(attempts))

            # Check if response is an error
            if isinstance(response, SandboxError):
                _raise_if_creation_timeout(response, _sandbox_name(sandbox), timeout)
                raise _create_error(response, _sandbox_name(sandbox), attempts)

            assert response is not None
            if create_if_not_exist:
                # The sandbox already holding the name comes back as is, whatever it was
                # created with. Say so when it is not what was asked for; only a warning.
                drift = drift_message(requested, response)
                if drift:
                    warnings.warn(drift, stacklevel=caller_stacklevel())
            instance = cls(response)
            # TODO remove this part once we have a better way to handle this
            if safe:
                try:
                    await instance.fs.ls("/")
                except Exception:
                    pass
        except BaseException as error:
            if drives is not None:
                left_behind = await drives.discard(error)
                # Only when a drive created for the sandbox is left in place.
                if left_behind is not None and isinstance(error, Exception):
                    raise left_behind from error
            raise
        if drives is not None:
            await drives.mount(instance)
        return instance

    @classmethod
    async def get(cls, sandbox_name: str) -> "SandboxInstance":
        """Read an existing sandbox by name.

        Use it to reconnect to a sandbox created earlier, or to refresh the
        status of an instance you already hold.

        Args:
            sandbox_name: The sandbox name.

        Returns:
            A ``SandboxInstance`` with the current record.

        Raises:
            SandboxAPIError: When the sandbox does not exist (``status_code``
                404) or the API rejects the request. A deleted sandbox is
                still returned, with status ``TERMINATED``, until its
                ``terminated_retention`` (5 minutes by default) has passed.

        Example:
            ```python
            sandbox = await SandboxInstance.get("my-sandbox")
            print(sandbox.status)
            ```
        """
        response = await get_sandbox(
            sandbox_name,
            client=client,
        )

        # Check if response is an error
        if isinstance(response, Error):
            status_code = response.code if response.code is not UNSET else None
            message = response.message if response.message is not UNSET else response.error
            raise SandboxAPIError(
                message, status_code=status_code, code=response.error, error=response
            )

        if response is None:
            raise SandboxAPIError(f"Sandbox '{sandbox_name}' not found", status_code=404)

        return cls(response)

    @classmethod
    async def list(
        cls, limit: int = 50, cursor: str | None = None
    ) -> AsyncPaginatedList["SandboxInstance"]:
        """List one page of sandboxes.

        Args:
            limit: Maximum number of sandboxes to return in this page.
            cursor: Cursor from a previous page. Leave unset for the first page.

        Returns:
            AsyncPaginatedList[SandboxInstance]: A list-like page with `.data`, `.meta`,
            `.has_more`, `.next_cursor`, `.next_page()`, and `.auto_paging_iter()`.

        Raises:
            SandboxAPIError: When the API rejects the request.

        Example:
            ```python
            page = await SandboxInstance.list(limit=50)

            for sandbox in page.data:
                print(sandbox.metadata.name)

            if page.has_more:
                next_page = await page.next_page()

            async for sandbox in page.auto_paging_iter():
                print(sandbox.metadata.name)
            ```
        """

        async def fetch_page(page_cursor: str | None):
            response = await list_sandboxes(
                client=client,
                cursor=normalize_cursor(page_cursor),
                limit=limit,
            )
            if isinstance(response, Error):
                status_code = response.code if response.code is not UNSET else None
                message = response.message if response.message is not UNSET else response.error
                raise SandboxAPIError(
                    message, status_code=status_code, code=response.error, error=response
                )
            return make_async_paginated_list(response, mapper=cls, fetch_next=fetch_page)

        return await fetch_page(cursor)

    @classmethod
    async def update_metadata(
        cls, sandbox_name: str, metadata: SandboxUpdateMetadata
    ) -> "SandboxInstance":
        """Update sandbox metadata by merging new metadata with existing metadata.

        The sandbox is read first, then written back with the changes. Given
        labels are added to the existing ones (a label with the same key is
        replaced); no label is removed. The sandbox keeps running.

        Args:
            sandbox_name: The name of the sandbox to update
            metadata: The metadata fields to update (labels and/or display_name)

        Returns:
            A new SandboxInstance with updated metadata

        Raises:
            SandboxAPIError: When the sandbox does not exist or the API rejects
                the update.

        Example:
            ```python
            from blaxel.core.sandbox.types import SandboxUpdateMetadata

            sandbox = await SandboxInstance.update_metadata(
                "my-sandbox", SandboxUpdateMetadata(labels={"team": "data"})
            )
            ```
        """
        # Get the existing sandbox
        sandbox_instance = await cls.get(sandbox_name)
        sandbox = sandbox_instance.sandbox

        # Prepare the updated sandbox object
        updated_sandbox = Sandbox.from_dict(sandbox.to_dict())
        if updated_sandbox is None:
            raise ValueError(f"Sandbox {sandbox_name} not found")

        # Merge metadata
        if updated_sandbox.metadata is None:
            updated_sandbox.metadata = Metadata(name=sandbox_name)

        # Update labels if provided
        if metadata.labels is not None:
            # Handle UNSET or None labels
            if updated_sandbox.metadata.labels is None or updated_sandbox.metadata.labels is UNSET:
                updated_sandbox.metadata.labels = {}
            else:
                # If labels exist, convert to dict (MetadataLabels stores in additional_properties)
                if hasattr(updated_sandbox.metadata.labels, "to_dict"):
                    updated_sandbox.metadata.labels = updated_sandbox.metadata.labels.to_dict()
                else:
                    updated_sandbox.metadata.labels = dict(updated_sandbox.metadata.labels)
            updated_sandbox.metadata.labels.update(metadata.labels)

        # Update display_name if provided
        if metadata.display_name is not None:
            updated_sandbox.metadata.display_name = metadata.display_name

        # Call the update API
        response = await update_sandbox(
            sandbox_name=sandbox_name,
            client=client,
            body=updated_sandbox,
        )

        # Return new instance with updated sandbox
        return cls(_unwrap_response(response, "update sandbox metadata"))

    @classmethod
    async def update_ttl(cls, sandbox_name: str, ttl: str | None) -> "SandboxInstance":
        """Update sandbox TTL without recreating it.

        The TTL counts from the sandbox creation, not from this call: a sandbox
        created two hours ago and given ``"1h"`` is deleted soon after. To
        delete after a period without activity, use :meth:`update_lifecycle`
        with a ``ttl-idle`` policy. Recipes:
        https://docs.blaxel.ai/Sandboxes/Lifecycle-recipe

        Args:
            sandbox_name: The name of the sandbox to update
            ttl: The new TTL value (e.g., "5m", "1h"; minimum 5m), or None/"" to clear.
                Units are ``s``, ``m``, ``h``, ``d`` or ``w``.

        Returns:
            A new SandboxInstance with updated TTL

        Raises:
            SandboxAPIError: When the sandbox does not exist, or with HTTP 400
                when the value is malformed or shorter than 5m.

        Example:
            ```python
            sandbox = await SandboxInstance.update_ttl("my-sandbox", "24h")
            ```
        """
        # Get the existing sandbox
        sandbox_instance = await cls.get(sandbox_name)
        sandbox = sandbox_instance.sandbox

        # Prepare the updated sandbox object
        updated_sandbox = Sandbox.from_dict(sandbox.to_dict())
        if updated_sandbox.spec is None or updated_sandbox.spec.runtime is None:
            raise ValueError(f"Sandbox {sandbox_name} has invalid spec")

        # Update TTL (None or empty string clears the TTL)
        updated_sandbox.spec.runtime.ttl = None if ttl is None or ttl == "" else ttl

        # Call the update API
        response = await update_sandbox(
            sandbox_name=sandbox_name,
            client=client,
            body=updated_sandbox,
        )

        return cls(_unwrap_response(response, "update sandbox TTL"))

    @classmethod
    async def update_lifecycle(
        cls, sandbox_name: str, lifecycle: SandboxLifecycle | None
    ) -> "SandboxInstance":
        """Update sandbox lifecycle configuration without recreating it.

        The given lifecycle replaces the current one as a whole, so include
        every policy you want to keep. Each expiration policy has a ``type``
        (``ttl-idle``, ``ttl-max-age`` or ``date``), a ``value`` and the action
        ``"delete"``. Durations use ``s``, ``m``, ``h``, ``d`` or ``w``;
        ``ttl-idle`` must be at least ``60s`` and ``ttl-max-age`` at least
        ``5m``. Recipes: https://docs.blaxel.ai/Sandboxes/Lifecycle-recipe

        Args:
            sandbox_name: The name of the sandbox to update
            lifecycle: The new lifecycle configuration, or None to clear

        Returns:
            A new SandboxInstance with updated lifecycle

        Raises:
            SandboxAPIError: When the sandbox does not exist, or with HTTP 400
                when a value is malformed or below its minimum.

        Example:
            ```python
            from blaxel.core.client.models import SandboxLifecycle

            lifecycle = SandboxLifecycle.from_dict(
                {"expiration_policies": [{"type": "ttl-idle", "value": "30m", "action": "delete"}]}
            )
            sandbox = await SandboxInstance.update_lifecycle("my-sandbox", lifecycle)
            ```
        """
        # Get the existing sandbox
        sandbox_instance = await cls.get(sandbox_name)
        sandbox = sandbox_instance.sandbox

        # Use dict approach to properly serialize null lifecycle
        body = sandbox.to_dict()
        if "spec" not in body:
            raise ValueError(f"Sandbox {sandbox_name} has invalid spec")
        body["spec"]["lifecycle"] = lifecycle.to_dict() if lifecycle is not None else None

        # Call the update API
        response = await update_sandbox(
            sandbox_name=sandbox_name,
            client=client,
            body=body,
        )

        return cls(_unwrap_response(response, "update sandbox lifecycle"))

    @classmethod
    async def update_network(
        cls, sandbox_name: str, network: SandboxUpdateNetwork
    ) -> "SandboxInstance":
        """Update sandbox network configuration without recreating it.

        The given network configuration replaces the current one. A
        ``SandboxUpdateNetwork`` whose ``network`` is None sends the update
        without a ``network`` field.

        Args:
            sandbox_name: The name of the sandbox to update
            network: The new network configuration

        Returns:
            A new SandboxInstance with updated network configuration

        Raises:
            SandboxAPIError: When the sandbox does not exist or the API rejects
                the configuration.
        """
        sandbox_instance = await cls.get(sandbox_name)
        sandbox = sandbox_instance.sandbox

        updated_sandbox = Sandbox.from_dict(sandbox.to_dict())
        if updated_sandbox.spec is None:
            raise ValueError(f"Sandbox {sandbox_name} has invalid spec")

        if network.network is not None:
            if isinstance(network.network, dict):
                updated_sandbox.spec.network = SandboxNetworkModel.from_dict(network.network)
            else:
                updated_sandbox.spec.network = network.network
        else:
            updated_sandbox.spec.network = UNSET

        response = await update_sandbox(
            sandbox_name=sandbox_name,
            client=client,
            body=updated_sandbox,
        )

        return cls(_unwrap_response(response, "update sandbox network"))

    @classmethod
    async def create_if_not_exists(
        cls,
        sandbox: Union[Sandbox, SandboxCreateConfiguration, Dict[str, Any]],
        timeout: int | None = None,
        *,
        mount_drives: "list[SandboxDriveMountConfiguration | dict] | None" = None,
    ) -> "SandboxInstance":
        """Create the sandbox, or return the one already holding this name.

        ``timeout`` and ``mount_drives`` are forwarded to :meth:`create`.

        The control plane owns the reconciliation: an alive sandbox is returned as
        is, a FAILED/TERMINATED one is replaced, and a deletion or concurrent
        creation still in flight is waited for server-side. A 409 therefore only
        surfaces when the name really cannot be used, and is raised as is.

        A live sandbox is reused as it is, including one in standby: the
        requested image, memory, region, envs and other settings are not
        applied to it. When the image, memory, region or envs you set differ
        from the sandbox returned, a ``UserWarning`` names the differences;
        delete and create again to change them. Without a name in ``sandbox`` this always
        creates a new sandbox. Name rules, defaults and lifetime settings are
        the same as for :meth:`create`; recipes:
        https://docs.blaxel.ai/Sandboxes/Lifecycle-recipe

        Args:
            sandbox: The sandbox to create, in any form :meth:`create` accepts.
                Give it a name so a second call finds the same sandbox.
            timeout: Optional creation deadline in whole seconds, as in
                :meth:`create`.

        Returns:
            The existing or new ``SandboxInstance``.

        Raises:
            ValueError: When ``timeout`` or ``lifecycle`` is invalid.
            SandboxCreationTimeoutError: When a new sandbox was not ready before
                the deadline.
            SandboxAPIError: When the API rejects the request, for example
                HTTP 400 for an invalid name.

        Example:
            ```python
            sandbox = await SandboxInstance.create_if_not_exists(
                {"name": "agent-workspace", "region": "us-pdx-1"}
            )
            ```
        """
        create_kwargs: Dict[str, Any] = {} if timeout is None else {"timeout": timeout}
        if mount_drives is not None:
            create_kwargs["mount_drives"] = mount_drives
        return await cls.create(sandbox, create_if_not_exist=True, **create_kwargs)

    @classmethod
    async def from_session(
        cls, session: Union[SessionWithToken, Dict[str, Any]]
    ) -> "SandboxInstance":
        """Create a sandbox instance from a session with token.

        Use it where the code must not hold a Blaxel API key, such as a browser
        backend or a separate service: create the session with an API key
        elsewhere (``sandbox.sessions.create()``) and pass it here. The
        instance reaches the sandbox through the session URL with the session
        token, so these calls work without an API key until the token
        expires: ``fs.read``, ``fs.write`` (up to 5 MB), ``fs.ls``,
        ``fs.mkdir``, ``fs.rm``, ``process.exec``, ``process.get`` and
        ``process.kill``. Other helpers, such as ``fs.read_binary``,
        ``fs.write_binary``, ``fs.find``, ``fs.grep``, ``fs.watch`` and log
        streaming, still read Blaxel credentials in this version and raise
        ``CredentialsError`` without them. Its ``metadata.name`` is derived
        from the session name, not read from the API: do not call
        control-plane methods (``previews``, ``sessions``, ``update_*``,
        ``delete``) on it.

        Args:
            session: A ``SessionWithToken``, or a dict with ``name``, ``url``,
                ``token`` and ``expires_at``.

        Returns:
            A ``SandboxInstance`` bound to the session URL and token. No request
            is made.

        Example:
            ```python
            session = await sandbox.sessions.create()
            remote = await SandboxInstance.from_session(session)
            await remote.fs.write("/tmp/hello.txt", "hi")
            ```
        """
        if isinstance(session, dict):
            session = SessionWithToken.from_dict(session)

        # Create a minimal sandbox configuration for session-based access
        sandbox_name = session.name.split("-")[0] if "-" in session.name else session.name
        sandbox = Sandbox(metadata=Metadata(name=sandbox_name), spec=SandboxSpec())

        # Authenticate with the preview token header only. The bl_preview_token
        # query-param transport exists for browser navigation (which cannot set
        # custom headers); on this programmatic client it would only place the
        # credential in request URLs where it leaks to logs, Referer, and history.
        return cls(
            sandbox=sandbox,
            force_url=session.url,
            headers={"X-Blaxel-Preview-Token": session.token},
        )


async def _delete_sandbox_by_name(sandbox_name: str) -> Sandbox:
    """Delete a sandbox by name.

    Exposed as ``await SandboxInstance.delete("name")`` and as
    ``await sandbox.delete()`` on an instance. The sandbox, its processes and
    its filesystem are removed; persistent volumes and drives attached to it
    are separate resources and are not deleted. The deletion finishes in the
    background, and the name can be reused once it is done. The record stays
    readable for the lifecycle's ``terminated_retention`` (5 minutes by
    default): ``get`` returns it with status ``TERMINATED`` instead of raising
    a 404, and ``list`` no longer includes it. To confirm a deletion, check
    for ``TERMINATED`` or for the name to leave ``list``.

    Args:
        sandbox_name: The sandbox name.

    Returns:
        The ``Sandbox`` record as the API returned it for the deletion.

    Raises:
        SandboxAPIError: When the sandbox does not exist (``status_code`` 404)
            or the API rejects the request.
    """
    response = await delete_sandbox(
        sandbox_name,
        client=client,
    )
    return _unwrap_response(response, f"delete sandbox {sandbox_name}")


async def _archive_sandbox_by_name(sandbox_name: str):
    return await archive_sandbox(sandbox_name, client=client)


async def _unarchive_sandbox_by_name(sandbox_name: str):
    return await unarchive_sandbox(sandbox_name, client=client)


# Assign the delete descriptor to support both class-level and instance-level calls
SandboxInstance.delete = _AsyncDeleteDescriptor(_delete_sandbox_by_name)
SandboxInstance.archive = _AsyncSandboxCallDescriptor(
    _archive_sandbox_by_name,
    "archive",
    "ARCHIVED",
    ARCHIVING_STATUSES,
    ARCHIVE_ENTRY_STATUS,
    """Archive a sandbox: keep its filesystem, stop the sandbox.

    The filesystem changes made over the image are exported to the archive store
    and the sandbox is shut down; memory and running processes are lost, and the
    saved processes start again from their configuration when the sandbox is
    unarchived. The export runs in the background: this waits until the sandbox
    is ARCHIVED, pass ``wait=False`` to return as soon as it is launched.

    ``max_wait`` (ms, default 30 minutes) bounds the wait. ``interval`` (ms,
    default 2 seconds) is the first delay between status reads; later reads
    back off with jitter up to 30 seconds (or ``interval`` if larger).
    """,
)
SandboxInstance.unarchive = _AsyncSandboxCallDescriptor(
    _unarchive_sandbox_by_name,
    "unarchive",
    "DEPLOYED",
    UNARCHIVING_STATUSES,
    UNARCHIVE_ENTRY_STATUS,
    """Recreate an archived sandbox from its archive.

    The sandbox is started again from its image, and the archived filesystem is
    written back over it. The sandbox answers, and its terminal is reachable, while the archived
    filesystem is written back over its image. This waits until the restore is
    done and the saved processes are running again; pass ``wait=False`` to return
    while the sandbox is still UNARCHIVING.

    ``max_wait`` (ms, default 30 minutes) bounds the wait. ``interval`` (ms,
    default 2 seconds) is the first delay between status reads; later reads
    back off with jitter up to 30 seconds (or ``interval`` if larger).
    """,
)

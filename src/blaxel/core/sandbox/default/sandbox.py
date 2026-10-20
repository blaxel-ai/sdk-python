import asyncio
import json
import logging
import math
import time
import uuid
import warnings
from typing import Any, Callable, Dict, Union

import httpx
from attrs import evolve

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
from ...common.settings import settings
from ...errors import _APIError
from ..client.api.system.get_health import asyncio_detailed as get_health
from ..transient_retry import (
    DEFAULT_BASE_DELAY_SECONDS,
    DEFAULT_MAX_DELAY_SECONDS,
    _backoff_delay_seconds,
    is_transient_reset_error,
)
from ..types import (
    SandboxConfiguration,
    SandboxCreateConfiguration,
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

# A reset gives the sandbox a fresh instance booted from its image. The control
# plane does it in one call, which replaces the instance and answers once the
# new one runs. A control plane without that call is reset by switching
# spec.enabled off and on, which runs the deployment pipeline twice.
RESET_MAX_WAIT_MS = 120_000
RESET_POLL_MS = 200
# The longest single call made while waiting on the sandbox, so that one slow
# answer cannot hold the reset much past its own deadline.
RESET_PROBE_TIMEOUT_MS = 5_000
# The statuses a switch-off/switch-on reset can start from. Any other status is
# refused before anything is written: TERMINATED and DELETING above all
# (updating a record that is being, or has been, deleted brings the sandbox
# back to life), and FAILED (a write makes the control plane release the record
# and create it again).
RESETTABLE_STATUSES = {"DEPLOYED", "DEPLOYING", "DEACTIVATING", "DEACTIVATED"}
RESET_OFF_STATUSES = {"DEACTIVATING", "DEACTIVATED"}
# Right after the switch-on write the record can still read as off while the
# control plane starts the redeploy. That is tolerated only until the redeploy
# has been seen, and never past the wait the caller asked for.
RESET_ENTRY_MAX_WAIT_MS = 30_000
# What the deployment pipeline writes on a sandbox once it has applied, or
# failed to apply, a change to it.
DEPLOYMENT_SUCCEEDED_EVENT = "ai.blaxel.controlplane.deployment.succeeded"
DEPLOYMENT_FAILED_EVENT = "ai.blaxel.controlplane.deployment.failed"
# What the edge in front of the control plane or the sandbox answers when it
# could not reach it: worth asking again while there is time.
GATEWAY_ERROR_STATUSES = {502, 503, 504}


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


def _check_resettable(sandbox_name: str, sandbox: Sandbox) -> bool:
    """Refuse a sandbox that cannot be reset; say whether it must be taken down first.

    A sandbox that is already off (or going off) only has to be switched back on.
    """
    status = _status_of(sandbox)
    if status not in RESETTABLE_STATUSES:
        raise SandboxAPIError(
            f"Sandbox {sandbox_name} is {status or 'in an unknown state'} and cannot be reset"
        )
    return sandbox.spec.enabled is not False and status not in RESET_OFF_STATUSES


def _enabled_body(sandbox: Sandbox, enabled: bool) -> Dict[str, Any]:
    """The sandbox as the control plane last returned it, with ``spec.enabled`` set.

    Secret environment variable values come back masked and are kept as stored.
    """
    body = sandbox.to_dict()
    return {
        "metadata": body.get("metadata", {}),
        "spec": {**body.get("spec", {}), "enabled": enabled},
    }


def _check_taken_down(sandbox_name: str, sandbox: Sandbox) -> None:
    """Writing it back on only redeploys a sandbox that was really taken down."""
    status = _status_of(sandbox)
    if sandbox.spec.enabled is not False or status not in RESET_OFF_STATUSES:
        raise SandboxAPIError(
            f"Sandbox {sandbox_name} could not be reset: the control plane did not take it "
            f"down (it is {status})"
        )


def _reset_failure(sandbox_name: str, message: str, cause: Exception) -> SandboxAPIError:
    return SandboxAPIError(
        f"Sandbox {sandbox_name} {message}: {cause}",
        status_code=_error_status(cause),
    )


def _error_status(error: Exception) -> int | None:
    status = getattr(getattr(error, "response", None), "status_code", None)
    if not isinstance(status, int):
        status = getattr(error, "status_code", None)
    return status if isinstance(status, int) else None


def _is_retryable(error: Exception) -> bool:
    """An edge error in front of the control plane, or a dropped connection."""
    status = _error_status(error)
    if status is not None:
        return status in GATEWAY_ERROR_STATUSES
    return is_transient_reset_error(error)


def _reset_deadline(max_wait: int) -> float:
    """When the reset gives up: ``max_wait`` covers every call and every wait of it."""
    return math.inf if max_wait == -1 else time.monotonic() + max_wait / 1000


def _remaining(deadline: float) -> float:
    """Seconds left before the reset's deadline (inf without one)."""
    return deadline - time.monotonic()


def _reset_entry_deadline(deadline: float) -> float:
    """Until when, from the switch-on, a record that still reads off is tolerated."""
    return min(time.monotonic() + RESET_ENTRY_MAX_WAIT_MS / 1000, deadline)


def _retry_delay(attempt: int) -> float:
    return _backoff_delay_seconds(attempt, DEFAULT_BASE_DELAY_SECONDS, DEFAULT_MAX_DELAY_SECONDS)


class _TimedRequests:
    """An httpx client whose requests carry a timeout unless the caller sets one."""

    def __init__(self, httpx_client: Any, timeout: float):
        self._httpx_client = httpx_client
        self._timeout = timeout

    def request(self, *args: Any, **kwargs: Any) -> Any:
        kwargs.setdefault("timeout", self._timeout)
        return self._httpx_client.request(*args, **kwargs)


class _DeadlineClient:
    """The control plane client, with every request cut at a reset's deadline.

    The generated API functions only ask a client for its httpx client and for
    ``raise_on_unexpected_status``, so this stands in for it while sharing its
    connections, so that no call, retried or not, outlives the reset.
    """

    def __init__(self, base: Client, timeout: float):
        self._base = base
        self.timeout = timeout
        self.raise_on_unexpected_status = base.raise_on_unexpected_status

    def get_httpx_client(self) -> _TimedRequests:
        return _TimedRequests(self._base.get_httpx_client(), self.timeout)

    def get_async_httpx_client(self) -> _TimedRequests:
        return _TimedRequests(self._base.get_async_httpx_client(), self.timeout)


def _deadline_client(base: Client, deadline: float) -> Any:
    """``base`` with its requests cut at ``deadline``; ``base`` itself without one."""
    remaining = _remaining(deadline)
    if math.isinf(remaining):
        return base
    return _DeadlineClient(base, max(remaining, 0.001))


def _hit_deadline(error: Exception, deadline: float) -> bool:
    """A call cut by the reset's deadline (calls only time out when there is one)."""
    return isinstance(error, httpx.TimeoutException) and not math.isinf(deadline)


def _resets_by_switching(status: int, content: bytes) -> bool:
    """A control plane that has no reset call answers its route as unknown, and
    one that cannot reset this sandbox in one call answers 501: either way the
    sandbox is reset by switching it off and on.
    """
    if status in (405, 501):
        return True
    if status != 404:
        return False
    body = _decode_error_content(content)
    text = body.get("error") if isinstance(body, dict) else body
    return isinstance(text, str) and "route not found" in text.lower()


def _reset_refusal(sandbox_name: str, response: "httpx.Response") -> SandboxAPIError:
    """What the control plane answered instead of resetting the sandbox."""
    body = _decode_error_content(response.content)
    message = None
    code = None
    if isinstance(body, dict):
        message = body.get("message") or body.get("error")
        code = body.get("error") if isinstance(body.get("error"), str) else None
    if not isinstance(message, str) or not message:
        message = f"Failed to reset sandbox {sandbox_name} (HTTP {response.status_code})"
    return SandboxAPIError(
        message, status_code=response.status_code, code=code, body=body, response=response
    )


def _not_reset_in_time(sandbox_name: str, seconds: int) -> SandboxAPIError:
    return SandboxAPIError(
        f"Sandbox {sandbox_name} was not reset within {seconds}s; a reset the control plane "
        "started still finishes, so the sandbox may yet get its fresh instance"
    )


def _probe_timeout(deadline: float) -> "httpx.Timeout":
    seconds = min(_remaining(deadline), RESET_PROBE_TIMEOUT_MS / 1000)
    return httpx.Timeout(max(seconds, 0.001))


def _probe_answer(sandbox_name: str, status: int, content: bytes) -> "bool | str":
    """True when the health route answered; why not yet when the gateway has no
    instance to route to (404 WORKLOAD_UNAVAILABLE) or the edge could not reach
    it. Anything else is an answer the reset cannot read, and is raised.
    """
    if 200 <= status < 300:
        return True
    body = _decode_error_content(content)
    detail = json.dumps(body) if isinstance(body, dict | list) else str(body)
    if status == 404 or status in GATEWAY_ERROR_STATUSES:
        return f"{status} {detail}"
    raise SandboxAPIError(
        f"Sandbox {sandbox_name} answered {status} after the reset: {detail}",
        status_code=status,
    )


def _transport_detail(error: Exception) -> str:
    return str(error) or type(error).__name__


def _not_answering(sandbox_name: str, seconds: int, answer: str) -> SandboxAPIError:
    return SandboxAPIError(
        f"Sandbox {sandbox_name} has a fresh instance but it did not answer within {seconds}s "
        f"after the reset: {answer}"
    )


def _created_at(sandbox: Sandbox) -> str | None:
    value = sandbox.metadata.created_at if sandbox.metadata else UNSET
    return None if isinstance(value, Unset) else value


class _ResetStopped(SandboxAPIError):
    """An error that ends a reset as it is, without being reworded by the step it stopped."""


def _recreated(sandbox_name: str) -> _ResetStopped:
    return _ResetStopped(
        f"Sandbox {sandbox_name} was deleted and created again during its reset; the new "
        "sandbox is left as it is"
    )


def _deleted(sandbox_name: str) -> _ResetStopped:
    return _ResetStopped(f"Sandbox {sandbox_name} was deleted during its reset", status_code=404)


def _check_same_sandbox(sandbox_name: str, entry: Sandbox, record: Sandbox) -> None:
    """Refuse to go on with a sandbox created again under the same name since the
    reset read it first: its creation date tells the two apart.
    """
    if _created_at(record) != _created_at(entry):
        raise _recreated(sandbox_name)


def _check_written_same(sandbox_name: str, entry: Sandbox, answer: Sandbox, enabled: bool) -> None:
    """A switch answered for another sandbox of the same name: it was written to."""
    if _created_at(answer) != _created_at(entry):
        switching, left = ("back on", "on") if enabled else ("off", "off")
        raise _ResetStopped(
            f"Sandbox {sandbox_name} was deleted and created again while it was being switched "
            f"{switching} for its reset; the new sandbox was written to and is left switched {left}"
        )


def _check_same_after_lost_write(
    sandbox_name: str, entry: Sandbox, record: Sandbox, enabled: bool
) -> None:
    """After a write whose answer was lost, a sandbox created again under the same
    name may have received it: the write goes by name, so say so.
    """
    if _created_at(record) != _created_at(entry):
        switch = "switch-on" if enabled else "switch-off"
        raise _ResetStopped(
            f"Sandbox {sandbox_name} was deleted and created again during its reset; the "
            f"reset's {switch} write whose answer was lost may have reached the new sandbox, "
            "which is left as it is now"
        )


def _check_same_before_reset_again(sandbox_name: str, entry: Sandbox, record: Sandbox) -> None:
    """Before a reset call is sent again: the call goes by name, so one whose answer
    was lost may have reached a sandbox created again under it, which is not reset
    a second time.
    """
    if _created_at(record) != _created_at(entry):
        raise _ResetStopped(
            f"Sandbox {sandbox_name} was deleted and created again during its reset; the "
            "reset call whose answer was lost may have reached the new sandbox, which is not "
            "reset again"
        )


def _check_reset_same(sandbox_name: str, entry: "Sandbox | None", record: Sandbox) -> None:
    """A reset that answered for another sandbox than the one under the name as the
    reset started (when that read succeeded) reset a sandbox created again under it.
    """
    if entry is not None and _created_at(record) != _created_at(entry):
        raise _ResetStopped(
            f"Sandbox {sandbox_name} was deleted and created again as its reset started; the "
            "new sandbox was reset"
        )


def _write_landed(record: Sandbox, enabled: bool) -> bool:
    """Whether the record already holds the switch a write cut short was sending."""
    return record.spec.enabled is not False if enabled else record.spec.enabled is False


def _check_still_running(sandbox_name: str, entry: Sandbox, record: Sandbox) -> None:
    """Refuse to send the switch-off again to anything but the sandbox being reset,
    still in a state a reset can start from.
    """
    _check_same_sandbox(sandbox_name, entry, record)
    status = _status_of(record)
    if status not in RESETTABLE_STATUSES:
        raise _ResetStopped(
            f"Sandbox {sandbox_name} is {status} while it should be running for the reset; "
            "it is left as it is"
        )


def _check_still_off(sandbox_name: str, entry: Sandbox, record: Sandbox) -> None:
    """Refuse to switch back on anything but the sandbox being reset, still off."""
    _check_same_sandbox(sandbox_name, entry, record)
    status = _status_of(record)
    if status not in RESET_OFF_STATUSES or record.spec.enabled is not False:
        raise _ResetStopped(
            f"Sandbox {sandbox_name} is {status} while it should be switched off for the reset; "
            "it is left as it is"
        )


def _teardown_state(record: Sandbox) -> str:
    """Where the deployment pipeline is with taking a switched-off sandbox's
    instance down, read from the newest event it or the API wrote: "done",
    "failed", or "pending" while an API write is not applied yet or a deployment
    is still running.
    """
    events = record.events if isinstance(record.events, list) else []
    for event in reversed(events):
        type_ = event.type_ if isinstance(event.type_, str) else None
        status = event.status if isinstance(event.status, str) else None
        if type_ == DEPLOYMENT_SUCCEEDED_EVENT:
            return "done" if status == "DEACTIVATED" else "pending"
        if type_ == DEPLOYMENT_FAILED_EVENT:
            return "failed"
        if type_ and type_.startswith("ai.blaxel.controlplane."):
            return "pending"
    return "pending"


def _left_off(sandbox_name: str, owner: str) -> str:
    return f'it is left DEACTIVATED; call {owner}.reset("{sandbox_name}") again to finish the reset'


def _teardown_failed(sandbox_name: str) -> SandboxAPIError:
    """The platform could not take the instance down. Resetting again cannot get
    past it: the sandbox is already off and the failed teardown stays its newest
    event.
    """
    return SandboxAPIError(
        f"Sandbox {sandbox_name} could not be taken down for the reset: the platform reported "
        "the teardown failed. It is left switched off; delete it and create it again to get a "
        "fresh instance"
    )


def _teardown_timeout(sandbox_name: str, seconds: int, owner: str) -> SandboxAPIError:
    return SandboxAPIError(
        f"Sandbox {sandbox_name} is switched off for the reset, but its old instance was not "
        f"reported gone within {seconds}s, {_left_off(sandbox_name, owner)}"
    )


def _teardown_unreadable(sandbox_name: str, error: Exception, owner: str) -> SandboxAPIError:
    if _error_status(error) == 404:
        return _deleted(sandbox_name)
    return _reset_failure(
        sandbox_name,
        "is switched off for the reset, but it could not be read again, "
        + _left_off(sandbox_name, owner),
        error,
    )


def _check_reset_status(sandbox_name: str, sandbox: Sandbox, *, tolerate_off: bool = False) -> bool:
    """While waiting for the redeploy: True once DEPLOYED, False while DEPLOYING.

    ``tolerate_off`` also lets a record that still reads DEACTIVATING/DEACTIVATED
    pass (False), for the moment right after the switch-on write.
    """
    status = _status_of(sandbox)
    if status == "DEPLOYED":
        return True
    if status == "FAILED":
        raise SandboxAPIError(f"Sandbox {sandbox_name} failed to deploy again after the reset")
    if tolerate_off and status in RESET_OFF_STATUSES:
        return False
    if status != "DEPLOYING":
        raise SandboxAPIError(
            f"Sandbox {sandbox_name} is {status} while it should be deployed again after the reset"
        )
    return False


def _still_redeploying(sandbox_name: str, sandbox: Sandbox, seconds: int) -> SandboxAPIError:
    return SandboxAPIError(
        f"Sandbox {sandbox_name} is still {_status_of(sandbox)} after waiting {seconds}s for it "
        "to deploy again after the reset"
    )


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
        while True:
            await asyncio.sleep(interval / 1000)
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
    delete: "_AsyncDeleteDescriptor"
    archive: "_AsyncSandboxCallDescriptor"
    unarchive: "_AsyncSandboxCallDescriptor"
    reset: "_AsyncResetDescriptor"

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
        return self.sandbox.metadata

    @property
    def status(self):
        return self.sandbox.status

    @property
    def events(self):
        return self.sandbox.events

    @property
    def spec(self):
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
        return self.sandbox.last_used_at

    @property
    def expires_in(self):
        return self.sandbox.expires_in

    async def fetch(
        self, port: int, path: str = "/", method: str = "GET", **kwargs
    ) -> "httpx.Response":
        """Fetch a resource served on a sandbox port.

        Args:
            port: The port number inside the sandbox
            path: Optional path appended after the port (default: "/")
            method: HTTP method (default: "GET")
            **kwargs: Additional arguments forwarded to httpx (e.g. headers, content)
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
    ) -> "SandboxInstance":
        """Create a sandbox.

        Args:
            timeout: Optional creation deadline in whole seconds (1 to
                ``MAX_CREATION_TIMEOUT_SECONDS``). When the sandbox is not ready
                in time the control plane cancels the creation, releases the
                sandbox and ``SandboxCreationTimeoutError`` is raised. Omitted, the
                platform default deadline applies; an explicit value can only
                shorten it.
        """
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
            if not region:
                warnings.warn(
                    "SandboxInstance.create: 'region' is not set. In a future version, 'region' will be a required parameter. "
                    "Please specify a region (e.g. 'us-pdx-1', 'eu-lon-1', 'us-was-1') in the sandbox configuration or set the BL_REGION environment variable.",
                    FutureWarning,
                    stacklevel=2,
                )
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
        else:
            # Handle existing Sandbox object or dict conversion
            if isinstance(sandbox, dict):
                sandbox = Sandbox.from_dict(sandbox)
                assert sandbox is not None

            assert isinstance(sandbox, Sandbox)
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

        body = _create_body(sandbox)
        try:
            if timeout is None:
                response = await create_sandbox(
                    client=client, body=body, create_if_not_exist=create_if_not_exist
                )
            else:
                async with _creation_client(timeout) as creation_client:
                    response = await create_sandbox(
                        client=creation_client, body=body, create_if_not_exist=create_if_not_exist
                    )
        except client_errors.UnexpectedStatus as e:
            _raise_if_creation_timeout(e, _sandbox_name(sandbox), timeout)
            raise

        # Check if response is an error
        if isinstance(response, SandboxError):
            _raise_if_creation_timeout(response, _sandbox_name(sandbox), timeout)
            status_code = response.status_code if response.status_code is not UNSET else None
            code = response.code if response.code else None
            message = response.message if response.message else str(response)
            raise SandboxAPIError(message, status_code=status_code, code=code, error=response)

        assert response is not None
        instance = cls(response)
        # TODO remove this part once we have a better way to handle this
        if safe:
            try:
                await instance.fs.ls("/")
            except Exception:
                pass
        return instance

    @classmethod
    async def get(cls, sandbox_name: str) -> "SandboxInstance":
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

        Args:
            sandbox_name: The name of the sandbox to update
            metadata: The metadata fields to update (labels and/or display_name)

        Returns:
            A new SandboxInstance with updated metadata
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

        Args:
            sandbox_name: The name of the sandbox to update
            ttl: The new TTL value (e.g., "5m", "1h"; minimum 5m), or None/"" to clear

        Returns:
            A new SandboxInstance with updated TTL
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

        Args:
            sandbox_name: The name of the sandbox to update
            lifecycle: The new lifecycle configuration, or None to clear

        Returns:
            A new SandboxInstance with updated lifecycle
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

        Args:
            sandbox_name: The name of the sandbox to update
            network: The new network configuration

        Returns:
            A new SandboxInstance with updated network configuration
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
    ) -> "SandboxInstance":
        """Create the sandbox, or return the one already holding this name.

        ``timeout`` is forwarded to :meth:`create`.

        The control plane owns the reconciliation: an alive sandbox is returned as
        is, a FAILED/TERMINATED one is replaced, and a deletion or concurrent
        creation still in flight is waited for server-side. A 409 therefore only
        surfaces when the name really cannot be used, and is raised as is.
        """
        create_kwargs: Dict[str, Any] = {} if timeout is None else {"timeout": timeout}
        return await cls.create(sandbox, create_if_not_exist=True, **create_kwargs)

    @classmethod
    async def from_session(
        cls, session: Union[SessionWithToken, Dict[str, Any]]
    ) -> "SandboxInstance":
        """Create a sandbox instance from a session with token."""
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


class _AsyncResetDescriptor:
    """Expose ``reset`` as both ``SandboxInstance.reset("name")`` and ``instance.reset()``.

    Both forms answer a ``SandboxInstance``; the instance form refreshes the
    record it was called on.
    """

    def __init__(self, doc: str):
        self.__doc__ = doc

    def __get__(self, instance, owner):
        if instance is None:

            async def class_call(
                sandbox_name: str,
                *,
                max_wait: int = RESET_MAX_WAIT_MS,
                interval: int = RESET_POLL_MS,
            ) -> "SandboxInstance":
                return await _reset_sandbox_by_name(sandbox_name, max_wait, interval)

            class_call.__doc__ = self.__doc__
            return class_call

        async def instance_call(
            *, max_wait: int = RESET_MAX_WAIT_MS, interval: int = RESET_POLL_MS
        ) -> "SandboxInstance":
            fresh = await _reset_sandbox_by_name(instance.metadata.name, max_wait, interval)
            instance.sandbox = fresh.sandbox
            instance.config.sandbox = instance.sandbox
            return instance

        instance_call.__doc__ = self.__doc__
        return instance_call


_RESET_OWNER = "SandboxInstance"


async def _reset_sandbox_by_name(
    sandbox_name: str, max_wait: int, interval: int
) -> "SandboxInstance":
    deadline = _reset_deadline(max_wait)
    seconds = round(max_wait / 1000)
    # The sandbox the reset is for, read alongside the reset call so that it adds
    # no wait: every later step checks it still has that creation date.
    entry = asyncio.ensure_future(_read_for_reset(sandbox_name, deadline, seconds))
    try:
        record = await _reset_on_control_plane(sandbox_name, entry, deadline, seconds)
        if record is not None:
            return await _wait_until_answering(
                sandbox_name, SandboxInstance(record), deadline, seconds, interval
            )
        return await _reset_by_switching(sandbox_name, await entry, deadline, seconds, interval)
    finally:
        if not entry.done():
            entry.cancel()
        elif not entry.cancelled():
            entry.exception()


async def _entry_or_none(entry: "asyncio.Future[Sandbox]") -> Sandbox | None:
    try:
        return await entry
    except Exception:
        return None


async def _check_still_there(
    sandbox_name: str, entry: Sandbox, deadline: float, seconds: int
) -> None:
    """Before a reset call is sent again: the sandbox must still be the one the reset is for."""
    try:
        latest = await _read_for_reset(sandbox_name, deadline, seconds)
    except Exception as e:
        if _error_status(e) == 404:
            raise _deleted(sandbox_name) from e
        raise
    _check_same_before_reset_again(sandbox_name, entry, latest)


async def _post_reset(sandbox_name: str, deadline: float, idempotency_key: str) -> httpx.Response:
    """POST /sandboxes/{name}/reset on the control plane, cut at the reset's deadline.

    The generated client has no function for it yet, so it goes through the
    configured httpx client the generated functions use, with the same auth.
    """
    return await (
        _deadline_client(client, deadline)
        .get_async_httpx_client()
        .request(
            "post",
            f"/sandboxes/{sandbox_name}/reset",
            headers={"Idempotency-Key": idempotency_key},
        )
    )


async def _reset_on_control_plane(
    sandbox_name: str, entry: "asyncio.Future[Sandbox]", deadline: float, seconds: int
) -> Sandbox | None:
    """Ask the control plane to replace the sandbox's instance.

    Answers the sandbox once its new instance runs, or None when the control
    plane has no such call, for the reset to switch the sandbox off and on
    instead. An answer lost at the edge or on the way is asked for again while
    there is time, with the same Idempotency-Key: a control plane that already
    ran the reset, or is still running it, answers with the sandbox instead of
    replacing its instance a second time. The call goes by name, so it is asked
    for again only while the name still holds the sandbox the reset is for
    (``entry``).
    """
    idempotency_key = str(uuid.uuid4())
    attempt = 0
    while True:
        attempt += 1
        if attempt > 1:
            await _check_still_there(sandbox_name, await entry, deadline, seconds)
        try:
            response = await _post_reset(sandbox_name, deadline, idempotency_key)
        except Exception as e:
            if _hit_deadline(e, deadline):
                raise _not_reset_in_time(sandbox_name, seconds) from e
            if not is_transient_reset_error(e):
                raise
            failure: Exception = e
        else:
            status = response.status_code
            if 200 <= status < 300:
                record = Sandbox.from_dict(response.json())
                _check_reset_same(sandbox_name, await _entry_or_none(entry), record)
                return record
            if _resets_by_switching(status, response.content):
                return None
            failure = _reset_refusal(sandbox_name, response)
            if status not in GATEWAY_ERROR_STATUSES:
                raise failure
        delay = _retry_delay(attempt)
        if _remaining(deadline) <= delay:
            raise SandboxAPIError(
                f"Sandbox {sandbox_name} could not be reset within {seconds}s: {failure}",
                status_code=_error_status(failure),
            ) from failure
        await asyncio.sleep(delay)


async def _probe(sandbox_name: str, instance: "SandboxInstance", deadline: float) -> "bool | str":
    """One call to the sandbox's health route, cut at the reset's deadline."""
    api = instance.system.get_api_client().with_timeout(_probe_timeout(deadline))
    try:
        async with api:
            response = await get_health(client=api)
    except httpx.TransportError as e:
        return _transport_detail(e)
    return _probe_answer(sandbox_name, int(response.status_code), response.content)


async def _wait_until_answering(
    sandbox_name: str, instance: "SandboxInstance", deadline: float, seconds: int, interval: int
) -> "SandboxInstance":
    """Wait until the sandbox answers on its new instance.

    The control plane answers once the instance runs; the gateway can take a
    moment more to route to it.
    """
    while True:
        answer = await _probe(sandbox_name, instance, deadline)
        if answer is True:
            return instance
        if _remaining(deadline) <= interval / 1000:
            raise _not_answering(sandbox_name, seconds, str(answer))
        await asyncio.sleep(interval / 1000)


async def _read_for_reset(sandbox_name: str, deadline: float, seconds: int) -> Sandbox:
    """Read the sandbox's record within the reset's deadline.

    A read is idempotent, so a dropped connection or an edge error is read again
    while there is time; anything else, a missing sandbox above all, is raised
    as the control plane answered it.
    """
    attempt = 0
    while True:
        attempt += 1
        try:
            response = await get_sandbox(sandbox_name, client=_deadline_client(client, deadline))
            return _unwrap_response(response, f"read sandbox {sandbox_name}")
        except Exception as e:
            if _hit_deadline(e, deadline):
                raise SandboxAPIError(
                    f"Sandbox {sandbox_name} could not be read within the {seconds}s of its reset"
                ) from e
            delay = _retry_delay(attempt)
            if not _is_retryable(e) or _remaining(deadline) <= delay:
                raise
            await asyncio.sleep(delay)


async def _write_enabled(
    sandbox_name: str,
    record: Sandbox,
    enabled: bool,
    entry: Sandbox,
    deadline: float,
    seconds: int,
) -> Sandbox:
    """Write the sandbox back with ``spec.enabled`` set, from the record as the
    control plane last returned it.

    A write cut short may or may not have landed, so before it is sent again the
    record is read again: a write that landed is not sent again, and one that did
    not is only sent again to the sandbox the reset started on (same creation
    date as ``entry``), still in the state the write is meant for, from that
    fresh read.
    """
    attempt = 0
    while True:
        attempt += 1
        try:
            response = await update_sandbox(
                sandbox_name=sandbox_name,
                client=_deadline_client(client, deadline),
                body=_enabled_body(record, enabled),
            )
            return _unwrap_response(response, f"update sandbox {sandbox_name}")
        except Exception as e:
            if _hit_deadline(e, deadline):
                raise SandboxAPIError(f"no answer within the {seconds}s of the reset") from e
            delay = _retry_delay(attempt)
            if not _is_retryable(e) or _remaining(deadline) <= delay:
                raise
            await asyncio.sleep(delay)
        try:
            latest = await _read_for_reset(sandbox_name, deadline, seconds)
        except Exception as e:
            if _error_status(e) == 404:
                raise _deleted(sandbox_name) from e
            raise
        _check_same_after_lost_write(sandbox_name, entry, latest, enabled)
        if _write_landed(latest, enabled):
            return latest
        if enabled:
            _check_still_off(sandbox_name, entry, latest)
        else:
            _check_still_running(sandbox_name, entry, latest)
        record = latest


async def _reset_by_switching(
    sandbox_name: str, current: Sandbox, deadline: float, seconds: int, interval: int
) -> "SandboxInstance":
    """Reset a sandbox on a control plane without the reset call.

    Switch it off, wait until the platform reports its instance gone, switch it
    back on and wait until it is deployed again and answers. Every write is
    preceded by a fresh read of the record, and refused unless the sandbox is
    still the one being reset and still in a state the write is meant for.
    """
    if _check_resettable(sandbox_name, current):
        try:
            off = await _write_enabled(sandbox_name, current, False, current, deadline, seconds)
        except _ResetStopped:
            raise
        except Exception as e:
            raise _reset_failure(
                sandbox_name, "could not be reset, it was left as it was", e
            ) from e
        _check_written_same(sandbox_name, current, off, False)
        _check_taken_down(sandbox_name, off)
    stopped = await _wait_for_teardown(sandbox_name, current, deadline, seconds, interval)
    try:
        on = await _write_enabled(sandbox_name, stopped, True, current, deadline, seconds)
    except _ResetStopped:
        raise
    except Exception as e:
        raise _reset_failure(
            sandbox_name,
            "was taken down for the reset but could not be switched back on, "
            + _left_off(sandbox_name, _RESET_OWNER),
            e,
        ) from e
    _check_written_same(sandbox_name, current, on, True)
    return await _wait_for_redeploy(sandbox_name, current, deadline, seconds, interval)


async def _wait_for_teardown(
    sandbox_name: str, entry: Sandbox, deadline: float, seconds: int, interval: int
) -> Sandbox:
    """Wait until the platform reports the switched-off instance gone.

    Answers the record read last, the one the switch-on is written from.
    Switched back on while the old instance still runs, the sandbox could keep
    it. The record says when it is gone: the deployment pipeline writes a
    succeeded deployment once it has taken the instance down. Nothing the old
    guest answers is taken as a sign of it.
    """
    while True:
        try:
            record = await _read_for_reset(sandbox_name, deadline, seconds)
        except Exception as e:
            raise _teardown_unreadable(sandbox_name, e, _RESET_OWNER) from e
        _check_still_off(sandbox_name, entry, record)
        state = _teardown_state(record)
        if state == "done":
            return record
        if state == "failed":
            raise _teardown_failed(sandbox_name)
        if _remaining(deadline) <= interval / 1000:
            raise _teardown_timeout(sandbox_name, seconds, _RESET_OWNER)
        await asyncio.sleep(interval / 1000)


async def _wait_for_redeploy(
    sandbox_name: str, entry: Sandbox, deadline: float, seconds: int, interval: int
) -> "SandboxInstance":
    """Wait until the sandbox is DEPLOYED again and answers.

    The record turns DEPLOYED a moment before the sandbox is routable, so
    DEPLOYED alone is not ready. Every read must still be the sandbox the reset
    started on.
    """
    entry_deadline = _reset_entry_deadline(deadline)
    redeploying = False
    while True:
        await asyncio.sleep(interval / 1000)
        record = await _read_for_reset(sandbox_name, deadline, seconds)
        _check_same_sandbox(sandbox_name, entry, record)
        redeploying = redeploying or _status_of(record) == "DEPLOYING"
        if _check_reset_status(
            sandbox_name,
            record,
            tolerate_off=not redeploying and time.monotonic() < entry_deadline,
        ):
            return await _wait_until_answering(
                sandbox_name, SandboxInstance(record), deadline, seconds, interval
            )
        if _remaining(deadline) <= interval / 1000:
            raise _still_redeploying(sandbox_name, record, seconds)


async def _delete_sandbox_by_name(sandbox_name: str) -> Sandbox:
    """Delete a sandbox by name."""
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
    """,
)
SandboxInstance.reset = _AsyncResetDescriptor(
    """Reset a sandbox to a fresh copy of its image.

    The sandbox gets a new instance booted from its image: everything written
    to its filesystem since it started and every running process are gone, as
    after a delete and a create. Unlike a delete and a create, the sandbox is
    never absent: it keeps its name and URL, its spec, its environment
    variables (secret values included), its volumes and the data on them, its
    previews, preview tokens and sessions. Running processes, and anything
    mounted from inside the sandbox such as a drive, belong to the old instance
    and have to be started or mounted again.

    The control plane replaces the instance in one call: the platform deletes
    the old instance and boots the new one, whatever ran in the old one. This
    then waits until the sandbox answers. Only a running (DEPLOYED) sandbox can
    be reset that way.

    On a control plane without that call, the sandbox is switched off and on
    again (``spec.enabled``): the reset waits for the platform to report the old
    instance gone, then for the redeploy. A sandbox that is disabled is switched
    back on. If ``max_wait`` runs out before the old instance is gone, or the
    second write fails, the sandbox is left DEACTIVATED and the error says so:
    calling ``reset`` again finishes the reset.

    Sandboxes that are archived, failed or being deleted cannot be reset.
    ``max_wait`` bounds the whole reset, every call included.

    Args:
        max_wait: Give up waiting for the reset after this many milliseconds;
            -1 waits indefinitely.
        interval: Milliseconds between two reads of the sandbox while waiting on it.
    """
)

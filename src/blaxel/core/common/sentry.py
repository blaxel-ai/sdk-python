import asyncio
import atexit
import builtins
import json
import logging
import sys
import threading
import time
import traceback
import uuid
from asyncio import CancelledError
from datetime import datetime, timezone
from pathlib import Path
from queue import Full, Queue
from typing import Any
from urllib.parse import urlparse

import httpx

from .settings import settings

try:
    from exceptiongroup import BaseExceptionGroup as BackportBaseExceptionGroup
except ImportError:  # The backport is optional and only needed on Python 3.10.
    BackportBaseExceptionGroup = None

logger = logging.getLogger(__name__)

# Lightweight Sentry client using httpx - only captures SDK errors
_sentry_initialized = False

# Parsed DSN components
_sentry_config: dict[str, str] | None = None

# Bounded queue for last-chance background capture.
_MAX_CAPTURE_EVENTS = 100
_BACKGROUND_CAPTURE_STOP = object()
_background_worker_init_lock = threading.Lock()
_handler_registration_lock = threading.Lock()
_background_capture_queue: Queue[Any] = Queue(maxsize=_MAX_CAPTURE_EVENTS)
_background_capture_thread: threading.Thread | None = None
_handlers_registered = False
_original_excepthook = None
_original_threading_excepthook = None
_original_unraisablehook = None
_original_asyncio_call_exception_handler = None

# Exceptions that are part of normal control flow and should not be captured
_IGNORED_EXCEPTIONS = (
    StopIteration,  # Iterator exhaustion
    StopAsyncIteration,  # Async iterator exhaustion
    GeneratorExit,  # Generator cleanup
    KeyboardInterrupt,  # User interrupt (Ctrl+C)
    SystemExit,  # Program exit
    CancelledError,  # Async task cancellation
)

# Optional dependencies that may not be installed - import errors for these are expected
_OPTIONAL_DEPENDENCIES = ("opentelemetry",)
_SAFE_ERROR_CODES = {
    "DRIVE_ALREADY_EXISTS",
    "NOT_FOUND",
    "SANDBOX_ALREADY_EXISTS",
    "VOLUME_ALREADY_ATTACHED",
    "VOLUME_ALREADY_EXISTS",
    "WORKLOAD_UNAVAILABLE",
}

# Optional blaxel framework integration subpackages. Importing any of these
# requires installing the matching extra (e.g. ``pip install blaxel[openai]``).
# When the extra -- or one of its transitive dependencies -- is missing, or when
# the integration files are absent from a stripped/partial install, importing the
# integration raises an ImportError. That is an expected environment issue, not an
# SDK bug, so it must not be reported to Sentry.
_OPTIONAL_INTEGRATION_PACKAGES = (
    "blaxel.langgraph",
    "blaxel.llamaindex",
    "blaxel.openai",
    "blaxel.crewai",
    "blaxel.googleadk",
    "blaxel.livekit",
    "blaxel.pydantic",
    "blaxel.telemetry",
)

_OPTIONAL_INTEGRATION_ENTRYPOINT_MODULES = {
    "blaxel.langgraph": ("model", "tools"),
    "blaxel.llamaindex": ("model", "tools"),
    "blaxel.openai": ("model", "tools"),
    "blaxel.crewai": ("model", "tools"),
    "blaxel.googleadk": ("model", "tools"),
    "blaxel.livekit": ("model", "tools"),
    "blaxel.pydantic": ("model", "tools"),
    "blaxel.telemetry": ("exporters", "instrumentation", "log", "manager", "span"),
}

# Resolve frames against the package that supplied this module. Matching arbitrary
# path substrings such as ``blaxel/`` can misclassify application code and report
# exceptions that did not originate in the installed SDK.
_SDK_PACKAGE_ROOT = Path(__file__).resolve().parents[2]
_OPTIONAL_INTEGRATION_ROOTS = tuple(
    _SDK_PACKAGE_ROOT / package.rsplit(".", 1)[-1] for package in _OPTIONAL_INTEGRATION_PACKAGES
)
_builtin_exception_group = getattr(builtins, "BaseExceptionGroup", None)
_EXCEPTION_GROUP_TYPES = tuple(
    dict.fromkeys(
        group_type
        for group_type in (_builtin_exception_group, BackportBaseExceptionGroup)
        if group_type is not None
    )
)


def _is_path_within(filename: str, root: Path) -> bool:
    """Return whether a traceback filename resolves inside a trusted package root."""
    try:
        Path(filename).resolve().relative_to(root)
        return True
    except (OSError, ValueError):
        return False


def _sdk_relative_filename(filename: str) -> str | None:
    """Return an SDK-relative frame name, excluding application filesystem paths."""
    try:
        relative_path = Path(filename).resolve().relative_to(_SDK_PACKAGE_ROOT)
    except (OSError, ValueError):
        return None
    return (Path(_SDK_PACKAGE_ROOT.name) / relative_path).as_posix()


def _is_from_sdk(error: BaseException) -> bool:
    """Check whether an error has a frame inside this installed SDK package."""
    tb = error.__traceback__
    while tb is not None:
        if _sdk_relative_filename(tb.tb_frame.f_code.co_filename) is not None:
            return True
        tb = tb.tb_next
    return False


def _contains_sdk_exception(error: BaseException) -> bool:
    """Check an ordinary exception or exception group for an SDK-owned frame."""
    if _is_from_sdk(error):
        return True
    if isinstance(error, _EXCEPTION_GROUP_TYPES):
        return any(_contains_sdk_exception(child) for child in getattr(error, "exceptions"))
    return False


def _parse_dsn(dsn: str) -> dict[str, str] | None:
    """
    Parse a Sentry DSN into its components.
    DSN format: https://{public_key}@{host}/{project_id}
    """
    try:
        parsed = urlparse(dsn)
        public_key = parsed.username
        host = parsed.hostname
        project_id = parsed.path.lstrip("/")

        if not public_key or not host or not project_id:
            return None

        return {"public_key": public_key, "host": host, "project_id": project_id}
    except Exception:
        return None


def _generate_event_id() -> str:
    """Generate a UUID v4 for event ID."""
    return uuid.uuid4().hex


def _parse_stack_trace(exc: BaseException) -> list[dict[str, Any]]:
    """Parse exception traceback into Sentry-compatible frames."""
    frames: list[dict[str, Any]] = []
    tb = traceback.extract_tb(exc.__traceback__)

    for frame in tb:
        filename = _sdk_relative_filename(frame.filename)
        if filename is None:
            continue
        frames.append(
            {
                "filename": filename,
                "function": frame.name or "<anonymous>",
                "lineno": frame.lineno,
                "colno": 0,
            }
        )

    return frames


def _safe_exception_value(error: BaseException) -> str:
    """Describe an SDK failure without including exception or response content."""
    if isinstance(error, _EXCEPTION_GROUP_TYPES):
        child_count = len(getattr(error, "exceptions"))
        return f"Unhandled SDK exception group ({child_count} sub-exceptions)"

    details = []
    status_code = getattr(error, "status_code", None)
    if status_code is None:
        status_code = getattr(getattr(error, "response", None), "status_code", None)
    if type(status_code) is int and 100 <= status_code <= 599:
        details.append(f"HTTP {status_code}")

    error_code = getattr(error, "error_code", None) or getattr(error, "code", None)
    if type(error_code) is int:
        if error_code != status_code:
            details.append(f"code {error_code}")
    elif isinstance(error_code, str) and error_code in _SAFE_ERROR_CODES:
        details.append(f"code {error_code}")

    suffix = f" ({', '.join(details)})" if details else ""
    return f"Unhandled SDK exception{suffix}"


def _exception_to_sentry_value(error: BaseException, mechanism: dict[str, Any]) -> dict[str, Any]:
    """Convert one exception or exception-group node to a Sentry exception value."""
    return {
        "type": type(error).__name__,
        "value": _safe_exception_value(error),
        "stacktrace": {"frames": _parse_stack_trace(error)},
        "mechanism": mechanism,
    }


def _exception_values(
    error: BaseException, mechanism_type: str = "generic"
) -> list[dict[str, Any]]:
    """Serialize an exception tree without sending one event per group leaf."""
    if not isinstance(error, _EXCEPTION_GROUP_TYPES):
        return [
            _exception_to_sentry_value(
                error,
                {"type": mechanism_type, "handled": False},
            )
        ]

    values: list[dict[str, Any]] = []

    def append_exception(
        exception: BaseException,
        parent_id: int | None = None,
        source: str | None = None,
    ) -> None:
        exception_id = len(values)
        mechanism: dict[str, Any] = {
            "type": mechanism_type if parent_id is None else "chained",
            "handled": False,
            "exception_id": exception_id,
        }
        if parent_id is not None:
            mechanism["parent_id"] = parent_id
            mechanism["source"] = source
        if isinstance(exception, _EXCEPTION_GROUP_TYPES):
            mechanism["is_exception_group"] = True

        values.append(_exception_to_sentry_value(exception, mechanism))
        if isinstance(exception, _EXCEPTION_GROUP_TYPES):
            for index, child in enumerate(getattr(exception, "exceptions")):
                append_exception(child, exception_id, f"exceptions[{index}]")

    append_exception(error)
    values.reverse()
    return values


def _error_to_sentry_event(error: BaseException, mechanism_type: str = "generic") -> dict[str, Any]:
    """Convert an exception to a Sentry event payload."""
    return {
        "event_id": _generate_event_id(),
        "timestamp": datetime.now(timezone.utc).timestamp(),
        "platform": "python",
        "level": "error",
        "environment": settings.env,
        "release": f"sdk-python@{settings.version}",
        "tags": {
            "blaxel.workspace": settings.workspace,
            "blaxel.version": settings.version,
            "blaxel.commit": settings.commit,
        },
        "exception": {"values": _exception_values(error, mechanism_type)},
    }


def _send_to_sentry(event: dict[str, Any], timeout: float = 2.0) -> bool:
    """Send an event to Sentry, returning whether delivery succeeded."""
    if not _sentry_config:
        return False

    public_key = _sentry_config["public_key"]
    host = _sentry_config["host"]
    project_id = _sentry_config["project_id"]
    envelope_url = f"https://{host}/api/{project_id}/envelope/"

    # Create envelope header
    envelope_header = json.dumps(
        {
            "event_id": event["event_id"],
            "sent_at": datetime.now(timezone.utc).isoformat(),
            "dsn": f"https://{public_key}@{host}/{project_id}",
        }
    )

    # Create item header
    item_header = json.dumps({"type": "event", "content_type": "application/json"})

    # Create envelope body
    envelope = f"{envelope_header}\n{item_header}\n{json.dumps(event)}"

    try:
        response = httpx.post(
            envelope_url,
            headers={
                "Content-Type": "application/x-sentry-envelope",
                "X-Sentry-Auth": f"Sentry sentry_version=7, sentry_client=blaxel-sdk/{settings.version}, sentry_key={public_key}",
            },
            content=envelope,
            timeout=max(timeout, 0.01),
        )
        response.raise_for_status()
        return True
    except Exception:
        # Silently fail - error reporting should never break the SDK
        return False


def _has_optional_integration_frame(exc_value) -> bool:
    """Check whether a traceback passed through an installed integration module."""
    tb = getattr(exc_value, "__traceback__", None)
    while tb is not None:
        filename = tb.tb_frame.f_code.co_filename
        if any(_is_path_within(filename, root) for root in _OPTIONAL_INTEGRATION_ROOTS):
            return True
        tb = tb.tb_next
    return False


def _is_optional_integration_entrypoint_missing(missing: str) -> bool:
    """Check whether the missing module is a public optional integration entrypoint."""
    if missing in _OPTIONAL_INTEGRATION_PACKAGES:
        return True

    for package, entrypoints in _OPTIONAL_INTEGRATION_ENTRYPOINT_MODULES.items():
        if any(missing == f"{package}.{entrypoint}" for entrypoint in entrypoints):
            return True
    return False


def _is_optional_dependency_error(exc_type, exc_value, seen: set[int] | None = None) -> bool:
    """Check if the exception is an import error that is expected when an optional
    integration extra is not installed.

    These are environment issues (the user imported, e.g., ``blaxel.openai``
    without ``pip install blaxel[openai]``, or runs a stripped/partial install
    that is missing the integration's modules) rather than SDK defects, so they
    should not be reported to Sentry.
    """
    if not (exc_type and issubclass(exc_type, ImportError)):
        return False

    if seen is None:
        seen = set()
    exc_id = id(exc_value)
    if exc_id in seen:
        return False
    seen.add(exc_id)

    # Name of the module that could not be imported, when available
    # (e.g. "blaxel.openai.model", "agents", "opentelemetry.exporter.otlp").
    missing = getattr(exc_value, "name", None) or ""

    # 1) A public optional integration entrypoint itself is unavailable -- e.g.
    #    a stripped/partial install missing ``blaxel/openai/model.py``,
    #    surfacing as ModuleNotFoundError("No module named 'blaxel.openai.model'").
    #    Do not suppress deeper ``blaxel.<integration>.*`` misses: those may be
    #    real SDK packaging or internal import bugs and should still reach Sentry.
    if _is_optional_integration_entrypoint_missing(missing):
        return True

    # 2) A known optional third-party dependency could not be imported.
    msg = str(exc_value).lower()
    if any(dep in missing for dep in _OPTIONAL_DEPENDENCIES) or any(
        dep in msg for dep in _OPTIONAL_DEPENDENCIES
    ):
        return True

    # 3) Optional integration import guards wrap the original import failure in
    #    a friendly ImportError with no module name. Suppress that wrapper when
    #    its explicit cause is already known optional-import noise.
    cause = getattr(exc_value, "__cause__", None)
    if isinstance(cause, ImportError) and _is_optional_dependency_error(type(cause), cause, seen):
        return True

    # 4) A non-blaxel (third-party) import failed while loading an optional
    #    integration package -- i.e. the matching extra is not installed. Only
    #    treat non-blaxel modules this way so that genuine SDK import bugs (which
    #    fail on a "blaxel.*" module) are still captured.
    if missing and not missing.startswith("blaxel") and _has_optional_integration_frame(exc_value):
        return True

    return False


def _should_capture_unhandled_exception(exc_type, exc_value) -> bool:
    """Return whether an unhandled exception represents an SDK failure."""
    if not exc_type or exc_value is None or not _is_from_sdk(exc_value):
        return False
    if issubclass(exc_type, _IGNORED_EXCEPTIONS):
        return False
    return not _is_optional_dependency_error(exc_type, exc_value)


def _filter_reportable_exception(exc_value: BaseException) -> BaseException | None:
    """Keep reportable SDK leaves while preserving an exception group's structure."""
    if isinstance(exc_value, _EXCEPTION_GROUP_TYPES):

        def is_reportable_leaf(exception: BaseException) -> bool:
            return not isinstance(
                exception, _EXCEPTION_GROUP_TYPES
            ) and _should_capture_unhandled_exception(type(exception), exception)

        return getattr(exc_value, "subgroup")(is_reportable_leaf)

    if _should_capture_unhandled_exception(type(exc_value), exc_value):
        return exc_value
    return None


def _capture_unhandled_exception(exc_value: BaseException | None, mechanism_type: str) -> None:
    """Capture one filtered event for an unhandled exception or exception group."""
    if exc_value is None:
        return
    reportable_exception = _filter_reportable_exception(exc_value)
    if reportable_exception is not None:
        capture_exception(reportable_exception, mechanism_type)


def _capture_unhandled_exception_safely(
    exc_value: BaseException | None, mechanism_type: str
) -> None:
    """Keep telemetry classification failures out of application exception paths."""
    try:
        _capture_unhandled_exception(exc_value, mechanism_type)
    except Exception:
        pass


def _drain_background_capture_queue(capture_queue: Queue[Any]) -> None:
    """Deliver queued hook events serially outside the failing runtime surface."""
    while True:
        item = capture_queue.get()
        try:
            if item is _BACKGROUND_CAPTURE_STOP:
                return
            exc_value, mechanism_type = item
            _capture_unhandled_exception_safely(exc_value, mechanism_type)
        finally:
            capture_queue.task_done()


def _start_background_capture_worker() -> None:
    """Start the process-wide bounded capture worker during SDK initialization."""
    global _background_capture_thread
    with _background_worker_init_lock:
        if _background_capture_thread is not None and _background_capture_thread.is_alive():
            return
        try:
            capture_queue = _background_capture_queue
            worker = threading.Thread(
                target=_drain_background_capture_queue,
                args=(capture_queue,),
                name="blaxel-sentry-capture",
                daemon=True,
            )
            _background_capture_thread = worker
            worker.start()
        except Exception:
            _background_capture_thread = None


def _stop_background_capture_worker(timeout: float = 1.0) -> None:
    """Stop the delivery worker after pending capture has been flushed."""
    global _background_capture_thread
    worker = _background_capture_thread
    if worker is None or not worker.is_alive():
        return
    try:
        _background_capture_queue.put_nowait(_BACKGROUND_CAPTURE_STOP)
    except Full:
        return
    worker.join(timeout=max(timeout, 0.0))
    if not worker.is_alive():
        _background_capture_thread = None


def _capture_unhandled_exception_in_background(
    exc_value: BaseException | None, mechanism_type: str
) -> None:
    """Queue asyncio/thread/finalizer failures without blocking their runtime hook."""
    worker = _background_capture_thread
    if worker is None or not worker.is_alive():
        return
    try:
        _background_capture_queue.put_nowait((exc_value, mechanism_type))
    except Full:
        pass


def _blaxel_excepthook(exc_type, exc_value, exc_tb) -> None:
    """Capture an unhandled main-thread SDK exception, then preserve hook chaining."""
    try:
        _capture_unhandled_exception_in_background(exc_value, "excepthook")
    finally:
        if _original_excepthook is not None and _original_excepthook is not _blaxel_excepthook:
            _original_excepthook(exc_type, exc_value, exc_tb)


def _blaxel_threading_excepthook(args: Any) -> None:
    """Capture an unhandled worker-thread SDK exception, then preserve hook chaining."""
    try:
        _capture_unhandled_exception_in_background(args.exc_value, "threading")
    finally:
        if (
            _original_threading_excepthook is not None
            and _original_threading_excepthook is not _blaxel_threading_excepthook
        ):
            _original_threading_excepthook(args)


def _blaxel_unraisablehook(args: Any) -> None:
    """Capture an SDK exception Python could not otherwise raise."""
    try:
        if not sys.is_finalizing():
            _capture_unhandled_exception_in_background(args.exc_value, "unraisablehook")
    finally:
        if (
            _original_unraisablehook is not None
            and _original_unraisablehook is not _blaxel_unraisablehook
        ):
            _original_unraisablehook(args)


def _blaxel_asyncio_call_exception_handler(self: asyncio.BaseEventLoop, context: Any) -> None:
    """Capture abandoned task/callback failures, then run asyncio's existing handler."""
    try:
        _capture_unhandled_exception_in_background(context.get("exception"), "asyncio")
    finally:
        if (
            _original_asyncio_call_exception_handler is not None
            and _original_asyncio_call_exception_handler
            is not _blaxel_asyncio_call_exception_handler
        ):
            _original_asyncio_call_exception_handler(self, context)


def init_sentry() -> None:
    """Initialize the lightweight Sentry client for SDK error tracking."""
    global _handlers_registered, _original_excepthook, _original_threading_excepthook
    global _original_unraisablehook, _original_asyncio_call_exception_handler
    global _sentry_config, _sentry_initialized
    try:
        dsn = settings.sentry_dsn
        if not dsn:
            return

        # Parse DSN
        _sentry_config = _parse_dsn(dsn)
        if not _sentry_config:
            return

        # Only allow dev/prod environments
        if settings.env not in ("dev", "prod"):
            return

        _sentry_initialized = True

        # Register handlers only once, preserving the hooks that were installed
        # before the first concurrent caller entered initialization.
        with _handler_registration_lock:
            if not _handlers_registered:
                _start_background_capture_worker()

                # Capture only exceptions that reach a last-chance runtime boundary.
                # A trace hook runs at throw-time and reports exceptions that callers
                # subsequently handle, which turns expected SDK control flow into noise.
                _original_excepthook = sys.excepthook
                _original_threading_excepthook = threading.excepthook
                _original_unraisablehook = sys.unraisablehook
                _original_asyncio_call_exception_handler = (
                    asyncio.BaseEventLoop.call_exception_handler
                )
                sys.excepthook = _blaxel_excepthook
                threading.excepthook = _blaxel_threading_excepthook
                sys.unraisablehook = _blaxel_unraisablehook
                asyncio.BaseEventLoop.call_exception_handler = (
                    _blaxel_asyncio_call_exception_handler
                )
                _handlers_registered = True

                # Register atexit handler to flush pending events and stop the worker.
                atexit.register(_shutdown_sentry)

    except Exception as e:
        logger.debug(f"Error initializing Sentry: {e}")


def capture_exception(
    exception: BaseException | None = None, mechanism_type: str = "generic"
) -> None:
    """Capture an exception to Sentry.
    Only errors originating from SDK code will be captured.
    """
    if (
        not _sentry_initialized
        or not _sentry_config
        or exception is None
        or not _contains_sdk_exception(exception)
    ):
        return

    try:
        # Delivery is best effort. Runtime hooks already execute this work on the
        # bounded background worker, so a Sentry outage never blocks the caller.
        event = _error_to_sentry_event(exception, mechanism_type)
        _send_to_sentry(event)

    except Exception:
        # Silently fail - error capturing should never break the SDK
        pass


def flush_sentry(timeout: float = 2.0) -> None:
    """Wait up to ``timeout`` for the bounded background queue to drain."""
    if not _sentry_initialized:
        return

    deadline = time.monotonic() + max(timeout, 0.0)
    capture_queue = _background_capture_queue
    while capture_queue.unfinished_tasks and time.monotonic() < deadline:
        time.sleep(min(0.01, max(deadline - time.monotonic(), 0.0)))


def _shutdown_sentry() -> None:
    """Best-effort process-exit flush for the lightweight telemetry worker."""
    flush_sentry()
    _stop_background_capture_worker()


def is_sentry_initialized() -> bool:
    """Check if Sentry is initialized and available."""
    return _sentry_initialized

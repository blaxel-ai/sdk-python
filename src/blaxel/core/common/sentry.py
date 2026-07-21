import atexit
import json
import logging
import sys
import threading
import traceback
import uuid
from asyncio import CancelledError
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

import httpx

from .settings import settings

logger = logging.getLogger(__name__)

# Lightweight Sentry client using httpx - only captures SDK errors
_sentry_initialized = False
_captured_exceptions: set = set()  # Track already captured exceptions to avoid duplicates

# Parsed DSN components
_sentry_config: dict[str, str] | None = None

# Queue for pending events
_pending_events: list[dict[str, Any]] = []
_flush_lock = threading.Lock()
_handlers_registered = False

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

# Filesystem fragments used to detect an import error raised while loading one of
# the optional integration packages above (covers both POSIX and Windows paths).
_OPTIONAL_INTEGRATION_PATHS = tuple(
    f"blaxel/{pkg.rsplit('.', 1)[-1]}/" for pkg in _OPTIONAL_INTEGRATION_PACKAGES
) + tuple(f"blaxel\\{pkg.rsplit('.', 1)[-1]}\\" for pkg in _OPTIONAL_INTEGRATION_PACKAGES)

# SDK path patterns to identify errors originating from our SDK
_SDK_PATTERNS = [
    "blaxel/",
    "blaxel\\",
    "site-packages/blaxel",
    "site-packages\\blaxel",
]


def _is_from_sdk(error: Exception) -> bool:
    """Check if an error originated from SDK code based on stack trace."""
    tb = error.__traceback__
    if not tb:
        return False

    # Walk through the traceback
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        if any(pattern in filename for pattern in _SDK_PATTERNS):
            return True
        tb = tb.tb_next

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


def _parse_stack_trace(exc: Exception) -> list[dict[str, Any]]:
    """Parse exception traceback into Sentry-compatible frames."""
    frames: list[dict[str, Any]] = []
    tb = traceback.extract_tb(exc.__traceback__)

    for frame in tb:
        frames.append(
            {
                "filename": frame.filename,
                "function": frame.name or "<anonymous>",
                "lineno": frame.lineno,
                "colno": 0,
            }
        )

    return frames


def _error_to_sentry_event(error: Exception) -> dict[str, Any]:
    """Convert an Exception to a Sentry event payload."""
    frames = _parse_stack_trace(error)

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
        "exception": {
            "values": [
                {
                    "type": type(error).__name__,
                    "value": str(error),
                    "stacktrace": {"frames": frames},
                }
            ]
        },
    }


def _send_to_sentry(event: dict[str, Any]) -> None:
    """Send an event to Sentry using httpx."""
    if not _sentry_config:
        return

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
        httpx.post(
            envelope_url,
            headers={
                "Content-Type": "application/x-sentry-envelope",
                "X-Sentry-Auth": f"Sentry sentry_version=7, sentry_client=blaxel-sdk/{settings.version}, sentry_key={public_key}",
            },
            content=envelope,
            timeout=5.0,
        )
    except Exception:
        # Silently fail - error reporting should never break the SDK
        pass


def _get_exception_key(exc_type, exc_value, frame) -> str:
    """Generate a unique key for an exception based on type, message, and origin."""
    exc_name = exc_type.__name__ if exc_type else "Unknown"
    exc_msg = str(exc_value) if exc_value else ""
    tb = getattr(exc_value, "__traceback__", None)
    if tb:
        while tb.tb_next:
            tb = tb.tb_next
        origin = f"{tb.tb_frame.f_code.co_filename}:{tb.tb_lineno}"
    else:
        origin = f"{frame.f_code.co_filename}:{frame.f_lineno}"
    return f"{exc_name}:{exc_msg}:{origin}"


def _has_optional_integration_frame(exc_value) -> bool:
    """Check whether an exception traceback passed through an integration module."""
    tb = getattr(exc_value, "__traceback__", None)
    while tb is not None:
        filename = tb.tb_frame.f_code.co_filename
        if any(path in filename for path in _OPTIONAL_INTEGRATION_PATHS):
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


def _trace_blaxel_exceptions(frame, event, arg):
    """Trace function that captures exceptions from blaxel SDK code."""
    if event == "exception":
        exc_type, exc_value, exc_tb = arg

        # Skip control flow exceptions (not actual errors)
        if exc_type and issubclass(exc_type, _IGNORED_EXCEPTIONS):
            return _trace_blaxel_exceptions

        # Skip import errors for optional dependencies (expected when not installed)
        if _is_optional_dependency_error(exc_type, exc_value):
            return _trace_blaxel_exceptions

        filename = frame.f_code.co_filename

        # Only capture if it's from blaxel in site-packages
        if "site-packages/blaxel" in filename:
            # Avoid capturing the same exception multiple times using a content-based key
            exc_key = _get_exception_key(exc_type, exc_value, frame)
            if exc_key not in _captured_exceptions:
                _captured_exceptions.add(exc_key)
                capture_exception(exc_value)
                # Clean up old exception keys to prevent memory leak
                if len(_captured_exceptions) > 1000:
                    _captured_exceptions.clear()

    return _trace_blaxel_exceptions


def init_sentry() -> None:
    """Initialize the lightweight Sentry client for SDK error tracking."""
    global _sentry_initialized, _sentry_config, _handlers_registered
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

        # Register handlers only once
        if not _handlers_registered:
            _handlers_registered = True

            # Install trace function to automatically capture SDK exceptions
            sys.settrace(_trace_blaxel_exceptions)
            threading.settrace(_trace_blaxel_exceptions)

            # Register atexit handler to flush pending events
            atexit.register(flush_sentry)

    except Exception as e:
        logger.debug(f"Error initializing Sentry: {e}")


def capture_exception(exception: Exception | None = None) -> None:
    """Capture an exception to Sentry.
    Only errors originating from SDK code will be captured.
    """
    if not _sentry_initialized or not _sentry_config or exception is None:
        return

    try:
        # Generate unique key to prevent duplicate captures
        exc_key = f"{type(exception).__name__}:{str(exception)}"
        if exc_key in _captured_exceptions:
            return

        _captured_exceptions.add(exc_key)

        # Clean up old exception keys to prevent memory leak
        if len(_captured_exceptions) > 1000:
            _captured_exceptions.clear()

        # Convert error to Sentry event and queue it
        event = _error_to_sentry_event(exception)
        with _flush_lock:
            _pending_events.append(event)

        # Send immediately (fire and forget)
        _send_to_sentry(event)

    except Exception:
        # Silently fail - error capturing should never break the SDK
        pass


def flush_sentry(timeout: float = 2.0) -> None:
    """Flush pending Sentry events."""
    if not _sentry_initialized:
        return

    with _flush_lock:
        if not _pending_events:
            return

        events_to_send = _pending_events.copy()
        _pending_events.clear()

    # Send all pending events
    for event in events_to_send:
        try:
            _send_to_sentry(event)
        except Exception:
            # Silently fail
            pass


def is_sentry_initialized() -> bool:
    """Check if Sentry is initialized and available."""
    return _sentry_initialized

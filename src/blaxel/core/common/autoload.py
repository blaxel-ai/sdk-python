import atexit
import logging
import sys
import threading
from asyncio import CancelledError

from sentry_sdk import Client, Hub

from ..client import client
from ..client.response_interceptor import (
    response_interceptors_async,
    response_interceptors_sync,
)
from ..sandbox.client import client as client_sandbox
from .settings import settings

logger = logging.getLogger(__name__)

# Isolated Sentry hub for SDK-only error tracking (doesn't interfere with user's Sentry)
_sentry_hub: Hub | None = None
_captured_exceptions: set = set()  # Track already captured exceptions to avoid duplicates

# Exceptions that are part of normal control flow and should not be captured
_IGNORED_EXCEPTIONS = (
    StopIteration,       # Iterator exhaustion
    StopAsyncIteration,  # Async iterator exhaustion
    GeneratorExit,       # Generator cleanup
    KeyboardInterrupt,   # User interrupt (Ctrl+C)
    SystemExit,          # Program exit
    CancelledError,      # Async task cancellation
)

# Optional dependencies that may not be installed - import errors for these are expected
_OPTIONAL_DEPENDENCIES = (
    'opentelemetry',
)


def _get_exception_key(exc_type, exc_value, frame) -> str:
    """Generate a unique key for an exception based on type, message, and origin."""
    # Use type name + message + original file/line where exception was raised
    # This ensures the same logical exception is only captured once
    exc_name = exc_type.__name__ if exc_type else "Unknown"
    exc_msg = str(exc_value) if exc_value else ""
    # Get the original traceback location (where exception was first raised)
    tb = getattr(exc_value, '__traceback__', None)
    if tb:
        # Walk to the deepest frame (origin of exception)
        while tb.tb_next:
            tb = tb.tb_next
        origin = f"{tb.tb_frame.f_code.co_filename}:{tb.tb_lineno}"
    else:
        origin = f"{frame.f_code.co_filename}:{frame.f_lineno}"
    return f"{exc_name}:{exc_msg}:{origin}"


def _is_optional_dependency_error(exc_type, exc_value) -> bool:
    """Check if the exception is an import error for an optional dependency."""
    # ModuleNotFoundError is a subclass of ImportError, so checking ImportError covers both
    if exc_type and issubclass(exc_type, ImportError):
        msg = str(exc_value).lower()
        return any(dep in msg for dep in _OPTIONAL_DEPENDENCIES)
    return False


def _trace_blaxel_exceptions(frame, event, arg):
    """Trace function that captures exceptions from blaxel SDK code."""
    if event == 'exception':
        exc_type, exc_value, exc_tb = arg

        # Skip control flow exceptions (not actual errors)
        if exc_type and issubclass(exc_type, _IGNORED_EXCEPTIONS):
            return _trace_blaxel_exceptions

        # Skip import errors for optional dependencies (expected when not installed)
        if _is_optional_dependency_error(exc_type, exc_value):
            return _trace_blaxel_exceptions

        filename = frame.f_code.co_filename

        # Only capture if it's from blaxel in site-packages
        if 'site-packages/blaxel' in filename:
            # Avoid capturing the same exception multiple times using a content-based key
            exc_key = _get_exception_key(exc_type, exc_value, frame)
            if exc_key not in _captured_exceptions:
                _captured_exceptions.add(exc_key)
                capture_exception(exc_value)
                # Clean up old exception keys to prevent memory leak
                if len(_captured_exceptions) > 1000:
                    _captured_exceptions.clear()

    return _trace_blaxel_exceptions


def sentry() -> None:
    """Initialize an isolated Sentry client for SDK error tracking."""
    global _sentry_hub
    try:
        dsn = settings.sentry_dsn
        if not dsn:
            return

        # Create an isolated client that won't interfere with user's Sentry
        sentry_client = Client(
            dsn=dsn,
            environment=settings.env,
            release=f"sdk-python@{settings.version}",
            default_integrations=False,
            auto_enabling_integrations=False,
        )
        _sentry_hub = Hub(sentry_client)

        # Set SDK-specific tags
        with _sentry_hub.configure_scope() as scope:
            scope.set_tag("blaxel.workspace", settings.workspace)
            scope.set_tag("blaxel.version", settings.version)
            scope.set_tag("blaxel.commit", settings.commit)

        # Install trace function to automatically capture SDK exceptions
        sys.settrace(_trace_blaxel_exceptions)
        threading.settrace(_trace_blaxel_exceptions)

        # Register atexit handler to flush pending events
        atexit.register(_flush_sentry)

    except Exception as e:
        logger.debug(f"Error initializing Sentry: {e}")


def capture_exception(exception: Exception | None = None) -> None:
    """Capture an exception to the SDK's isolated Sentry hub."""
    if _sentry_hub is not None and _sentry_hub.client is not None:
        _sentry_hub.capture_exception(exception)


def _flush_sentry():
    """Flush pending Sentry events on program exit."""
    if _sentry_hub is not None and _sentry_hub.client is not None:
        _sentry_hub.client.flush(timeout=2)


def telemetry() -> None:
    from blaxel.telemetry import telemetry_manager

    telemetry_manager.initialize(settings)


def autoload() -> None:
    client.with_base_url(settings.base_url)
    client.with_auth(settings.auth)

    # Register response interceptors for authentication error handling
    # Access the underlying httpx clients and add event hooks
    # Use sync interceptors for sync clients and async interceptors for async clients
    httpx_client = client.get_httpx_client()
    httpx_client.event_hooks["response"] = response_interceptors_sync

    httpx_async_client = client.get_async_httpx_client()
    httpx_async_client.event_hooks["response"] = response_interceptors_async

    httpx_sandbox_client = client_sandbox.get_httpx_client()
    httpx_sandbox_client.event_hooks["response"] = response_interceptors_sync

    httpx_sandbox_async_client = client_sandbox.get_async_httpx_client()
    httpx_sandbox_async_client.event_hooks["response"] = response_interceptors_async

    if settings.tracking:
        try:
            sentry()
        except Exception:
            pass

    try:
        telemetry()
    except Exception:
        pass

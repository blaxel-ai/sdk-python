import atexit
import logging
import sys
import threading

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


def _trace_blaxel_exceptions(frame, event, arg):
    """Trace function that captures exceptions from blaxel SDK code."""
    if event == 'exception':
        exc_type, exc_value, exc_tb = arg
        filename = frame.f_code.co_filename

        # Only capture if it's from blaxel in site-packages
        if 'site-packages/blaxel' in filename:
            # Avoid capturing the same exception multiple times
            exc_id = id(exc_value)
            if exc_id not in _captured_exceptions:
                _captured_exceptions.add(exc_id)
                capture_exception(exc_value)
                # Clean up old exception IDs to prevent memory leak
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

    try:
        sentry()
    except Exception:
        pass

    try:
        telemetry()
    except Exception:
        pass

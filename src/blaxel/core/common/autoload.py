import atexit
import logging
import sys

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
_original_excepthook = None


def _is_from_blaxel_sdk(tb) -> bool:
    """Check if any frame in the traceback is from the blaxel SDK (installed package)."""
    while tb is not None:
        frame = tb.tb_frame
        filename = frame.f_code.co_filename
        # Check if it's from blaxel package
        if "blaxel" in filename and "site-packages" in filename:
            return True
        tb = tb.tb_next
    return False


def _sentry_excepthook(exc_type, exc_value, exc_tb):
    """Custom excepthook that captures SDK exceptions to our isolated Sentry hub."""
    # Always call the original excepthook first (to preserve normal behavior)
    if _original_excepthook:
        _original_excepthook(exc_type, exc_value, exc_tb)

    # Capture to our isolated hub if it's from the SDK
    if _sentry_hub is not None and _sentry_hub.client is not None and exc_tb is not None:
        if _is_from_blaxel_sdk(exc_tb):
            _sentry_hub.capture_exception((exc_type, exc_value, exc_tb))
            # Flush immediately to ensure the event is sent before program exits
            _sentry_hub.client.flush(timeout=2)

def sentry() -> None:
    """Initialize an isolated Sentry client for SDK error tracking."""
    global _sentry_hub, _original_excepthook
    try:
        dsn = settings.sentry_dsn
        if not dsn:
            return

        # Create an isolated client that won't interfere with user's Sentry
        sentry_client = Client(
            dsn=dsn,
            environment=settings.env,
            release=f"sdk-python@{settings.version}",
            default_integrations=False,  # No integrations - we only want manual capture
            auto_enabling_integrations=False,
        )
        _sentry_hub = Hub(sentry_client)

        # Set SDK-specific tags
        with _sentry_hub.configure_scope() as scope:
            scope.set_tag("blaxel.workspace", settings.workspace)
            scope.set_tag("blaxel.version", settings.version)
            scope.set_tag("blaxel.commit", settings.commit)

        # Install custom excepthook to automatically capture SDK exceptions
        _original_excepthook = sys.excepthook
        sys.excepthook = _sentry_excepthook

        # Register atexit handler to flush pending events
        atexit.register(_flush_sentry)

    except Exception as e:
        logger.debug(f"Error initializing Sentry: {e}")


def capture_exception(exception: Exception | None = None) -> None:
    """Capture an exception in the SDK's isolated Sentry hub."""
    if _sentry_hub is not None and _sentry_hub.client is not None:
        _sentry_hub.capture_exception(exception)
        _sentry_hub.client.flush(timeout=2)


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

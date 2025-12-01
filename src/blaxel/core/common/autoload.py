import logging

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


def _before_send(event, hint):
    """Filter to only capture errors originating from blaxel SDK code."""
    exc_info = hint.get("exc_info")
    if exc_info:
        tb = exc_info[2]
        # Walk the traceback to check if any frame is from blaxel
        while tb is not None:
            frame = tb.tb_frame
            filename = frame.f_code.co_filename
            if "blaxel" in filename and "site-packages" in filename:
                return event
            tb = tb.tb_next
    return None  # Don't send events not from blaxel SDK


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
            before_send=_before_send,
            default_integrations=False,  # No integrations - we only want manual capture
            auto_enabling_integrations=False,
        )
        _sentry_hub = Hub(sentry_client)

        # Set SDK-specific tags
        with _sentry_hub.configure_scope() as scope:
            scope.set_tag("blaxel.workspace", settings.workspace)
            scope.set_tag("blaxel.version", settings.version)
            scope.set_tag("blaxel.commit", settings.commit)

    except Exception as e:
        logger.debug(f"Error initializing Sentry: {e}")


def capture_exception(exception: Exception) -> None:
    """Capture an exception in the SDK's isolated Sentry hub."""
    if _sentry_hub is not None:
        _sentry_hub.capture_exception(exception)


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

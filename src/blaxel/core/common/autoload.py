import asyncio
import logging
import threading
from urllib.parse import urlparse

from ..client import client
from ..client.response_interceptor import (
    response_interceptors_async,
    response_interceptors_sync,
)
from ..sandbox.client import client as client_sandbox
from .h3warm import H3WarmSession, establish_h3_best_effort
from .sentry import init_sentry
from .settings import settings

logger = logging.getLogger(__name__)

# Module-level H3 session for API endpoint warming
_api_h3_session: H3WarmSession | None = None


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
            init_sentry()
        except Exception:
            pass

    try:
        telemetry()
    except Exception:
        pass

    # Warm H3 connection to API endpoint in background
    try:
        api_hostname = urlparse(settings.base_url).hostname
        if api_hostname:
            _warm_api_h3(api_hostname)
    except Exception:
        pass


def _warm_api_h3(hostname: str) -> None:
    """Start background H3 connection warming for the API endpoint."""
    global _api_h3_session

    def _do_warm() -> None:
        global _api_h3_session
        try:
            loop = asyncio.new_event_loop()
            _api_h3_session = loop.run_until_complete(establish_h3_best_effort(hostname))
            loop.close()
        except Exception:
            pass

    thread = threading.Thread(target=_do_warm, daemon=True)
    thread.start()


def close_api_h3_session() -> None:
    """Close the API H3 warming session. Call this for clean shutdown."""
    global _api_h3_session
    if _api_h3_session is not None:
        _api_h3_session.close()
        _api_h3_session = None

import logging
import threading
from urllib.parse import urlparse

from ..client import client
from ..client.response_interceptor import (
    response_interceptors_async,
    response_interceptors_sync,
)
from ..sandbox.client import client as client_sandbox
from .h3transport import pool as h3_pool
from .sentry import init_sentry
from .settings import settings

logger = logging.getLogger(__name__)


def telemetry() -> None:
    from blaxel.telemetry import telemetry_manager

    telemetry_manager.initialize(settings)


def autoload() -> None:
    client.with_base_url(settings.base_url)
    client.with_auth(settings.auth)

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

    # Pre-warm H3 connection to API endpoint in background
    try:
        api_hostname = urlparse(settings.base_url).hostname
        if api_hostname:
            _warm_api_h3(api_hostname)
    except Exception:
        pass


def _warm_api_h3(hostname: str) -> None:
    """Pre-warm the H3 pool for the API endpoint in a background thread."""

    def _do_warm() -> None:
        try:
            h3_pool.get_sync_transport(hostname, 443)
        except Exception:
            pass

    thread = threading.Thread(target=_do_warm, daemon=True)
    thread.start()

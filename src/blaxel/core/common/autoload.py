import logging

from ..client import client
from ..client.response_interceptor import (
    response_interceptors_async,
    response_interceptors_sync,
)
from ..sandbox.client import client as client_sandbox
from .sentry import init_sentry
from .settings import settings

logger = logging.getLogger(__name__)


def telemetry() -> None:
    from blaxel.telemetry import telemetry_manager

    telemetry_manager.initialize(settings)


def autoload() -> None:
    client.with_base_url(settings.base_url)
    client.with_auth(settings.auth)
    # Send SDK-identifying headers on every control-plane request so backend
    # observability can classify Python SDK traffic and list endpoints return
    # cursor-paginated `{data, meta}` responses (>= 2026-04-28). Without the
    # User-Agent httpx falls back to `python-httpx/<version>`, which is tracked
    # as a generic API request instead of SDK usage.
    client.with_headers(
        {
            "Blaxel-Version": settings.api_version,
            "User-Agent": settings.headers["User-Agent"],
        }
    )

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

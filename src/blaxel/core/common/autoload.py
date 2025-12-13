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

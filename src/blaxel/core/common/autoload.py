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


def _set_user_agent(request) -> None:
    # Resolved per request so a later `settings.integration = ...` is honored.
    request.headers["User-Agent"] = settings.user_agent


async def _set_user_agent_async(request) -> None:
    _set_user_agent(request)


def autoload() -> None:
    client.with_base_url(settings.base_url)
    client.with_auth(settings.auth)
    # Send the Blaxel-Version header on every control-plane request so list
    # endpoints, including images, return cursor-paginated `{data, meta}` responses.
    # Without it the API falls back to legacy bare-array listings and pagination
    # (limit/cursor/next_page) is silently ignored.
    client.with_headers({"Blaxel-Version": settings.api_version})

    # Register request/response hooks through the client so they survive re-creation
    # of the httpx clients (the async client is rebuilt whenever the event loop changes).
    # Use sync hooks for sync clients and async hooks for async clients.
    client.with_event_hooks(
        sync_hooks={"request": [_set_user_agent], "response": response_interceptors_sync},
        async_hooks={
            "request": [_set_user_agent_async],
            "response": response_interceptors_async,
        },
    )
    client_sandbox.with_event_hooks(
        sync_hooks={"response": response_interceptors_sync},
        async_hooks={"response": response_interceptors_async},
    )

    if settings.tracking:
        try:
            init_sentry()
        except Exception:
            pass

    try:
        telemetry()
    except Exception:
        pass

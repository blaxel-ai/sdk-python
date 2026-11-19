"""Preview and session times are sent in UTC, and empty preview lists are empty.

The control plane reads every expiry as RFC 3339, so a timestamp must carry its
offset (``Z`` here) and be the real UTC instant, whatever the machine's time zone.
"""

import json
import time
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import httpx
import pytest

from blaxel.core.client.client import client as api_client
from blaxel.core.client.models import Preview
from blaxel.core.sandbox.default import preview as async_preview
from blaxel.core.sandbox.default.session import SandboxSessions
from blaxel.core.sandbox.sync import preview as sync_preview
from blaxel.core.sandbox.sync.session import SyncSandboxSessions
from blaxel.core.sandbox.types import SessionWithToken

FORMATTERS = [sync_preview.to_utc_z, async_preview.to_utc_z]


def parse_utc(value: str) -> datetime:
    assert value.endswith("Z"), value
    return datetime.fromisoformat(value[:-1]).replace(tzinfo=timezone.utc)


@pytest.fixture
def local_time_zone(monkeypatch):
    """Run the test with the machine clock in another time zone."""
    if not hasattr(time, "tzset"):
        pytest.skip("time.tzset is not available on this platform")

    def set_zone(name: str) -> None:
        monkeypatch.setenv("TZ", name)
        time.tzset()

    yield set_zone
    monkeypatch.undo()
    time.tzset()


@pytest.mark.parametrize("to_utc_z", FORMATTERS)
def test_aware_datetime_outside_utc_is_converted(to_utc_z):
    paris = timezone(timedelta(hours=2))
    value = datetime(2026, 11, 18, 14, 30, 5, 123000, tzinfo=paris)

    assert to_utc_z(value) == "2026-11-18T12:30:05.123000Z"


@pytest.mark.parametrize("to_utc_z", FORMATTERS)
def test_utc_and_naive_datetimes_keep_their_wall_time(to_utc_z):
    assert to_utc_z(datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)) == "2026-11-18T12:00:00Z"
    assert to_utc_z(datetime(2026, 11, 18, 12, 0)) == "2026-11-18T12:00:00Z"


@pytest.fixture
def serve(monkeypatch):
    """Answer the SDK's requests with ``handler(request) -> (status, json)``."""
    requests: list[httpx.Request] = []

    def install(handler):
        def respond(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            status, body = handler(request)
            return httpx.Response(status, json=body, request=request)

        transport = httpx.MockTransport(respond)
        sync_http = httpx.Client(base_url="https://api.blaxel.test", transport=transport)
        async_http = httpx.AsyncClient(base_url="https://api.blaxel.test", transport=transport)
        monkeypatch.setattr(type(api_client), "get_httpx_client", lambda self: sync_http)
        monkeypatch.setattr(type(api_client), "get_async_httpx_client", lambda self: async_http)
        return requests

    return install


def test_sync_empty_preview_list_is_empty(serve):
    serve(lambda request: (200, []))
    previews = sync_preview.SyncSandboxPreviews(
        SimpleNamespace(metadata=SimpleNamespace(name="sbx"))
    )

    assert previews.list() == []


def test_sync_empty_preview_token_list_is_empty(serve):
    serve(lambda request: (200, []))
    preview = sync_preview.SyncSandboxPreview(
        Preview.from_dict({"metadata": {"name": "web", "resourceName": "sbx"}, "spec": {}})
    )

    assert preview.tokens.list() == []


def session_server(request: httpx.Request):
    body = json.loads(request.content)
    if request.url.path.endswith("/tokens"):
        spec = {"token": "secret", "expiresAt": body["spec"]["expiresAt"]}
        return 200, {"metadata": {"name": "token"}, "spec": spec}
    metadata = {**body["metadata"], "resourceName": "sbx"}
    return 200, {"metadata": metadata, "spec": {**body["spec"], "url": "https://preview.test"}}


def sent_expiries(requests: list[httpx.Request]) -> list[str]:
    preview, token = (json.loads(request.content) for request in requests)
    return [preview["spec"]["expires"], token["spec"]["expiresAt"]]


def assert_one_day_from_now_utc(expiries: list[str]) -> None:
    expected = datetime.now(timezone.utc) + timedelta(days=1)
    for value in expiries:
        assert abs(parse_utc(value) - expected) < timedelta(minutes=1), value


@pytest.mark.parametrize("zone", ["America/Los_Angeles", "Asia/Tokyo"])
def test_sync_session_default_expiry_is_one_day_from_now_in_utc(serve, local_time_zone, zone):
    local_time_zone(zone)
    requests = serve(session_server)

    SyncSandboxSessions(SimpleNamespace(metadata=SimpleNamespace(name="sbx"))).create()

    assert_one_day_from_now_utc(sent_expiries(requests))


@pytest.mark.asyncio
@pytest.mark.parametrize("zone", ["America/Los_Angeles", "Asia/Tokyo"])
async def test_async_session_default_expiry_is_one_day_from_now_in_utc(
    serve, local_time_zone, zone
):
    local_time_zone(zone)
    requests = serve(session_server)

    await SandboxSessions(SimpleNamespace(metadata=SimpleNamespace(name="sbx"))).create()

    assert_one_day_from_now_utc(sent_expiries(requests))


def existing_session(expires_in: timedelta) -> SessionWithToken:
    expires_at = datetime.now(timezone.utc) + expires_in
    return SessionWithToken(
        name="session-1",
        url="https://preview.test",
        token="secret",
        expires_at=expires_at.isoformat().replace("+00:00", "Z"),
    )


# The machine clock is UTC-8 or UTC+9; the reuse threshold is one hour.
REUSE_CASES = [
    ("America/Los_Angeles", timedelta(minutes=30), True),
    ("Asia/Tokyo", timedelta(hours=3), False),
]


@pytest.mark.parametrize(("zone", "expires_in", "replaced"), REUSE_CASES)
def test_sync_create_if_expired_compares_in_utc(local_time_zone, zone, expires_in, replaced):
    local_time_zone(zone)
    sessions = SyncSandboxSessions(SimpleNamespace(metadata=SimpleNamespace(name="sbx")))
    current = existing_session(expires_in)
    fresh = existing_session(timedelta(days=1))
    deleted = []
    sessions.list = lambda: [current]
    sessions.delete = deleted.append
    sessions.create = lambda options: fresh

    result = sessions.create_if_expired(delta_seconds=3600)

    assert result is (fresh if replaced else current)
    assert deleted == (["session-1"] if replaced else [])


@pytest.mark.asyncio
@pytest.mark.parametrize(("zone", "expires_in", "replaced"), REUSE_CASES)
async def test_async_create_if_expired_compares_in_utc(local_time_zone, zone, expires_in, replaced):
    local_time_zone(zone)
    sessions = SandboxSessions(SimpleNamespace(metadata=SimpleNamespace(name="sbx")))
    current = existing_session(expires_in)
    fresh = existing_session(timedelta(days=1))
    deleted = []

    async def list_sessions():
        return [current]

    async def delete(name):
        deleted.append(name)

    async def create(options):
        return fresh

    sessions.list = list_sessions
    sessions.delete = delete
    sessions.create = create

    result = await sessions.create_if_expired(delta_seconds=3600)

    assert result is (fresh if replaced else current)
    assert deleted == (["session-1"] if replaced else [])

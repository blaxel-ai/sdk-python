"""Unit tests for sandbox creations that go on after the create call has answered.

The control plane answers 202 Accepted, with the sandbox still DEPLOYING, when it
cannot finish a creation while the request is open; an edge in front of it can
cut a slow request with a 504 while the creation keeps running. In both cases
SandboxInstance.create reads the sandbox until it is DEPLOYED (and returns it) or
FAILED (and raises). A creation answered 200 is returned as is, without reading
the sandbox again.
"""

import json
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from unittest.mock import AsyncMock

import httpx
import pytest

from blaxel.core import SandboxAPIError, SandboxInstance, SyncSandboxInstance
from blaxel.core.client import errors as client_errors
from blaxel.core.client.client import Client
from blaxel.core.client.models import Sandbox
from blaxel.core.client.types import Response
from blaxel.core.sandbox.default.sandbox import _unix_time

ASYNC_MODULE = "blaxel.core.sandbox.default.sandbox"
SYNC_MODULE = "blaxel.core.sandbox.sync.sandbox"
REGION = "us-pdx-1"
NAME = "sbx-accepted"
NAMED = {"name": NAME, "region": REGION}
LONG_AGO = "2020-01-01T00:00:00Z"


def _timestamp(moment: datetime) -> str:
    # As the control plane sends it: RFC 3339 in UTC, with nanoseconds.
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "123Z"


def _sandbox(status: str, name: str = NAME, created_at: str | None = None, **extra) -> dict:
    return {
        "metadata": {"name": name, "createdAt": created_at or _timestamp(datetime.now())},
        "spec": {"runtime": {"image": "blaxel/base-image:latest"}, "region": REGION},
        "status": status,
        **extra,
    }


def _failed(reason: str) -> dict:
    return _sandbox(
        "FAILED",
        events=[
            {"status": "DEPLOYING", "message": "Deploying sandbox"},
            {"status": "FAILED", "message": reason, "type": "deployment.failed"},
        ],
    )


def _ok(status: str, **extra) -> httpx.Response:
    return httpx.Response(200, json=_sandbox(status, **extra))


ACCEPTED = httpx.Response(202, json=_sandbox("DEPLOYING"))
GATEWAY_TIMEOUT = httpx.Response(504, text="<html><body>504 Gateway Timeout</body></html>")
NOT_FOUND = httpx.Response(404, json={"error": "Sandbox not found", "code": 404})


class FakeAPI:
    """Answers the creation with ``created`` and each read with the next of ``reads``."""

    def __init__(self, created: httpx.Response, reads: list[httpx.Response] = ()):
        self.created = created
        self.reads = list(reads)
        self.requests: list[tuple[str, str]] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append((request.method, request.url.path))
        if request.method == "POST" and request.url.path == "/v0/sandboxes":
            answer = self.created
        elif request.method == "GET" and request.url.path == f"/v0/sandboxes/{NAME}":
            answer = self.reads.pop(0) if len(self.reads) > 1 else self.reads[0]
        else:
            answer = NOT_FOUND
        # A fresh copy each time: a response is read once, by one kind of client.
        return httpx.Response(answer.status_code, content=answer.content, headers=answer.headers)

    @property
    def reads_made(self) -> int:
        return sum(1 for method, _ in self.requests if method == "GET")


@pytest.fixture
def api(monkeypatch):
    def install(created: httpx.Response, reads: list[httpx.Response] = ()) -> FakeAPI:
        fake = FakeAPI(created, reads)
        mock_client = Client(
            base_url="https://api.test/v0",
            httpx_args={"transport": httpx.MockTransport(fake)},
        )
        for module in (ASYNC_MODULE, SYNC_MODULE):
            monkeypatch.setattr(f"{module}.client", mock_client)
            monkeypatch.setattr(f"{module}._creation_poll_delay", lambda _: 0)
        return fake

    return install


@pytest.fixture
def short_wait(monkeypatch):
    monkeypatch.setattr(f"{ASYNC_MODULE}.CREATION_WAIT_MAX_SECONDS", 0.05)


@pytest.fixture
def short_not_found(monkeypatch):
    monkeypatch.setattr(f"{ASYNC_MODULE}.CREATION_WAIT_NOT_FOUND_SECONDS", 0.05)


# 202 Accepted


async def test_202_waits_until_deployed(api):
    fake = api(ACCEPTED, [_ok("DEPLOYING"), _ok("DEPLOYED")])

    # No name: the server assigns one, and the 202 body carries it.
    instance = await SandboxInstance.create({"region": REGION})

    assert isinstance(instance, SandboxInstance)
    assert instance.metadata.name == NAME
    assert str(instance.status) == "DEPLOYED"
    assert fake.requests == [
        ("POST", "/v0/sandboxes"),
        ("GET", f"/v0/sandboxes/{NAME}"),
        ("GET", f"/v0/sandboxes/{NAME}"),
    ]


async def test_create_if_not_exists_202_waits_until_deployed(api):
    fake = api(ACCEPTED, [_ok("DEPLOYED")])

    instance = await SandboxInstance.create_if_not_exists(NAMED)

    assert str(instance.status) == "DEPLOYED"
    assert fake.reads_made == 1


async def test_202_is_told_by_status_code_once_the_client_models_it(api, monkeypatch):
    # A generated client that documents 202 parses it like a 200 instead of
    # raising it; the wait must not depend on which one is installed.
    fake = api(ACCEPTED, [_ok("DEPLOYED")])
    body = _sandbox("DEPLOYING")
    parsed_202 = Response(
        status_code=HTTPStatus.ACCEPTED,
        content=json.dumps(body).encode(),
        headers={},
        parsed=Sandbox.from_dict(body),
    )
    monkeypatch.setattr(
        f"{ASYNC_MODULE}.create_sandbox_detailed", AsyncMock(return_value=parsed_202)
    )

    instance = await SandboxInstance.create({"region": REGION})

    assert str(instance.status) == "DEPLOYED"
    assert fake.reads_made == 1


async def test_202_then_failed_raises_with_the_sandbox_reason(api):
    reason = "Sandbox creation failed | Cause: image pull timed out"
    fake = api(ACCEPTED, [_ok("DEPLOYING"), httpx.Response(200, json=_failed(reason))])

    with pytest.raises(SandboxAPIError) as excinfo:
        await SandboxInstance.create(NAMED)

    error = excinfo.value
    assert str(error) == f"Sandbox {NAME} is FAILED instead of DEPLOYED: {reason}"
    assert error.code == "DEPLOYMENT_FAILED"
    assert fake.reads_made == 2


async def test_202_then_failed_uses_a_fatal_infrastructure_error_as_reason(api):
    errors = [
        {"code": "VM_RESTARTED", "message": "restarted", "fatal": False},
        {"code": "VM_NETWORK_FAILURE", "message": "network setup failed", "fatal": True},
    ]
    api(ACCEPTED, [_ok("FAILED", errors=errors)])

    with pytest.raises(SandboxAPIError, match="FAILED instead of DEPLOYED: network setup failed$"):
        await SandboxInstance.create(NAMED)


async def test_202_then_failed_without_reason(api):
    api(ACCEPTED, [_ok("FAILED")])

    with pytest.raises(SandboxAPIError) as excinfo:
        await SandboxInstance.create(NAMED)

    assert str(excinfo.value) == f"Sandbox {NAME} is FAILED instead of DEPLOYED"


async def test_202_wait_survives_a_transient_read_failure(api):
    fake = api(ACCEPTED, [httpx.Response(503, text="service unavailable"), _ok("DEPLOYED")])

    instance = await SandboxInstance.create(NAMED)

    assert str(instance.status) == "DEPLOYED"
    assert fake.reads_made == 2


async def test_202_then_not_found_stops_the_wait(api):
    # The 202 comes after the record is saved: not found means it was deleted.
    fake = api(ACCEPTED, [NOT_FOUND])

    with pytest.raises(SandboxAPIError) as excinfo:
        await SandboxInstance.create(NAMED)

    assert excinfo.value.status == 404
    assert fake.reads_made == 1


async def test_202_wait_is_bounded(api, short_wait):
    fake = api(ACCEPTED, [_ok("DEPLOYING")])

    with pytest.raises(SandboxAPIError, match=f"^Sandbox {NAME} is still DEPLOYING after waiting"):
        await SandboxInstance.create(NAMED)

    assert fake.reads_made >= 1


# 504 Gateway Timeout


async def test_504_for_a_named_creation_waits_until_deployed(api):
    # The record can lag behind the creation: not found keeps the wait going.
    fake = api(GATEWAY_TIMEOUT, [NOT_FOUND, _ok("DEPLOYING"), _ok("DEPLOYED")])

    instance = await SandboxInstance.create(NAMED)

    assert str(instance.status) == "DEPLOYED"
    assert fake.reads_made == 3


async def test_504_then_failed_raises_with_the_sandbox_reason(api):
    api(GATEWAY_TIMEOUT, [httpx.Response(200, json=_failed("no capacity"))])

    with pytest.raises(SandboxAPIError) as excinfo:
        await SandboxInstance.create(NAMED)

    assert str(excinfo.value) == f"Sandbox {NAME} is FAILED instead of DEPLOYED: no capacity"
    assert excinfo.value.code == "DEPLOYMENT_FAILED"


async def test_504_for_an_unnamed_creation_raises_it(api):
    # The server picked the name and the 504 does not say it: nothing to read.
    fake = api(GATEWAY_TIMEOUT)

    with pytest.raises(client_errors.UnexpectedStatus) as excinfo:
        await SandboxInstance.create({"region": REGION})

    assert excinfo.value.status_code == 504
    assert fake.reads_made == 0


async def test_504_for_a_sandbox_that_never_shows_up_raises_the_504(api, short_not_found):
    fake = api(GATEWAY_TIMEOUT, [NOT_FOUND])

    with pytest.raises(client_errors.UnexpectedStatus) as excinfo:
        await SandboxInstance.create(NAMED)

    assert excinfo.value.status_code == 504
    assert fake.reads_made >= 1


async def test_504_wait_is_bounded(api, short_wait):
    api(GATEWAY_TIMEOUT, [_ok("DEPLOYING")])

    with pytest.raises(SandboxAPIError, match=f"^Sandbox {NAME} is still DEPLOYING after waiting"):
        await SandboxInstance.create(NAMED)


async def test_504_does_not_take_a_sandbox_older_than_the_request(api):
    # The name was held before the request, so the creation would have been
    # refused: the sandbox found is not this creation, and the 504 stands.
    fake = api(GATEWAY_TIMEOUT, [_ok("DEPLOYED", created_at=LONG_AGO)])

    with pytest.raises(client_errors.UnexpectedStatus) as excinfo:
        await SandboxInstance.create(NAMED)

    assert excinfo.value.status_code == 504
    assert fake.reads_made == 1


async def test_504_allows_for_a_small_clock_difference(api):
    # The control plane clock a little behind this one.
    a_bit_before = _timestamp(datetime.now() - timedelta(seconds=10))
    api(GATEWAY_TIMEOUT, [_ok("DEPLOYED", created_at=a_bit_before)])

    instance = await SandboxInstance.create(NAMED)

    assert str(instance.status) == "DEPLOYED"


async def test_create_if_not_exists_504_returns_the_sandbox_holding_the_name(api):
    # There a sandbox that already holds the name is the expected answer.
    fake = api(GATEWAY_TIMEOUT, [_ok("DEPLOYED", created_at=LONG_AGO)])

    instance = await SandboxInstance.create_if_not_exists(NAMED)

    assert str(instance.status) == "DEPLOYED"
    assert fake.reads_made == 1


async def test_504_stops_when_the_sandbox_goes_away(api):
    # Seen, then not found: the creation went away, and a sandbox created later
    # under the same name would not be this one.
    fake = api(GATEWAY_TIMEOUT, [_ok("DEPLOYING"), NOT_FOUND, _ok("DEPLOYED")])

    with pytest.raises(SandboxAPIError) as excinfo:
        await SandboxInstance.create(NAMED)

    assert excinfo.value.status == 404
    assert fake.reads_made == 2


SECOND = datetime(2026, 11, 18, 22, 27, 16, tzinfo=timezone.utc).timestamp()


@pytest.mark.parametrize(
    ("timestamp", "expected"),
    [
        ("2026-11-18T22:27:16.569123456Z", SECOND + 0.569123),
        ("2026-11-18T22:27:16Z", SECOND),
        ("2026-11-18T23:27:16.5+01:00", SECOND + 0.5),
        ("2026-11-18T22:27:16", SECOND),
        ("yesterday", None),
        (None, None),
    ],
)
def test_control_plane_timestamps_are_read(timestamp, expected):
    if expected is None:
        assert _unix_time(timestamp) is None
    else:
        assert _unix_time(timestamp) == pytest.approx(expected)


# Everything else is unchanged


@pytest.mark.parametrize("status", ["DEPLOYED", "DEPLOYING", "BUILDING"])
async def test_200_is_returned_as_is_without_reading_again(api, status):
    fake = api(_ok(status))

    instance = await SandboxInstance.create(NAMED)

    assert str(instance.status) == status
    assert fake.requests == [("POST", "/v0/sandboxes")]


async def test_other_unexpected_statuses_still_raise(api):
    fake = api(httpx.Response(502, text="bad gateway"))

    with pytest.raises(client_errors.UnexpectedStatus) as excinfo:
        await SandboxInstance.create(NAMED)

    assert excinfo.value.status_code == 502
    assert fake.reads_made == 0


# Sync


def test_sync_202_waits_until_deployed(api):
    fake = api(ACCEPTED, [_ok("DEPLOYING"), _ok("DEPLOYED")])

    instance = SyncSandboxInstance.create({"region": REGION})

    assert isinstance(instance, SyncSandboxInstance)
    assert instance.metadata.name == NAME
    assert str(instance.status) == "DEPLOYED"
    assert fake.reads_made == 2


def test_sync_202_is_told_by_status_code_once_the_client_models_it(api, monkeypatch):
    fake = api(ACCEPTED, [_ok("DEPLOYED")])
    body = _sandbox("DEPLOYING")
    parsed_202 = Response(
        status_code=HTTPStatus.ACCEPTED,
        content=json.dumps(body).encode(),
        headers={},
        parsed=Sandbox.from_dict(body),
    )
    monkeypatch.setattr(f"{SYNC_MODULE}.create_sandbox_detailed", lambda **_: parsed_202)

    instance = SyncSandboxInstance.create({"region": REGION})

    assert str(instance.status) == "DEPLOYED"
    assert fake.reads_made == 1


def test_sync_202_then_failed_raises_with_the_sandbox_reason(api):
    api(ACCEPTED, [httpx.Response(200, json=_failed("quota reached"))])

    with pytest.raises(SandboxAPIError) as excinfo:
        SyncSandboxInstance.create(NAMED)

    assert str(excinfo.value) == f"Sandbox {NAME} is FAILED instead of DEPLOYED: quota reached"
    assert excinfo.value.code == "DEPLOYMENT_FAILED"


def test_sync_202_wait_is_bounded(api, short_wait):
    api(ACCEPTED, [_ok("DEPLOYING")])

    with pytest.raises(SandboxAPIError, match=f"^Sandbox {NAME} is still DEPLOYING after waiting"):
        SyncSandboxInstance.create(NAMED)


def test_sync_504_for_a_named_creation_waits_until_deployed(api):
    fake = api(GATEWAY_TIMEOUT, [NOT_FOUND, _ok("DEPLOYED")])

    instance = SyncSandboxInstance.create(NAMED)

    assert str(instance.status) == "DEPLOYED"
    assert fake.reads_made == 2


def test_sync_504_for_a_sandbox_that_never_shows_up_raises_the_504(api, short_not_found):
    api(GATEWAY_TIMEOUT, [NOT_FOUND])

    with pytest.raises(client_errors.UnexpectedStatus) as excinfo:
        SyncSandboxInstance.create(NAMED)

    assert excinfo.value.status_code == 504


def test_sync_504_does_not_take_a_sandbox_older_than_the_request(api):
    fake = api(GATEWAY_TIMEOUT, [_ok("DEPLOYED", created_at=LONG_AGO)])

    with pytest.raises(client_errors.UnexpectedStatus) as excinfo:
        SyncSandboxInstance.create(NAMED)

    assert excinfo.value.status_code == 504
    assert fake.reads_made == 1


def test_sync_504_stops_when_the_sandbox_goes_away(api):
    api(GATEWAY_TIMEOUT, [_ok("DEPLOYING"), NOT_FOUND, _ok("DEPLOYED")])

    with pytest.raises(SandboxAPIError) as excinfo:
        SyncSandboxInstance.create(NAMED)

    assert excinfo.value.status == 404


@pytest.mark.parametrize("status", ["DEPLOYING", "BUILDING"])
def test_sync_200_is_returned_as_is_without_reading_again(api, status):
    fake = api(_ok(status))

    instance = SyncSandboxInstance.create(NAMED)

    assert str(instance.status) == status
    assert fake.requests == [("POST", "/v0/sandboxes")]

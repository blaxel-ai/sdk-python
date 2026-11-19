"""Unit tests for SandboxInstance.create errors on the common path.

- A creation rejected by a transient authentication failure (403 UNAUTHORIZED,
  503 AUTHENTICATION_UNAVAILABLE) is retried a bounded number of times, and the
  final error does not claim the credentials are invalid.
- A key the API does not recognize (AUTHENTICATION_FAILED) is not retried, and
  the error says the API key is not valid.
- A creation without a region says so once per process, not on every call.
- A 400 for a name that breaks the naming rule says how to build a valid one.
- Listing an empty workspace returns an empty page.
"""

import json
import warnings
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from blaxel.core import SandboxAPIError, SandboxInstance, SyncSandboxInstance
from blaxel.core.client import errors as client_errors
from blaxel.core.client.client import Client
from blaxel.core.client.models import Metadata, Sandbox, SandboxRuntime, SandboxSpec
from blaxel.core.client.models.sandbox_error import SandboxError
from blaxel.core.sandbox.default import sandbox as async_module
from blaxel.core.sandbox.default.sandbox import (
    CREATE_AUTH_RETRIES,
    CREATE_AUTH_RETRY_BASE_DELAY_SECONDS,
    CREATE_AUTH_RETRY_MAX_DELAY_SECONDS,
    _create_auth_retry_delay,
)

ASYNC_CREATE = "blaxel.core.sandbox.default.sandbox.create_sandbox"
SYNC_CREATE = "blaxel.core.sandbox.sync.sandbox.create_sandbox"
CONFIG = {"name": "agent-errors", "region": "us-pdx-1"}


@pytest.fixture(autouse=True)
def no_retry_delay(monkeypatch):
    monkeypatch.setattr("blaxel.core.sandbox.default.sandbox._create_auth_retry_delay", lambda _: 0)


def _created(name: str = "agent-errors") -> Sandbox:
    return Sandbox(
        metadata=Metadata(name=name),
        spec=SandboxSpec(runtime=SandboxRuntime(image="blaxel/base-image:latest")),
    )


def _auth_failed() -> SandboxError:
    return SandboxError(code="UNAUTHORIZED", message="Authorization failed", status_code=403)


def _auth_unavailable() -> client_errors.UnexpectedStatus:
    body = {
        "code": "AUTHENTICATION_UNAVAILABLE",
        "message": "Unable to verify credentials, please retry",
        "status_code": 503,
    }
    return client_errors.from_response(503, json.dumps(body).encode())


# Transient authentication failures


async def test_transient_auth_failure_is_retried_then_succeeds():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = [_auth_failed(), _auth_failed(), _created()]

        instance = await SandboxInstance.create(CONFIG)

        assert instance.metadata.name == "agent-errors"
        assert mock_create.await_count == 3


async def test_auth_unavailable_is_retried_then_succeeds():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = [_auth_unavailable(), _created()]

        instance = await SandboxInstance.create(CONFIG)

        assert instance.metadata.name == "agent-errors"
        assert mock_create.await_count == 2


async def test_persistent_auth_failure_stops_after_bounded_retries_with_clear_message():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = _auth_failed()

        with pytest.raises(SandboxAPIError) as excinfo:
            await SandboxInstance.create(CONFIG)

        assert mock_create.await_count == CREATE_AUTH_RETRIES + 1
        error = excinfo.value
        assert error.status_code == 403
        assert error.code == "UNAUTHORIZED"
        message = str(error)
        assert message.startswith("Authorization failed")
        assert f"after {CREATE_AUTH_RETRIES + 1} attempts" in message
        assert "a key it does not recognize" in message
        assert "if they are right, retry in a few seconds" in message
        assert "BL_API_KEY and BL_WORKSPACE" in message
        assert "current workspace: '" in message


async def test_persistent_auth_unavailable_reraises_the_original_error():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = _auth_unavailable()

        with pytest.raises(client_errors.UnexpectedStatus) as excinfo:
            await SandboxInstance.create(CONFIG)

        assert excinfo.value.status_code == 503
        assert mock_create.await_count == CREATE_AUTH_RETRIES + 1


def _auth_unavailable_response(headers: dict[str, str]) -> client_errors.UnexpectedStatus:
    body = {
        "code": "AUTHENTICATION_UNAVAILABLE",
        "message": "Unable to verify credentials, please retry",
        "retryable": True,
    }
    content = json.dumps(body).encode()
    response = httpx.Response(503, content=content, headers=headers)
    return client_errors.from_response(503, content, response.headers, response=response)


async def test_auth_unavailable_waits_retry_after_and_is_not_called_an_auth_error():
    """503 AUTHENTICATION_UNAVAILABLE: the server's Retry-After sets the wait between
    attempts and on the final error, which says it is not a credential problem."""
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    with (
        patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create,
        patch.object(async_module.asyncio, "sleep", fake_sleep),
    ):
        mock_create.side_effect = lambda **_: (_ for _ in ()).throw(
            _auth_unavailable_response({"Retry-After": "7"})
        )

        with pytest.raises(client_errors.UnexpectedStatus) as excinfo:
            await SandboxInstance.create(CONFIG)

    assert sleeps == [7.0] * CREATE_AUTH_RETRIES
    error = excinfo.value
    assert error.retryable is True
    assert error.retry_after_seconds == 7
    message = str(error)
    assert "HTTP 503 AUTHENTICATION_UNAVAILABLE" in message
    assert "not a credential or permission error; retry after 7 s" in message
    assert "BL_API_KEY" not in message


async def test_auth_unavailable_is_not_retried_when_the_server_says_no():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = _auth_unavailable_response({"X-Should-Retry": "false"})

        with pytest.raises(client_errors.UnexpectedStatus) as excinfo:
            await SandboxInstance.create(CONFIG)

    mock_create.assert_awaited_once()
    assert excinfo.value.retryable is False
    assert "the server says not to retry" in str(excinfo.value)


@pytest.mark.parametrize(
    "error",
    [
        SandboxError(code="TOKEN_REVOKED", message="Token has been revoked", status_code=401),
        SandboxError(
            code="UNAUTHORIZED_WORKSPACE",
            message="You don't have write access to this workspace",
            status_code=403,
        ),
        SandboxError(code="QUOTA", message="nope", status_code=403),
        SandboxError(code="BAD_REQUEST", message="invalid", status_code=400),
        SandboxError(code="ALREADY_EXISTS", message="exists", status_code=409),
    ],
)
async def test_final_errors_are_not_retried(error):
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = error

        with pytest.raises(SandboxAPIError) as excinfo:
            await SandboxInstance.create(CONFIG)

        mock_create.assert_awaited_once()
        assert "after" not in str(excinfo.value)
        assert str(excinfo.value).startswith(error.message)


def _invalid_api_key(status: int = 403) -> SandboxError:
    return SandboxError(
        code="AUTHENTICATION_FAILED", message="The API key is not valid", status_code=status
    )


def _assert_says_the_api_key_is_not_valid(error: SandboxAPIError, status: int) -> None:
    assert error.code == "AUTHENTICATION_FAILED"
    assert error.status_code == status
    assert error.retryable is False
    assert str(error) == (
        f"The API key is not valid (HTTP {status} AUTHENTICATION_FAILED: this API key is not"
        " valid; not retried, the same key is refused every time). Check the API key the SDK"
        " sends (BL_API_KEY) for a typo or a missing part; if it was deleted, create a new one"
        " in the Blaxel Console."
    )


@pytest.mark.parametrize("status", [403, 401])
async def test_invalid_api_key_is_not_retried_and_says_so(status):
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = _invalid_api_key(status)

        with pytest.raises(SandboxAPIError) as excinfo:
            await SandboxInstance.create(CONFIG)

    mock_create.assert_awaited_once()
    _assert_says_the_api_key_is_not_valid(excinfo.value, status)


def test_sync_invalid_api_key_is_not_retried_and_says_so():
    with patch(SYNC_CREATE) as mock_create:
        mock_create.return_value = _invalid_api_key()

        with pytest.raises(SandboxAPIError) as excinfo:
            SyncSandboxInstance.create(CONFIG)

    mock_create.assert_called_once()
    _assert_says_the_api_key_is_not_valid(excinfo.value, 403)


async def test_other_unexpected_statuses_are_not_retried():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = client_errors.UnexpectedStatus(503, b"service unavailable")

        with pytest.raises(client_errors.UnexpectedStatus):
            await SandboxInstance.create(CONFIG)

        mock_create.assert_awaited_once()


async def test_create_if_not_exists_retries_transient_auth_failure():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = [_auth_failed(), _created()]

        await SandboxInstance.create_if_not_exists(CONFIG)

        assert mock_create.await_count == 2
        for call in mock_create.await_args_list:
            assert call.kwargs["create_if_not_exist"] is True


def test_sync_transient_auth_failure_is_retried():
    with patch(SYNC_CREATE) as mock_create:
        mock_create.side_effect = [_auth_failed(), _auth_unavailable(), _created()]

        instance = SyncSandboxInstance.create(CONFIG)

        assert instance.metadata.name == "agent-errors"
        assert mock_create.call_count == 3

    with patch(SYNC_CREATE) as mock_create:
        mock_create.return_value = _auth_failed()

        with pytest.raises(SandboxAPIError) as excinfo:
            SyncSandboxInstance.create(CONFIG)

        assert mock_create.call_count == CREATE_AUTH_RETRIES + 1
        assert "a key it does not recognize" in str(excinfo.value)

    with patch(SYNC_CREATE) as mock_create:
        mock_create.return_value = SandboxError(
            code="TOKEN_REVOKED", message="Token has been revoked", status_code=401
        )

        with pytest.raises(SandboxAPIError):
            SyncSandboxInstance.create(CONFIG)

        mock_create.assert_called_once()


def test_retry_delay_is_bounded():
    # Exponential from the base delay, capped, plus up to one base delay of jitter.
    ceiling = CREATE_AUTH_RETRY_MAX_DELAY_SECONDS + CREATE_AUTH_RETRY_BASE_DELAY_SECONDS
    for attempt in range(1, 10):
        assert CREATE_AUTH_RETRY_BASE_DELAY_SECONDS <= _create_auth_retry_delay(attempt) <= ceiling


# Region notice


@pytest.fixture
def no_region(monkeypatch):
    monkeypatch.delenv("BL_REGION", raising=False)
    monkeypatch.setattr(async_module, "_region_notice_shown", False)


def _region_notices(caught):
    return [
        w for w in caught if issubclass(w.category, FutureWarning) and "region" in str(w.message)
    ]


async def test_region_notice_is_shown_once_per_process(no_region):
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = _created()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            await SandboxInstance.create({"name": "agent-errors"})
            await SandboxInstance.create({"name": "agent-errors"})

        notices = _region_notices(caught)
        assert len(notices) == 1
        assert str(notices[0].message).startswith("SandboxInstance.create:")
        assert "BL_REGION" in str(notices[0].message)
        assert "shown once per process" in str(notices[0].message)
        assert notices[0].filename == __file__


def test_sync_region_notice_is_shown_once_per_process(no_region):
    with patch(SYNC_CREATE) as mock_create:
        mock_create.return_value = _created()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            SyncSandboxInstance.create({"name": "agent-errors"})
            SyncSandboxInstance.create({"name": "agent-errors"})

        notices = _region_notices(caught)
        assert len(notices) == 1
        assert str(notices[0].message).startswith("SyncSandboxInstance.create:")
        assert notices[0].filename == __file__


async def test_no_region_notice_when_region_is_set(no_region, monkeypatch):
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = _created()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            await SandboxInstance.create(CONFIG)
            monkeypatch.setenv("BL_REGION", "eu-lon-1")
            await SandboxInstance.create({"name": "agent-errors"})

        assert _region_notices(caught) == []
        assert mock_create.await_args.kwargs["body"].spec.region == "eu-lon-1"


# Invalid names


async def test_invalid_name_400_says_how_to_fix_it():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = SandboxError(
            code="BAD_REQUEST", message="invalid sandbox name", status_code=400
        )

        with pytest.raises(SandboxAPIError) as excinfo:
            await SandboxInstance.create({"name": "sesn_01AbC", "region": "us-pdx-1"})

        message = str(excinfo.value)
        assert message.startswith("invalid sandbox name (HTTP 400 BAD_REQUEST). Sandbox names use")
        assert "lowercase letters, digits and single hyphens" in message
        assert "sanitize_sandbox_name('sesn_01AbC') gives 'sesn-01abc'" in message
        assert excinfo.value.status_code == 400


async def test_invalid_name_is_sent_as_is():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = _created("sesn_01AbC")

        await SandboxInstance.create({"name": "sesn_01AbC", "region": "us-pdx-1"})

        assert mock_create.await_args.kwargs["body"].metadata.name == "sesn_01AbC"


async def test_invalid_name_400_without_status_in_body_keeps_http_status():
    message = "metadata.name must contain only lower case alphanumeric characters and hyphens"
    error = SandboxError.from_dict({"code": "BAD_REQUEST", "message": message})
    client_errors.retain_response(error, httpx.Response(400, json={"code": "BAD_REQUEST"}))
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = error

        with pytest.raises(SandboxAPIError) as excinfo:
            await SandboxInstance.create({"name": "sesn_01AbC", "region": "us-pdx-1"})

        assert excinfo.value.status_code == 400
        assert "gives 'sesn-01abc'" in str(excinfo.value)
        mock_create.assert_awaited_once()


def test_sync_invalid_name_400_says_how_to_fix_it():
    with patch(SYNC_CREATE) as mock_create:
        mock_create.return_value = SandboxError(
            code="BAD_REQUEST", message="invalid sandbox name", status_code=400
        )

        with pytest.raises(SandboxAPIError) as excinfo:
            SyncSandboxInstance.create({"name": "My_Box", "region": "us-pdx-1"})

        assert "sanitize_sandbox_name('My_Box') gives 'my-box'" in str(excinfo.value)


# Empty workspace


def _mock_api(monkeypatch, body):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/sandboxes")
        return httpx.Response(200, json=body)

    mock_client = Client(
        base_url="https://api.test/v0",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    monkeypatch.setattr("blaxel.core.sandbox.default.sandbox.client", mock_client)
    monkeypatch.setattr("blaxel.core.sandbox.sync.sandbox.client", mock_client)


EMPTY_BODIES = [[], {"data": [], "meta": {"hasMore": False}}, {}, {"data": None}]


@pytest.mark.parametrize("body", EMPTY_BODIES)
async def test_list_on_empty_workspace_returns_empty_page(monkeypatch, body):
    _mock_api(monkeypatch, body)

    page = await SandboxInstance.list()

    assert list(page) == []
    assert page.data == []
    assert page.has_more is False


@pytest.mark.parametrize("body", EMPTY_BODIES)
def test_sync_list_on_empty_workspace_returns_empty_page(monkeypatch, body):
    _mock_api(monkeypatch, body)

    page = SyncSandboxInstance.list()

    assert list(page) == []
    assert page.data == []
    assert page.has_more is False


# Limits and edge blocks: each answer goes through the real generated client.


def _mock_create(monkeypatch, status, content=b"", headers=None):
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("/sandboxes")
        calls.append(request)
        return httpx.Response(status, content=content, headers=headers or {})

    mock_client = Client(
        base_url="https://api.test/v0",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    monkeypatch.setattr("blaxel.core.sandbox.default.sandbox.client", mock_client)
    monkeypatch.setattr("blaxel.core.sandbox.sync.sandbox.client", mock_client)
    return calls


def _limit_body(code: str, message: str) -> bytes:
    return json.dumps({"code": code, "message": message, "status_code": 429}).encode()


async def test_quota_exceeded_says_it_is_not_retryable(monkeypatch):
    calls = _mock_create(
        monkeypatch,
        429,
        _limit_body("QUOTA_EXCEEDED", "Sandbox quota exceeded"),
        {"Retry-After": "5"},
    )

    with pytest.raises(client_errors.QuotaExceededError) as excinfo:
        await SandboxInstance.create(CONFIG)

    error = excinfo.value
    assert not isinstance(error, client_errors.RateLimitError)
    assert len(calls) == 1
    assert error.code == "QUOTA_EXCEEDED"
    assert error.retryable is False
    assert str(error) == (
        "Sandbox quota exceeded (HTTP 429 QUOTA_EXCEEDED: not retryable until usage drops,"
        " the request asks for less (such as a smaller volume), or the quota is raised:"
        " https://docs.blaxel.ai/Security/Quotas)"
    )
    assert error.message == str(error)


async def test_workspace_rate_limit_says_when_to_retry(monkeypatch):
    calls = _mock_create(
        monkeypatch,
        429,
        _limit_body("WORKSPACE_RATE_LIMIT_EXCEEDED", "Too many sandbox creations"),
        {"Retry-After": "7"},
    )

    with pytest.raises(client_errors.RateLimitError) as excinfo:
        await SandboxInstance.create(CONFIG)

    error = excinfo.value
    assert len(calls) == 1
    assert error.retryable is True
    assert error.retry_after_seconds == 7
    assert str(error) == (
        "Too many sandbox creations (HTTP 429 WORKSPACE_RATE_LIMIT_EXCEEDED: too many"
        " creations in flight in this workspace; retry after 7 s)"
    )


def test_sync_workspace_rate_limit_without_retry_after_says_to_back_off(monkeypatch):
    _mock_create(
        monkeypatch, 429, _limit_body("WORKSPACE_RATE_LIMIT_EXCEEDED", "Too many sandbox creations")
    )

    with pytest.raises(client_errors.RateLimitError) as excinfo:
        SyncSandboxInstance.create(CONFIG)

    assert excinfo.value.retryable is True
    assert excinfo.value.retry_after_seconds is None
    assert str(excinfo.value).endswith("in flight in this workspace; retry with backoff)")


EDGE_HTML = b"<!DOCTYPE HTML><HTML><BODY><H1>403 ERROR</H1>Generated by cloudfront</BODY></HTML>"


@pytest.mark.parametrize("sync", [False, True])
@pytest.mark.parametrize("content", [b"", EDGE_HTML])
async def test_403_without_json_says_it_is_not_a_quota_and_was_blocked_before_the_api(
    monkeypatch, sync, content
):
    calls = _mock_create(monkeypatch, 403, content, {"Content-Type": "text/html"})

    with pytest.raises(client_errors.UnexpectedStatus) as excinfo:
        if sync:
            SyncSandboxInstance.create(CONFIG)
        else:
            await SandboxInstance.create(CONFIG)

    assert len(calls) == 1
    assert excinfo.value.status_code == 403
    assert str(excinfo.value) == (
        "HTTP 403 without a JSON error body: not a quota. The request was blocked or"
        " throttled before the API could answer it, for example by an edge rate limit or"
        " firewall block. Slow down and retry after about 60 s. Blaxel quota and"
        " permission errors carry a JSON error code"
    )


async def test_json_403_is_not_called_an_edge_block():
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = SandboxError(
            code="UNAUTHORIZED_WORKSPACE", message="no write access", status_code=403
        )

        with pytest.raises(SandboxAPIError) as excinfo:
            await SandboxInstance.create(CONFIG)

    assert str(excinfo.value) == "no write access (HTTP 403 UNAUTHORIZED_WORKSPACE)"


def _modeled(status: int, code: str, message: str, headers=None) -> SandboxError:
    """A limit error as the generated client returns it once the spec models the status."""
    body = {"code": code, "message": message, "status_code": status}
    error = SandboxError.from_dict(body)
    client_errors.retain_response(error, httpx.Response(status, json=body, headers=headers or {}))
    return error


@pytest.mark.parametrize("sync", [False, True])
async def test_modeled_429_quota_raises_quota_exceeded_error(sync):
    error = _modeled(429, "QUOTA_EXCEEDED", "Sandbox quota exceeded")
    target = SYNC_CREATE if sync else ASYNC_CREATE
    with patch(target, **({} if sync else {"new_callable": AsyncMock})) as mock_create:
        mock_create.return_value = error

        with pytest.raises(client_errors.QuotaExceededError) as excinfo:
            if sync:
                SyncSandboxInstance.create(CONFIG)
            else:
                await SandboxInstance.create(CONFIG)

    assert excinfo.value.status_code == 429
    assert excinfo.value.code == "QUOTA_EXCEEDED"
    assert excinfo.value.retryable is False
    assert "not retryable until usage drops, the request asks for less" in str(excinfo.value)


async def test_modeled_429_rate_limit_keeps_retry_after():
    error = _modeled(
        429, "WORKSPACE_RATE_LIMIT_EXCEEDED", "Too many sandbox creations", {"Retry-After": "3"}
    )
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = error

        with pytest.raises(client_errors.RateLimitError) as excinfo:
            await SandboxInstance.create(CONFIG)

    assert excinfo.value.retryable is True
    assert excinfo.value.retry_after_seconds == 3
    assert str(excinfo.value).endswith("retry after 3 s)")


async def test_cluster_rate_limit_is_retryable(monkeypatch):
    _mock_create(monkeypatch, 429, _limit_body("RATE_LIMIT_EXCEEDED", "rate limit exceeded"))

    with pytest.raises(client_errors.RateLimitError) as excinfo:
        await SandboxInstance.create(CONFIG)

    assert excinfo.value.retryable is True
    assert str(excinfo.value) == (
        "rate limit exceeded (HTTP 429 RATE_LIMIT_EXCEEDED: the region's creation rate limit"
        " was reached; retry with backoff)"
    )


@pytest.mark.parametrize("sync", [False, True])
async def test_volume_over_per_volume_maximum_is_not_retryable(sync):
    message = "Ephemeral volume 'scratch' size 900000 MB exceeds maximum allowed size"
    error = _modeled(400, "QUOTA_EXCEEDED", message)
    target = SYNC_CREATE if sync else ASYNC_CREATE
    with patch(target, **({} if sync else {"new_callable": AsyncMock})) as mock_create:
        mock_create.return_value = error

        with pytest.raises(SandboxAPIError) as excinfo:
            if sync:
                SyncSandboxInstance.create(CONFIG)
            else:
                await SandboxInstance.create(CONFIG)

    assert excinfo.value.status_code == 400
    assert excinfo.value.code == "QUOTA_EXCEEDED"
    assert excinfo.value.retryable is False
    assert str(excinfo.value) == (
        f"{message} (HTTP 400 QUOTA_EXCEEDED: not retryable as is; request a smaller volume"
        " or raise the quota: https://docs.blaxel.ai/Security/Quotas)"
    )


def test_image_build_quota_429_says_it_is_not_retryable():
    from blaxel.core.image.image import _limit_hint

    old_server = json.dumps(
        {
            "error": "Image storage quota reached: 10/10 MiB used by images across your"
            " workspaces. Delete unused images before building again, or request additional"
            " quota at https://app.blaxel.ai/account/plan-quotas?id=acc",
            "code": 429,
        }
    ).encode()
    new_server = _limit_body("QUOTA_EXCEEDED", "Image storage quota reached")
    for content in (old_server, new_server):
        assert _limit_hint(429, content).startswith(
            " (not retryable until usage drops or the quota is raised"
        )
    assert _limit_hint(429, b'{"error": "slow down", "code": 429}') == ""
    assert _limit_hint(429, _limit_body("RATE_LIMIT_EXCEEDED", "x")) == (
        " (rate limited: retry with backoff)"
    )
    assert _limit_hint(400, new_server) == ""


def test_image_build_backlog_429_is_retryable_not_a_quota():
    from blaxel.core.image.image import _limit_hint

    backlog = (
        "Too many image builds are waiting for this account: 40 queued builds reserve"
        " 327680 MB of memory, 1310720 MB of scratch disk and 160 vCPUs, and the queue"
        " holds at most five times your build quota. Retry once some builds finish, or"
        " upgrade your tier at https://app.blaxel.ai/account/plan-quotas?id=acc"
    )
    old_server = json.dumps({"error": backlog, "code": 429}).encode()
    assert _limit_hint(429, old_server) == (
        " (the account's build queue is full: retry with backoff, once some builds finish)"
    )
    named = json.dumps(
        {"error": backlog, "code": "BUILD_QUEUE_FULL", "message": backlog, "retryable": True}
    ).encode()
    assert _limit_hint(429, named, {"X-Should-Retry": "true", "Retry-After": "12"}) == (
        " (the account's build queue is full: retry after 12 s, once some builds finish)"
    )


def test_image_build_limit_hint_follows_the_server_signal_over_the_link():
    from blaxel.core.image.image import _limit_hint

    linked = json.dumps(
        {"error": "over quota, see https://app.blaxel.ai/account/plan-quotas?id=acc", "code": 429}
    ).encode()
    assert _limit_hint(429, linked, {"x-should-retry": "true"}) == (
        " (rate limited: retry with backoff)"
    )
    assert _limit_hint(
        429, _limit_body("RATE_LIMIT_EXCEEDED", "x"), {"X-Should-Retry": "false"}
    ) == (" (the server says not to retry)")
    retryable_body = json.dumps({"error": "busy", "code": 429, "retryable": True}).encode()
    assert _limit_hint(429, retryable_body) == " (rate limited: retry with backoff)"


# The registered error contract (control plane error stack): the dispatcher sends
# error_code next to code, the platform fields, X-Should-Retry and request_id.

REGISTERED_QUOTA = {
    "code": "QUOTA_EXCEEDED",
    "error_code": "QUOTA_EXCEEDED",
    "message": "You have reached the maximum memory (32768) for your account. Requested: 49152",
    "status_code": 429,
    "action": "Bring usage under the limit named in the message, or raise the quota.",
    "do_not": "Do not retry with backoff: this is a quota, not a rate limit.",
    "docs_url": "https://docs.blaxel.ai/troubleshooting/error-codes#quota-exceeded",
    "retryable": False,
    "safe_to_retry_request": False,
    "dispatch_state": "not_dispatched",
    "status": 429,
    "origin": "platform",
    "request_id": "trace-123",
}


@pytest.mark.parametrize("sync", [False, True])
async def test_registered_quota_body_carries_code_status_and_request_id(monkeypatch, sync):
    calls = _mock_create(
        monkeypatch,
        429,
        json.dumps(REGISTERED_QUOTA).encode(),
        {"X-Should-Retry": "false", "X-Blaxel-Error-Code": "QUOTA_EXCEEDED", "X-Amz-Cf-Id": "edge"},
    )

    with pytest.raises(client_errors.QuotaExceededError) as excinfo:
        if sync:
            SyncSandboxInstance.create(CONFIG)
        else:
            await SandboxInstance.create(CONFIG)

    error = excinfo.value
    assert len(calls) == 1
    assert error.status_code == 429
    assert error.code == "QUOTA_EXCEEDED"
    assert error.retryable is False
    assert error.safe_to_retry_request is False
    assert error.dispatch_state == "not_dispatched"
    assert error.request_id == "trace-123"
    assert error.action == REGISTERED_QUOTA["action"]
    assert str(error).startswith(
        "You have reached the maximum memory (32768) for your account. Requested: 49152"
        " (HTTP 429 QUOTA_EXCEEDED: not retryable"
    )


async def test_rate_limit_follows_the_server_retry_headers(monkeypatch):
    body = {
        "code": "WORKSPACE_RATE_LIMIT_EXCEEDED",
        "error_code": "WORKSPACE_RATE_LIMIT_EXCEEDED",
        "message": "Too many sandbox creations",
        "status_code": 429,
        "retryable": True,
        "safe_to_retry_request": True,
        "dispatch_state": "not_dispatched",
    }
    _mock_create(
        monkeypatch, 429, json.dumps(body).encode(), {"X-Should-Retry": "true", "Retry-After": "1"}
    )

    with pytest.raises(client_errors.RateLimitError) as excinfo:
        await SandboxInstance.create(CONFIG)

    assert excinfo.value.retryable is True
    assert excinfo.value.safe_to_retry_request is True
    assert excinfo.value.retry_after_seconds == 1
    assert str(excinfo.value).endswith("retry after 1 s)")


REQUEST_BLOCKED_BODY = {
    "code": "REQUEST_BLOCKED",
    "message": "The request was blocked before it reached the API.",
    "error": {
        "code": "REQUEST_BLOCKED",
        "message": "The request was blocked before it reached the API.",
        "action": "Send a User-Agent header and retry later.",
        "do_not": "Do not rotate the API key: it was never checked.",
        "retryable": False,
        "safe_to_retry_request": False,
        "dispatch_state": "not_dispatched",
        "origin": "platform",
        "status": 403,
    },
}


@pytest.mark.parametrize("sync", [False, True])
async def test_request_blocked_is_not_an_auth_error_or_retried(monkeypatch, sync):
    calls = _mock_create(
        monkeypatch,
        403,
        json.dumps(REQUEST_BLOCKED_BODY).encode(),
        {"Content-Type": "application/json", "X-Should-Retry": "false"},
    )

    with pytest.raises((SandboxAPIError, client_errors.UnexpectedStatus)) as excinfo:
        if sync:
            SyncSandboxInstance.create(CONFIG)
        else:
            await SandboxInstance.create(CONFIG)

    error = excinfo.value
    assert len(calls) == 1
    assert error.code == "REQUEST_BLOCKED"
    assert error.retryable is False
    message = str(error)
    assert (
        "(HTTP 403 REQUEST_BLOCKED: blocked at the edge before the API read the request" in message
    )
    assert "not a quota and not an API key problem" in message
    assert "Send a User-Agent header and retry later." in message
    assert "BL_API_KEY" not in message


def test_unwrap_reads_the_registered_code_over_the_status():
    from blaxel.core.client.models.error import Error

    body = {
        "error": "Network proxy settings need the network proxy",
        "code": 400,
        "error_code": "NETWORK_PROXY_NOT_ENABLED",
        "retryable": False,
    }
    with pytest.raises(SandboxAPIError) as excinfo:
        async_module._unwrap_response(Error.from_dict(body), "update sandbox")

    assert excinfo.value.status_code == 400
    assert excinfo.value.code == "NETWORK_PROXY_NOT_ENABLED"
    assert str(excinfo.value) == "Network proxy settings need the network proxy"


def test_unwrap_keeps_the_legacy_code_without_error_code():
    from blaxel.core.client.models.error import Error

    with pytest.raises(SandboxAPIError) as excinfo:
        async_module._unwrap_response(Error.from_dict({"error": "not found", "code": 404}), "get")

    assert excinfo.value.code == "not found"


EDGE_BLOCK_PAGES = [
    b"403 Request blocked",
    b"<!DOCTYPE html><html><body><h1>Request blocked.</h1></body></html>",
]


@pytest.mark.parametrize("sync", [False, True])
@pytest.mark.parametrize("content", EDGE_BLOCK_PAGES)
async def test_edge_block_page_gets_the_request_blocked_advice(monkeypatch, sync, content):
    calls = _mock_create(monkeypatch, 403, content, {"Content-Type": "text/html"})

    with pytest.raises(client_errors.UnexpectedStatus) as excinfo:
        if sync:
            SyncSandboxInstance.create(CONFIG)
        else:
            await SandboxInstance.create(CONFIG)

    assert len(calls) == 1
    assert excinfo.value.status_code == 403
    assert excinfo.value.code == "REQUEST_BLOCKED"
    assert excinfo.value.retryable is False
    assert str(excinfo.value) == (
        "Request blocked (HTTP 403 REQUEST_BLOCKED: blocked at the edge before the API read"
        " the request; not a quota and not an API key problem; send a User-Agent header and"
        " slow down; do not rotate the API key, it was never checked)"
    )


@pytest.mark.parametrize("sync", [False, True])
async def test_workspace_access_denied_is_not_retried_as_a_credential_check(sync):
    body = {
        "code": "UNAUTHORIZED",
        "error_code": "WORKSPACE_ACCESS_DENIED",
        "message": "You do not have access to this workspace",
        "status_code": 403,
        "action": "Ask a workspace admin for access, or use a key from this workspace.",
    }
    target = SYNC_CREATE if sync else ASYNC_CREATE
    with patch(target, new_callable=MagicMock if sync else AsyncMock) as mock_create:
        mock_create.return_value = SandboxError.from_dict(body)

        with pytest.raises(SandboxAPIError) as excinfo:
            if sync:
                SyncSandboxInstance.create(CONFIG)
            else:
                await SandboxInstance.create(CONFIG)

    assert mock_create.call_count == 1
    assert excinfo.value.code == "WORKSPACE_ACCESS_DENIED"
    assert str(excinfo.value) == (
        "You do not have access to this workspace (HTTP 403 WORKSPACE_ACCESS_DENIED: Ask a"
        " workspace admin for access, or use a key from this workspace)"
    )


async def test_server_action_and_docs_are_the_next_step_for_codes_without_a_hint():
    body = {
        "code": 409,
        "error_code": "SANDBOX_ALREADY_EXISTS",
        "message": "Sandbox agent-errors already exists",
        "status_code": 409,
        "error": {
            "code": "SANDBOX_ALREADY_EXISTS",
            "action": "Use createIfNotExists, or pick another name.",
            "docs_url": "https://docs.blaxel.ai/Sandboxes/Overview",
        },
    }
    with patch(ASYNC_CREATE, new_callable=AsyncMock) as mock_create:
        mock_create.return_value = SandboxError.from_dict(body)

        with pytest.raises(SandboxAPIError) as excinfo:
            await SandboxInstance.create(CONFIG)

    assert str(excinfo.value) == (
        "Sandbox agent-errors already exists (HTTP 409 SANDBOX_ALREADY_EXISTS: Use"
        " createIfNotExists, or pick another name: https://docs.blaxel.ai/Sandboxes/Overview)"
    )


async def test_unmodeled_429_names_the_code_and_the_server_action(monkeypatch):
    content = json.dumps(
        {
            "code": "PLAN_LIMIT_REACHED",
            "message": "Your plan allows 10 sandboxes",
            "action": "Upgrade the plan.",
            "status_code": 429,
        }
    ).encode()
    calls = _mock_create(monkeypatch, 429, content, {"Content-Type": "application/json"})

    with pytest.raises(client_errors.RateLimitError) as excinfo:
        await SandboxInstance.create(CONFIG)

    assert len(calls) == 1
    assert str(excinfo.value) == (
        "Your plan allows 10 sandboxes (HTTP 429 PLAN_LIMIT_REACHED: Upgrade the plan)"
    )


def test_unwrap_reads_an_edge_block_envelope():
    from blaxel.core.client.models.error import Error

    with pytest.raises(SandboxAPIError) as excinfo:
        async_module._unwrap_response(Error.from_dict(dict(REQUEST_BLOCKED_BODY)), "get")

    assert excinfo.value.code == "REQUEST_BLOCKED"
    assert excinfo.value.status_code == 403
    assert str(excinfo.value) == "The request was blocked before it reached the API."

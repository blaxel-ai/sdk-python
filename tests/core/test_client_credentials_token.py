"""Unit tests for client-credentials token acquisition (SDK-PYTHON-130).

When the configured client credentials are rejected by the auth endpoint
(HTTP 401/403), the SDK must fail fast with a clear, actionable
``CredentialsError`` instead of (a) leaking the raw ``requests`` transport error
``403 Client Error: Forbidden for url: .../oauth/token`` to the caller and
Sentry, and (b) pointlessly retrying a permanent authorization failure three
times. Genuinely transient failures (network errors, 5xx) must still be
retried and still surface.
"""

import requests

from blaxel.core.authentication import clientcredentials
from blaxel.core.authentication.clientcredentials import ClientCredentials
from blaxel.core.authentication.types import CredentialsError, CredentialsType

BASE_URL = "https://api.blaxel.ai/v0"


class _FakeResponse:
    """Minimal stand-in for ``requests.Response`` covering the paths we use."""

    def __init__(self, status_code: int, payload: dict | None = None):
        self.status_code = status_code
        self.reason = {401: "Unauthorized", 403: "Forbidden"}.get(status_code, "Error")
        self.url = f"{BASE_URL}/oauth/token"
        self._payload = payload or {}

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(
                f"{self.status_code} Client Error: {self.reason} for url: {self.url}",
                response=self,
            )


def _make_client() -> ClientCredentials:
    return ClientCredentials(
        CredentialsType(client_credentials="Zm9vOmJhcg=="), "my-workspace", BASE_URL
    )


def _count_posts(monkeypatch, response_factory):
    """Patch ``requests.post`` (and no-op sleeps) and count invocations."""
    calls = {"n": 0}

    def fake_post(*_args, **_kwargs):
        calls["n"] += 1
        return response_factory()

    monkeypatch.setattr(clientcredentials.requests, "post", fake_post)
    monkeypatch.setattr(clientcredentials.time, "sleep", lambda _s: None)
    return calls


def test_rejected_credentials_raise_credentials_error(monkeypatch):
    """A 403 must surface an actionable CredentialsError, not a raw HTTPError."""
    _count_posts(monkeypatch, lambda: _FakeResponse(403))
    client = _make_client()

    try:
        client.get_headers()
    except CredentialsError as err:
        message = str(err)
    else:  # pragma: no cover - defensive
        raise AssertionError("get_headers did not raise")

    assert "403" in message
    assert "BL_CLIENT_CREDENTIALS" in message
    # The raw transport wording must not leak to the caller.
    assert "Client Error" not in message


def test_unauthorized_credentials_raise_credentials_error(monkeypatch):
    """A 401 is treated the same as a 403: rejected credentials."""
    _count_posts(monkeypatch, lambda: _FakeResponse(401))
    client = _make_client()

    err = client.get_token()
    assert isinstance(err, CredentialsError)
    assert "401" in str(err)


def test_rejected_credentials_are_not_retried(monkeypatch):
    """A permanent 403 must hit the token endpoint exactly once."""
    calls = _count_posts(monkeypatch, lambda: _FakeResponse(403))
    client = _make_client()

    err = client.get_token()
    assert isinstance(err, CredentialsError)
    assert calls["n"] == 1


def test_transient_network_failure_is_retried_and_surfaced(monkeypatch):
    """A connection error is transient: retry the full budget, then return it."""
    calls = {"n": 0}

    def fake_post(*_args, **_kwargs):
        calls["n"] += 1
        raise requests.exceptions.ConnectionError("connection reset")

    monkeypatch.setattr(clientcredentials.requests, "post", fake_post)
    monkeypatch.setattr(clientcredentials.time, "sleep", lambda _s: None)
    client = _make_client()

    err = client.get_token()
    # Initial attempt + 3 retries.
    assert calls["n"] == 4
    assert isinstance(err, requests.exceptions.ConnectionError)
    assert not isinstance(err, CredentialsError)


def test_server_error_is_retried_and_not_masked_as_credentials_error(monkeypatch):
    """A 5xx is a server fault, not a credentials problem: retried, still an HTTPError."""
    calls = _count_posts(monkeypatch, lambda: _FakeResponse(500))
    client = _make_client()

    err = client.get_token()
    assert calls["n"] == 4
    assert isinstance(err, requests.exceptions.HTTPError)
    assert not isinstance(err, CredentialsError)


def test_successful_token_populates_credentials(monkeypatch):
    """Control: a 200 with a token body authenticates with a single request."""
    payload = {
        "access_token": "access-123",
        "refresh_token": "refresh-456",
        "expires_in": 3600,
        "token_type": "Bearer",
    }
    calls = _count_posts(monkeypatch, lambda: _FakeResponse(200, payload))
    client = _make_client()

    headers = client.get_headers()
    assert calls["n"] == 1
    assert headers["X-Blaxel-Authorization"] == "Bearer access-123"
    assert headers["X-Blaxel-Workspace"] == "my-workspace"
    assert client.credentials.access_token == "access-123"

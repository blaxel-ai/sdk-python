"""Unit tests for env-var credential error handling (ENG-2253).

Covers the three reported failure modes when BL_WORKSPACE / BL_API_KEY are
missing or partially set: instead of a cryptic httpx ``'NoneType' has no
encode`` error, an import-time ``FileNotFoundError``, or a misleading
server-side "workspace is required" message, the SDK must fail fast with a
clear, actionable ``CredentialsError``.
"""

import httpx
import pytest

from blaxel.core.authentication import (
    CredentialsError,
    MissingCredentials,
    auth,
    get_credentials,
)
from blaxel.core.authentication.apikey import ApiKey

BASE_URL = "https://api.blaxel.ai/v0"


@pytest.fixture
def no_config(monkeypatch, tmp_path):
    """Point Path.home() at an empty dir so no ~/.blaxel/config.yaml is found."""
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    return tmp_path


@pytest.fixture
def clear_auth_env(monkeypatch):
    """Remove every auth-related env var so each test controls its own state."""
    for var in ("BL_API_KEY", "BL_WORKSPACE", "BL_CLIENT_CREDENTIALS", "BL_ENV"):
        monkeypatch.delenv(var, raising=False)


def test_get_credentials_missing_config_does_not_raise(no_config, clear_auth_env, monkeypatch):
    """Root cause of import-time crash: only BL_API_KEY set with no config file.

    ``get_workspace()`` used to open a non-existent config and raise
    FileNotFoundError, breaking ``import blaxel`` entirely.
    """
    monkeypatch.setenv("BL_API_KEY", "fake-key")
    creds = get_credentials()
    assert creds is not None
    assert creds.api_key == "fake-key"
    assert creds.workspace is None


def test_apikey_without_workspace_get_headers_raises(no_config, clear_auth_env, monkeypatch):
    """Case 1: BL_API_KEY set, BL_WORKSPACE missing -> clear error, never a None header."""
    monkeypatch.setenv("BL_API_KEY", "fake-key")
    a = auth("prod", BASE_URL)
    assert isinstance(a, ApiKey)
    with pytest.raises(CredentialsError) as exc:
        a.get_headers()
    assert "BL_WORKSPACE" in str(exc.value)


def test_apikey_without_workspace_auth_flow_raises(no_config, clear_auth_env, monkeypatch):
    """Case 1, real httpx path: the auth_flow must raise instead of encoding a None header."""
    monkeypatch.setenv("BL_API_KEY", "fake-key")
    a = auth("prod", BASE_URL)
    req = httpx.Request("GET", f"{BASE_URL}/sandboxes")
    with pytest.raises(CredentialsError):
        next(a.auth_flow(req))


def test_workspace_only_names_missing_api_key(no_config, clear_auth_env, monkeypatch):
    """Case 2: BL_WORKSPACE set, BL_API_KEY missing -> error names the API key, not workspace."""
    monkeypatch.setenv("BL_WORKSPACE", "my-workspace")
    a = auth("prod", BASE_URL)
    assert isinstance(a, MissingCredentials)
    with pytest.raises(CredentialsError) as exc:
        a.get_headers()
    assert "BL_API_KEY" in str(exc.value)


def test_no_credentials_clear_error(no_config, clear_auth_env):
    """Neither var set, no config -> clear error naming both vars; token access also raises."""
    a = auth("prod", BASE_URL)
    assert isinstance(a, MissingCredentials)
    with pytest.raises(CredentialsError) as exc:
        a.get_headers()
    msg = str(exc.value)
    assert "BL_API_KEY" in msg and "BL_WORKSPACE" in msg
    with pytest.raises(CredentialsError):
        _ = a.token


def test_both_set_builds_clean_headers(no_config, clear_auth_env, monkeypatch):
    """Control: both present -> normal headers, no None values reach httpx."""
    monkeypatch.setenv("BL_API_KEY", "fake-key")
    monkeypatch.setenv("BL_WORKSPACE", "my-workspace")
    a = auth("prod", BASE_URL)
    headers = a.get_headers()
    assert headers["X-Blaxel-Workspace"] == "my-workspace"
    assert headers["X-Blaxel-Authorization"] == "Bearer fake-key"
    assert None not in headers.values()
    # and the real httpx encoding path no longer crashes
    encoded = dict(httpx.Headers(headers))
    assert encoded["x-blaxel-workspace"] == "my-workspace"


def test_settings_headers_clear_error_without_credentials(no_config, clear_auth_env):
    """Settings.headers must surface CredentialsError, not AttributeError on a None auth."""
    from blaxel.core.common.settings import Settings

    s = Settings()
    with pytest.raises(CredentialsError):
        _ = s.headers

"""Tests for the integration product token appended to the User-Agent."""

import os
import re

import pytest

from blaxel.core.common.settings import settings

SDK_USER_AGENT = re.compile(r"^blaxel/sdk/python/\S+ \([^)]+\) blaxel/\S+")


@pytest.fixture(autouse=True)
def _reset_integration():
    settings.integration = None
    settings._warned_integration = None
    os.environ.pop("BL_INTEGRATION", None)
    yield
    settings.integration = None
    os.environ.pop("BL_INTEGRATION", None)


def test_user_agent_has_no_token_by_default():
    user_agent = settings.headers["User-Agent"]
    assert SDK_USER_AGENT.fullmatch(user_agent), user_agent
    assert settings.integration == ""


def test_programmatic_token_is_appended_once():
    settings.integration = "deepseek-harness-blaxel-sandbox/0.1.2"
    user_agent = settings.headers["User-Agent"]
    assert user_agent.endswith(" deepseek-harness-blaxel-sandbox/0.1.2")
    assert SDK_USER_AGENT.match(user_agent)
    assert user_agent.count("deepseek-harness-blaxel-sandbox") == 1


def test_env_token_is_used_when_not_set_programmatically():
    os.environ["BL_INTEGRATION"] = "herdr/1.4.0-rc.1"
    assert settings.headers["User-Agent"].endswith(" herdr/1.4.0-rc.1")


def test_programmatic_token_wins_over_env():
    os.environ["BL_INTEGRATION"] = "herdr/1.4.0-rc.1"
    settings.integration = "deepseek-harness-blaxel-sandbox/0.1.2"
    assert settings.headers["User-Agent"].endswith(" deepseek-harness-blaxel-sandbox/0.1.2")


@pytest.mark.parametrize(
    "value",
    [
        "Deepseek/0.1.2",
        "deepseek-harness",
        "deepseek/0.1",
        "a/1.0.0 b/1.0.0",
        "deepseek/0.1.2 (extra)",
        " x/1.0.0",
        "x/1.0.0\n",
        "x/1.0.0\r\n",
    ],
)
def test_invalid_token_is_ignored(value, caplog):
    settings.integration = value
    with caplog.at_level("WARNING"):
        user_agent = settings.headers["User-Agent"]
    assert SDK_USER_AGENT.fullmatch(user_agent), user_agent
    assert "invalid Blaxel integration token" in caplog.text


def test_other_headers_are_untouched():
    settings.integration = "deepseek-harness-blaxel-sandbox/0.1.2"
    with_token = dict(settings.headers)
    settings.integration = None
    without_token = dict(settings.headers)
    with_token.pop("User-Agent")
    without_token.pop("User-Agent")
    assert with_token == without_token


def test_control_plane_client_sends_sdk_user_agent(monkeypatch):
    from blaxel.core.client.client import client
    from blaxel.core.common.autoload import autoload

    monkeypatch.setenv("BL_INTEGRATION", "my-integration/1.2.0")
    autoload()
    httpx_client = client.get_httpx_client()
    request = httpx_client.build_request("GET", "https://example.invalid/v0/sandboxes")
    for hook in httpx_client.event_hooks["request"]:
        hook(request)
    ua = request.headers["User-Agent"]
    assert ua.startswith("blaxel/sdk/python/")
    assert ua.endswith(" my-integration/1.2.0")
    assert "python-httpx" not in ua


def test_async_control_plane_client_keeps_user_agent_across_event_loops(monkeypatch):
    import asyncio

    from blaxel.core.client.client import client
    from blaxel.core.common.autoload import autoload

    monkeypatch.setenv("BL_INTEGRATION", "my-integration/1.2.0")
    autoload()

    async def user_agent_in_loop():
        # Created inside a running loop, so this is a fresh client, not the import-time one.
        httpx_client = client.get_async_httpx_client()
        request = httpx_client.build_request("GET", "https://example.invalid/v0/sandboxes")
        for hook in httpx_client.event_hooks["request"]:
            await hook(request)
        assert httpx_client.event_hooks["response"], "response interceptors were dropped"
        return request.headers["User-Agent"]

    for _ in range(2):
        ua = asyncio.run(user_agent_in_loop())
        assert ua.startswith("blaxel/sdk/python/")
        assert ua.endswith(" my-integration/1.2.0")


def test_invalid_token_warns_once(caplog):
    settings.integration = "Not-Valid"
    with caplog.at_level("WARNING"):
        for _ in range(5):
            assert settings.integration == ""
    assert caplog.text.count("invalid Blaxel integration token") == 1

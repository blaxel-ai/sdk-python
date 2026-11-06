"""Tests for the coding agent token appended to the User-Agent."""

import asyncio
import re
from pathlib import Path

import pytest

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.common.coding_agent import detect_coding_agent
from blaxel.core.common.settings import settings
from blaxel.core.sandbox.default.action import SandboxAction
from blaxel.core.sandbox.sync.action import SyncSandboxAction
from blaxel.core.sandbox.types import SandboxConfiguration

SDK_USER_AGENT = re.compile(r"^blaxel/sdk/python/\S+ \([^)]+\) blaxel/\S+")

pytestmark = pytest.mark.usefixtures("clear_coding_agent_env")


@pytest.fixture(autouse=True)
def _reset_integration():
    settings.integration = None
    yield
    settings.integration = None


def _home_with_config(config: str) -> None:
    home = Path.home()
    (home / ".blaxel").mkdir()
    (home / ".blaxel" / "config.yaml").write_text(config, encoding="utf-8")


def test_detect_returns_nothing_outside_a_coding_agent():
    assert detect_coding_agent({}.get) == ""
    assert detect_coding_agent({"CLAUDECODE": "", "AI_AGENT": "  "}.get) == ""


@pytest.mark.parametrize(
    ("env", "agent"),
    [
        ({"CLAUDECODE": "1"}, "claude-code"),
        ({"CODEX_THREAD_ID": "thread"}, "codex"),
        ({"CODEX_SANDBOX": "seatbelt"}, "codex"),
        ({"CURSOR_AGENT": "1"}, "cursor"),
        ({"GEMINI_CLI": "1"}, "gemini-cli"),
        ({"QWEN_CODE": "1"}, "qwen-code"),
        ({"OPENCODE_TERMINAL": "1"}, "opencode"),
        ({"OPENCODE": "1", "AGENT": "1"}, "opencode"),
        ({"GOOSE_TERMINAL": "1"}, "goose"),
        ({"AUGMENT_AGENT": "1"}, "augment"),
        ({"AI_AGENT": "claude-code_2-1-306_agent"}, "claude-code"),
        ({"AI_AGENT": "Cursor"}, "cursor"),
        ({"AI_AGENT": "crush", "AGENT": "crush"}, "crush"),
        ({"AI_AGENT": "github-copilot-cli"}, "github-copilot"),
        ({"AI_AGENT": "some-new-agent"}, "other"),
        ({"AI_AGENT": "Jane Doe's laptop"}, "other"),
        ({"AGENT": "goose"}, "goose"),
        ({"AGENT": "1"}, ""),
        ({"AGENT": "build-runner"}, ""),
        ({"AGENT": "goose", "AI_AGENT": "claude"}, "claude-code"),
        ({"AI_AGENT": "something-else", "CODEX_SANDBOX": "seatbelt"}, "codex"),
    ],
)
def test_detect_maps_markers_to_agent_ids(env, agent):
    assert detect_coding_agent(env.get) == agent


def test_user_agent_has_no_agent_token_by_default():
    assert settings.coding_agent == ""
    assert SDK_USER_AGENT.fullmatch(settings.headers["User-Agent"])


def test_agent_token_is_appended(monkeypatch):
    monkeypatch.setenv("CLAUDECODE", "1")
    assert settings.coding_agent == "claude-code"
    user_agent = settings.headers["User-Agent"]
    assert SDK_USER_AGENT.match(user_agent)
    assert user_agent.endswith(" agent/claude-code")


def test_agent_token_comes_after_the_integration_token(monkeypatch):
    monkeypatch.setenv("CODEX_SANDBOX", "seatbelt")
    settings.integration = "herdr/1.4.0"
    assert settings.user_agent.endswith(" herdr/1.4.0 agent/codex")


@pytest.mark.parametrize("value", ["1", "true", "TRUE"])
def test_do_not_track_drops_the_agent_token(monkeypatch, value):
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("DO_NOT_TRACK", value)
    assert settings.coding_agent == ""
    assert SDK_USER_AGENT.fullmatch(settings.user_agent)


def test_do_not_track_turning_tracking_on_keeps_the_agent_token(monkeypatch):
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("DO_NOT_TRACK", "0")
    assert settings.coding_agent == "claude-code"


def test_saved_tracking_false_keeps_the_agent_token(monkeypatch):
    # bl login saves tracking: false until the user opts in to error reports.
    _home_with_config("tracking: false\n")
    monkeypatch.setenv("CURSOR_AGENT", "1")
    assert settings.coding_agent == "cursor"


def test_unsaved_tracking_choice_keeps_the_agent_token(monkeypatch):
    _home_with_config("context:\n  workspace: test-ws\n")
    monkeypatch.setenv("CURSOR_AGENT", "1")
    assert settings.tracking is False
    assert settings.coding_agent == "cursor"


def test_control_plane_clients_send_the_agent_token(monkeypatch):
    from blaxel.core.client.client import client
    from blaxel.core.common.autoload import autoload

    monkeypatch.setenv("GEMINI_CLI", "1")
    autoload()

    sync_client = client.get_httpx_client()
    request = sync_client.build_request("GET", "https://example.invalid/v0/sandboxes")
    for hook in sync_client.event_hooks["request"]:
        hook(request)
    assert request.headers["User-Agent"].endswith(" agent/gemini-cli")

    async def async_user_agent():
        async_client = client.get_async_httpx_client()
        request = async_client.build_request("GET", "https://example.invalid/v0/sandboxes")
        for hook in async_client.event_hooks["request"]:
            await hook(request)
        return request.headers["User-Agent"]

    assert asyncio.run(async_user_agent()).endswith(" agent/gemini-cli")


def _sandbox_config() -> SandboxConfiguration:
    sandbox = Sandbox(
        metadata=Metadata(name="sandbox-a", url="https://sandbox-a.example.invalid"),
        spec=SandboxSpec(),
    )
    return SandboxConfiguration(sandbox)


def test_sandbox_clients_send_the_sdk_user_agent(monkeypatch):
    monkeypatch.setenv("OPENCODE", "1")
    config = _sandbox_config()

    sync_action = SyncSandboxAction(config)
    async_action = SandboxAction(config)
    user_agents = [
        sync_action.get_client().headers["User-Agent"],
        sync_action.get_api_client().get_httpx_client().headers["User-Agent"],
        async_action.get_client().headers["User-Agent"],
        async_action.get_api_client().get_httpx_client().headers["User-Agent"],
    ]

    for user_agent in user_agents:
        assert SDK_USER_AGENT.match(user_agent), user_agent
        assert user_agent.endswith(" agent/opencode"), user_agent
        assert "python-httpx" not in user_agent

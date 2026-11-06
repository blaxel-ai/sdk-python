"""Detect the coding agent (Claude Code, Codex, Cursor, ...) that runs the SDK."""

import re
from typing import Callable

# Environment variables coding agents set for the commands they run, first match
# wins, with the agent id the SDK reports. Ids match the Blaxel CLI's.
CODING_AGENTS: tuple[tuple[str, str], ...] = (
    ("CLAUDECODE", "claude-code"),
    ("CODEX_THREAD_ID", "codex"),
    ("CODEX_SANDBOX", "codex"),
    ("CURSOR_AGENT", "cursor"),
    ("GEMINI_CLI", "gemini-cli"),
    ("QWEN_CODE", "qwen-code"),
    ("OPENCODE_TERMINAL", "opencode"),
    ("OPENCODE", "opencode"),
    ("GOOSE_TERMINAL", "goose"),
    ("AUGMENT_AGENT", "augment"),
)

# Agent names found in the generic AI_AGENT and AGENT variables, mapped to the
# same ids. Any other AI_AGENT name is reported as "other".
CODING_AGENT_NAMES: dict[str, str] = {
    "claude-code": "claude-code",
    "claude": "claude-code",
    "codex": "codex",
    "cursor": "cursor",
    "cursor-cli": "cursor",
    "gemini-cli": "gemini-cli",
    "gemini": "gemini-cli",
    "qwen-code": "qwen-code",
    "opencode": "opencode",
    "goose": "goose",
    "augment": "augment",
    "augment-cli": "augment",
    "crush": "crush",
    "github-copilot": "github-copilot",
    "github-copilot-cli": "github-copilot",
}

# Every environment variable detect_coding_agent reads.
CODING_AGENT_ENV_VARS: tuple[str, ...] = tuple(name for name, _ in CODING_AGENTS) + (
    "AI_AGENT",
    "AGENT",
)

_NAME_END = re.compile(r"[_/@ ]")


def _agent_name(value: str | None) -> str:
    value = (value or "").strip().lower()
    # Claude Code sets AI_AGENT=claude-code_<version>_agent: keep the name.
    end = _NAME_END.search(value)
    if end and end.start() > 0:
        value = value[: end.start()]
    return value


def detect_coding_agent(getenv: Callable[[str], str | None]) -> str:
    """Id of the coding agent whose environment the SDK runs in.

    Returns "other" for an agent without a known name, or "" for none.
    """
    for name, agent_id in CODING_AGENTS:
        if (getenv(name) or "").strip():
            return agent_id
    name = _agent_name(getenv("AI_AGENT"))
    if name:
        return CODING_AGENT_NAMES.get(name, "other")
    # AGENT is a generic name, so only a known agent name counts.
    return CODING_AGENT_NAMES.get(_agent_name(getenv("AGENT")), "")

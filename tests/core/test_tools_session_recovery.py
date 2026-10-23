"""Tests for MCP tool-call recovery from terminated sessions.

Regression coverage for the "McpError: Session terminated" storm: a persisted
``PersistentMcpClient`` session can be torn down server-side (idle timeout,
redeploy, load-balancer drop). The client must drop the dead session so the next
call reconnects, and transparently reconnect-and-retry once when it was reusing a
persisted session (where the failed request never reached a live server).
"""

from mcp.shared.exceptions import McpError
from mcp.types import CallToolResult, ErrorData, TextContent

from blaxel.core.tools import PersistentMcpClient


def _terminated_error() -> McpError:
    # Mirrors what mcp's streamable_http client raises on a 404 (session gone):
    # ErrorData(code=32600, message="Session terminated").
    return McpError(ErrorData(code=32600, message="Session terminated"))


def _ok_result(text: str = "ok") -> CallToolResult:
    return CallToolResult(content=[TextContent(type="text", text=text)], isError=False)


class _FakeSession:
    """Fake MCP ClientSession whose ``send_request`` replays queued outcomes."""

    def __init__(self, outcomes):
        self._outcomes = list(outcomes)
        self.requests = 0

    async def send_request(self, request, result_type):
        self.requests += 1
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


def _make_client(connections):
    """Build a client whose ``initialize`` hands out ``connections`` in order.

    ``connections`` are the sessions produced by successive (re)connections,
    simulating what a fresh transport would yield.
    """
    client = PersistentMcpClient("test-fn", timeout_enabled=True)
    # Keep the inactivity timer out of the test: no background tasks.
    client._remove_timer = lambda: None
    client._reset_timer = lambda: None

    pending = list(connections)

    async def fake_initialize():
        if client.session is None:
            client.session = pending.pop(0)

    client.initialize = fake_initialize
    return client


async def test_reused_terminated_session_reconnects_and_retries():
    """A stale persisted session is dropped, reconnected, and the call retried."""
    dead = _FakeSession([_terminated_error()])
    healthy = _FakeSession([_ok_result()])
    client = _make_client([healthy])
    client.session = dead  # simulate a persisted session from a prior call

    result = await client.call_tool("ListInvestorUpdatesByStatus", {})

    assert result.isError is not True
    assert result.content[0].text == "ok"
    assert dead.requests == 1
    assert healthy.requests == 1
    # The healthy reconnected session is kept for subsequent calls.
    assert client.session is healthy


async def test_fresh_session_failure_is_not_retried_but_is_cleaned_up():
    """A freshly-connected session that fails is not retried (no double-call),
    but the session is dropped so the next call reconnects."""
    dead = _FakeSession([_terminated_error()])
    client = _make_client([dead])
    client.session = None  # no persisted session -> initialize() connects fresh

    result = await client.call_tool("ListInvestorUpdatesByStatus", {})

    assert result.isError is True
    assert "Session terminated" in result.content[0].text
    assert dead.requests == 1  # not retried
    assert client.session is None  # cleaned up for the next call


async def test_retry_failure_surfaces_error_and_resets_session():
    """When both the stale call and the reconnect fail, surface an error result
    and leave no dead session behind."""
    dead = _FakeSession([_terminated_error()])
    still_dead = _FakeSession([_terminated_error()])
    client = _make_client([still_dead])
    client.session = dead

    result = await client.call_tool("ListInvestorUpdatesByStatus", {})

    assert result.isError is True
    assert dead.requests == 1
    assert still_dead.requests == 1  # retried exactly once
    assert client.session is None


async def test_successful_call_keeps_session_without_retry():
    """The happy path returns the result and performs no reconnect."""
    healthy = _FakeSession([_ok_result("done")])
    client = _make_client([])
    client.session = healthy

    result = await client.call_tool("ListInvestorUpdatesByStatus", {})

    assert result.content[0].text == "done"
    assert healthy.requests == 1
    assert client.session is healthy

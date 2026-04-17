"""Proxy end-to-end tests with Claude Code agent."""

import os

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name

from .helpers import default_region

pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="requires ANTHROPIC_API_KEY",
)

CLAUDE_ENV = " ".join([
    "export PATH=/usr/local/bin:/usr/bin:/bin",
    "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY",
    "HTTP_PROXY=$HTTP_PROXY",
    "HTTPS_PROXY=$HTTPS_PROXY",
    "NO_PROXY=$NO_PROXY",
    "NODE_EXTRA_CA_CERTS=$NODE_EXTRA_CA_CERTS",
    "SSL_CERT_FILE=$SSL_CERT_FILE",
])


@pytest.mark.asyncio(loop_scope="class")
class TestProxyClaudeCode:
    """Proxy end-to-end with the Claude Code agent."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        api_key = os.environ["ANTHROPIC_API_KEY"]

        request.cls.sandbox_name = unique_name("proxy-claude")
        request.cls.sandbox = await SandboxInstance.create({
            "name": request.cls.sandbox_name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "envs": [{"name": "ANTHROPIC_API_KEY", "value": api_key}],
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["httpbin.org"],
                            "headers": {"X-Agent-Test": "claude-injected"},
                        },
                    ],
                },
            },
        })

        setup = await request.cls.sandbox.process.exec({
            "command": (
                "apk add --no-cache curl bash 2>&1 && "
                "npm install -g @anthropic-ai/claude-code 2>&1 && "
                "adduser -D -s /bin/bash agent 2>&1"
            ),
            "wait_for_completion": True,
        })
        if setup.exit_code != 0:
            raise RuntimeError(f"setup failed: {(setup.logs or '')[:500]}")

        yield
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_agent_reaches_anthropic_api_through_proxy(self):
        result = await self.sandbox.process.exec({
            "command": (
                f'su - agent -c "{CLAUDE_ENV} && '
                "claude --dangerously-skip-permissions -p "
                '\\"What is 2+2? Reply with ONLY the number.\\" '
                '--output-format text" 2>&1'
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert "4" in (result.logs or "")

    async def test_agent_makes_outbound_call_with_header_injection(self):
        result = await self.sandbox.process.exec({
            "command": (
                f'su - agent -c "{CLAUDE_ENV} && '
                "claude --dangerously-skip-permissions -p "
                '\\"Run: curl -s https://httpbin.org/headers — then print the full JSON output.\\" '
                '--output-format text" 2>&1'
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert "X-Agent-Test" in (result.logs or "")
        assert "claude-injected" in (result.logs or "")

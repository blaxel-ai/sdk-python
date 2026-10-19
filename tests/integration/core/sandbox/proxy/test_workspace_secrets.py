"""Workspace secrets resolved by the egress proxy: set via the SDK, injected at runtime."""

import asyncio

import pytest
import pytest_asyncio

from blaxel.core import SecretInstance
from blaxel.core.client.client import client
from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name
from tests.helpers.echo import echo_host

from .helpers import (
    PROXY_HELPER_SCRIPT,
    default_region,
    lowercase_keys,
    parse_json_output,
    write_echo_url,
)

# Workspace secrets are behind the "workspace-secrets" feature flag (403 when off,
# 404 on environments that predate controlplane#5736): skip unless the workspace has them.
pytestmark = pytest.mark.skipif(
    client.get_httpx_client().get("/secrets").status_code in (403, 404),
    reason="workspace secrets not enabled for this workspace/environment",
)


async def headers_seen_by_upstream(
    sandbox: SandboxInstance, extra_headers: str = ""
) -> dict[str, str]:
    command = "node /tmp/proxy-test.js GET $(cat /tmp/echo-url)/headers"
    if extra_headers:
        command += f" '{extra_headers}'"
    result = await sandbox.process.exec({"command": command, "wait_for_completion": True})
    assert result.exit_code == 0, result.logs
    return lowercase_keys(parse_json_output(result.logs)["headers"])


async def wait_for_header(sandbox: SandboxInstance, header: str, expected: str | None) -> None:
    """A secret write reaches the proxy synchronously, but a running sandbox only
    observes it on its next proxied request, so poll briefly. ``expected=None``
    means the proxy must stop injecting the header altogether."""
    seen = None
    for _ in range(15):
        seen = (await headers_seen_by_upstream(sandbox)).get(header)
        if seen == expected:
            return
        await asyncio.sleep(2)
    assert seen == expected


@pytest.mark.asyncio(loop_scope="class")
class TestWorkspaceSecretsResolvedByProxy:
    sandbox: SandboxInstance
    sandbox_name: str
    ws_secret: str
    shared_name: str
    missing_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup(self, request):
        cls = request.cls
        cls.ws_secret = unique_name("ws-token")
        cls.shared_name = unique_name("ws-shared")
        cls.missing_name = unique_name("ws-missing")
        await SecretInstance.set(cls.ws_secret, "ws-value-1")
        await SecretInstance.set(cls.shared_name, "workspace-level")

        echo_hostname = await echo_host()
        cls.sandbox_name = unique_name("proxy-ws-sec")
        cls.sandbox = await SandboxInstance.create(
            {
                "name": cls.sandbox_name,
                "image": default_image,
                "region": default_region,
                "labels": default_labels,
                "network": {
                    "proxy": {
                        "routing": [
                            {
                                "destinations": [echo_hostname],
                                "headers": {
                                    "X-Ws-Token": f"Bearer {{{{SECRET:{cls.ws_secret}}}}}",
                                    "X-Shared": f"{{{{SECRET:{cls.shared_name}}}}}",
                                    "X-Missing": f"{{{{SECRET:{cls.missing_name}}}}}",
                                },
                                "body": {"ws_key": f"{{{{SECRET:{cls.ws_secret}}}}}"},
                                # same name as a workspace secret: the rule-level value must win
                                "secrets": {cls.shared_name: "rule-level"},
                            },
                        ],
                    },
                },
            }
        )
        await cls.sandbox.fs.write("/tmp/proxy-test.js", PROXY_HELPER_SCRIPT)
        await write_echo_url(cls.sandbox)
        yield
        for name in (cls.ws_secret, cls.shared_name):
            try:
                await SecretInstance.delete(name)
            except Exception:
                pass
        try:
            await SandboxInstance.delete(cls.sandbox_name)
        except Exception:
            pass

    async def test_resolves_workspace_secret_the_rule_does_not_declare(self):
        headers = await headers_seen_by_upstream(self.sandbox)
        assert headers["x-ws-token"] == "Bearer ws-value-1"

    async def test_resolves_workspace_secret_in_post_body(self):
        result = await self.sandbox.process.exec(
            {
                "command": "node /tmp/proxy-test.js POST $(cat /tmp/echo-url)/post '{}' '{\"user_field\":\"untouched\"}'",
                "wait_for_completion": True,
            }
        )
        assert result.exit_code == 0, result.logs
        body = parse_json_output(result.logs)["json"]
        assert body["user_field"] == "untouched"
        assert body["ws_key"] == "ws-value-1"

    async def test_resolves_workspace_secret_in_user_sent_headers(self):
        headers = await headers_seen_by_upstream(
            self.sandbox, f'{{"X-User-Token":"{{{{SECRET:{self.ws_secret}}}}}"}}'
        )
        assert headers["x-user-token"] == "ws-value-1"

    async def test_rule_level_secret_wins_over_workspace_secret_with_same_name(self):
        headers = await headers_seen_by_upstream(self.sandbox)
        assert headers["x-shared"] == "rule-level"

    async def test_does_not_inject_header_whose_secret_exists_nowhere(self):
        headers = await headers_seen_by_upstream(self.sandbox)
        assert "x-missing" not in headers

    async def test_serves_latest_value_after_rotation(self):
        await SecretInstance.set(self.ws_secret, "ws-value-2")
        await wait_for_header(self.sandbox, "x-ws-token", "Bearer ws-value-2")

    async def test_stops_injecting_header_once_workspace_secret_is_deleted(self):
        await SecretInstance.delete(self.ws_secret)
        await wait_for_header(self.sandbox, "x-ws-token", None)

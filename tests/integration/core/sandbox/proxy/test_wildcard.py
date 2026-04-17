"""Proxy wildcard (``*``) destination tests."""

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name

from .helpers import (
    PROXY_HELPER_SCRIPT,
    default_region,
    lowercase_keys,
    parse_json_output,
)


@pytest.mark.asyncio(loop_scope="class")
class TestProxyWildcardDestination:
    """Proxy routing with wildcard (``*``) destination."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.sandbox_name = unique_name("proxy-wild")
        request.cls.sandbox = await SandboxInstance.create({
            "name": request.cls.sandbox_name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["*"],
                            "headers": {"X-Global-Auth": "Bearer {{SECRET:global-key}}"},
                            "secrets": {"global-key": "global-token-xyz"},
                        },
                    ],
                },
            },
        })
        await request.cls.sandbox.fs.write("/tmp/proxy-test.js", PROXY_HELPER_SCRIPT)
        yield
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_applies_global_rule_to_httpbin(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/headers",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert headers["x-global-auth"] == "Bearer global-token-xyz"

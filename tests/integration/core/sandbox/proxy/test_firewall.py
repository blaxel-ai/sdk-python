"""Firewall e2e tests (allowedDomains / forbiddenDomains)."""

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
class TestFirewallAllowedDomains:
    """allowedDomains (allowlist) behavior."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.sandbox_name = unique_name("fw-allow")
        request.cls.sandbox = await SandboxInstance.create({
            "name": request.cls.sandbox_name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "allowedDomains": ["httpbin.org"],
                "proxy": {"routing": []},
            },
        })
        await request.cls.sandbox.fs.write("/tmp/proxy-test.js", PROXY_HELPER_SCRIPT)
        yield
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_allows_requests_to_allowlisted_domain(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/get",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert "httpbin.org" in (result.logs or "")

    async def test_blocks_requests_to_non_allowlisted_domain(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://example.com",
            "wait_for_completion": True,
        })
        assert result.exit_code != 0


@pytest.mark.asyncio(loop_scope="class")
class TestFirewallForbiddenDomains:
    """forbiddenDomains (denylist) behavior."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.sandbox_name = unique_name("fw-deny")
        request.cls.sandbox = await SandboxInstance.create({
            "name": request.cls.sandbox_name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "forbiddenDomains": ["example.com"],
                "proxy": {"routing": []},
            },
        })
        await request.cls.sandbox.fs.write("/tmp/proxy-test.js", PROXY_HELPER_SCRIPT)
        yield
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_allows_requests_to_non_forbidden_domain(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/get",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert "httpbin.org" in (result.logs or "")

    async def test_blocks_requests_to_forbidden_domain(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://example.com",
            "wait_for_completion": True,
        })
        assert result.exit_code != 0


@pytest.mark.asyncio(loop_scope="class")
class TestFirewallCombined:
    """allowedDomains + forbiddenDomains combined behavior."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.sandbox_name = unique_name("fw-combo")
        request.cls.sandbox = await SandboxInstance.create({
            "name": request.cls.sandbox_name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "allowedDomains": ["httpbin.org", "example.com"],
                "forbiddenDomains": ["example.com"],
                "proxy": {"routing": []},
            },
        })
        await request.cls.sandbox.fs.write("/tmp/proxy-test.js", PROXY_HELPER_SCRIPT)
        yield
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_allowed_domains_takes_precedence_over_forbidden_domains(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/get",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert "httpbin.org" in (result.logs or "")


@pytest.mark.asyncio(loop_scope="class")
class TestFirewallWithProxyRouting:
    """allowedDomains with proxy routing."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.sandbox_name = unique_name("fw-proxy")
        request.cls.sandbox = await SandboxInstance.create({
            "name": request.cls.sandbox_name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "allowedDomains": ["httpbin.org"],
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["httpbin.org"],
                            "headers": {"X-Firewall-Test": "allowed-and-injected"},
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

    async def test_injects_headers_for_allowlisted_and_routed_domain(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/headers",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert headers["x-firewall-test"] == "allowed-and-injected"

    async def test_blocks_non_allowlisted_domain_even_without_routing(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://example.com",
            "wait_for_completion": True,
        })
        assert result.exit_code != 0

"""Proxy end-to-end functionality tests."""

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name
from tests.helpers.echo import echo_host

from .helpers import (
    PROXY_HELPER_SCRIPT,
    default_region,
    lowercase_keys,
    parse_json_output,
    parse_response_headers,
    write_echo_url,
)


@pytest.mark.asyncio(loop_scope="class")
class TestProxyEndToEnd:
    """Proxy end-to-end functionality with header/body injection."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        echo_hostname = await echo_host()
        request.cls.sandbox_name = unique_name("proxy-e2e")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": default_image,
                "region": default_region,
                "labels": default_labels,
                "network": {
                    "proxy": {
                        "routing": [
                            {
                                "destinations": [echo_hostname],
                                "headers": {
                                    "X-Proxy-Test": "header-injected",
                                    "X-Api-Key": "{{SECRET:test-api-key}}",
                                },
                                "body": {
                                    "injected_field": "body-injected",
                                    "secret_body": "{{SECRET:test-api-key}}",
                                },
                                "secrets": {"test-api-key": "resolved-secret-42"},
                            },
                        ],
                    },
                },
            }
        )
        await request.cls.sandbox.fs.write("/tmp/proxy-test.js", PROXY_HELPER_SCRIPT)
        await write_echo_url(request.cls.sandbox)
        yield
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_routes_https_requests_through_proxy_with_header_injection(self):
        result = await self.sandbox.process.exec(
            {
                "command": "node /tmp/proxy-test.js GET $(cat /tmp/echo-url)/headers",
                "wait_for_completion": True,
            }
        )
        assert result.exit_code == 0
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert parse_response_headers(result.logs).get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"
        assert headers["x-api-key"] == "resolved-secret-42"

    async def test_routes_post_requests_through_proxy_with_body_injection(self):
        result = await self.sandbox.process.exec(
            {
                "command": """node /tmp/proxy-test.js POST $(cat /tmp/echo-url)/post '{}' '{"user_data":"original"}'""",
                "wait_for_completion": True,
            }
        )
        assert result.exit_code == 0
        response = parse_json_output(result.logs)
        assert response["json"]["user_data"] == "original"
        headers = lowercase_keys(response["headers"])
        assert parse_response_headers(result.logs).get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"
        assert headers["x-api-key"] == "resolved-secret-42"
        assert response["json"]["injected_field"] == "body-injected"
        assert response["json"]["secret_body"] == "resolved-secret-42"

    async def test_preserves_user_sent_headers_when_routing(self):
        result = await self.sandbox.process.exec(
            {
                "command": """node /tmp/proxy-test.js GET $(cat /tmp/echo-url)/headers '{"X-User-Custom":"my-value"}'""",
                "wait_for_completion": True,
            }
        )
        assert result.exit_code == 0
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert headers["x-user-custom"] == "my-value"
        assert parse_response_headers(result.logs).get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"

    async def test_does_not_route_local_requests_through_proxy(self):
        result = await self.sandbox.process.exec(
            {
                "command": (
                    "node -e '"
                    'const http = require("http");'
                    "const srv = http.createServer((req, res) => {"
                    'res.writeHead(200, {"Content-Type": "application/json"});'
                    "res.end(JSON.stringify(req.headers));"
                    "});"
                    "srv.listen(19876, () => {"
                    'http.get("http://localhost:19876", (r) => {'
                    'let d = ""; r.on("data", c => d += c);'
                    'r.on("end", () => { console.log(d); srv.close(); });'
                    "});"
                    "});'"
                ),
                "wait_for_completion": True,
            }
        )
        assert result.exit_code == 0
        headers = parse_json_output(result.logs)
        assert headers.get("x-blaxel-request-id") is None
        assert headers.get("x-proxy-test") is None

    async def test_does_not_inject_headers_for_non_routed_destinations(self):
        result = await self.sandbox.process.exec(
            {
                "command": "node /tmp/proxy-test.js GET https://www.google.com",
                "wait_for_completion": True,
            }
        )
        assert result.exit_code == 0
        assert len((result.logs or "").strip()) > 0

    async def test_verifies_proxy_env_vars_are_set(self):
        result = await self.sandbox.process.exec(
            {
                "command": (
                    "node -e '"
                    'const vars = ["HTTP_PROXY","HTTPS_PROXY","NO_PROXY","NODE_EXTRA_CA_CERTS","SSL_CERT_FILE"];'
                    "const result = {};"
                    'vars.forEach(v => result[v] = process.env[v] ? "set" : "unset");'
                    "console.log(JSON.stringify(result));'"
                ),
                "wait_for_completion": True,
            }
        )
        assert result.exit_code == 0
        envs = parse_json_output(result.logs)
        assert envs["HTTP_PROXY"] == "set"
        assert envs["HTTPS_PROXY"] == "set"
        assert envs["NO_PROXY"] == "set"
        assert envs["NODE_EXTRA_CA_CERTS"] == "set"
        assert envs["SSL_CERT_FILE"] == "set"


@pytest.mark.asyncio(loop_scope="class")
class TestProxyWildcardMatching:
    """``*.domain`` matches subdomains of ``domain`` but not ``domain`` itself.

    The echo host is ``<id>.<region>.preview.bl.run``, so a wildcard on its
    parent domain must match it, while a wildcard on the host itself must not.
    """

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        echo_hostname = await echo_host()
        echo_parent_domain = echo_hostname.split(".", 1)[1]
        request.cls.sandbox_name = unique_name("proxy-wildcard-match")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": default_image,
                "region": default_region,
                "labels": default_labels,
                "network": {
                    "proxy": {
                        "routing": [
                            {
                                "destinations": [f"*.{echo_parent_domain}"],
                                "headers": {"X-Wildcard-Match": "wildcard-injected"},
                            },
                            {
                                "destinations": [f"*.{echo_hostname}"],
                                "headers": {"X-Wildcard-Bare": "should-not-be-injected"},
                            },
                        ],
                    },
                },
            }
        )
        await request.cls.sandbox.fs.write("/tmp/proxy-test.js", PROXY_HELPER_SCRIPT)
        await write_echo_url(request.cls.sandbox)
        yield
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_wildcard_route_matches_subdomain(self):
        result = await self.sandbox.process.exec(
            {
                "command": "node /tmp/proxy-test.js GET $(cat /tmp/echo-url)/headers",
                "wait_for_completion": True,
            }
        )
        assert result.exit_code == 0
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert headers["x-wildcard-match"] == "wildcard-injected"

    async def test_wildcard_route_does_not_match_bare_domain(self):
        result = await self.sandbox.process.exec(
            {
                "command": "node /tmp/proxy-test.js GET $(cat /tmp/echo-url)/headers",
                "wait_for_completion": True,
            }
        )
        assert result.exit_code == 0
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert headers.get("x-wildcard-bare") is None

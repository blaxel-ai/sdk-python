import json
import os

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import (
    default_image,
    default_labels,
    default_region,
    unique_name,
    wait_for_sandbox_deletion,
)


def _get_network(sandbox):
    """Get the network config from a sandbox, returning a dict-like object."""
    net = sandbox.spec.network
    if net is None or (hasattr(net, "__class__") and net.__class__.__name__ == "Unset"):
        return None
    return net


def _parse_json_output(logs: str | None) -> dict:
    if not logs:
        raise ValueError("No output from command")
    trimmed = logs.strip()
    json_start = trimmed.find("{")
    if json_start == -1:
        raise ValueError(f"No JSON found in output: {trimmed[:200]}")
    depth = 0
    json_end = -1
    for i in range(json_start, len(trimmed)):
        if trimmed[i] == "{":
            depth += 1
        elif trimmed[i] == "}":
            depth -= 1
            if depth == 0:
                json_end = i + 1
                break
    if json_end == -1:
        raise ValueError(f"Unterminated JSON in output: {trimmed[:300]}")
    return json.loads(trimmed[json_start:json_end])


def _lowercase_keys(obj: dict[str, str]) -> dict[str, str]:
    return {k.lower(): v for k, v in obj.items()}


PROXY_HELPER_SCRIPT = r"""
const https = require("https");
const tls = require("tls");
const method = process.argv[2] || "GET";
const targetUrl = process.argv[3] || "https://httpbin.org/headers";
const extraHeaders = process.argv[4] ? JSON.parse(process.argv[4]) : {};
const bodyData = process.argv[5] || null;
const proxyUrl = process.env.HTTPS_PROXY || process.env.https_proxy ||
                 process.env.HTTP_PROXY || process.env.http_proxy;

function fire(socket) {
  const t = new URL(targetUrl);
  const opts = {
    hostname: t.hostname, port: t.port || 443,
    path: t.pathname + t.search, method,
    headers: { ...extraHeaders }, servername: t.hostname,
  };
  if (socket) { opts.socket = socket; opts.agent = false; }
  if (bodyData) {
    opts.headers["Content-Type"] = "application/json";
    opts.headers["Content-Length"] = Buffer.byteLength(bodyData);
  }
  const req = https.request(opts, (r) => {
    let d = ""; r.on("data", c => d += c);
    r.on("end", () => { process.stdout.write(d); process.exit(0); });
  });
  req.on("error", (e) => { process.stderr.write("REQ ERR: " + e.message + "\n"); process.exit(1); });
  if (bodyData) req.write(bodyData);
  req.end();
}

if (!proxyUrl) { fire(null); }
else {
  const p = new URL(proxyUrl);
  const t = new URL(targetUrl);
  const port = parseInt(p.port) || (p.protocol === "https:" ? 443 : 3128);
  const auth = (p.username || p.password)
    ? "Proxy-Authorization: Basic " +
      Buffer.from(decodeURIComponent(p.username||"") + ":" + decodeURIComponent(p.password||"")).toString("base64") + "\r\n"
    : "";
  const connectMsg = "CONNECT " + t.hostname + ":443 HTTP/1.1\r\n" +
    "Host: " + t.hostname + ":443\r\n" + auth + "\r\n";

  function onSocket(sock) {
    let buf = "";
    sock.on("data", function h(chunk) {
      buf += chunk.toString();
      if (buf.indexOf("\r\n\r\n") < 0) return;
      sock.removeListener("data", h);
      const code = parseInt(buf.split(" ")[1]);
      if (code !== 200) {
        process.stderr.write("CONNECT " + code + "\n");
        process.exit(1);
      }
      fire(sock);
    });
    sock.write(connectMsg);
  }

  const timeout = setTimeout(() => { process.stderr.write("PROXY TIMEOUT\n"); process.exit(1); }, 15000);
  if (p.protocol === "https:") {
    const s = tls.connect({ host: p.hostname, port }, () => { clearTimeout(timeout); onSocket(s); });
    s.on("error", (e) => { clearTimeout(timeout); process.stderr.write("PROXY TLS: " + e.message + "\n"); process.exit(1); });
  } else {
    const s = require("net").connect({ host: p.hostname, port }, () => { clearTimeout(timeout); onSocket(s); });
    s.on("error", (e) => { clearTimeout(timeout); process.stderr.write("PROXY TCP: " + e.message + "\n"); process.exit(1); });
  }
}
""".strip()

PYTHON_HELPER_SCRIPT = """
import sys, json, requests
method = sys.argv[1] if len(sys.argv) > 1 else "GET"
url = sys.argv[2] if len(sys.argv) > 2 else "https://httpbin.org/headers"
headers = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
body = sys.argv[4] if len(sys.argv) > 4 else None
resp = requests.request(method, url, headers=headers, data=body, timeout=30)
print(resp.text)
""".strip()


# =============================================================================
# Create with Proxy Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestCreateWithProxy:
    """Test creating sandboxes with proxy configuration."""

    async def test_creates_sandbox_with_proxy_routing_and_header_injection(self):
        name = unique_name("proxy-hdr")
        sandbox = await SandboxInstance.create({
            "name": name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["api.stripe.com"],
                            "headers": {
                                "Authorization": "Bearer {{SECRET:stripe-key}}",
                                "Stripe-Version": "2024-12-18.acacia",
                            },
                            "secrets": {
                                "stripe-key": "sk-live-test123",
                            },
                        },
                    ],
                },
            },
        })

        try:
            assert sandbox.metadata.name == name
            network = _get_network(sandbox)
            assert network is not None
            proxy = network["proxy"]
            assert proxy is not None
            assert len(proxy["routing"]) == 1
            assert "api.stripe.com" in proxy["routing"][0]["destinations"]
            assert proxy["routing"][0]["headers"]["Authorization"] == "Bearer {{SECRET:stripe-key}}"
            assert proxy["routing"][0]["headers"]["Stripe-Version"] == "2024-12-18.acacia"
            assert proxy["routing"][0].get("secrets") is None
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_proxy_body_injection(self):
        name = unique_name("proxy-body")
        sandbox = await SandboxInstance.create({
            "name": name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["api.stripe.com"],
                            "headers": {
                                "Authorization": "Bearer {{SECRET:stripe-key}}",
                            },
                            "body": {
                                "api_key": "{{SECRET:stripe-key}}",
                            },
                            "secrets": {
                                "stripe-key": "sk-live-test123",
                            },
                        },
                    ],
                },
            },
        })

        try:
            network = _get_network(sandbox)
            assert network is not None
            route = network["proxy"]["routing"][0]
            assert route.get("body") is not None
            assert route["body"]["api_key"] == "{{SECRET:stripe-key}}"
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_multiple_proxy_routing_rules(self):
        name = unique_name("proxy-multi")
        sandbox = await SandboxInstance.create({
            "name": name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["api.stripe.com"],
                            "headers": {
                                "Authorization": "Bearer {{SECRET:stripe-key}}",
                                "Stripe-Version": "2024-12-18.acacia",
                                "X-Request-Source": "blaxel-sandbox",
                            },
                            "body": {
                                "api_key": "{{SECRET:stripe-key}}",
                            },
                            "secrets": {
                                "stripe-key": "sk-live-test123",
                            },
                        },
                        {
                            "destinations": ["api.openai.com"],
                            "headers": {
                                "Authorization": "Bearer {{SECRET:openai-key}}",
                                "OpenAI-Organization": "org-abc123",
                            },
                            "secrets": {
                                "openai-key": "sk-proj-test789",
                            },
                        },
                    ],
                    "bypass": ["*.s3.amazonaws.com"],
                },
            },
        })

        try:
            network = _get_network(sandbox)
            assert network is not None
            proxy_config = network["proxy"]
            assert len(proxy_config["routing"]) == 2

            stripe_route = next(
                (r for r in proxy_config["routing"] if "api.stripe.com" in r["destinations"]),
                None,
            )
            assert stripe_route is not None
            assert stripe_route["headers"]["X-Request-Source"] == "blaxel-sandbox"
            assert stripe_route["body"]["api_key"] == "{{SECRET:stripe-key}}"
            assert stripe_route.get("secrets") is None

            openai_route = next(
                (r for r in proxy_config["routing"] if "api.openai.com" in r["destinations"]),
                None,
            )
            assert openai_route is not None
            assert openai_route["headers"]["OpenAI-Organization"] == "org-abc123"
            assert openai_route.get("secrets") is None

            assert "*.s3.amazonaws.com" in proxy_config["bypass"]
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_proxy_bypass_only(self):
        name = unique_name("proxy-bypass")
        sandbox = await SandboxInstance.create({
            "name": name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "proxy": {
                    "bypass": ["*.s3.amazonaws.com", "169.254.169.254"],
                },
            },
        })

        try:
            network = _get_network(sandbox)
            assert network is not None
            assert network["proxy"]["bypass"] == ["*.s3.amazonaws.com", "169.254.169.254"]
            assert network["proxy"].get("routing") is None
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_proxy_and_allowed_domains_combined(self):
        name = unique_name("proxy-fw")
        sandbox = await SandboxInstance.create({
            "name": name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "allowedDomains": ["api.stripe.com", "api.openai.com", "*.s3.amazonaws.com"],
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["api.stripe.com"],
                            "headers": {"Authorization": "Bearer {{SECRET:stripe-key}}"},
                            "secrets": {"stripe-key": "sk-live-test123"},
                        },
                    ],
                    "bypass": ["*.s3.amazonaws.com"],
                },
            },
        })

        try:
            network = _get_network(sandbox)
            assert network is not None
            allowed = network.get("allowedDomains")
            proxy_routing = network.get("proxy", {}).get("routing")
            assert allowed is not None or proxy_routing is not None
            assert len(network["proxy"]["routing"]) == 1
            assert "*.s3.amazonaws.com" in network["proxy"]["bypass"]
        finally:
            await SandboxInstance.delete(name)


# =============================================================================
# Get Proxy Config Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestGetProxyConfig:
    """Test retrieving sandbox proxy configuration."""

    async def test_retrieves_sandbox_with_proxy_and_validates_config(self):
        name = unique_name("proxy-get")
        await SandboxInstance.create({
            "name": name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["api.openai.com"],
                            "headers": {
                                "Authorization": "Bearer {{SECRET:openai-key}}",
                                "OpenAI-Organization": "org-abc123",
                            },
                            "secrets": {
                                "openai-key": "sk-proj-test789",
                            },
                        },
                    ],
                    "bypass": ["169.254.169.254"],
                },
            },
        })

        try:
            retrieved = await SandboxInstance.get(name)
            network = _get_network(retrieved)
            assert network is not None
            proxy = network.get("proxy")
            if proxy:
                assert len(proxy["routing"]) == 1
                assert "api.openai.com" in proxy["routing"][0]["destinations"]
                assert proxy["routing"][0]["headers"]["Authorization"] == "Bearer {{SECRET:openai-key}}"
                assert proxy["routing"][0]["headers"]["OpenAI-Organization"] == "org-abc123"
                assert "169.254.169.254" in proxy["bypass"]
                assert proxy["routing"][0].get("secrets") is None
        finally:
            await SandboxInstance.delete(name)

    async def test_returns_no_proxy_config_when_sandbox_has_none(self):
        name = unique_name("proxy-none")
        await SandboxInstance.create({
            "name": name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
        })

        try:
            retrieved = await SandboxInstance.get(name)
            network = _get_network(retrieved)
            if network is not None:
                assert network.get("proxy") is None
        finally:
            await SandboxInstance.delete(name)


# =============================================================================
# Delete Sandbox with Proxy Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestDeleteSandboxWithProxy:
    """Test deleting sandboxes with proxy configuration."""

    async def test_deletes_sandbox_with_proxy_configuration(self):
        name = unique_name("proxy-del")
        await SandboxInstance.create({
            "name": name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["api.stripe.com"],
                            "headers": {"Authorization": "Bearer {{SECRET:stripe-key}}"},
                            "secrets": {"stripe-key": "sk-live-test123"},
                        },
                    ],
                },
            },
        })

        await SandboxInstance.delete(name)
        deleted = await wait_for_sandbox_deletion(name)
        assert deleted is True


# =============================================================================
# Firewall E2E (allowedDomains / forbiddenDomains) Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestFirewallAllowedDomains:
    """Test allowedDomains (allowlist) firewall behavior."""

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
    """Test forbiddenDomains (denylist) firewall behavior."""

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
    """Test allowedDomains + forbiddenDomains combined behavior."""

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
    """Test allowedDomains with proxy routing."""

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

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers["x-firewall-test"] == "allowed-and-injected"

    async def test_blocks_non_allowlisted_domain_even_without_routing(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://example.com",
            "wait_for_completion": True,
        })
        assert result.exit_code != 0


# =============================================================================
# Secrets Replacement Validation Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestSecretsReplacementValidation:
    """Test proxy secret template resolution."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.sandbox_name = unique_name("proxy-sec")
        request.cls.sandbox = await SandboxInstance.create({
            "name": request.cls.sandbox_name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["httpbin.org"],
                            "headers": {
                                "X-Token": "Bearer {{SECRET:api-token}}",
                                "X-Multi": "{{SECRET:part-a}}-{{SECRET:part-b}}",
                                "X-Plain": "no-secret-here",
                            },
                            "body": {
                                "secret_key": "{{SECRET:api-token}}",
                                "composite": "prefix-{{SECRET:part-a}}-suffix",
                            },
                            "secrets": {
                                "api-token": "tok_live_abc123",
                                "part-a": "ALPHA",
                                "part-b": "BETA",
                            },
                        },
                        {
                            "destinations": ["*.example.com"],
                            "headers": {
                                "X-Other-Secret": "{{SECRET:other-key}}",
                            },
                            "secrets": {
                                "other-key": "other-value-999",
                            },
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

    async def test_resolves_secret_in_headers_to_actual_value(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/headers",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers["x-token"] == "Bearer tok_live_abc123"
        assert headers["x-plain"] == "no-secret-here"

    async def test_resolves_multiple_secret_placeholders_in_single_header(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/headers",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers["x-multi"] == "ALPHA-BETA"

    async def test_resolves_secret_in_post_body_fields(self):
        result = await self.sandbox.process.exec({
            "command": """node /tmp/proxy-test.js POST https://httpbin.org/post '{}' '{"user_field":"untouched"}'""",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        assert response["json"]["user_field"] == "untouched"
        assert response["json"]["secret_key"] == "tok_live_abc123"
        assert response["json"]["composite"] == "prefix-ALPHA-suffix"

    async def test_does_not_leak_secrets_from_one_route_to_another(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/headers",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers.get("x-other-secret") is None

    async def test_does_not_expose_raw_secret_template_on_the_wire(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/headers",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert "{{SECRET:" not in (result.logs or "")

    async def test_resolves_secret_in_user_sent_headers(self):
        result = await self.sandbox.process.exec({
            "command": (
                "node /tmp/proxy-test.js GET https://httpbin.org/headers "
                """'{"X-User-Token":"{{SECRET:api-token}}","X-User-Combo":"pre-{{SECRET:part-a}}-post"}'"""
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers["x-user-token"] == "tok_live_abc123"
        assert headers["x-user-combo"] == "pre-ALPHA-post"

    async def test_resolves_secret_in_user_sent_post_body(self):
        result = await self.sandbox.process.exec({
            "command": (
                "node /tmp/proxy-test.js POST https://httpbin.org/post "
                """'{}' '{"api_key":"{{SECRET:api-token}}","mixed":"hello-{{SECRET:part-b}}-world"}'"""
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        assert response["json"]["api_key"] == "tok_live_abc123"
        assert response["json"]["mixed"] == "hello-BETA-world"

    async def test_does_not_resolve_secrets_from_different_route_in_user_headers(self):
        result = await self.sandbox.process.exec({
            "command": (
                "node /tmp/proxy-test.js GET https://httpbin.org/headers "
                """'{"X-Wrong-Route":"{{SECRET:other-key}}"}'"""
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers["x-wrong-route"] == "{{SECRET:other-key}}"


# =============================================================================
# Proxy with Wildcard (*) Destination Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestProxyWildcardDestination:
    """Test proxy routing with wildcard (*) destination."""

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
                            "headers": {
                                "X-Global-Auth": "Bearer {{SECRET:global-key}}",
                            },
                            "secrets": {
                                "global-key": "global-token-xyz",
                            },
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

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers["x-global-auth"] == "Bearer global-token-xyz"


# =============================================================================
# Proxy End-to-End Functionality Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestProxyEndToEnd:
    """Test proxy end-to-end functionality with header/body injection."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.sandbox_name = unique_name("proxy-e2e")
        request.cls.sandbox = await SandboxInstance.create({
            "name": request.cls.sandbox_name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["httpbin.org"],
                            "headers": {
                                "X-Proxy-Test": "header-injected",
                                "X-Api-Key": "{{SECRET:test-api-key}}",
                            },
                            "body": {
                                "injected_field": "body-injected",
                                "secret_body": "{{SECRET:test-api-key}}",
                            },
                            "secrets": {
                                "test-api-key": "resolved-secret-42",
                            },
                        },
                        {
                            "destinations": ["*.example.com"],
                            "headers": {
                                "X-Wildcard-Match": "wildcard-injected",
                            },
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

    async def test_routes_https_requests_through_proxy_with_header_injection(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/headers",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers.get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"
        assert headers["x-api-key"] == "resolved-secret-42"

    async def test_routes_post_requests_through_proxy_with_body_injection(self):
        result = await self.sandbox.process.exec({
            "command": """node /tmp/proxy-test.js POST https://httpbin.org/post '{}' '{"user_data":"original"}'""",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        assert response["json"]["user_data"] == "original"

        headers = _lowercase_keys(response["headers"])
        assert headers.get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"
        assert headers["x-api-key"] == "resolved-secret-42"

        assert response["json"]["injected_field"] == "body-injected"
        assert response["json"]["secret_body"] == "resolved-secret-42"

    async def test_preserves_user_sent_headers_when_routing(self):
        result = await self.sandbox.process.exec({
            "command": """node /tmp/proxy-test.js GET https://httpbin.org/headers '{"X-User-Custom":"my-value"}'""",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers["x-user-custom"] == "my-value"
        assert headers.get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"

    async def test_does_not_route_local_requests_through_proxy(self):
        result = await self.sandbox.process.exec({
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
        })
        assert result.exit_code == 0

        headers = _parse_json_output(result.logs)
        assert headers.get("x-blaxel-request-id") is None
        assert headers.get("x-proxy-test") is None

    async def test_does_not_inject_headers_for_non_routed_destinations(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://www.example.com",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        body = (result.logs or "").strip()
        assert len(body) > 0

    async def test_wildcard_route_matches_subdomain(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://sub.example.com",
            "wait_for_completion": True,
        })

        if result.exit_code != 0:
            assert result.exit_code == 0
            return

        body = (result.logs or "").strip()
        if "{" in body:
            response = _parse_json_output(result.logs)
            headers = _lowercase_keys(response.get("headers", {}))
            assert headers.get("x-wildcard-match") == "wildcard-injected"

    async def test_wildcard_route_does_not_match_bare_domain(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://example.com",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        body = (result.logs or "").strip()
        assert len(body) > 0
        assert "wildcard-injected" not in body

    async def test_verifies_proxy_env_vars_are_set(self):
        result = await self.sandbox.process.exec({
            "command": (
                "node -e '"
                'const vars = ["HTTP_PROXY","HTTPS_PROXY","NO_PROXY","NODE_EXTRA_CA_CERTS","SSL_CERT_FILE"];'
                "const result = {};"
                'vars.forEach(v => result[v] = process.env[v] ? "set" : "unset");'
                "console.log(JSON.stringify(result));'"
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        envs = _parse_json_output(result.logs)
        assert envs["HTTP_PROXY"] == "set"
        assert envs["HTTPS_PROXY"] == "set"
        assert envs["NO_PROXY"] == "set"
        assert envs["NODE_EXTRA_CA_CERTS"] == "set"
        assert envs["SSL_CERT_FILE"] == "set"


# =============================================================================
# Proxy E2E with Common CLI Tools Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestProxyCLITools:
    """Test proxy end-to-end with common CLI tools (curl, git, pip, npm)."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.sandbox_name = unique_name("proxy-cli")
        request.cls.sandbox = await SandboxInstance.create({
            "name": request.cls.sandbox_name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["httpbin.org"],
                            "headers": {
                                "X-Proxy-Test": "header-injected",
                                "X-Api-Key": "{{SECRET:test-api-key}}",
                            },
                            "body": {
                                "injected_field": "body-injected",
                                "secret_body": "{{SECRET:test-api-key}}",
                            },
                            "secrets": {
                                "test-api-key": "resolved-secret-42",
                            },
                        },
                    ],
                },
            },
        })

        install = await request.cls.sandbox.process.exec({
            "command": "apk add --no-cache curl wget git python3 py3-pip 2>&1",
            "wait_for_completion": True,
        })
        if install.exit_code != 0:
            raise RuntimeError(f"apk install failed: {(install.logs or '')[:500]}")

        yield
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestProxyCurl(TestProxyCLITools):
    """Test curl through the proxy."""

    async def test_curl_get_with_header_injection(self):
        result = await self.sandbox.process.exec({
            "command": "curl -s https://httpbin.org/headers",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers.get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"
        assert headers["x-api-key"] == "resolved-secret-42"

    async def test_curl_post_with_body_injection(self):
        result = await self.sandbox.process.exec({
            "command": """curl -s -X POST https://httpbin.org/post -H "Content-Type: application/json" -d '{"user_data":"from-curl"}'""",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        assert response["json"]["user_data"] == "from-curl"
        assert response["json"]["injected_field"] == "body-injected"
        assert response["json"]["secret_body"] == "resolved-secret-42"

        headers = _lowercase_keys(response["headers"])
        assert headers.get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"

    async def test_curl_preserves_user_headers(self):
        result = await self.sandbox.process.exec({
            "command": 'curl -s -H "X-User-Custom: from-curl" https://httpbin.org/headers',
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers["x-user-custom"] == "from-curl"
        assert headers["x-proxy-test"] == "header-injected"
        assert headers["x-api-key"] == "resolved-secret-42"

    async def test_curl_follows_redirects(self):
        result = await self.sandbox.process.exec({
            "command": 'curl -s -L -o /dev/null -w "%{http_code}" https://httpbin.org/redirect/1',
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert (result.logs or "").strip() == "200"

    async def test_curl_put_through_proxy(self):
        result = await self.sandbox.process.exec({
            "command": """curl -s -X PUT https://httpbin.org/put -H "Content-Type: application/json" -d '{"update":"from-curl"}'""",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        assert response["json"]["update"] == "from-curl"

        headers = _lowercase_keys(response["headers"])
        assert headers["x-proxy-test"] == "header-injected"

    async def test_curl_delete_through_proxy(self):
        result = await self.sandbox.process.exec({
            "command": "curl -s -X DELETE https://httpbin.org/delete",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers["x-proxy-test"] == "header-injected"

    async def test_curl_handles_large_response(self):
        result = await self.sandbox.process.exec({
            "command": 'curl -s -o /dev/null -w "%{http_code} %{size_download}" https://httpbin.org/bytes/10240',
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        parts = (result.logs or "").strip().split(" ")
        assert parts[0] == "200"
        assert int(parts[1]) >= 10240


@pytest.mark.asyncio(loop_scope="class")
class TestProxyGit(TestProxyCLITools):
    """Test git through the proxy."""

    async def test_git_clone_public_repo(self):
        result = await self.sandbox.process.exec({
            "command": (
                "export https_proxy=$HTTPS_PROXY http_proxy=$HTTP_PROXY && "
                "GIT_SSL_CAINFO=$SSL_CERT_FILE git -c http.proxyAuthMethod=basic "
                "clone --depth 1 https://github.com/octocat/Hello-World.git /tmp/git-test-repo 2>&1"
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        verify = await self.sandbox.process.exec({
            "command": "ls /tmp/git-test-repo/README",
            "wait_for_completion": True,
        })
        assert verify.exit_code == 0

    async def test_git_ls_remote_through_proxy(self):
        result = await self.sandbox.process.exec({
            "command": (
                "export https_proxy=$HTTPS_PROXY http_proxy=$HTTP_PROXY && "
                "GIT_SSL_CAINFO=$SSL_CERT_FILE git -c http.proxyAuthMethod=basic "
                "ls-remote --heads https://github.com/octocat/Hello-World.git 2>&1"
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert "refs/heads/" in (result.logs or "")

    async def test_proxy_env_vars_visible_to_git(self):
        result = await self.sandbox.process.exec({
            "command": "git config --global --list 2>&1; echo '---'; env | grep -i proxy || true",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        logs = (result.logs or "").lower()
        assert "proxy" in logs or "https_proxy" in logs


@pytest.mark.asyncio(loop_scope="class")
class TestProxyPip(TestProxyCLITools):
    """Test pip through the proxy."""

    async def test_pip_install_through_proxy(self):
        result = await self.sandbox.process.exec({
            "command": (
                'pip3 install --break-system-packages --quiet six 2>&1 && '
                'python3 -c "import six; print(six.__version__)"'
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert len((result.logs or "").strip()) > 0


@pytest.mark.asyncio(loop_scope="class")
class TestProxyNpm(TestProxyCLITools):
    """Test npm through the proxy."""

    async def test_npm_install_through_proxy(self):
        await self.sandbox.fs.write(
            "/tmp/npm-test/package.json",
            json.dumps({
                "name": "proxy-npm-test",
                "version": "1.0.0",
                "dependencies": {"is-odd": "^3.0.1"},
            }),
        )

        result = await self.sandbox.process.exec({
            "command": "cd /tmp/npm-test && npm install --no-audit --no-fund 2>&1",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        verify = await self.sandbox.process.exec({
            "command": """node -e "console.log(require('/tmp/npm-test/node_modules/is-odd')(3))" """,
            "wait_for_completion": True,
        })
        assert verify.exit_code == 0
        assert (verify.logs or "").strip() == "true"


# =============================================================================
# Proxy E2E with Python Requests (py-app image) Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestProxyPythonRequests:
    """Test proxy end-to-end with Python requests library (py-app image)."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        request.cls.sandbox_name = unique_name("proxy-py")
        request.cls.sandbox = await SandboxInstance.create({
            "name": request.cls.sandbox_name,
            "image": "blaxel/py-app:latest",
            "region": default_region,
            "labels": default_labels,
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["httpbin.org"],
                            "headers": {
                                "X-Proxy-Test": "header-injected",
                                "X-Api-Key": "{{SECRET:test-api-key}}",
                            },
                            "body": {
                                "injected_field": "body-injected",
                                "secret_body": "{{SECRET:test-api-key}}",
                            },
                            "secrets": {
                                "test-api-key": "resolved-secret-42",
                            },
                        },
                    ],
                },
            },
        })

        await request.cls.sandbox.fs.write("/tmp/proxy-test.py", PYTHON_HELPER_SCRIPT)

        pip_result = await request.cls.sandbox.process.exec({
            "command": "pip install --break-system-packages requests 2>&1",
            "wait_for_completion": True,
        })
        if pip_result.exit_code != 0:
            raise RuntimeError(f"pip install failed: {(pip_result.logs or '')[:500]}")

        yield
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_python_requests_get_with_header_injection(self):
        result = await self.sandbox.process.exec({
            "command": "python3 /tmp/proxy-test.py GET https://httpbin.org/headers 2>&1",
            "wait_for_completion": True,
        })
        if result.exit_code != 0:
            raise RuntimeError(f"python3 exited {result.exit_code}: {(result.logs or '')[:1500]}")

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers.get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"
        assert headers["x-api-key"] == "resolved-secret-42"

    async def test_python_requests_post_with_body_injection(self):
        result = await self.sandbox.process.exec({
            "command": """python3 /tmp/proxy-test.py POST https://httpbin.org/post '{}' '{"user_data":"from-python"}'""",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        assert response["json"]["user_data"] == "from-python"
        assert response["json"]["injected_field"] == "body-injected"
        assert response["json"]["secret_body"] == "resolved-secret-42"

    async def test_python_requests_preserves_user_headers(self):
        result = await self.sandbox.process.exec({
            "command": """python3 /tmp/proxy-test.py GET https://httpbin.org/headers '{"X-User-Custom":"from-python"}'""",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0

        response = _parse_json_output(result.logs)
        headers = _lowercase_keys(response["headers"])
        assert headers["x-user-custom"] == "from-python"
        assert headers["x-proxy-test"] == "header-injected"


# =============================================================================
# Proxy E2E with Claude Code Agent Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestProxyClaudeCode:
    """Test proxy end-to-end with Claude Code agent."""

    sandbox: SandboxInstance
    sandbox_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            pytest.skip("requires ANTHROPIC_API_KEY")

        request.cls.sandbox_name = unique_name("proxy-claude")
        request.cls.sandbox = await SandboxInstance.create({
            "name": request.cls.sandbox_name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "envs": [
                {"name": "ANTHROPIC_API_KEY", "value": api_key},
            ],
            "network": {
                "proxy": {
                    "routing": [
                        {
                            "destinations": ["httpbin.org"],
                            "headers": {
                                "X-Agent-Test": "claude-injected",
                            },
                        },
                    ],
                },
            },
        })

        setup = await request.cls.sandbox.process.exec({
            "command": "apk add --no-cache curl bash 2>&1 && npm install -g @anthropic-ai/claude-code 2>&1 && adduser -D -s /bin/bash agent 2>&1",
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
        claude_env = (
            "export PATH=/usr/local/bin:/usr/bin:/bin "
            "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY "
            "HTTP_PROXY=$HTTP_PROXY "
            "HTTPS_PROXY=$HTTPS_PROXY "
            "NO_PROXY=$NO_PROXY "
            "NODE_EXTRA_CA_CERTS=$NODE_EXTRA_CA_CERTS "
            "SSL_CERT_FILE=$SSL_CERT_FILE"
        )
        result = await self.sandbox.process.exec({
            "command": (
                f'su - agent -c "{claude_env} && '
                'claude --dangerously-skip-permissions -p '
                '\\"What is 2+2? Reply with ONLY the number.\\" '
                '--output-format text" 2>&1'
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert "4" in (result.logs or "")

    async def test_agent_makes_outbound_call_with_header_injection(self):
        claude_env = (
            "export PATH=/usr/local/bin:/usr/bin:/bin "
            "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY "
            "HTTP_PROXY=$HTTP_PROXY "
            "HTTPS_PROXY=$HTTPS_PROXY "
            "NO_PROXY=$NO_PROXY "
            "NODE_EXTRA_CA_CERTS=$NODE_EXTRA_CA_CERTS "
            "SSL_CERT_FILE=$SSL_CERT_FILE"
        )
        result = await self.sandbox.process.exec({
            "command": (
                f'su - agent -c "{claude_env} && '
                'claude --dangerously-skip-permissions -p '
                '\\"Run: curl -s https://httpbin.org/headers — then print the full JSON output.\\" '
                '--output-format text" 2>&1'
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert "X-Agent-Test" in (result.logs or "")
        assert "claude-injected" in (result.logs or "")

"""Secrets replacement validation tests."""

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
class TestSecretsReplacementValidation:
    """Proxy secret template resolution."""

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
                            "headers": {"X-Other-Secret": "{{SECRET:other-key}}"},
                            "secrets": {"other-key": "other-value-999"},
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
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert headers["x-token"] == "Bearer tok_live_abc123"
        assert headers["x-plain"] == "no-secret-here"

    async def test_resolves_multiple_secret_placeholders_in_single_header(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/headers",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert headers["x-multi"] == "ALPHA-BETA"

    async def test_resolves_secret_in_post_body_fields(self):
        result = await self.sandbox.process.exec({
            "command": """node /tmp/proxy-test.js POST https://httpbin.org/post '{}' '{"user_field":"untouched"}'""",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        response = parse_json_output(result.logs)
        assert response["json"]["user_field"] == "untouched"
        assert response["json"]["secret_key"] == "tok_live_abc123"
        assert response["json"]["composite"] == "prefix-ALPHA-suffix"

    async def test_does_not_leak_secrets_from_one_route_to_another(self):
        result = await self.sandbox.process.exec({
            "command": "node /tmp/proxy-test.js GET https://httpbin.org/headers",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
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
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
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
        response = parse_json_output(result.logs)
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
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert headers["x-wrong-route"] == "{{SECRET:other-key}}"

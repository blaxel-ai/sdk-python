"""Proxy end-to-end tests with the Python ``requests`` library (py-app image)."""

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_labels, unique_name

from .helpers import (
    PYTHON_HELPER_SCRIPT,
    default_region,
    lowercase_keys,
    parse_json_output,
)


@pytest.mark.asyncio(loop_scope="class")
class TestProxyPythonRequests:
    """Proxy end-to-end with the Python ``requests`` library."""

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
                            "secrets": {"test-api-key": "resolved-secret-42"},
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
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert headers.get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"
        assert headers["x-api-key"] == "resolved-secret-42"

    async def test_python_requests_post_with_body_injection(self):
        result = await self.sandbox.process.exec({
            "command": """python3 /tmp/proxy-test.py POST https://httpbin.org/post '{}' '{"user_data":"from-python"}'""",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        response = parse_json_output(result.logs)
        assert response["json"]["user_data"] == "from-python"
        assert response["json"]["injected_field"] == "body-injected"
        assert response["json"]["secret_body"] == "resolved-secret-42"

    async def test_python_requests_preserves_user_headers(self):
        result = await self.sandbox.process.exec({
            "command": """python3 /tmp/proxy-test.py GET https://httpbin.org/headers '{"X-User-Custom":"from-python"}'""",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert headers["x-user-custom"] == "from-python"
        assert headers["x-proxy-test"] == "header-injected"

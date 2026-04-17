"""Proxy end-to-end tests with common CLI tools (curl, git, pip, npm)."""

import json

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name

from .helpers import default_region, lowercase_keys, parse_json_output


@pytest.mark.asyncio(loop_scope="class")
class TestProxyCLITools:
    """Shares a single sandbox across all CLI-tool tests, like the TS suite."""

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
                            "secrets": {"test-api-key": "resolved-secret-42"},
                        },
                    ],
                },
            },
        })

        install = await request.cls.sandbox.process.exec({
            "command": "apk add --no-cache curl wget git python3 py3-pip ca-certificates 2>&1",
            "wait_for_completion": True,
        })
        if install.exit_code != 0:
            raise RuntimeError(f"apk install failed: {(install.logs or '')[:500]}")

        cert_install = await request.cls.sandbox.process.exec({
            "command": (
                '[ -f "$SSL_CERT_FILE" ] && '
                'cp "$SSL_CERT_FILE" /usr/local/share/ca-certificates/blaxel-proxy.crt && '
                'update-ca-certificates 2>&1 || echo "no SSL_CERT_FILE"'
            ),
            "wait_for_completion": True,
        })
        if cert_install.exit_code != 0:
            raise RuntimeError(f"CA cert install failed: {(cert_install.logs or '')[:500]}")

        yield
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    # ----- curl -----

    async def test_curl_get_with_header_injection(self):
        result = await self.sandbox.process.exec({
            "command": "curl -s https://httpbin.org/headers",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
        assert headers.get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"
        assert headers["x-api-key"] == "resolved-secret-42"

    async def test_curl_post_with_body_injection(self):
        result = await self.sandbox.process.exec({
            "command": """curl -s -X POST https://httpbin.org/post -H "Content-Type: application/json" -d '{"user_data":"from-curl"}'""",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        response = parse_json_output(result.logs)
        assert response["json"]["user_data"] == "from-curl"
        assert response["json"]["injected_field"] == "body-injected"
        assert response["json"]["secret_body"] == "resolved-secret-42"
        headers = lowercase_keys(response["headers"])
        assert headers.get("x-blaxel-request-id") is not None
        assert headers["x-proxy-test"] == "header-injected"

    async def test_curl_preserves_user_headers(self):
        result = await self.sandbox.process.exec({
            "command": 'curl -s -H "X-User-Custom: from-curl" https://httpbin.org/headers',
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        headers = lowercase_keys(parse_json_output(result.logs)["headers"])
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
        response = parse_json_output(result.logs)
        assert response["json"]["update"] == "from-curl"
        assert lowercase_keys(response["headers"])["x-proxy-test"] == "header-injected"

    async def test_curl_delete_through_proxy(self):
        result = await self.sandbox.process.exec({
            "command": "curl -s -X DELETE https://httpbin.org/delete",
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert lowercase_keys(parse_json_output(result.logs)["headers"])["x-proxy-test"] == "header-injected"

    async def test_curl_handles_large_response(self):
        result = await self.sandbox.process.exec({
            "command": 'curl -s -o /dev/null -w "%{http_code} %{size_download}" https://httpbin.org/bytes/10240',
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        status_code, size_str = (result.logs or "").strip().split(" ")
        assert status_code == "200"
        assert int(size_str) >= 10240

    # ----- git -----

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
        logs = result.logs or ""
        assert "proxy" in logs.lower() or "HTTPS_PROXY" in logs or "https_proxy" in logs

    # ----- pip -----

    async def test_pip_install_through_proxy(self):
        result = await self.sandbox.process.exec({
            "command": (
                "pip3 install --break-system-packages --quiet six 2>&1 && "
                'python3 -c "import six; print(six.__version__)"'
            ),
            "wait_for_completion": True,
        })
        assert result.exit_code == 0
        assert len((result.logs or "").strip()) > 0

    # ----- npm -----

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

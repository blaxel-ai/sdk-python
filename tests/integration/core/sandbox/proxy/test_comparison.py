"""Proxy vs no-proxy comparison tests."""

import asyncio
import time

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import async_sleep, default_image, default_labels, unique_name

from .helpers import (
    PROXY_HELPER_SCRIPT,
    default_region,
    lowercase_keys,
    parse_json_output,
)


async def _timed_exec(sandbox: SandboxInstance, command: str):
    start = time.monotonic()
    result = await sandbox.process.exec({"command": command, "wait_for_completion": True})
    return {
        "logs": result.logs,
        "exit_code": result.exit_code,
        "duration_ms": int((time.monotonic() - start) * 1000),
    }


@pytest.mark.asyncio(loop_scope="class")
class TestProxyComparison:
    """Compare behavior and latency between a proxy and a no-proxy sandbox."""

    proxy_sandbox: SandboxInstance
    no_proxy_sandbox: SandboxInstance
    proxy_name: str
    no_proxy_name: str

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandboxes(self, request):
        request.cls.proxy_name = unique_name("cmp-proxy")
        request.cls.no_proxy_name = unique_name("cmp-noproxy")

        proxy_sb, no_proxy_sb = await asyncio.gather(
            SandboxInstance.create({
                "name": request.cls.proxy_name,
                "image": default_image,
                "region": default_region,
                "labels": default_labels,
                "network": {
                    "proxy": {
                        "routing": [
                            {
                                "destinations": ["httpbin.org"],
                                "headers": {
                                    "X-Proxy-Compare": "with-proxy",
                                    "X-Api-Key": "{{SECRET:cmp-key}}",
                                },
                                "body": {"injected_field": "proxy-injected"},
                                "secrets": {"cmp-key": "comparison-secret-123"},
                            },
                        ],
                    },
                },
            }),
            SandboxInstance.create({
                "name": request.cls.no_proxy_name,
                "image": default_image,
                "region": default_region,
                "labels": default_labels,
            }),
        )
        request.cls.proxy_sandbox = proxy_sb
        request.cls.no_proxy_sandbox = no_proxy_sb

        await asyncio.gather(
            proxy_sb.fs.write("/tmp/proxy-test.js", PROXY_HELPER_SCRIPT),
            no_proxy_sb.fs.write("/tmp/proxy-test.js", PROXY_HELPER_SCRIPT),
        )

        # Warm up the proxy path: the proxy config may take a moment to propagate.
        for _ in range(10):
            warmup = await proxy_sb.process.exec({
                "command": "node /tmp/proxy-test.js GET https://httpbin.org/headers",
                "wait_for_completion": True,
            })
            if warmup.exit_code == 0:
                try:
                    hdr = lowercase_keys(parse_json_output(warmup.logs)["headers"])
                    if hdr.get("x-proxy-compare"):
                        break
                except Exception:
                    pass
            await async_sleep(2)

        yield
        for name in (request.cls.proxy_name, request.cls.no_proxy_name):
            try:
                await SandboxInstance.delete(name)
            except Exception:
                pass

    async def test_proxy_injects_headers_no_proxy_does_not(self):
        cmd = "node /tmp/proxy-test.js GET https://httpbin.org/headers"
        proxy_result, no_proxy_result = await asyncio.gather(
            _timed_exec(self.proxy_sandbox, cmd),
            _timed_exec(self.no_proxy_sandbox, cmd),
        )
        assert proxy_result["exit_code"] == 0
        assert no_proxy_result["exit_code"] == 0

        proxy_headers = lowercase_keys(parse_json_output(proxy_result["logs"])["headers"])
        no_proxy_headers = lowercase_keys(parse_json_output(no_proxy_result["logs"])["headers"])

        assert proxy_headers["x-proxy-compare"] == "with-proxy"
        assert proxy_headers["x-api-key"] == "comparison-secret-123"
        assert proxy_headers.get("x-blaxel-request-id") is not None

        assert no_proxy_headers.get("x-proxy-compare") is None
        assert no_proxy_headers.get("x-api-key") is None
        assert no_proxy_headers.get("x-blaxel-request-id") is None

        print(
            f"[compare GET headers] proxy: {proxy_result['duration_ms']}ms, "
            f"no-proxy: {no_proxy_result['duration_ms']}ms, "
            f"overhead: {proxy_result['duration_ms'] - no_proxy_result['duration_ms']}ms"
        )

    async def test_proxy_injects_body_fields_no_proxy_does_not(self):
        cmd = (
            """node /tmp/proxy-test.js POST https://httpbin.org/post """
            """'{}' '{"user_data":"original"}'"""
        )
        proxy_result, no_proxy_result = await asyncio.gather(
            _timed_exec(self.proxy_sandbox, cmd),
            _timed_exec(self.no_proxy_sandbox, cmd),
        )
        assert proxy_result["exit_code"] == 0
        assert no_proxy_result["exit_code"] == 0

        proxy_json = parse_json_output(proxy_result["logs"])["json"]
        no_proxy_json = parse_json_output(no_proxy_result["logs"])["json"]

        assert proxy_json["user_data"] == "original"
        assert proxy_json["injected_field"] == "proxy-injected"
        assert no_proxy_json["user_data"] == "original"
        assert no_proxy_json.get("injected_field") is None

        print(
            f"[compare POST body] proxy: {proxy_result['duration_ms']}ms, "
            f"no-proxy: {no_proxy_result['duration_ms']}ms, "
            f"overhead: {proxy_result['duration_ms'] - no_proxy_result['duration_ms']}ms"
        )

    async def test_proxy_has_env_vars_no_proxy_does_not(self):
        env_cmd = (
            "node -e '"
            'const vars = ["HTTP_PROXY","HTTPS_PROXY","NO_PROXY","NODE_EXTRA_CA_CERTS","SSL_CERT_FILE"];'
            "const r = {};"
            'vars.forEach(v => r[v] = process.env[v] ? "set" : "unset");'
            "console.log(JSON.stringify(r));'"
        )
        proxy_env, no_proxy_env = await asyncio.gather(
            self.proxy_sandbox.process.exec({"command": env_cmd, "wait_for_completion": True}),
            self.no_proxy_sandbox.process.exec({"command": env_cmd, "wait_for_completion": True}),
        )
        assert proxy_env.exit_code == 0
        assert no_proxy_env.exit_code == 0

        p_envs = parse_json_output(proxy_env.logs)
        np_envs = parse_json_output(no_proxy_env.logs)

        assert p_envs["HTTP_PROXY"] == "set"
        assert p_envs["HTTPS_PROXY"] == "set"
        assert p_envs["NODE_EXTRA_CA_CERTS"] == "set"

        assert np_envs["HTTP_PROXY"] == "unset"
        assert np_envs["HTTPS_PROXY"] == "unset"
        assert np_envs["NODE_EXTRA_CA_CERTS"] == "unset"

    async def test_both_sandboxes_reach_same_endpoint_successfully(self):
        cmd = "node /tmp/proxy-test.js GET https://httpbin.org/get"
        proxy_result, no_proxy_result = await asyncio.gather(
            _timed_exec(self.proxy_sandbox, cmd),
            _timed_exec(self.no_proxy_sandbox, cmd),
        )
        assert proxy_result["exit_code"] == 0
        assert no_proxy_result["exit_code"] == 0
        assert parse_json_output(proxy_result["logs"])["url"] == "https://httpbin.org/get"
        assert parse_json_output(no_proxy_result["logs"])["url"] == "https://httpbin.org/get"
        print(
            f"[compare GET /get] proxy: {proxy_result['duration_ms']}ms, "
            f"no-proxy: {no_proxy_result['duration_ms']}ms, "
            f"overhead: {proxy_result['duration_ms'] - no_proxy_result['duration_ms']}ms"
        )

    async def test_latency_overhead_within_acceptable_bounds(self):
        iterations = 3
        proxy_times: list[int] = []
        no_proxy_times: list[int] = []
        for _ in range(iterations):
            p, np = await asyncio.gather(
                _timed_exec(self.proxy_sandbox, "node /tmp/proxy-test.js GET https://httpbin.org/get"),
                _timed_exec(self.no_proxy_sandbox, "node /tmp/proxy-test.js GET https://httpbin.org/get"),
            )
            assert p["exit_code"] == 0
            assert np["exit_code"] == 0
            proxy_times.append(p["duration_ms"])
            no_proxy_times.append(np["duration_ms"])

        proxy_avg = sum(proxy_times) / len(proxy_times)
        no_proxy_avg = sum(no_proxy_times) / len(no_proxy_times)
        overhead_ms = proxy_avg - no_proxy_avg
        overhead_pct = (overhead_ms / no_proxy_avg * 100) if no_proxy_avg > 0 else 0.0

        print(
            f"[latency benchmark] proxy avg: {proxy_avg:.0f}ms, "
            f"no-proxy avg: {no_proxy_avg:.0f}ms"
        )
        print(
            f"[latency benchmark] overhead: {overhead_ms:.0f}ms ({overhead_pct:.1f}%)"
        )
        print(
            f"[latency benchmark] proxy samples: {proxy_times}, "
            f"no-proxy samples: {no_proxy_times}"
        )
        assert overhead_ms < 5000

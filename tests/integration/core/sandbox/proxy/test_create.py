"""Tests for creating sandboxes with proxy configuration."""

import pytest

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name

from .helpers import default_region, not_unset

pytestmark = pytest.mark.asyncio(loop_scope="module")


async def test_creates_sandbox_with_proxy_routing_and_header_injection(created_sandboxes):
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
                        "secrets": {"stripe-key": "sk-live-test123"},
                    },
                ],
            },
        },
    })
    created_sandboxes.append(name)

    assert sandbox.metadata.name == name
    proxy = sandbox.spec.network.proxy
    assert not_unset(proxy)
    assert len(proxy.routing) == 1
    route = proxy.routing[0]
    assert route.destinations == ["api.stripe.com"]
    assert route.headers["Authorization"] == "Bearer {{SECRET:stripe-key}}"
    assert route.headers["Stripe-Version"] == "2024-12-18.acacia"


async def test_creates_sandbox_with_proxy_body_injection(created_sandboxes):
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
                        "headers": {"Authorization": "Bearer {{SECRET:stripe-key}}"},
                        "body": {"api_key": "{{SECRET:stripe-key}}"},
                        "secrets": {"stripe-key": "sk-live-test123"},
                    },
                ],
            },
        },
    })
    created_sandboxes.append(name)

    route = sandbox.spec.network.proxy.routing[0]
    assert not_unset(route.body)
    assert route.body["api_key"] == "{{SECRET:stripe-key}}"


async def test_creates_sandbox_with_multiple_proxy_routing_rules(created_sandboxes):
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
                        "body": {"api_key": "{{SECRET:stripe-key}}"},
                        "secrets": {"stripe-key": "sk-live-test123"},
                    },
                    {
                        "destinations": ["api.openai.com"],
                        "headers": {
                            "Authorization": "Bearer {{SECRET:openai-key}}",
                            "OpenAI-Organization": "org-abc123",
                        },
                        "secrets": {"openai-key": "sk-proj-test789"},
                    },
                ],
                "bypass": ["*.s3.amazonaws.com"],
            },
        },
    })
    created_sandboxes.append(name)

    proxy = sandbox.spec.network.proxy
    assert len(proxy.routing) == 2

    stripe_route = next(r for r in proxy.routing if r.destinations == ["api.stripe.com"])
    assert stripe_route.headers["X-Request-Source"] == "blaxel-sandbox"
    assert stripe_route.body["api_key"] == "{{SECRET:stripe-key}}"

    openai_route = next(r for r in proxy.routing if r.destinations == ["api.openai.com"])
    assert openai_route.headers["OpenAI-Organization"] == "org-abc123"

    assert "*.s3.amazonaws.com" in proxy.bypass


async def test_creates_sandbox_with_proxy_bypass_only(created_sandboxes):
    name = unique_name("proxy-bypass")
    sandbox = await SandboxInstance.create({
        "name": name,
        "image": default_image,
        "region": default_region,
        "labels": default_labels,
        "network": {
            "proxy": {"bypass": ["*.s3.amazonaws.com", "169.254.169.254"]},
        },
    })
    created_sandboxes.append(name)

    proxy = sandbox.spec.network.proxy
    assert proxy.bypass == ["*.s3.amazonaws.com", "169.254.169.254"]
    assert not not_unset(proxy.routing) or len(proxy.routing) == 0


async def test_creates_sandbox_with_proxy_and_allowed_domains_combined(created_sandboxes):
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
    created_sandboxes.append(name)

    network = sandbox.spec.network
    assert not_unset(network.allowed_domains) or not_unset(network.proxy)
    assert len(network.proxy.routing) == 1
    assert "*.s3.amazonaws.com" in network.proxy.bypass

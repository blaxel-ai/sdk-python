"""Tests for retrieving and deleting sandboxes with proxy configuration."""

import pytest

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import (
    default_image,
    default_labels,
    unique_name,
    wait_for_sandbox_deletion,
)

from .helpers import default_region, not_unset

pytestmark = pytest.mark.asyncio(loop_scope="module")


async def test_retrieves_sandbox_with_proxy_and_validates_config(created_sandboxes):
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
                        "secrets": {"openai-key": "sk-proj-test789"},
                    },
                ],
                "bypass": ["169.254.169.254"],
            },
        },
    })
    created_sandboxes.append(name)

    retrieved = await SandboxInstance.get(name)
    network = retrieved.spec.network
    assert not_unset(network)
    if not_unset(network.proxy):
        proxy = network.proxy
        assert len(proxy.routing) == 1
        route = proxy.routing[0]
        assert "api.openai.com" in route.destinations
        assert route.headers["Authorization"] == "Bearer {{SECRET:openai-key}}"
        assert route.headers["OpenAI-Organization"] == "org-abc123"
        assert "169.254.169.254" in proxy.bypass


async def test_returns_no_proxy_config_when_sandbox_has_none(created_sandboxes):
    name = unique_name("proxy-none")
    await SandboxInstance.create({
        "name": name,
        "image": default_image,
        "region": default_region,
        "labels": default_labels,
    })
    created_sandboxes.append(name)

    retrieved = await SandboxInstance.get(name)
    network = retrieved.spec.network
    if not_unset(network):
        assert not not_unset(network.proxy)


async def test_deletes_sandbox_with_proxy_configuration():
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
    deleted = await wait_for_sandbox_deletion(name, max_attempts=60)
    assert deleted is True

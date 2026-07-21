import pytest

from blaxel.core import SandboxInstance
from blaxel.core.sandbox.types import SandboxUpdateNetwork
from tests.helpers import (
    default_image,
    default_labels,
    unique_name,
)

# =============================================================================
# Sandbox UpdateNetwork Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxUpdateNetwork:
    """Test sandbox update_network operations."""

    async def test_updates_sandbox_network_with_allowed_domains(self):
        """Test updating sandbox network with allowed domains using httpbin."""
        name = unique_name("update-net-allow")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "labels": default_labels,
            }
        )

        try:
            updated = await SandboxInstance.update_network(
                name,
                SandboxUpdateNetwork(network={"allowedDomains": ["httpbin.org", "*.httpbin.org"]}),
            )
            assert updated.spec.network is not None
            assert set(updated.spec.network.allowed_domains) == {"httpbin.org", "*.httpbin.org"}
        finally:
            await SandboxInstance.delete(name)

    async def test_updates_sandbox_network_with_forbidden_domains(self):
        """Test updating sandbox network with forbidden domains using httpbin."""
        name = unique_name("update-net-forbid")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "labels": default_labels,
            }
        )

        try:
            updated = await SandboxInstance.update_network(
                name,
                SandboxUpdateNetwork(
                    network={"forbiddenDomains": ["httpbin.org", "*.httpbin.org"]}
                ),
            )
            assert updated.spec.network is not None
            assert set(updated.spec.network.forbidden_domains) == {"httpbin.org", "*.httpbin.org"}
        finally:
            await SandboxInstance.delete(name)

    async def test_updates_sandbox_network_with_model_object(self):
        """Test updating sandbox network using SandboxNetwork model object."""
        from blaxel.core.client.models import SandboxNetwork

        name = unique_name("update-net-model")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "labels": default_labels,
            }
        )

        try:
            network_config = SandboxNetwork(
                allowed_domains=["httpbin.org"],
            )
            updated = await SandboxInstance.update_network(
                name,
                SandboxUpdateNetwork(network=network_config),
            )
            assert updated.spec.network is not None
            assert updated.spec.network.allowed_domains == ["httpbin.org"]
        finally:
            await SandboxInstance.delete(name)

    async def test_clears_sandbox_network_config(self):
        """Test clearing sandbox network configuration by passing network=None."""
        name = unique_name("update-net-clear")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "network": {"allowedDomains": ["httpbin.org"]},
                "labels": default_labels,
            }
        )

        try:
            updated = await SandboxInstance.update_network(
                name,
                SandboxUpdateNetwork(network=None),
            )
            from blaxel.core.client.types import UNSET

            assert updated.spec.network is UNSET or updated.spec.network is None
        finally:
            await SandboxInstance.delete(name)

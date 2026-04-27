import pytest

from blaxel.core import SandboxInstance
from blaxel.core.client.types import Unset
from tests.helpers import (
    default_image,
    default_labels,
    unique_name,
)


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxExtraArgs:
    """Test sandbox extraArgs (kernel selection) feature."""

    async def test_creates_sandbox_with_iptables_enabled(self):
        """Test creating a sandbox with iptables extra arg."""
        name = unique_name("extra-args-iptables")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "extra_args": {"iptables": "enabled"},
                "labels": default_labels,
            }
        )

        try:
            retrieved = await SandboxInstance.get(name)
            assert retrieved.spec.runtime.extra_args is not None
            assert retrieved.spec.runtime.extra_args["iptables"] == "enabled"
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_nvme_enabled(self):
        """Test creating a sandbox with nvme extra arg."""
        name = unique_name("extra-args-nvme")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "extra_args": {"nvme": "enabled"},
                "labels": default_labels,
            }
        )

        try:
            retrieved = await SandboxInstance.get(name)
            assert retrieved.spec.runtime.extra_args is not None
            assert retrieved.spec.runtime.extra_args["nvme"] == "enabled"
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_with_both_iptables_and_nvme(self):
        """Test creating a sandbox with both iptables and nvme enabled."""
        name = unique_name("extra-args-both")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "extra_args": {"iptables": "enabled", "nvme": "enabled"},
                "labels": default_labels,
            }
        )

        try:
            retrieved = await SandboxInstance.get(name)
            assert retrieved.spec.runtime.extra_args["iptables"] == "enabled"
            assert retrieved.spec.runtime.extra_args["nvme"] == "enabled"
        finally:
            await SandboxInstance.delete(name)

    async def test_creates_sandbox_without_extra_args(self):
        """Test creating a sandbox without extraArgs uses default kernel."""
        name = unique_name("extra-args-default")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "labels": default_labels,
            }
        )

        try:
            retrieved = await SandboxInstance.get(name)
            extra_args = retrieved.spec.runtime.extra_args
            assert (
                extra_args is None
                or isinstance(extra_args, Unset)
                or len(extra_args.additional_properties) == 0
            )
        finally:
            await SandboxInstance.delete(name)

    async def test_extra_args_immutable_after_creation(self):
        """Test that extraArgs cannot be changed via update."""
        name = unique_name("extra-args-immutable")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "extra_args": {"iptables": "enabled"},
                "labels": default_labels,
            }
        )

        try:
            await SandboxInstance.update_metadata(
                name, {"labels": {**default_labels, "updated": "true"}}
            )
            retrieved = await SandboxInstance.get(name)
            assert retrieved.spec.runtime.extra_args["iptables"] == "enabled"
        finally:
            await SandboxInstance.delete(name)

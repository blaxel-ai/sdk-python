import pytest

from blaxel.core import SandboxInstance
from blaxel.core.client.types import Unset
from blaxel.core.sandbox.types import SandboxUpdateMetadata
from tests.helpers import (
    default_image,
    default_labels,
    unique_name,
)

# The control plane accepts iptables, nfs and tun. Only ``tun`` (mk3.1) is used
# for the tests that actually deploy: iptables and nfs select mk3.0 kernels,
# which currently fail to deploy in every region (DEPLOYMENT_FAILED, tracked
# separately as a platform bug). ``nvme`` used to be accepted and no longer is.


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxExtraArgs:
    """Test sandbox extraArgs (kernel selection) feature."""

    async def test_creates_sandbox_with_tun_enabled(self):
        """Test creating a sandbox with tun extra arg."""
        name = unique_name("extra-args-tun")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "extra_args": {"tun": "enabled"},
                "labels": default_labels,
            }
        )

        try:
            retrieved = await SandboxInstance.get(name)
            assert retrieved.spec.runtime.extra_args is not None
            assert retrieved.spec.runtime.extra_args["tun"] == "enabled"
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
                "extra_args": {"tun": "enabled"},
                "labels": default_labels,
            }
        )

        try:
            await SandboxInstance.update_metadata(
                name,
                SandboxUpdateMetadata(labels={**default_labels, "updated": "true"}),
            )
            retrieved = await SandboxInstance.get(name)
            assert retrieved.spec.runtime.extra_args["tun"] == "enabled"
        finally:
            await SandboxInstance.delete(name)

    async def test_rejects_unsupported_extra_args_key(self):
        """An unknown extraArgs key is rejected instead of silently ignored."""
        name = unique_name("extra-args-bad-key")
        with pytest.raises(Exception, match="nvme"):
            await SandboxInstance.create(
                {
                    "name": name,
                    "image": default_image,
                    "extra_args": {"nvme": "enabled"},
                    "labels": default_labels,
                }
            )

    async def test_rejects_nfs_combined_with_iptables(self):
        """nfs and iptables select different kernels and cannot be combined."""
        name = unique_name("extra-args-conflict")
        with pytest.raises(Exception, match="nfs"):
            await SandboxInstance.create(
                {
                    "name": name,
                    "image": default_image,
                    "extra_args": {"nfs": "enabled", "iptables": "enabled"},
                    "labels": default_labels,
                }
            )

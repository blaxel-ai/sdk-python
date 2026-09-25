"""Integration tests for the infrastructure error history of a sandbox.

The compute plane matches configured patterns in the microVM logs and signals
them to the control plane, which appends them to ``sandbox.errors``
(controlplane#5198). A healthy sandbox has none, so what is asserted here is the
contract of the accessor: always a list, and never carried by a listing (the
projection drops the field, so it reads as empty too).
"""

import pytest

from blaxel.core import SandboxInstance
from tests.helpers import default_image, default_labels, default_region, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxErrors:
    """Test reading the infrastructure errors recorded on a sandbox."""

    async def test_reads_empty_error_history_on_healthy_sandbox(self):
        """A sandbox that never hit an infrastructure failure reports no error."""
        name = unique_name("errors")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "region": default_region,
                "labels": default_labels,
            }
        )

        try:
            sandbox = await SandboxInstance.get(name)

            # The shape of an entry (code, fatal, instance, message, time) is
            # not exercisable here: covering it would mean provoking a real
            # infrastructure failure on the compute plane.
            assert isinstance(sandbox.errors, list)
            assert sandbox.errors == []
        finally:
            await SandboxInstance.delete(name)

    async def test_listing_does_not_carry_the_error_history(self):
        """Listings project the field out, so they must not be read for it."""
        page = await SandboxInstance.list(limit=1)

        assert len(page.data) > 0
        assert page.data[0].errors == []

"""Integration tests for the sandbox naming rule and its helpers.

The control plane rejects a name that is not lowercase letters and digits
separated by single hyphens. The SDK sends the name as given; callers that name
sandboxes after their own ids pass them through ``sanitize_sandbox_name``.
"""

import uuid

import pytest

from blaxel.core import SandboxAPIError, SandboxInstance
from blaxel.core.sandbox import is_valid_sandbox_name, sanitize_sandbox_name
from tests.helpers import default_image, default_labels, default_region


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxNames:
    """Create sandboxes named after ids that break the naming rule."""

    async def test_sanitized_external_id_is_accepted(self):
        external_id = f"Sesn_{uuid.uuid4().hex[:8].upper()}"
        name = sanitize_sandbox_name(external_id)
        assert is_valid_sandbox_name(name)

        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "region": default_region,
                "labels": {**default_labels, "external-id": name},
            }
        )
        try:
            assert sandbox.metadata.name == name
        finally:
            await SandboxInstance.delete(name)

    async def test_invalid_name_is_rejected_with_a_fix(self):
        external_id = f"sesn_{uuid.uuid4().hex[:8]}"
        assert not is_valid_sandbox_name(external_id)

        with pytest.raises(SandboxAPIError) as excinfo:
            await SandboxInstance.create(
                {
                    "name": external_id,
                    "image": default_image,
                    "region": default_region,
                    "labels": default_labels,
                }
            )

        assert excinfo.value.status_code == 400
        assert sanitize_sandbox_name(external_id) in str(excinfo.value)

"""Integration test for the drift warning of create_if_not_exists.

create_if_not_exists returns the sandbox already holding the name, whatever it was
created with. When that sandbox is not what the call asked for, the SDK warns once
naming the fields that differ; what the call returns does not change.
"""

import warnings

import pytest

from blaxel.core import SandboxInstance, SyncSandboxInstance
from tests.helpers import default_image, default_labels, default_region, unique_name

OTHER_REGION = "us-was-1" if default_region == "us-pdx-1" else "us-pdx-1"


def _drift_warnings(caught) -> list[str]:
    return [str(w.message) for w in caught if "already exists" in str(w.message)]


@pytest.mark.asyncio(loop_scope="class")
class TestCreateIfNotExistsDrift:
    async def test_warns_with_the_differing_fields_and_returns_the_existing_sandbox(self):
        name = unique_name("drift")
        config = {
            "name": name,
            "image": default_image,
            "memory": 2048,
            "region": default_region,
            "labels": default_labels,
            "envs": [{"name": "KEEP", "value": "same"}],
        }
        differs = {
            **config,
            "image": "blaxel/node:latest",
            "memory": 4096,
            "region": OTHER_REGION,
            "envs": [*config["envs"], {"name": "ADDED", "value": "never-logged"}],
        }
        try:
            created = await SandboxInstance.create(config)

            # The same request: nothing to say.
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                again = await SandboxInstance.create_if_not_exists(config)
            assert again.metadata.created_at == created.metadata.created_at
            assert _drift_warnings(caught) == []

            # A different request: one warning, and the sandbox comes back as it was.
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                again = await SandboxInstance.create_if_not_exists(differs)
            assert again.metadata.created_at == created.metadata.created_at
            assert again.spec.runtime.image == default_image
            assert again.spec.runtime.memory == 2048
            assert again.spec.region == default_region
            [message] = _drift_warnings(caught)
            assert f'sandbox "{name}" already exists' in message
            assert f"image (requested blaxel/node:latest, existing {default_image})" in message
            assert "memory (requested 4096 MB, existing 2048 MB)" in message
            assert f"region (requested {OTHER_REGION}, existing {default_region})" in message
            assert "envs (not set on the existing sandbox: ADDED)" in message
            assert "never-logged" not in message

            # The sync client says the same.
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                SyncSandboxInstance.create_if_not_exists(differs)
            [sync_message] = _drift_warnings(caught)
            assert sync_message == message
        finally:
            try:
                await SandboxInstance.delete(name)
            except Exception:
                pass

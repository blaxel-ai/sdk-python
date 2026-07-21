"""Integration tests for the externalId feature (ENG-3141).

Tests:
- Creating a sandbox with an externalId in metadata
- Retrieving a sandbox by externalId via the dedicated endpoint
- Filtering sandboxes by externalId via the list endpoint
"""

import json
import uuid

import pytest

from blaxel.core import SandboxInstance
from blaxel.core.client.api.compute.get_sandbox_by_external_id import (
    asyncio as get_sandbox_by_external_id,
)
from blaxel.core.client.api.compute.list_sandboxes import _get_kwargs as _list_sandboxes_kwargs
from blaxel.core.client.client import client
from blaxel.core.client.models import Metadata, Sandbox, SandboxRuntime, SandboxSpec
from blaxel.core.client.models.error import Error
from blaxel.core.client.models.metadata_labels import MetadataLabels
from tests.helpers import (
    default_image,
    default_labels,
    default_region,
    unique_name,
)


def _make_external_id() -> str:
    """Generate a unique externalId for testing."""
    return f"test-ext-{uuid.uuid4().hex[:12]}"


# =============================================================================
# External ID CRUD Tests
# =============================================================================


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxExternalId:
    """Test externalId on sandbox metadata."""

    async def test_creates_sandbox_with_external_id(self):
        """Test creating a sandbox with an externalId in metadata."""
        name = unique_name("ext-id-create")
        external_id = _make_external_id()

        labels = MetadataLabels.from_dict(default_labels)
        sandbox = Sandbox(
            metadata=Metadata(name=name, labels=labels, external_id=external_id),
            spec=SandboxSpec(
                runtime=SandboxRuntime(image=default_image, memory=512),
                region=default_region,
            ),
        )

        from blaxel.core.client.api.compute.create_sandbox import asyncio as create_sandbox

        response = await create_sandbox(client=client, body=sandbox)
        assert not isinstance(response, Error), f"Create failed: {response}"
        assert response is not None

        try:
            # Verify the externalId was persisted
            retrieved = await SandboxInstance.get(name)
            assert retrieved.metadata.external_id == external_id
        finally:
            await SandboxInstance.delete(name)

    async def test_get_sandbox_by_external_id(self):
        """Test retrieving a sandbox by externalId via the dedicated endpoint."""
        name = unique_name("ext-id-get")
        external_id = _make_external_id()

        labels = MetadataLabels.from_dict(default_labels)
        sandbox = Sandbox(
            metadata=Metadata(name=name, labels=labels, external_id=external_id),
            spec=SandboxSpec(
                runtime=SandboxRuntime(image=default_image, memory=512),
                region=default_region,
            ),
        )

        from blaxel.core.client.api.compute.create_sandbox import asyncio as create_sandbox

        response = await create_sandbox(client=client, body=sandbox)
        assert not isinstance(response, Error), f"Create failed: {response}"

        try:
            # Use the dedicated GET by externalId endpoint
            result = await get_sandbox_by_external_id(external_id=external_id, client=client)
            assert not isinstance(result, Error), f"Get by externalId failed: {result}"
            assert result is not None
            assert result.metadata.name == name
            assert result.metadata.external_id == external_id
        finally:
            await SandboxInstance.delete(name)

    async def test_list_sandboxes_filtered_by_external_id(self):
        """Test listing sandboxes with the externalId query parameter."""
        name = unique_name("ext-id-list")
        external_id = _make_external_id()

        labels = MetadataLabels.from_dict(default_labels)
        sandbox = Sandbox(
            metadata=Metadata(name=name, labels=labels, external_id=external_id),
            spec=SandboxSpec(
                runtime=SandboxRuntime(image=default_image, memory=512),
                region=default_region,
            ),
        )

        from blaxel.core.client.api.compute.create_sandbox import asyncio as create_sandbox

        response = await create_sandbox(client=client, body=sandbox)
        assert not isinstance(response, Error), f"Create failed: {response}"

        try:
            # Make raw HTTP request to bypass generated parser that chokes on bare arrays
            kwargs = _list_sandboxes_kwargs(external_id=external_id)
            httpx_client = client.get_async_httpx_client()
            resp = await httpx_client.request(**kwargs)
            assert resp.status_code == 200, f"List returned {resp.status_code}"

            raw = json.loads(resp.content)

            # Handle both formats: bare array or {data: [...], meta: {...}}
            if isinstance(raw, list):
                sandbox_dicts = raw
            else:
                sandbox_dicts = raw.get("data", [])

            sandboxes = [Sandbox.from_dict(s) for s in sandbox_dicts]
            assert len(sandboxes) == 1
            assert sandboxes[0].metadata.name == name
            assert sandboxes[0].metadata.external_id == external_id
        finally:
            await SandboxInstance.delete(name)

    async def test_external_id_not_found_returns_error(self):
        """Test that looking up a non-existent externalId returns a 404 error."""
        result = await get_sandbox_by_external_id(
            external_id="nonexistent-ext-id-xyz", client=client
        )
        assert isinstance(result, Error), "Expected an error for non-existent externalId"

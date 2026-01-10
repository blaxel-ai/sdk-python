from datetime import datetime, timedelta, timezone

import httpx
import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_labels, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestPreviewOperations:
    """Test sandbox preview operations."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("preview-test")
        # Use nextjs image for preview tests (has a server)
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": "blaxel/nextjs:latest",
                "memory": 4096,
                "ports": [{"target": 3000}],
                "labels": default_labels,
            }
        )

        # Start the dev server
        await request.cls.sandbox.process.exec(
            {
                "command": "npm run dev -- --port 3000",
                "working_dir": "/blaxel/app",
                "wait_for_ports": [3000],
            }
        )

        yield

        # Cleanup
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestPreviewCreate(TestPreviewOperations):
    """Test preview creation operations."""

    async def test_creates_public_preview(self):
        """Test creating a public preview."""
        preview = await self.sandbox.previews.create(
            {
                "metadata": {"name": "public-preview"},
                "spec": {
                    "port": 3000,
                    "public": True,
                },
            }
        )

        assert preview.metadata.name == "public-preview"
        assert preview.spec.url is not None
        assert "preview" in preview.spec.url

        await self.sandbox.previews.delete("public-preview")

    async def test_creates_private_preview(self):
        """Test creating a private preview."""
        preview = await self.sandbox.previews.create(
            {
                "metadata": {"name": "private-preview"},
                "spec": {
                    "port": 3000,
                    "public": False,
                },
            }
        )

        assert preview.metadata.name == "private-preview"
        assert preview.spec.url is not None

        await self.sandbox.previews.delete("private-preview")

    async def test_creates_preview_with_custom_prefix_url(self):
        """Test creating a preview with custom prefix URL."""
        preview = await self.sandbox.previews.create(
            {
                "metadata": {"name": "prefix-preview"},
                "spec": {
                    "port": 3000,
                    "prefix_url": "my-custom-prefix",
                    "public": True,
                },
            }
        )

        assert "my-custom-prefix" in preview.spec.url

        await self.sandbox.previews.delete("prefix-preview")


@pytest.mark.asyncio(loop_scope="class")
class TestPreviewCreateIfNotExists(TestPreviewOperations):
    """Test createIfNotExists operations."""

    async def test_creates_new_preview_if_not_exists(self):
        """Test creating a new preview if it doesn't exist."""
        preview = await self.sandbox.previews.create_if_not_exists(
            {
                "metadata": {"name": "cine-preview"},
                "spec": {
                    "port": 3000,
                    "public": True,
                },
            }
        )

        assert preview.metadata.name == "cine-preview"

        await self.sandbox.previews.delete("cine-preview")

    async def test_returns_existing_preview_if_exists(self):
        """Test returning existing preview if it already exists."""
        # Create first
        await self.sandbox.previews.create(
            {
                "metadata": {"name": "existing-preview"},
                "spec": {"port": 3000, "public": True},
            }
        )

        # Should return existing
        second = await self.sandbox.previews.create_if_not_exists(
            {
                "metadata": {"name": "existing-preview"},
                "spec": {"port": 3000, "public": True},
            }
        )

        assert second.metadata.name == "existing-preview"

        await self.sandbox.previews.delete("existing-preview")


@pytest.mark.asyncio(loop_scope="class")
class TestPreviewGet(TestPreviewOperations):
    """Test preview get operations."""

    async def test_retrieves_existing_preview(self):
        """Test retrieving an existing preview."""
        await self.sandbox.previews.create(
            {
                "metadata": {"name": "get-preview"},
                "spec": {"port": 3000, "public": True},
            }
        )

        preview = await self.sandbox.previews.get("get-preview")

        assert preview.name == "get-preview"
        assert preview.spec.url is not None

        await self.sandbox.previews.delete("get-preview")


@pytest.mark.asyncio(loop_scope="class")
class TestPreviewList(TestPreviewOperations):
    """Test preview list operations."""

    async def test_lists_all_previews(self):
        """Test listing all previews."""
        await self.sandbox.previews.create(
            {
                "metadata": {"name": "list-preview-1"},
                "spec": {"port": 3000, "public": True},
            }
        )
        await self.sandbox.previews.create(
            {
                "metadata": {"name": "list-preview-2"},
                "spec": {"port": 3000, "public": True},
            }
        )

        previews = await self.sandbox.previews.list()

        assert len(previews) >= 2
        names = [p.name for p in previews]
        assert "list-preview-1" in names
        assert "list-preview-2" in names

        await self.sandbox.previews.delete("list-preview-1")
        await self.sandbox.previews.delete("list-preview-2")


@pytest.mark.asyncio(loop_scope="class")
class TestPreviewDelete(TestPreviewOperations):
    """Test preview delete operations."""

    async def test_deletes_preview(self):
        """Test deleting a preview."""
        await self.sandbox.previews.create(
            {
                "metadata": {"name": "delete-preview"},
                "spec": {"port": 3000, "public": True},
            }
        )

        await self.sandbox.previews.delete("delete-preview")

        previews = await self.sandbox.previews.list()
        names = [p.name for p in previews]
        assert "delete-preview" not in names


@pytest.mark.asyncio(loop_scope="class")
class TestPublicPreviewAccess(TestPreviewOperations):
    """Test public preview access."""

    async def test_public_preview_is_accessible_without_token(self):
        """Test that public preview is accessible without token."""
        preview = await self.sandbox.previews.create(
            {
                "metadata": {"name": "access-public"},
                "spec": {
                    "port": 3000,
                    "public": True,
                },
            }
        )

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(preview.spec.url)
        assert response.status_code == 200

        await self.sandbox.previews.delete("access-public")


@pytest.mark.asyncio(loop_scope="class")
class TestPrivatePreviewTokens(TestPreviewOperations):
    """Test private preview tokens."""

    async def test_private_preview_requires_token(self):
        """Test that private preview requires token."""
        preview = await self.sandbox.previews.create(
            {
                "metadata": {"name": "token-required"},
                "spec": {
                    "port": 3000,
                    "public": False,
                },
            }
        )

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(preview.spec.url)
        assert response.status_code == 401

        await self.sandbox.previews.delete("token-required")

    async def test_creates_and_uses_preview_token(self):
        """Test creating and using a preview token."""
        preview = await self.sandbox.previews.create(
            {
                "metadata": {"name": "token-test"},
                "spec": {
                    "port": 3000,
                    "public": False,
                },
            }
        )

        # Create token (expires in 10 minutes)
        expiration = datetime.now(timezone.utc) + timedelta(minutes=10)
        token = await preview.tokens.create(expiration)

        assert token.value is not None

        # Access with token
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(f"{preview.spec.url}?bl_preview_token={token.value}")
        assert response.status_code == 200

        await self.sandbox.previews.delete("token-test")

    async def test_lists_tokens(self):
        """Test listing tokens."""
        preview = await self.sandbox.previews.create(
            {
                "metadata": {"name": "list-tokens"},
                "spec": {"port": 3000, "public": False},
            }
        )

        expiration = datetime.now(timezone.utc) + timedelta(minutes=10)
        token = await preview.tokens.create(expiration)

        tokens = await preview.tokens.list()

        assert len(tokens) > 0
        assert any(t.value == token.value for t in tokens)

        await self.sandbox.previews.delete("list-tokens")

    async def test_deletes_token(self):
        """Test deleting a token."""
        preview = await self.sandbox.previews.create(
            {
                "metadata": {"name": "delete-token"},
                "spec": {"port": 3000, "public": False},
            }
        )

        expiration = datetime.now(timezone.utc) + timedelta(minutes=10)
        token = await preview.tokens.create(expiration)

        await preview.tokens.delete(token.value)

        tokens = await preview.tokens.list()
        assert not any(t.value == token.value for t in tokens)

        await self.sandbox.previews.delete("delete-token")


@pytest.mark.asyncio(loop_scope="class")
class TestCORSHeaders(TestPreviewOperations):
    """Test CORS headers."""

    async def test_sets_custom_cors_headers(self):
        """Test setting custom CORS headers."""
        preview = await self.sandbox.previews.create(
            {
                "metadata": {"name": "cors-test"},
                "spec": {
                    "port": 3000,
                    "public": True,
                    "response_headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                        "Access-Control-Allow-Headers": "Content-Type, Authorization",
                    },
                },
            }
        )

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.options(
                preview.spec.url,
                headers={
                    "Origin": "https://example.com",
                    "Access-Control-Request-Method": "POST",
                },
            )

        assert response.headers.get("access-control-allow-origin") == "*"

        await self.sandbox.previews.delete("cors-test")

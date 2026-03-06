"""Integration tests for Image build functionality."""

import uuid

import pytest
import pytest_asyncio

from blaxel.core import ImageInstance, SandboxInstance


@pytest.mark.asyncio(loop_scope="class")
class TestImage:
    """Test re-building the same image with an updated spec (update scenario)."""

    image_name: str
    sandbox: SandboxInstance

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_rebuilt_image(self, request):
        image_name = f"image-test-{uuid.uuid4().hex[:8]}"
        request.cls.image_name = image_name

        # Build initial image (v1)
        image_v1 = (
            ImageInstance.from_registry("python:3.11-slim")
            .apt_install("curl", "git", "wget")
            .workdir("/app")
            .pip_install("requests", "httpx", "pydantic")
            .env(PYTHONUNBUFFERED="1", APP_NAME="blaxel-test")
            .copy(".", "/app")
            .expose(8080)
        )

        await image_v1.build(
            name=image_name,
            memory=4096,
            timeout=900.0,
            sandbox_version="latest",
        )

        # Rebuild with updated spec (v2)
        image_v2 = (
            ImageInstance.from_registry("python:3.11-alpine")
            .apk_add("curl", "git", "wget", "vim")
            .workdir("/app")
            .pip_install("requests", "httpx", "pydantic", "aiohttp")
            .env(
                PYTHONUNBUFFERED="1",
                APP_NAME="blaxel-test",
                DEBUG="true",
                LOG_LEVEL="debug",
                VERSION="2.0.0",
            )
            .label(
                maintainer="blaxel",
                version="2.0.0",
                description="Integration test image v2",
            )
            .run_commands(
                "python --version",
                "curl --version",
                "git --version",
                "vim --version | head -1",
            )
            .copy(".", "/app")
            .expose(8080)
        )

        await image_v2.build(
            name=image_name,
            memory=4096,
            timeout=900.0,
            sandbox_version="latest",
        )

        request.cls.sandbox = await SandboxInstance.create(
            {
                "image": image_name,
                "memory": 4096,
            }
        )

        yield

        await SandboxInstance.delete(self.sandbox.metadata.name)

    async def test_new_python_package_available(self):
        result = await self.sandbox.process.exec(
            {
                "command": "python -c \"import aiohttp; print('aiohttp OK')\"",
                "waitForCompletion": True,
            }
        )
        process_name = result.name if result.name else "unknown"
        logs = await self.sandbox.process.logs(process_name, "all")

        assert logs is not None
        assert "aiohttp OK" in logs

    async def test_new_apt_package_available(self):
        result = await self.sandbox.process.exec(
            {
                "command": "vim --version | head -1",
                "waitForCompletion": True,
            }
        )
        process_name = result.name if result.name else "unknown"
        logs = await self.sandbox.process.logs(process_name, "all")

        assert logs is not None
        assert "vim" in logs.lower()

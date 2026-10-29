"""Create a sandbox from a private registry image with docker_config.

Needs a private image and credentials that can pull it, e.g.
PRIVATE_REGISTRY_IMAGE=ghcr.io/org/private:v1
PRIVATE_REGISTRY_DOCKER_CONFIG='{"auths":{"ghcr.io":{"auth":"<base64 user:token>"}}}'
The registry import can take minutes, so it also needs RUN_SLOW_TESTS=1.
"""

import asyncio
import os
import time

import pytest

from blaxel.core import SandboxInstance
from tests.helpers import default_labels, unique_name

IMAGE = os.environ.get("PRIVATE_REGISTRY_IMAGE")
DOCKER_CONFIG = os.environ.get("PRIVATE_REGISTRY_DOCKER_CONFIG")


async def _wait_for_terminal_status(name: str) -> str | None:
    deadline = time.monotonic() + 600
    status = None
    while time.monotonic() < deadline:
        status = (await SandboxInstance.get(name)).status
        if status in ("DEPLOYED", "FAILED"):
            return status
        await asyncio.sleep(5)
    return status


@pytest.mark.skipif(
    not (os.environ.get("RUN_SLOW_TESTS") and IMAGE and DOCKER_CONFIG),
    reason="slow test; set RUN_SLOW_TESTS=1, PRIVATE_REGISTRY_IMAGE and PRIVATE_REGISTRY_DOCKER_CONFIG",
)
@pytest.mark.asyncio(loop_scope="class")
class TestPrivateRegistry:
    async def test_pulls_image_with_docker_config(self):
        name = unique_name("private-registry")
        await SandboxInstance.create(
            {"name": name, "image": IMAGE, "docker_config": DOCKER_CONFIG, "labels": default_labels}
        )
        try:
            assert await _wait_for_terminal_status(name) == "DEPLOYED"
            sandbox = await SandboxInstance.get(name)
            result = await sandbox.process.exec(
                {"command": "echo pulled", "wait_for_completion": True}
            )
            assert (result.logs or "").strip() == "pulled"
        finally:
            await SandboxInstance.delete(name)

    async def test_fails_without_docker_config(self):
        name = unique_name("private-registry-nocreds")
        await SandboxInstance.create({"name": name, "image": IMAGE, "labels": default_labels})
        try:
            assert await _wait_for_terminal_status(name) == "FAILED"
        finally:
            await SandboxInstance.delete(name)

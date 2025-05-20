import asyncio
import logging
from datetime import datetime, timedelta, timezone

import aiohttp
from utils import create_or_get_sandbox

from blaxel.client.models import Metadata, Preview, PreviewSpec
from blaxel.common.settings import settings
from blaxel.sandbox.sandbox import SandboxInstance

logger = logging.getLogger(__name__)

async def test_public_preview(sandbox: SandboxInstance):
    try:
        # Create a public preview
        await sandbox.previews.create(Preview(
            metadata=Metadata(name="preview-test-public"),
            spec=PreviewSpec(
                port=443,
                prefix_url="small-prefix",
                public=True
            )
        ))

        # List previews
        previews = await sandbox.previews.list()
        assert len(previews) >= 1, "No previews found"

        # Get the preview
        retrieved_preview = await sandbox.previews.get("preview-test-public")
        assert retrieved_preview.name == "preview-test-public", "Preview name is not correct"

        # Check the URL
        url = retrieved_preview.spec.url if retrieved_preview.spec else None
        assert url is not None, "Preview URL is not correct"
        workspace = settings.workspace
        expected_url = f"https://small-prefix-{workspace}.preview.bl.run"
        assert url == expected_url, f"Preview URL is not correct => {url}"

        # Test the preview endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}/health") as response:
                assert response.status == 200, f"Preview is not working => {response.status}:{await response.text()}"

        logger.info("Public preview is healthy :)")
    except Exception as e:
        logger.error("ERROR IN PUBLIC PREVIEW TEST => ", exc_info=e)
        raise
    finally:
        await sandbox.previews.delete("preview-test-public")

async def test_private_preview(sandbox: SandboxInstance):
    try:
        # Create a private preview
        preview = await sandbox.previews.create(Preview(
            metadata=Metadata(name="preview-test-private"),
            spec=PreviewSpec(
                port=443,
                public=False
            )
        ))

        # Get the preview URL
        url = preview.spec.url if preview.spec else None
        assert url is not None, "Preview URL is not correct"

        # Create a token
        token = await preview.tokens.create(datetime.now(timezone.utc) + timedelta(minutes=10))
        logger.info(f"Token created => {token.value}")

        # List tokens
        tokens = await preview.tokens.list()
        assert len(tokens) >= 1, "No tokens found"
        assert any(t.value == token.value for t in tokens), "Token not found in list"

        # Test the preview endpoint without token
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}/health") as response:
                assert response.status == 401, f"Preview is not protected by token, response => {response.status}"

        # Test the preview endpoint with token
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}/health?bl_preview_token={token.value}") as response:
                assert response.status == 200, f"Preview is not working with token, response => {response.status}"

        logger.info("Private preview is healthy with token :)")

        # Delete the token
        await preview.tokens.delete(token.value)
    except Exception as e:
        logger.error("ERROR IN PRIVATE PREVIEW TEST => ", exc_info=e)
        raise
    finally:
        await sandbox.previews.delete("preview-test-private")

async def main():
    sandbox_name = "sandbox-preview-test"
    sandbox = None
    try:
        sandbox = await create_or_get_sandbox(sandbox_name)
        await test_public_preview(sandbox)
        await test_private_preview(sandbox)
    finally:
        if sandbox:
            logger.info("Deleting sandbox")
            await SandboxInstance.delete(sandbox_name)

if __name__ == "__main__":
    asyncio.run(main())
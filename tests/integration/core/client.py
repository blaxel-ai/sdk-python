import asyncio
import os
from logging import getLogger

from dotenv import load_dotenv

load_dotenv()

logger = getLogger(__name__)


async def test_blaxel_config():
    """Test blaxel client configuration."""
    print("Testing blaxel client configuration...")
    from blaxel.core.client import client
    from blaxel.core.client.api.models import list_models

    models = await list_models.asyncio(client=client)
    assert models is not None
    assert len(models) > 0
    logger.info([model.metadata.name for model in models])
    print(f"✓ Found {len(models)} models")


async def test_blaxel_client_credentials():
    """Test blaxel client with client credentials authentication."""
    print("Testing blaxel client credentials authentication...")
    os.environ["BL_WORKSPACE"] = os.getenv("BL_WORKSPACE") or "test-workspace"
    os.environ["BL_CLIENT_CREDENTIALS"] = os.getenv("BL_CLIENT_CREDENTIALS") or "test-credentials"
    os.environ["BL_ENV"] = "dev"

    from blaxel.core.client import client
    from blaxel.core.client.api.models import list_models

    models = await list_models.asyncio(client=client)
    assert models is not None
    logger.info([model.metadata.name for model in models])
    print(f"✓ Client credentials auth successful, found {len(models)} models")


async def test_blaxel_api_key():
    """Test blaxel client with API key authentication."""
    print("Testing blaxel API key authentication...")
    os.environ["BL_WORKSPACE"] = os.getenv("BL_WORKSPACE") or "test-workspace"
    os.environ["BL_API_KEY"] = os.getenv("BL_API_KEY") or "test-api-key"
    os.environ["BL_ENV"] = "dev"

    from blaxel.core.client import client
    from blaxel.core.client.api.models import list_models

    models = await list_models.asyncio(client=client)
    assert models is not None
    logger.info([model.metadata.name for model in models])
    print(f"✓ API key auth successful, found {len(models)} models")


async def main():
    """Main function for standalone execution."""
    # You can only execute one test at a time, cause of autoload
    try:
        await test_blaxel_config()
        print("✅ Blaxel config test passed!")
    except Exception as e:
        print(f"❌ Config test failed: {e}")

    # Uncomment to test other authentication methods
    # try:
    #     await test_blaxel_client_credentials()
    #     print("✅ Client credentials test passed!")
    # except Exception as e:
    #     print(f"❌ Client credentials test failed: {e}")

    # try:
    #     await test_blaxel_api_key()
    #     print("✅ API key test passed!")
    # except Exception as e:
    #     print(f"❌ API key test failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os
from logging import getLogger

from dotenv import load_dotenv

load_dotenv()

logger = getLogger(__name__)

async def test_blaxel_config():
    from blaxel.client import client
    from blaxel.client.api.models import list_models

    models = await list_models.asyncio(client=client)
    logger.info([model.metadata.name for model in models])

async def test_blaxel_client_credentials():
    os.environ["BL_WORKSPACE"] = os.getenv("BL_WORKSPACE") or input("Enter workspace: ")
    os.environ["BL_CLIENT_CREDENTIALS"] = os.getenv("BL_CLIENT_CREDENTIALS") or input("Enter client credentials: ")
    os.environ["BL_ENV"] = "dev"

    from blaxel.client import client
    from blaxel.client.api.models import list_models

    models = await list_models.asyncio(client=client)
    logger.info([model.metadata.name for model in models])

async def test_blaxel_api_key():
    os.environ["BL_WORKSPACE"] = os.getenv("BL_WORKSPACE") or input("Enter workspace: ")
    os.environ["BL_API_KEY"] = os.getenv("BL_API_KEY") or input("Enter API key: ")
    os.environ["BL_ENV"] = "dev"

    from blaxel.client import client
    from blaxel.client.api.models import list_models

    models = await list_models.asyncio(client=client)
    logger.info([model.metadata.name for model in models])


if __name__ == "__main__":
    # You can only execute one test at a time, cause of autoload
    asyncio.run(test_blaxel_config())
    # asyncio.run(test_blaxel_client_credentials())
    # asyncio.run(test_blaxel_api_key())
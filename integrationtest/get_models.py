import asyncio

from blaxel.client import client
from blaxel.client.api.models import list_models


async def main():
    models = await list_models.asyncio(client=client)
    print(models)


if __name__ == "__main__":
    asyncio.run(main())

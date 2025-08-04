import asyncio

from utils import create_or_get_sandbox

SANDBOX_NAME = "py-custom-domain"


async def main():
    sandbox = await create_or_get_sandbox(SANDBOX_NAME)
    preview = await sandbox.previews.create(
        {
            "metadata": {"name": "preview-test-public"},
            "spec": {"port": 443, "public": True, "customDomain": "prod-3.mathis.beamlit.dev"},
        }
    )
    print(preview.spec.url)


if __name__ == "__main__":
    asyncio.run(main())

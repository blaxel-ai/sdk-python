import asyncio
import logging

from blaxel.sandbox.sandbox import SandboxInstance

logger = logging.getLogger(__name__)


async def main():
    sandbox_name = "base-3"
    sandbox = await SandboxInstance.get(sandbox_name)
    print(await sandbox.fs.ls("/"))
    # Filesystem tests

if __name__ == "__main__":
    asyncio.run(main())

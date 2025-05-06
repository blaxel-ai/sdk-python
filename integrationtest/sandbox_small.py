import asyncio
import json
import logging

from blaxel.sandbox.sandbox import SandboxInstance

logger = logging.getLogger(__name__)


async def main():
    sandbox_name = "spinup-test5"
    sandbox = await SandboxInstance.get(sandbox_name)
    result = await sandbox.fs.ls("/root")
    print(json.dumps(result.to_dict(), indent=4))
    # Filesystem tests

if __name__ == "__main__":
    asyncio.run(main())

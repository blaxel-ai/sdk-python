import asyncio
import json
import logging

from utils import create_or_get_sandbox

logger = logging.getLogger(__name__)


async def main():
    sandbox_name = "sandbox-test-3"
    sandbox = await create_or_get_sandbox(sandbox_name)
    result = await sandbox.fs.ls("/root")
    print(json.dumps(result.to_dict(), indent=4))
    # Filesystem tests

if __name__ == "__main__":
    asyncio.run(main())

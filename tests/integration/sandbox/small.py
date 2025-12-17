import asyncio
import time
from logging import getLogger

from utils import create_or_get_sandbox
from blaxel.core import SandboxInstance

logger = getLogger(__name__)

SANDBOX_NAME = "next-js-7"


async def main():
    """Main small sandbox test function."""

    # Test with controlplane
    start = time.time()
    sandbox = await create_or_get_sandbox(SANDBOX_NAME)
    duration_ms = int((time.time() - start) * 1000)
    print(f"Time taken for create_or_get_sandbox: {duration_ms}ms")

    # Verify with a simple process execution
    result = await sandbox.process.exec(
        {"command": "echo 'Hello, world!'", "waitForCompletion": True}
    )
    print(result)

    await sandbox.delete()

    sandbox = await SandboxInstance.create()

    await SandboxInstance.delete(sandbox.metadata.name)

if __name__ == "__main__":
    asyncio.run(main())

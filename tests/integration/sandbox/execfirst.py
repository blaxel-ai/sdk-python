import asyncio
import sys

from utils import create_or_get_sandbox

from blaxel.core.sandbox import SandboxInstance


async def main():
    """Test that validates the exec fix by creating multiple sandboxes and executing commands immediately."""
    sandbox_created = []
    try:
        i = 0
        while i < 10:
            sandbox_name = f"next-js-{i}"
            sandbox = await create_or_get_sandbox(sandbox_name=sandbox_name)

            process = await sandbox.process.exec(
                {
                    "command": "echo 'Hello, world!'",
                    "workingDir": "/blaxel",
                    "waitForCompletion": True,
                }
            )

            print(process.logs)
            sandbox_created.append(sandbox_name)
            i += 1

    except Exception as e:
        print(f"There was an error => {e}")
    finally:
        for sandbox_name in sandbox_created:
            await SandboxInstance.delete(sandbox_name)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        sys.exit(0)
    except Exception as err:
        print(f"There was an error => {err}")
        sys.exit(1)

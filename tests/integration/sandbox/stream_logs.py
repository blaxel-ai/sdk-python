import asyncio

from blaxel.core import SandboxInstance


async def main():
    sandbox = await SandboxInstance.create()

    print(f"sandbox created => {sandbox.metadata.name}")

    result_expected = """Hello, world!
Hello, world!
Hello, world!
Hello, world!
Hello, world!
Hello, world!
"""

    # Start the long-running process
    await sandbox.process.exec(
        {
            "name": "test",
            "command": 'i=1; while [ $i -le 3 ]; do echo "Hello, world!"; sleep 31; echo "Hello, world!"; i=$((i+1)); done',
        }
    )

    result = ""

    # Define the callback for log handling
    def on_log(log: str):
        nonlocal result
        print(f"received log => {log}")
        result += log + "\n"

    # Use the auto-reconnecting wrapper
    stream_control = sandbox.process.stream_logs("test", {"on_log": on_log})

    # Wait for process to finish
    await sandbox.process.wait("test", max_wait=1000000)

    print(f"\nresult => {result}")
    print(f"resultExpected => {result_expected}")
    print(f"result === resultExpected => {result == result_expected}")

    if result != result_expected:
        raise Exception("Result does not match expected result")

    # Stop the streaming
    stream_control["close"]()

    await SandboxInstance.delete(sandbox.metadata.name)


if __name__ == "__main__":
    asyncio.run(main())

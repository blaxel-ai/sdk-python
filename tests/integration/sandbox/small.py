import asyncio
from logging import getLogger

from utils import create_or_get_sandbox

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.sandbox.client.models.process_request import ProcessRequest

logger = getLogger(__name__)

SANDBOX_NAME = "sandbox-test-python-small"


async def main():
    """Main small sandbox test function."""
    print("🚀 Starting small sandbox test...")

    try:
        # Create or get sandbox
        sandbox = await create_or_get_sandbox(SANDBOX_NAME)
        print(f"✅ Sandbox ready: {sandbox.metadata.name}")

        # Wait for sandbox to be deployed
        await sandbox.wait()
        print("✅ Sandbox deployed successfully")

        # Quick filesystem test
        print("🔧 Quick filesystem test...")
        test_file = "/tmp/small_test.txt"
        test_content = "Hello from small test!"

        # Write and read
        await sandbox.fs.write(test_file, test_content)
        content = await sandbox.fs.read(test_file)

        assert content == test_content, f"Content mismatch: {content}"
        print("✅ Filesystem read/write working")

        # Quick process test
        print("🔧 Quick process test...")
        process_request = ProcessRequest(name="small-test", command="echo 'Small test process'")
        await sandbox.process.exec(process_request)

        # Wait for completion
        await sandbox.process.wait("small-test", max_wait=10000)
        logs = await sandbox.process.logs("small-test")

        assert "Small test process" in logs, f"Process output unexpected: {logs}"
        print("✅ Process execution working")

        # Quick cleanup
        await sandbox.fs.rm(test_file)
        print("✅ Cleanup completed")

        print("🎉 Small sandbox test completed successfully!")

    except Exception as e:
        print(f"❌ Small sandbox test failed with error: {e}")
        logger.exception("Small sandbox test error")
        raise
    finally:
        print("🧹 Final cleanup...")
        try:
            await SandboxInstance.delete(SANDBOX_NAME)
            print("✅ Sandbox deleted")
        except Exception as e:
            print(f"⚠️ Failed to delete sandbox: {e}")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from logging import getLogger

from utils import create_or_get_sandbox

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.sandbox.client.models.process_request import ProcessRequest

logger = getLogger(__name__)

SANDBOX_NAME = "sandbox-test-python-process-kill"


async def test_quick_process_kill(sandbox: SandboxInstance):
    """Test killing a quick process."""
    print("🔧 Testing quick process kill...")

    quick_process_name = "quick-test"
    quick_command = "echo 'Quick process'"

    # Start process
    process_request = ProcessRequest(name=quick_process_name, command=quick_command)
    await sandbox.process.exec(process_request)

    # Try to kill it (might already be completed)
    try:
        await sandbox.process.kill(quick_process_name)
        print("✅ Quick process kill successful")
    except Exception as e:
        print(f"⚠️ Quick process kill failed (expected if already completed): {e}")

    # Check final status
    try:
        final_process = await sandbox.process.get(quick_process_name)
        print(f"Final process status: {final_process.status}")
    except Exception as e:
        print(f"Could not get final process status: {e}")


async def test_stop_vs_kill(sandbox: SandboxInstance):
    """Test the difference between stop and kill."""
    print("🔧 Testing stop vs kill...")

    stop_process_name = "stop-test"
    stop_test_command = "sh -c 'trap \"echo Caught SIGTERM; exit 0\" TERM; echo Starting process; sleep 30; echo Process completed'"

    # Start long-running process
    process_request = ProcessRequest(name=stop_process_name, command=stop_test_command)
    await sandbox.process.exec(process_request)

    # Wait a bit for process to start
    await asyncio.sleep(2)

    # Test stop (graceful termination)
    print("Testing graceful stop...")
    try:
        await sandbox.process.stop(stop_process_name)
        print("✅ Process stop successful")

        # Wait for process to handle the signal
        await asyncio.sleep(2)

        # Check if process stopped gracefully
        stopped_process = await sandbox.process.get(stop_process_name)
        print(f"Stopped process status: {stopped_process.status}")
        print(f"Stopped process exit code: {stopped_process.exit_code}")

        # Get logs to see if it caught the signal
        logs = await sandbox.process.logs(stop_process_name)
        if "Caught SIGTERM" in logs:
            print("✅ Process handled SIGTERM gracefully")
        else:
            print("⚠️ Process may not have handled SIGTERM")

    except Exception as e:
        print(f"❌ Stop test failed: {e}")


async def test_force_kill(sandbox: SandboxInstance):
    """Test force killing a stubborn process."""
    print("🔧 Testing force kill...")

    kill_process_name = "kill-test"
    # Process that ignores SIGTERM
    kill_command = "sh -c 'trap \"\" TERM; echo Starting stubborn process; while true; do echo Still running...; sleep 2; done'"

    # Start stubborn process
    process_request = ProcessRequest(name=kill_process_name, command=kill_command)
    await sandbox.process.exec(process_request)

    # Wait for process to start
    await asyncio.sleep(3)

    # Check process is running
    running_process = await sandbox.process.get(kill_process_name)
    print(f"Process before kill: {running_process.status}")

    # Force kill the process
    try:
        await sandbox.process.kill(kill_process_name)
        print("✅ Force kill command sent")

        # Wait for kill to take effect
        await asyncio.sleep(2)

        # Check final status
        killed_process = await sandbox.process.get(kill_process_name)
        print(f"Process after kill: {killed_process.status}")
        print(f"Exit code: {killed_process.exit_code}")
    except Exception as e:
        print(f"❌ Force kill test failed: {e}")


async def main():
    """Main process kill test function."""
    print("🚀 Starting sandbox process kill tests...")

    try:
        # Create or get sandbox
        sandbox = await create_or_get_sandbox(SANDBOX_NAME)
        print(f"✅ Sandbox ready: {sandbox.metadata.name}")

        # Wait for sandbox to be deployed
        await sandbox.wait()
        print("✅ Sandbox deployed successfully")

        # Run different kill tests
        await test_quick_process_kill(sandbox)
        print()

        await test_stop_vs_kill(sandbox)
        print()

        await test_force_kill(sandbox)
        print()

        # Test process listing
        print("🔧 Testing process listing...")
        processes = await sandbox.process.list()
        print(f"Total processes: {len(processes)}")
        for proc in processes[-5:]:  # Show last 5 processes
            print(f"  - {proc.name}: {proc.status} (PID: {proc.pid})")

        print("🎉 All process kill tests completed successfully!")

    except Exception as e:
        print(f"❌ Process kill test failed with error: {e}")
        logger.exception("Process kill test error")
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

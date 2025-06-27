import asyncio
from logging import getLogger

from utils import create_or_get_sandbox

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.sandbox.client.models.process_request import ProcessRequest

logger = getLogger(__name__)

SANDBOX_NAME = "sandbox-test-python-process-features"


async def test_wait_for_completion_with_logs(sandbox: SandboxInstance):
    """Test exec with wait_for_completion parameter that retrieves logs."""
    print("🔧 Testing wait_for_completion with logs...")

    # Create a process that outputs some logs
    process_request = ProcessRequest(
        name="wait-completion-test",
        command='sh -c "echo Starting process; echo This is stdout; echo This is stderr >&2; sleep 2; echo Process completed"',
        wait_for_completion=True,
    )

    # Execute with wait_for_completion=True
    response = await sandbox.process.exec(process_request)

    # Check that we got the response
    assert response is not None
    assert response.name == "wait-completion-test"
    assert response.status is not None  # Should have a status

    # Check that logs were added to the response
    assert hasattr(response, "logs")
    assert response.logs is not None
    logs = response.logs
    assert isinstance(logs, str)
    assert len(logs) > 0

    # Verify log content
    assert "Starting process" in logs
    assert "This is stdout" in logs
    assert "This is stderr" in logs
    assert "Process completed" in logs

    print(f"✅ Process completed with status: {response.status}")
    print(f"✅ Retrieved logs (length: {len(logs)} chars)")
    print(f"   First 100 chars: {logs[:100]}...")


async def test_on_log_callback(sandbox: SandboxInstance):
    """Test exec with on_log callback parameter."""
    print("🔧 Testing on_log callback...")

    # Create a list to collect log messages
    log_messages = []

    def log_collector(message: str):
        log_messages.append(message)
        print(f"   📝 Log received: {message!r}")  # Show repr to see exact content

    # Create a process that outputs logs over time
    process_request = ProcessRequest(
        command='sh -c "echo First message; sleep 1; echo Second message; sleep 1; echo Third message"'
    )

    # Execute with on_log callback (name will be auto-generated)
    response = await sandbox.process.exec(process_request, on_log=log_collector)

    # Check that a name was generated
    assert response.name is not None
    assert response.name.startswith("proc-")
    print(f"✅ Auto-generated process name: {response.name}")

    # Wait for the process to complete and logs to be collected
    await sandbox.process.wait(response.name)

    # Give a bit more time for final logs to arrive
    await asyncio.sleep(2)

    # Check that we received log messages
    assert len(log_messages) > 0
    print(f"✅ Received {len(log_messages)} log messages")

    # Join all messages to check content
    all_logs = " ".join(log_messages)

    # Verify we got expected messages
    assert "First message" in all_logs
    assert "Second message" in all_logs
    assert "Third message" in all_logs

    print("✅ Log callback test completed successfully")


async def test_combined_features(sandbox: SandboxInstance):
    """Test using both wait_for_completion and on_log together."""
    print("🔧 Testing combined wait_for_completion and on_log...")

    # Create a list to collect real-time logs
    realtime_logs = []

    def realtime_collector(message: str):
        realtime_logs.append(message)

    # Create a process with a specific name
    process_request = ProcessRequest(
        name="combined-test",
        command='sh -c "echo Starting combined test; sleep 1; echo Middle of test; sleep 1; echo Test completed"',
        wait_for_completion=True,
    )

    # Execute with both features
    response = await sandbox.process.exec(process_request, on_log=realtime_collector)

    # Check the response
    assert response.name == "combined-test"
    assert response.status is not None

    # Check that we got logs in the response
    assert hasattr(response, "logs")
    final_logs = response.logs

    # Check that we got real-time logs
    assert len(realtime_logs) > 0

    print(f"✅ Process completed with status: {response.status}")
    print(f"✅ Real-time logs collected: {len(realtime_logs)} messages")
    print(f"✅ Final logs in response: {len(final_logs)} chars")

    # Verify content
    assert "Starting combined test" in final_logs
    assert "Test completed" in final_logs

    # Real-time logs should also contain the messages
    all_realtime = " ".join(realtime_logs)
    assert "Starting combined test" in all_realtime
    assert "Middle of test" in all_realtime
    assert "Test completed" in all_realtime


async def test_on_log_without_name(sandbox: SandboxInstance):
    """Test that on_log works when no name is provided (auto-generates name)."""
    print("🔧 Testing on_log with auto-generated name...")

    log_count = 0

    def count_logs(message: str):
        nonlocal log_count
        log_count += 1

    # Process without name
    process_dict = {"command": "echo 'Testing auto name generation'"}

    # Execute with on_log (should auto-generate name)
    response = await sandbox.process.exec(process_dict, on_log=count_logs)

    # Check that name was generated
    assert response.name is not None
    assert response.name.startswith("proc-")
    assert len(response.name) > len("proc-")  # Should have UUID suffix

    print(f"✅ Auto-generated name: {response.name}")

    # Wait a bit for logs
    await asyncio.sleep(2)

    # Should have received at least one log
    assert log_count > 0
    print(f"✅ Received {log_count} log messages")


async def main():
    """Main test function for new process features."""
    print("🚀 Starting sandbox process feature tests...")

    try:
        # Create or get sandbox
        sandbox = await create_or_get_sandbox(SANDBOX_NAME)
        print(f"✅ Sandbox ready: {sandbox.metadata.name}")

        await sandbox.fs.ls("/blaxel")
        # Run tests
        await test_wait_for_completion_with_logs(sandbox)
        print()

        await test_on_log_callback(sandbox)
        print()

        await test_combined_features(sandbox)
        print()

        await test_on_log_without_name(sandbox)
        print()

        print("🎉 All process feature tests completed successfully!")

    except Exception as e:
        print(f"❌ Process feature test failed with error: {e}")
        logger.exception("Process feature test error")
        raise
    finally:
        print("🧹 Cleaning up...")
        try:
            await SandboxInstance.delete(SANDBOX_NAME)
            print("✅ Sandbox deleted")
        except Exception as e:
            print(f"⚠️ Failed to delete sandbox: {e}")


if __name__ == "__main__":
    asyncio.run(main())

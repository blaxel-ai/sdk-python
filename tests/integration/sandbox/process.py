import asyncio
import time
from logging import getLogger

from utils import create_or_get_sandbox

from blaxel.core.sandbox import (
    ProcessRequestWithLog,
    ProcessResponseWithLog,
    SandboxInstance,
)
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

    proc = await sandbox.process.exec(
        {
            "command": "echo 'Hello, World!'",
            "wait_for_completion": True,
        }
    )
    assert proc.status == "completed"

    proc = await sandbox.process.exec(
        {
            "command": "echo 'Hello, World!'",
            "waitForCompletion": True,
        }
    )
    assert proc.status == "completed"


async def test_on_log_callback(sandbox: SandboxInstance):
    """Test exec with on_log callback parameter."""
    print("🔧 Testing on_log callback...")

    # Create a list to collect log messages
    log_messages = []

    def log_collector(message: str):
        log_messages.append(message)
        print(f"   📝 Log received: {message!r}")  # Show repr to see exact content

    # Create a process that outputs logs over time
    process_request = ProcessRequestWithLog(
        command='sh -c "echo First message; sleep 1; echo Second message; sleep 1; echo Third message"',
        on_log=log_collector,
    )

    # Execute with on_log callback (name will be auto-generated)
    response = await sandbox.process.exec(process_request)

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
    process_request = ProcessRequestWithLog(
        name="combined-test",
        command='sh -c "echo Starting combined test; sleep 1; echo Middle of test; sleep 1; echo Test completed"',
        wait_for_completion=True,
        on_log=realtime_collector,
    )

    # Execute with both features
    response = await sandbox.process.exec(process_request)

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
    """Test on_log callback without specifying name (should generate one)."""
    print("🔧 Testing on_log callback without name...")

    # Track logs
    log_messages = []

    def log_collector(message: str):
        log_messages.append(message)
        print(f"   📝 Log received: {repr(message)}")

    # Create a process without specifying a name
    process_request = ProcessRequestWithLog(
        command='sh -c "echo Hello from unnamed process; echo Second message; sleep 1; echo Final message"',
        wait_for_completion=True,
        on_log=log_collector,
    )

    # Execute
    response = await sandbox.process.exec(process_request)

    # Check that a name was generated
    assert response.name is not None
    assert len(response.name) > 0

    # Check that we received logs
    assert len(log_messages) > 0
    all_logs = " ".join(log_messages)
    assert "Hello from unnamed process" in all_logs
    assert "Second message" in all_logs
    assert "Final message" in all_logs

    print(f"✅ Process completed with generated name: {response.name}")
    print(f"✅ Received {len(log_messages)} log messages")


async def test_stream_close(sandbox: SandboxInstance):
    """Test stream close functionality."""
    print("🔧 Testing stream close functionality...")

    # Track logs and when they stop
    log_messages = []
    last_log_time = time.time()
    is_receiving_logs = True

    def log_collector(message: str):
        nonlocal last_log_time, is_receiving_logs
        log_messages.append(message)
        last_log_time = time.time()
        is_receiving_logs = True
        print(f"   📝 Log received at {time.time()}: {repr(message)}")

    # Create a long-running process that outputs logs continuously
    process_request = ProcessRequestWithLog(
        name="stream-close-test",
        command="sh -c 'for i in $(seq 1 5); do echo \"Hello from stdout $i\"; sleep 1; done'",
        wait_for_completion=False,  # Important: don't wait for completion
        on_log=log_collector,
    )

    # Execute and get response with close() method
    response = await sandbox.process.exec(process_request)

    # Check that we got a response with close method
    assert isinstance(response, ProcessResponseWithLog), "Response should be ProcessResponseWithLog"
    assert hasattr(response, "close"), "Response should have close() method"
    assert callable(response.close), "close should be a function"

    # Wait for a few logs to come in
    await asyncio.sleep(2)

    # Should have received some logs by now
    logs_before_close = len(log_messages)
    assert logs_before_close > 0, "Should have received some logs before close"
    print(f"✅ Received {logs_before_close} logs before closing")

    # Close the stream
    print("   🛑 Calling close() to stop the stream...")
    response.close()

    # Mark that we're no longer expecting logs
    is_receiving_logs = False

    # Wait a bit to ensure no more logs come in
    logs_at_close = len(log_messages)
    await asyncio.sleep(3)

    # Check that no new logs were received after close
    logs_after_close = len(log_messages)
    assert logs_after_close == logs_at_close, (
        f"No new logs should be received after close (before: {logs_at_close}, after: {logs_after_close})"
    )

    print(f"✅ Stream closed successfully. Total logs received: {len(log_messages)}")
    print("✅ Process should still be running in background (not killed by close)")

    # Verify the process is still running (close should only stop streaming, not kill the process)
    try:
        process_info = await sandbox.process.get(response.name)
        print(f"✅ Process status after close: {process_info.status} -> {process_info.logs}")
    except Exception as error:
        print(f"⚠️ Could not check process status: {error}")


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

        await test_stream_close(sandbox)
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

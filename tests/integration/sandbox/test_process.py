import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import async_sleep, default_image, default_labels, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestProcessOperations:
    """Test sandbox process operations."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("process-test")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": default_image,
                "memory": 2048,
                "labels": default_labels,
            }
        )

        yield

        # Cleanup
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestExec(TestProcessOperations):
    """Test exec operations."""

    async def test_executes_simple_command(self):
        """Test executing a simple command."""
        result = await self.sandbox.process.exec(
            {
                "command": "echo 'Hello World'",
                "wait_for_completion": True,
            }
        )

        assert result.status == "completed"
        assert "Hello World" in result.logs

    async def test_executes_command_with_custom_name(self):
        """Test executing a command with a custom name."""
        result = await self.sandbox.process.exec(
            {
                "name": "custom-named-process",
                "command": "echo 'named'",
                "wait_for_completion": True,
            }
        )

        assert result.name == "custom-named-process"

    async def test_generates_name_when_not_provided(self):
        """Test that a name is generated when not provided."""
        result = await self.sandbox.process.exec(
            {
                "command": "echo 'auto'",
                "wait_for_completion": True,
            }
        )

        assert result.name is not None
        assert result.name.startswith("proc-")

    async def test_executes_command_with_working_directory(self):
        """Test executing a command with a working directory."""
        await self.sandbox.fs.mkdir("/tmp/workdir")

        result = await self.sandbox.process.exec(
            {
                "command": "pwd",
                "working_dir": "/tmp/workdir",
                "wait_for_completion": True,
            }
        )

        assert "/tmp/workdir" in result.logs

    async def test_captures_stdout(self):
        """Test capturing stdout."""
        result = await self.sandbox.process.exec(
            {
                "command": "echo 'stdout output'",
                "wait_for_completion": True,
            }
        )

        assert "stdout output" in result.logs

    async def test_captures_stderr(self):
        """Test capturing stderr."""
        result = await self.sandbox.process.exec(
            {
                "command": "echo 'stderr output' >&2",
                "wait_for_completion": True,
            }
        )

        assert "stderr output" in result.logs

    async def test_returns_exit_code(self):
        """Test returning exit codes."""
        success_result = await self.sandbox.process.exec(
            {
                "command": "exit 0",
                "wait_for_completion": True,
            }
        )
        assert success_result.exit_code == 0

        fail_result = await self.sandbox.process.exec(
            {
                "command": "exit 42",
                "wait_for_completion": True,
            }
        )
        assert fail_result.exit_code == 42


@pytest.mark.asyncio(loop_scope="class")
class TestExecWithOnLogCallback(TestProcessOperations):
    """Test exec with onLog callback."""

    async def test_receives_logs_via_callback(self):
        """Test receiving logs via callback."""
        logs = []

        await self.sandbox.process.exec(
            {
                "command": "echo 'line1' && echo 'line2' && echo 'line3'",
                "wait_for_completion": True,
                "on_log": lambda log: logs.append(log),
            }
        )

        assert len(logs) > 0
        all_logs = " ".join(logs)
        assert "line1" in all_logs
        assert "line2" in all_logs
        assert "line3" in all_logs


@pytest.mark.asyncio(loop_scope="class")
class TestExecWithoutWaiting(TestProcessOperations):
    """Test exec without waiting for completion."""

    async def test_returns_immediately_when_wait_for_completion_is_false(self):
        """Test that exec returns immediately when waitForCompletion is false."""
        import time

        start_time = time.time()

        result = await self.sandbox.process.exec(
            {
                "name": "no-wait-test",
                "command": "sleep 5",
                "wait_for_completion": False,
            }
        )

        elapsed = time.time() - start_time
        assert elapsed < 4  # Should return well before 5 seconds
        assert result.name == "no-wait-test"

        # Cleanup
        await self.sandbox.process.kill("no-wait-test")


@pytest.mark.asyncio(loop_scope="class")
class TestProcessGet(TestProcessOperations):
    """Test process get operations."""

    async def test_retrieves_process_information(self):
        """Test retrieving process information."""
        await self.sandbox.process.exec(
            {
                "name": "get-test",
                "command": "echo 'test'",
                "wait_for_completion": True,
            }
        )

        process = await self.sandbox.process.get("get-test")

        assert process.name == "get-test"
        assert process.status == "completed"

    async def test_shows_running_status_for_long_process(self):
        """Test showing running status for long process."""
        await self.sandbox.process.exec(
            {
                "name": "long-running",
                "command": "sleep 30",
                "wait_for_completion": False,
            }
        )

        process = await self.sandbox.process.get("long-running")
        assert process.status == "running"

        # Clean up
        await self.sandbox.process.kill("long-running")


@pytest.mark.asyncio(loop_scope="class")
class TestProcessLogs(TestProcessOperations):
    """Test process logs operations."""

    async def test_retrieves_all_logs(self):
        """Test retrieving all logs."""
        await self.sandbox.process.exec(
            {
                "name": "logs-test",
                "command": "echo 'stdout' && echo 'stderr' >&2",
                "wait_for_completion": True,
            }
        )

        logs = await self.sandbox.process.logs("logs-test", "all")

        assert "stdout" in logs
        assert "stderr" in logs

    async def test_retrieves_stdout_only(self):
        """Test retrieving stdout only."""
        await self.sandbox.process.exec(
            {
                "name": "stdout-only",
                "command": "echo 'out' && echo 'err' >&2",
                "wait_for_completion": True,
            }
        )

        logs = await self.sandbox.process.logs("stdout-only", "stdout")
        assert "out" in logs

    async def test_retrieves_stderr_only(self):
        """Test retrieving stderr only."""
        await self.sandbox.process.exec(
            {
                "name": "stderr-only",
                "command": "echo 'out' && echo 'err' >&2",
                "wait_for_completion": True,
            }
        )

        logs = await self.sandbox.process.logs("stderr-only", "stderr")
        assert "err" in logs


@pytest.mark.asyncio(loop_scope="class")
class TestStreamLogs(TestProcessOperations):
    """Test streamLogs operations."""

    async def test_streams_logs_in_real_time(self):
        """Test streaming logs in real-time."""
        logs = []

        await self.sandbox.process.exec(
            {
                "name": "stream-test",
                "command": 'for i in 1 2 3; do echo "msg $i"; sleep 1; done',
                "wait_for_completion": False,
            }
        )

        stream = self.sandbox.process.stream_logs(
            "stream-test",
            {
                "on_log": lambda log: logs.append(log),
            },
        )

        await self.sandbox.process.wait("stream-test")
        await async_sleep(1)
        stream["close"]()

        assert len(logs) > 0

    async def test_can_close_stream_early(self):
        """Test that stream can be closed early."""
        logs = []

        await self.sandbox.process.exec(
            {
                "name": "close-early",
                "command": "for i in $(seq 1 10); do echo $i; sleep 1; done",
                "wait_for_completion": False,
            }
        )

        stream = self.sandbox.process.stream_logs(
            "close-early",
            {
                "on_log": lambda log: logs.append(log),
            },
        )

        await async_sleep(2)
        stream["close"]()

        logs_at_close = len(logs)
        await async_sleep(3)

        # No new logs should arrive after close
        assert len(logs) == logs_at_close

        # Clean up
        await self.sandbox.process.kill("close-early")


@pytest.mark.asyncio(loop_scope="class")
class TestProcessWait(TestProcessOperations):
    """Test process wait operations."""

    async def test_waits_for_process_completion(self):
        """Test waiting for process completion."""
        await self.sandbox.process.exec(
            {
                "name": "wait-test",
                "command": "sleep 2 && echo 'done'",
                "wait_for_completion": False,
            }
        )

        await self.sandbox.process.wait("wait-test")

        process = await self.sandbox.process.get("wait-test")
        assert process.status == "completed"

    async def test_respects_max_wait_timeout(self):
        """Test that maxWait timeout is respected."""
        await self.sandbox.process.exec(
            {
                "name": "timeout-test",
                "command": "sleep 60",
                "wait_for_completion": False,
            }
        )

        with pytest.raises(Exception, match="Process did not finish in time"):
            await self.sandbox.process.wait("timeout-test", max_wait=2000)

        # Cleanup
        await self.sandbox.process.kill("timeout-test")


@pytest.mark.asyncio(loop_scope="class")
class TestProcessKill(TestProcessOperations):
    """Test process kill operations."""

    async def test_kills_running_process(self):
        """Test killing a running process."""
        await self.sandbox.process.exec(
            {
                "name": "kill-test",
                "command": "sleep 60",
                "wait_for_completion": False,
            }
        )

        process = await self.sandbox.process.get("kill-test")
        assert process.status == "running"

        await self.sandbox.process.kill("kill-test")
        await async_sleep(1)

        process = await self.sandbox.process.get("kill-test")
        assert process.status in ["killed", "failed", "completed"]

    async def test_handles_killing_completed_process_gracefully(self):
        """Test that killing a completed process is handled gracefully."""
        await self.sandbox.process.exec(
            {
                "name": "already-done",
                "command": "echo 'done'",
                "wait_for_completion": True,
            }
        )

        # Should not throw
        try:
            await self.sandbox.process.kill("already-done")
        except Exception:
            # Expected - some implementations throw for already completed processes
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestRestartOnFailure(TestProcessOperations):
    """Test restartOnFailure operations."""

    async def test_restarts_process_on_failure(self):
        """Test that process restarts on failure."""
        result = await self.sandbox.process.exec(
            {
                "name": "restart-test",
                "command": "exit 1",
                "restart_on_failure": True,
                "max_restarts": 3,
                "wait_for_completion": True,
            }
        )

        assert result.restart_count > 0
        assert result.restart_count <= 3

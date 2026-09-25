"""Process stdin: JSON-RPC over a writable pipe, EOF shutdown, and a real MCP server."""

import json
import time
from typing import Any, Callable

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.sandbox.client.models import ProcessResponse
from blaxel.core.sandbox.types import ResponseError
from tests.helpers import async_sleep, default_image, default_labels, unique_name

# A JSON-RPC echo server in sh: every line in becomes a reply with the same id.
ECHO_LOOP = (
    "while IFS= read -r l; do "
    "id=$(printf '%s' \"$l\" | sed -n 's/.*\"id\":\\([0-9]*\\).*/\\1/p'); "
    'echo "{\\"jsonrpc\\":\\"2.0\\",\\"id\\":$id,\\"result\\":{\\"echo\\":$l}}"; '
    "done"
)


class JsonRpcReader:
    """Collects JSON-RPC replies from a process's stdout, by id.

    This is what a stdio MCP client does on its side of the pipe: the live log
    stream is the fast path, and the log endpoint (which holds everything the
    process wrote so far) covers a stream the dev gateway dropped on connect.
    """

    def __init__(self, sandbox: SandboxInstance, name: str):
        self.sandbox = sandbox
        self.name = name
        self.replies: dict[int, dict[str, Any]] = {}
        self.last_error: Exception | None = None
        self._stream = sandbox.process.stream_logs(name, {"on_stdout": self._collect})

    def _collect(self, line: str) -> None:
        try:
            message = json.loads(line)
        except ValueError:
            return  # not JSON, ignore
        if isinstance(message, dict) and isinstance(message.get("id"), int):
            self.replies[message["id"]] = message

    async def _collect_from_logs(self) -> None:
        try:
            stdout = await self.sandbox.process.logs(self.name, "stdout")
        except Exception as error:
            self.last_error = error  # transient gateway error, the next poll will see the logs
            return
        for line in stdout.splitlines():
            self._collect(line)

    async def reply(self, id: int, timeout: float = 30.0) -> dict[str, Any]:
        deadline = time.monotonic() + timeout
        while id not in self.replies and time.monotonic() < deadline:
            await async_sleep(0.5)
            if id not in self.replies:
                await self._collect_from_logs()
        assert id in self.replies, (
            f"no JSON-RPC reply with id {id} (last log fetch error: {self.last_error!r}, "
            f"process: {await self._describe()})"
        )
        return self.replies[id]

    async def _describe(self) -> str:
        try:
            process = await self.sandbox.process.get(self.name)
            logs = await self.sandbox.process.logs(self.name, "all")
            return f"status={process.status} exit_code={process.exit_code} logs={logs[-800:]!r}"
        except Exception as error:
            return f"unavailable: {error!r}"

    def close(self) -> None:
        self._stream.close()


async def exec_retrying(sandbox: SandboxInstance, request: dict[str, Any], attempts: int = 3):
    """The dev gateway sometimes answers a process start with a 502 after ~10s
    even though the sandbox is healthy; that is unrelated to stdin, so retry."""
    for attempt in range(1, attempts + 1):
        try:
            return await sandbox.process.exec(request)
        except ResponseError as error:
            if error.response.status_code != 502 or attempt >= attempts:
                raise


async def wait_for_process(
    sandbox: SandboxInstance, name: str, done: Callable[[ProcessResponse], bool], timeout: float
) -> ProcessResponse:
    """Poll the process until ``done`` accepts it, riding through gateway flakes."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            process = await sandbox.process.get(name)
        except Exception:
            process = None  # transient gateway error, poll again
        if process is not None and done(process):
            return process
        await async_sleep(0.5)
    raise AssertionError(f"process {name} did not finish in {timeout}s")


async def kill_quietly(sandbox: SandboxInstance, name: str) -> None:
    try:
        await sandbox.process.kill(name)
    except Exception:
        pass


@pytest.mark.asyncio(loop_scope="class")
class TestProcessStdin:
    """Test writing to and closing a process's stdin."""

    sandbox: SandboxInstance
    sandbox_name: str
    # False on a sandbox-api release without the stdin routes: the tests then
    # skip instead of failing, and run on their own once the release lands.
    stdin_supported: bool

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class and probe stdin support."""
        request.cls.sandbox_name = unique_name("process-stdin")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": default_image,
                "memory": 2048,
                "labels": default_labels,
            }
        )
        probe = await exec_retrying(
            request.cls.sandbox,
            {"name": "stdin-probe", "stdin": True, "command": "true", "wait_for_completion": True},
        )
        request.cls.stdin_supported = probe.stdin is True

        yield

        # Cleanup
        try:
            await request.cls.sandbox.delete()
        except Exception:
            pass

    def require_stdin(self) -> None:
        if not self.stdin_supported:
            pytest.skip("sandbox-api without the process stdin routes")

    async def test_drives_a_json_rpc_echo_loop_and_stops_it_with_eof(self):
        self.require_stdin()
        name = "stdin-echo"
        started = await exec_retrying(
            self.sandbox, {"name": name, "stdin": True, "command": ECHO_LOOP}
        )
        assert started.stdin is True

        reader = JsonRpcReader(self.sandbox, name)
        try:
            await self.sandbox.process.write_stdin(
                name, '{"jsonrpc":"2.0","id":1,"method":"ping"}\n'
            )
            reply = await reader.reply(1)
            assert reply["result"]["echo"]["method"] == "ping"

            # Order survives back-to-back writes.
            await self.sandbox.process.write_stdin(name, '{"jsonrpc":"2.0","id":2,"method":"a"}\n')
            await self.sandbox.process.write_stdin(name, '{"jsonrpc":"2.0","id":3,"method":"b"}\n')
            assert (await reader.reply(2))["id"] == 2
            assert (await reader.reply(3))["id"] == 3

            await self.sandbox.process.close_stdin(name)
            done = await wait_for_process(
                self.sandbox, name, lambda p: p.status == "completed", timeout=20.0
            )
            assert done.exit_code == 0
        finally:
            reader.close()

    async def test_refuses_writes_to_a_process_started_without_stdin(self):
        self.require_stdin()
        name = "no-stdin"
        await exec_retrying(self.sandbox, {"name": name, "command": "sleep 10"})
        try:
            with pytest.raises(ResponseError) as raised:
                await self.sandbox.process.write_stdin(name, "x\n")
            assert raised.value.response.status_code == 409
        finally:
            await kill_quietly(self.sandbox, name)

    async def test_runs_a_real_mcp_stdio_server(self):
        """initialize, tools/list, then shutdown on EOF."""
        self.require_stdin()
        name = "mcp-fs"
        # `npx -y @modelcontextprotocol/server-filesystem /tmp` is what a user types,
        # but `npm exec` has been seen to stall past a minute on a fresh sandbox even
        # with a warm cache, so install once (measured 6 to 10 seconds) and start the
        # server binary directly.
        install = await exec_retrying(
            self.sandbox,
            {
                "name": "mcp-fs-install",
                "command": "mkdir -p /tmp/mcp && cd /tmp/mcp"
                " && npm install --no-save @modelcontextprotocol/server-filesystem",
                "wait_for_completion": True,
            },
        )
        assert install.exit_code == 0, install.logs
        await exec_retrying(
            self.sandbox,
            {
                "name": name,
                "stdin": True,
                "command": "node /tmp/mcp/node_modules/.bin/mcp-server-filesystem /tmp",
            },
        )
        reader = JsonRpcReader(self.sandbox, name)
        try:
            initialize = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "sdk-integration", "version": "0"},
                },
            }
            await self.sandbox.process.write_stdin(name, json.dumps(initialize) + "\n")
            init = await reader.reply(1)
            assert "error" not in init
            assert init["result"]["serverInfo"]["name"]

            await self.sandbox.process.write_stdin(
                name, '{"jsonrpc":"2.0","method":"notifications/initialized"}\n'
            )
            await self.sandbox.process.write_stdin(
                name, '{"jsonrpc":"2.0","id":2,"method":"tools/list"}\n'
            )
            tools = (await reader.reply(2))["result"]["tools"]
            assert len(tools) > 0

            await self.sandbox.process.close_stdin(name)
            done = await wait_for_process(
                self.sandbox, name, lambda p: p.status != "running", timeout=30.0
            )
            assert done.status != "running"
        finally:
            reader.close()
            await kill_quietly(self.sandbox, name)

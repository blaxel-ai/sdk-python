import math
import threading
import time
from typing import Any, Callable, Dict, Literal, Union
from urllib.parse import quote

import httpx

from ...common.settings import settings
from ..client.api.process.delete_process_identifier_stdin import (
    sync_detailed as delete_process_stdin,
)
from ..client.api.process.get_process_identifier import sync_detailed as get_process
from ..client.api.process.post_process_identifier_stdin import (
    sync_detailed as post_process_stdin,
)
from ..client.models import ProcessResponse, SuccessResponse
from ..client.models.process_request import ProcessRequest
from ..transient_retry import is_retryable_read_error, retry_on_transient_reset
from ..types import (
    ProcessRequestWithLog,
    ProcessResponseWithLog,
    SandboxConfiguration,
    StreamHandle,
    api_result,
    is_missing_route,
    wait_request_timeout,
    wait_seconds,
)
from .action import SyncSandboxAction


class SyncSandboxProcess(SyncSandboxAction):
    """Run commands in a sandbox and read their status and output (synchronous).

    Reach it as ``sandbox.process``. Methods that take an ``identifier``
    accept the process name or its PID. A command that exits with a non-zero
    code ends with status ``"failed"`` and its ``exit_code``; no exception is
    raised for it. ``get`` and ``list`` return at most the last 64 KB of each
    output stream; :meth:`logs` returns up to 4 MB. An error status from the
    sandbox API raises ``ResponseError``.

    Example:
        ```python
        result = sandbox.process.exec(
            {"name": "build", "command": "npm run build", "wait_for_completion": True}
        )
        print(result.status, result.exit_code, result.stdout)
        ```
    """

    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    def stream_logs(
        self,
        process_name: str,
        options: Dict[str, Callable[[str], None]] | None = None,
    ) -> StreamHandle:
        """Stream logs from a process with automatic reconnection and deduplication.

        The stream starts with the output written so far, then follows live
        output. It runs in daemon threads, reconnects every 30 seconds and
        drops lines already delivered.

        Args:
            process_name: Process name or PID.
            options: Optional dict of callbacks, each called with one line from
                a background thread: ``on_log`` (stdout and stderr),
                ``on_stdout`` and ``on_stderr``.

        Returns a StreamHandle that can be used as a context manager:

            with sandbox.process.stream_logs(name, options) as handle:
                # do something
            # handle is automatically closed

        Or manually:

            handle = sandbox.process.stream_logs(name, options)
            try:
                # do something
            finally:
                handle.close()
        """
        if options is None:
            options = {}
        reconnect_interval = 30
        is_running = threading.Event()
        is_running.set()
        seen_logs = set()
        current_stream: StreamHandle | None = None
        timer_lock = threading.Lock()
        reconnect_timer: dict[str, threading.Timer | None] = {"t": None}

        def start_stream():
            nonlocal current_stream
            log_counter = [0]

            def make_dedup(cb_key: str):
                def inner(content: str):
                    key = f"{log_counter[0]}:{content}"
                    log_counter[0] += 1
                    if key not in seen_logs:
                        seen_logs.add(key)
                        if options.get(cb_key):
                            options[cb_key](content)

                return inner

            wrapped_options: Dict[str, Callable[[str], None]] = {}
            if "on_log" in options:
                wrapped_options["on_log"] = make_dedup("on_log")
            if "on_stdout" in options:
                wrapped_options["on_stdout"] = make_dedup("on_stdout")
            if "on_stderr" in options:
                wrapped_options["on_stderr"] = make_dedup("on_stderr")
            if current_stream:
                current_stream.close()
            current_stream = self._stream_logs(process_name, wrapped_options)

            def schedule():
                if is_running.is_set():
                    start_stream()

            with timer_lock:
                if reconnect_timer["t"]:
                    reconnect_timer["t"].cancel()
                t = threading.Timer(reconnect_interval, schedule)
                reconnect_timer["t"] = t
                t.daemon = True
                t.start()

        start_stream()

        def close():
            nonlocal current_stream
            is_running.clear()
            with timer_lock:
                if reconnect_timer["t"]:
                    reconnect_timer["t"].cancel()
                    reconnect_timer["t"] = None
            if current_stream:
                current_stream.close()
                current_stream = None
            seen_logs.clear()

        def wait_func(timeout=None):
            if current_stream:
                current_stream.wait(timeout=timeout)

        return StreamHandle(close, wait_func)

    def _stream_logs(
        self,
        identifier: str,
        options: Dict[str, Callable[[str], None]] | None = None,
    ) -> StreamHandle:
        """Private method to stream logs from a process with callbacks for different output types."""
        if options is None:
            options = {}
        closed = threading.Event()
        errors: list[Exception] = []

        def run():
            url = f"{self.url}/process/{identifier}/logs/stream"
            headers = {**settings.headers, **self.sandbox_config.headers}
            try:
                with httpx.Client() as client_instance:
                    with client_instance.stream("GET", url, headers=headers) as response:
                        if response.status_code != 200:
                            raise Exception(f"Failed to stream logs: {response.read().decode()}")
                        buffer = ""
                        for chunk in response.iter_text():
                            if closed.is_set():
                                break
                            buffer += chunk
                            lines = buffer.split("\n")
                            buffer = lines.pop()
                            for line in lines:
                                if line.startswith("[keepalive]"):
                                    continue
                                if line.startswith("stdout:"):
                                    content = line[7:]
                                    if options.get("on_stdout"):
                                        options["on_stdout"](content)
                                    if options.get("on_log"):
                                        options["on_log"](content)
                                elif line.startswith("stderr:"):
                                    content = line[7:]
                                    if options.get("on_stderr"):
                                        options["on_stderr"](content)
                                    if options.get("on_log"):
                                        options["on_log"](content)
                                else:
                                    if options.get("on_log"):
                                        options["on_log"](line)
            except Exception as e:
                # Ignore on close
                if not closed.is_set():
                    errors.append(e)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

        def close():
            closed.set()

        def wait_func(timeout=None):
            thread.join(timeout=timeout)
            if errors:
                raise errors[0]

        return StreamHandle(close, wait_func)

    def exec(
        self,
        process: Union[ProcessRequest, ProcessRequestWithLog, Dict[str, Any]],
    ) -> Union[ProcessResponse, ProcessResponseWithLog]:
        """Execute a process in the sandbox.

        By default this starts the command and returns at once with status
        ``"running"``; use :meth:`wait`, :meth:`get` or :meth:`logs` to follow
        it. With ``wait_for_completion`` it returns when the command ends:

        - Without log callbacks the request waits silently. The edge closes a
          request that stays silent for about 60 seconds with HTTP 504
          (``ResponseError``) while the command keeps running. For longer
          commands, start without waiting and call :meth:`wait`, or pass a
          log callback.
        - With ``on_log``, ``on_stdout`` or ``on_stderr`` the output is
          streamed to the callbacks and keepalives hold the request open, so
          long commands are safe.

        Log callbacks without ``wait_for_completion`` start a background log
        stream and return a ``ProcessResponseWithLog``; call its ``close()``
        when done.

        Without ``timeout`` a command runs with no time limit, or 600 seconds
        when ``keep_alive`` is set; ``0`` means no limit. Starting a process
        with the name of a process that is still running fails with HTTP 400.

        Args:
            process: A ``ProcessRequest``, a ``ProcessRequestWithLog`` or a dict
                with ``command`` and optional ``name``, ``working_dir``,
                ``env``, ``wait_for_completion``, ``timeout`` (seconds),
                ``keep_alive`` (keep the sandbox from scaling to zero while the
                command runs), ``wait_for_ports`` (return once these ports
                listen on a non-loopback address), ``restart_on_failure``,
                ``max_restarts``, ``stdin`` (open a pipe for
                :meth:`write_stdin`) and the ``on_log``, ``on_stdout`` and
                ``on_stderr`` callbacks.

        Returns:
            ``ProcessResponse`` with ``pid``, ``name``, ``status``,
            ``exit_code``, ``stdout``, ``stderr`` and ``logs``, or a
            ``ProcessResponseWithLog`` when log callbacks were given.

        Raises:
            ResponseError: When the sandbox API rejects the request, such as
                HTTP 400 for a name in use or HTTP 504 for a silent wait.
            Exception: When a streamed execution fails.

        Example:
            ```python
            result = sandbox.process.exec(
                {
                    "command": "pip install -r requirements.txt",
                    "working_dir": "/app",
                    "wait_for_completion": True,
                    "on_log": print,
                }
            )
            if result.status == "failed":
                print(result.exit_code, result.stderr)
            ```
        """
        on_log = None
        on_stdout = None
        on_stderr = None

        if isinstance(process, ProcessRequestWithLog):
            on_log = process.on_log
            on_stdout = process.on_stdout
            on_stderr = process.on_stderr
            process = process.to_dict()

        if isinstance(process, dict):
            process = dict(process)
            if "on_log" in process:
                on_log = process["on_log"]
                del process["on_log"]
            if "on_stdout" in process:
                on_stdout = process["on_stdout"]
                del process["on_stdout"]
            if "on_stderr" in process:
                on_stderr = process["on_stderr"]
                del process["on_stderr"]
            process = ProcessRequest.from_dict(process)

        should_wait_for_completion = process.wait_for_completion

        # When waiting for completion with streaming callbacks, use streaming endpoint
        if should_wait_for_completion and (on_log or on_stdout or on_stderr):
            return self._exec_with_streaming(
                process, on_log=on_log, on_stdout=on_stdout, on_stderr=on_stderr
            )
        else:
            with self.get_client() as client_instance:
                response = client_instance.post("/process", json=process.to_dict(), timeout=None)
                response_data = None
                if response.content:
                    try:
                        response_data = response.json()
                    except Exception:
                        self.handle_response_error(response)
                        raise
                self.handle_response_error(response)
                result = ProcessResponse.from_dict(response_data)

                if on_log or on_stdout or on_stderr:
                    stream_control = self._stream_logs(
                        result.pid,
                        {"on_log": on_log, "on_stdout": on_stdout, "on_stderr": on_stderr},
                    )
                    return ProcessResponseWithLog(
                        result,
                        lambda: stream_control.close() if stream_control else None,
                    )

                return result

    def _exec_with_streaming(
        self,
        process_request: ProcessRequest,
        on_log: Callable[[str], None] | None = None,
        on_stdout: Callable[[str], None] | None = None,
        on_stderr: Callable[[str], None] | None = None,
    ) -> ProcessResponseWithLog:
        """Execute a process with streaming response handling for NDJSON."""
        import json

        headers = (
            self.sandbox_config.headers
            if self.sandbox_config.force_url
            else {**settings.headers, **self.sandbox_config.headers}
        )

        with httpx.Client() as client_instance:
            with client_instance.stream(
                "POST",
                f"{self.url}/process",
                headers={
                    **headers,
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream",
                },
                json=process_request.to_dict(),
                timeout=None,
            ) as response:
                if response.status_code >= 400:
                    error_text = response.read()
                    raise Exception(f"Failed to execute process: {error_text}")

                content_type = response.headers.get("Content-Type", "")
                is_streaming = "application/x-ndjson" in content_type

                # Fallback: server doesn't support streaming, use legacy approach
                if not is_streaming:
                    content = response.read()
                    data = json.loads(content)
                    result = ProcessResponse.from_dict(data)

                    # If process already completed (server waited), emit logs through callbacks
                    if result.status == "completed" or result.status == "failed":
                        if result.stdout:
                            for line in result.stdout.split("\n"):
                                if line:
                                    if on_stdout:
                                        on_stdout(line)
                        if result.stderr:
                            for line in result.stderr.split("\n"):
                                if line:
                                    if on_stderr:
                                        on_stderr(line)
                        if result.logs:
                            for line in result.logs.split("\n"):
                                if line:
                                    if on_log:
                                        on_log(line)

                    return ProcessResponseWithLog(result, lambda: None)

                # Streaming response handling
                buffer = ""
                result = None

                for chunk in response.iter_text():
                    buffer += chunk
                    lines = buffer.split("\n")
                    buffer = lines.pop()

                    for line in lines:
                        if not line.strip():
                            continue
                        try:
                            parsed = json.loads(line)
                            parsed_type = parsed.get("type", "")
                            parsed_data = parsed.get("data", "")

                            if parsed_type == "stdout":
                                if parsed_data:
                                    if on_stdout:
                                        on_stdout(parsed_data)
                                    if on_log:
                                        on_log(parsed_data)
                            elif parsed_type == "stderr":
                                if parsed_data:
                                    if on_stderr:
                                        on_stderr(parsed_data)
                                    if on_log:
                                        on_log(parsed_data)
                            elif parsed_type == "result":
                                try:
                                    result = ProcessResponse.from_dict(json.loads(parsed_data))
                                except Exception:
                                    raise Exception(f"Failed to parse result JSON: {parsed_data}")
                        except json.JSONDecodeError:
                            continue

                # Process any remaining buffer
                if buffer.strip():
                    if buffer.startswith("result:"):
                        json_str = buffer[7:]
                        try:
                            result = ProcessResponse.from_dict(json.loads(json_str))
                        except Exception:
                            raise Exception(f"Failed to parse result JSON: {json_str}")

                if not result:
                    raise Exception("No result received from streaming response")

                return ProcessResponseWithLog(result, lambda: None)

    def wait(self, identifier: str, max_wait: int = 60000, interval: int = 1000) -> ProcessResponse:
        """Wait for a terminal API state; max_wait=-1 waits indefinitely. Never stops the command.

        Polls :meth:`get` until the status is ``completed``, ``failed``,
        ``killed`` or ``stopped``. Transient read errors are retried until the
        deadline.

        Args:
            identifier: Process name or PID.
            max_wait: Deadline in milliseconds, or -1 for no deadline.
            interval: Delay between polls in milliseconds.

        Returns:
            The final ``ProcessResponse``. Check ``status`` and ``exit_code``.

        Raises:
            TimeoutError: When the deadline passes first. The command may
                still be running.
            ValueError: When ``max_wait`` or ``interval`` is out of range, or
                the API reports an unknown status.
            ResponseError: When the process does not exist.

        Example:
            ```python
            sandbox.process.exec({"name": "train", "command": "python train.py"})
            result = sandbox.process.wait("train", max_wait=-1, interval=5000)
            ```
        """
        if (
            not math.isfinite(max_wait)
            or (max_wait < 0 and max_wait != -1)
            or not math.isfinite(interval)
            or interval <= 0
        ):
            raise ValueError(
                "max_wait must be -1 or finite and non-negative; interval must be finite and positive"
            )
        deadline = math.inf if max_wait == -1 else time.monotonic() + max_wait / 1000
        last_error = None
        long_poll = True
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(
                    f"Process did not finish in time ({identifier}); it may still be running"
                ) from last_error
            try:
                result = self._wait_once(identifier, remaining) if long_poll else None
                if result is None:
                    long_poll = False
                    # The route probe used part of the budget: re-measure before the GET.
                    left = max(0.001, deadline - time.monotonic())
                    result = self.get(
                        identifier, retry=False, timeout=None if max_wait == -1 else left
                    )
            except Exception as error:
                if not is_retryable_read_error(error):
                    raise
                last_error = error
            else:
                if time.monotonic() >= deadline:
                    raise TimeoutError(
                        f"Process did not finish in time ({identifier}); it may still be running"
                    ) from last_error
                if result.status in {"completed", "failed", "killed", "stopped"}:
                    return result
                if result.status != "running":
                    raise ValueError(f"Unknown process status: {result.status}")
                last_error = None
            time.sleep(max(0, min(interval / 1000, deadline - time.monotonic())))

    def _wait_once(self, identifier: str, remaining: float) -> ProcessResponse | None:
        """One long-poll on GET /process/{identifier}/wait; None when the sandbox predates it."""
        seconds = wait_seconds(remaining)
        # Not in the generated client yet (ENG-6233): raw call on the shared client.
        with self.get_client() as client:
            response = client.get(
                f"/process/{quote(identifier, safe='')}/wait",
                params={"timeout": seconds},
                timeout=wait_request_timeout(seconds, remaining),
            )
        if is_missing_route(response):
            return None
        self.handle_response_error(response)
        result = ProcessResponse.from_dict(response.json())
        assert result is not None
        return result

    def get(
        self, identifier: str, *, retry: bool = True, timeout: float | None = None
    ) -> ProcessResponse:
        """Read the current state of a process.

        Output fields hold at most the last 64 KB of each stream; use
        :meth:`logs` for more.

        Args:
            identifier: Process name or PID.
            retry: Retry transient connection resets.
            timeout: Optional HTTP timeout for this read, in seconds.

        Returns:
            ``ProcessResponse`` with ``status``, ``exit_code`` and output.

        Raises:
            ResponseError: When the process does not exist (``status`` 404) or
                the sandbox API rejects the request.
        """

        def read() -> ProcessResponse:
            with self.get_client() as transport:
                if timeout is not None:
                    transport.timeout = httpx.Timeout(timeout)
                client = self.get_api_client().set_httpx_client(transport)
                return api_result(get_process(identifier, client=client), ProcessResponse)

        # wait owns its deadline and retry cadence; standalone GET keeps its retries.
        return retry_on_transient_reset(read) if retry else read()

    def list(self) -> list[ProcessResponse]:
        """List running and finished processes.

        Output fields hold at most the last 64 KB of each stream.

        Returns:
            A list of ``ProcessResponse``.

        Raises:
            ResponseError: When the sandbox API rejects the request.
        """

        def list_once() -> list[ProcessResponse]:
            with self.get_client() as client_instance:
                response = client_instance.get("/process")
                self.handle_response_error(response)
                results = []
                for item in response.json():
                    result = ProcessResponse.from_dict(item)
                    assert result is not None
                    results.append(result)
                return results

        return retry_on_transient_reset(list_once)

    def stop(self, identifier: str) -> SuccessResponse:
        """Ask a process to terminate gracefully.

        Returns once the request is accepted. Call :meth:`wait` to confirm the
        process has exited, or :meth:`kill` to force it.

        Args:
            identifier: Process name or PID.

        Returns:
            ``SuccessResponse`` for the accepted request.

        Raises:
            ResponseError: With HTTP 404 when the process does not exist or is
                not running.
        """
        with self.get_client() as client_instance:
            response = client_instance.delete(f"/process/{identifier}")
            self.handle_response_error(response)
            return SuccessResponse.from_dict(response.json())

    def kill(self, identifier: str) -> SuccessResponse:
        """Force a process to terminate.

        Returns once the request is accepted. Call :meth:`wait` to confirm the
        process has exited.

        Args:
            identifier: Process name or PID.

        Returns:
            ``SuccessResponse`` for the accepted request.

        Raises:
            ResponseError: With HTTP 404 when the process does not exist or is
                not running.
        """
        with self.get_client() as client_instance:
            response = client_instance.delete(f"/process/{identifier}/kill")
            self.handle_response_error(response)
            return SuccessResponse.from_dict(response.json())

    def write_stdin(self, identifier: str, data: Union[str, bytes]) -> SuccessResponse:
        """Write raw bytes to the stdin of a process started with ``stdin=True``.

        Bytes are forwarded verbatim, so include the trailing newline your protocol
        expects. Not retried: a duplicate write would corrupt the stream.

        Args:
            identifier: Process name or PID.
            data: Text or bytes to write.

        Returns:
            ``SuccessResponse`` once the data is written.

        Raises:
            ResponseError: With HTTP 409 when the process has no open stdin
                pipe (not started with ``stdin=True``, closed, or lost in a
                sandbox API restart), or 404 when it does not exist.

        Example:
            ```python
            sandbox.process.exec({"name": "repl", "command": "python3 -i", "stdin": True})
            sandbox.process.write_stdin("repl", "print(1 + 1)\\n")
            sandbox.process.close_stdin("repl")
            ```
        """
        with self.get_api_client() as client:
            # str or bytes, sent as-is with the octet-stream content type.
            response = post_process_stdin(identifier, client=client, body=data)
        return api_result(response, SuccessResponse)

    def close_stdin(self, identifier: str) -> SuccessResponse:
        """Close the process's stdin (EOF). Idempotent.

        For stdio protocols such as MCP this is the clean shutdown path.

        Args:
            identifier: Process name or PID.

        Returns:
            ``SuccessResponse`` once stdin is closed.

        Raises:
            ResponseError: When the process does not exist or the sandbox API
                rejects the request.
        """
        with self.get_api_client() as client:
            response = delete_process_stdin(identifier, client=client)
        return api_result(response, SuccessResponse)

    def logs(
        self,
        identifier: str,
        log_type: Literal["stdout", "stderr", "all"] = "all",
    ) -> str:
        """Read the output of a process, up to 4 MB.

        Args:
            identifier: Process name or PID.
            log_type: ``"stdout"``, ``"stderr"`` or ``"all"`` (both streams
                combined).

        Returns:
            The output as text.

        Raises:
            ResponseError: When the process does not exist or the sandbox API
                rejects the request.
        """

        def logs_once() -> str:
            with self.get_client() as client_instance:
                response = client_instance.get(f"/process/{identifier}/logs")
                self.handle_response_error(response)
                data = response.json()
                if log_type == "all":
                    return data.get("logs", "")
                elif log_type == "stdout":
                    return data.get("stdout", "")
                elif log_type == "stderr":
                    return data.get("stderr", "")
                raise Exception("Unsupported log type")

        return retry_on_transient_reset(logs_once)

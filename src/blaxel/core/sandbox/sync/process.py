import threading
import time
from typing import Any, Callable, Dict, Literal, Union

import httpx

from ...common.settings import settings
from ..client.models import ProcessResponse, SuccessResponse
from ..client.models.process_request import ProcessRequest
from ..types import ProcessRequestWithLog, ProcessResponseWithLog, SandboxConfiguration
from .action import SyncSandboxAction


class SyncSandboxProcess(SyncSandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    def stream_logs(
        self,
        process_name: str,
        options: Dict[str, Callable[[str], None]] | None = None,
    ) -> Dict[str, Callable[[], None]]:
        if options is None:
            options = {}
        reconnect_interval = 30
        is_running = threading.Event()
        is_running.set()
        seen_logs = set()
        current_close = {"fn": None}
        timer_lock = threading.Lock()
        reconnect_timer = {"t": None}

        def start_stream():
            nonlocal current_close
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
            if current_close["fn"]:
                current_close["fn"]()
            current_close["fn"] = self._stream_logs(process_name, wrapped_options)["close"]

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
            is_running.clear()
            with timer_lock:
                if reconnect_timer["t"]:
                    reconnect_timer["t"].cancel()
                    reconnect_timer["t"] = None
            if current_close["fn"]:
                current_close["fn"]()
                current_close["fn"] = None
            seen_logs.clear()

        return {"close": close}

    def _stream_logs(
        self,
        identifier: str,
        options: Dict[str, Callable[[str], None]] | None = None,
    ) -> Dict[str, Callable[[], None]]:
        if options is None:
            options = {}
        closed = threading.Event()

        def run():
            url = f"{self.url}/process/{identifier}/logs/stream"
            headers = {**settings.headers, **self.sandbox_config.headers}
            try:
                with httpx.Client() as client_instance:
                    with client_instance.stream("GET", url, headers=headers) as response:
                        if response.status_code != 200:
                            raise Exception(f"Failed to stream logs: {response.text}")
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
                    raise e

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

        def close():
            closed.set()

        return {"close": close}

    def exec(
        self,
        process: Union[ProcessRequest, ProcessRequestWithLog, Dict[str, Any]],
    ) -> Union[ProcessResponse, ProcessResponseWithLog]:
        on_log = None
        on_stdout = None
        on_stderr = None

        if isinstance(process, ProcessRequestWithLog):
            on_log = process.on_log
            on_stdout = process.on_stdout
            on_stderr = process.on_stderr
            process = process.to_dict()

        if isinstance(process, dict):
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
                response = client_instance.post("/process", json=process.to_dict())
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
                        lambda: stream_control["close"]() if stream_control else None,
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
        start_time = time.monotonic() * 1000
        status = "running"
        data = self.get(identifier)
        while status == "running":
            time.sleep(interval / 1000)
            try:
                data = self.get(identifier)
                status = data.status or "running"
            except Exception:
                break
            if (time.monotonic() * 1000) - start_time > max_wait:
                raise Exception("Process did not finish in time")
        return data

    def get(self, identifier: str) -> ProcessResponse:
        with self.get_client() as client_instance:
            response = client_instance.get(f"/process/{identifier}")
            self.handle_response_error(response)
            return ProcessResponse.from_dict(response.json())

    def list(self) -> list[ProcessResponse]:
        with self.get_client() as client_instance:
            response = client_instance.get("/process")
            self.handle_response_error(response)
            return [ProcessResponse.from_dict(item) for item in response.json()]

    def stop(self, identifier: str) -> SuccessResponse:
        with self.get_client() as client_instance:
            response = client_instance.delete(f"/process/{identifier}")
            self.handle_response_error(response)
            return SuccessResponse.from_dict(response.json())

    def kill(self, identifier: str) -> SuccessResponse:
        with self.get_client() as client_instance:
            response = client_instance.delete(f"/process/{identifier}/kill")
            self.handle_response_error(response)
            return SuccessResponse.from_dict(response.json())

    def logs(
        self,
        identifier: str,
        log_type: Literal["stdout", "stderr", "all"] = "all",
    ) -> str:
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

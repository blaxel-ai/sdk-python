import asyncio
from typing import Any, Callable, Dict, Literal, Union

import httpx

from ...common.settings import settings
from ..client.models import ProcessResponse, SuccessResponse
from ..client.models.process_request import ProcessRequest
from ..types import ProcessRequestWithLog, ProcessResponseWithLog, SandboxConfiguration
from .action import SandboxAction


class SandboxProcess(SandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    def stream_logs(
        self,
        process_name: str,
        options: Dict[str, Callable[[str], None]] | None = None,
    ) -> Dict[str, Callable[[], None]]:
        """Stream logs from a process with automatic reconnection and deduplication."""
        if options is None:
            options = {}

        reconnect_interval = 30  # 30 seconds in Python (TypeScript uses milliseconds)
        current_stream = None
        is_running = True
        reconnect_timer = None

        # Track seen logs to avoid duplicates
        seen_logs = set()

        def start_stream():
            nonlocal current_stream, reconnect_timer
            log_counter = [0]  # Use list to make it mutable in nested function

            # Close existing stream if any
            if current_stream:
                current_stream["close"]()

            # Create wrapper options with deduplication
            wrapped_options = {}

            if "on_log" in options:

                def deduplicated_on_log(log: str):
                    log_key = f"{log_counter[0]}:{log}"
                    log_counter[0] += 1
                    if log_key not in seen_logs:
                        seen_logs.add(log_key)
                        options["on_log"](log)

                wrapped_options["on_log"] = deduplicated_on_log

            if "on_stdout" in options:

                def deduplicated_on_stdout(stdout: str):
                    log_key = f"{log_counter[0]}:{stdout}"
                    log_counter[0] += 1
                    if log_key not in seen_logs:
                        seen_logs.add(log_key)
                        options["on_stdout"](stdout)

                wrapped_options["on_stdout"] = deduplicated_on_stdout

            if "on_stderr" in options:

                def deduplicated_on_stderr(stderr: str):
                    log_key = f"{log_counter[0]}:{stderr}"
                    log_counter[0] += 1
                    if log_key not in seen_logs:
                        seen_logs.add(log_key)
                        options["on_stderr"](stderr)

                wrapped_options["on_stderr"] = deduplicated_on_stderr

            # Start new stream with deduplication
            current_stream = self._stream_logs(process_name, wrapped_options)

            # Schedule next reconnection
            if is_running:

                def schedule_reconnect():
                    if is_running:
                        start_stream()

                reconnect_timer = asyncio.get_event_loop().call_later(
                    reconnect_interval, schedule_reconnect
                )

        # Start the initial stream
        start_stream()

        # Return control functions
        def close():
            nonlocal is_running, reconnect_timer, current_stream
            is_running = False

            # Cancel reconnect timer
            if reconnect_timer:
                reconnect_timer.cancel()
                reconnect_timer = None

            # Close current stream
            if current_stream:
                current_stream["close"]()
                current_stream = None

            # Clear seen logs
            seen_logs.clear()

        return {"close": close}

    def _stream_logs(
        self,
        identifier: str,
        options: Dict[str, Callable[[str], None]] | None = None,
    ) -> Dict[str, Callable[[], None]]:
        """Private method to stream logs from a process with callbacks for different output types."""
        if options is None:
            options = {}

        closed = False

        async def start_streaming():
            nonlocal closed

            url = f"{self.url}/process/{identifier}/logs/stream"
            headers = {**settings.headers, **self.sandbox_config.headers}

            try:
                async with httpx.AsyncClient() as client_instance:
                    async with client_instance.stream("GET", url, headers=headers) as response:
                        if response.status_code != 200:
                            raise Exception(f"Failed to stream logs: {await response.aread()}")

                        buffer = ""
                        async for chunk in response.aiter_text():
                            if closed:
                                break

                            buffer += chunk
                            lines = buffer.split("\n")
                            buffer = lines.pop()  # Keep incomplete line in buffer

                            for line in lines:
                                # Skip keepalive messages
                                if line.startswith("[keepalive]"):
                                    continue
                                if line.startswith("stdout:"):
                                    content = line[7:]  # Remove 'stdout:' prefix
                                    if options.get("on_stdout"):
                                        options["on_stdout"](content)
                                    if options.get("on_log"):
                                        options["on_log"](content)
                                elif line.startswith("stderr:"):
                                    content = line[7:]  # Remove 'stderr:' prefix
                                    if options.get("on_stderr"):
                                        options["on_stderr"](content)
                                    if options.get("on_log"):
                                        options["on_log"](content)
                                else:
                                    if options.get("on_log"):
                                        options["on_log"](line)
            except Exception as e:
                # Suppress AbortError when closing
                if not (hasattr(e, "name") and e.name == "AbortError"):
                    raise e

        # Start streaming in the background
        task = asyncio.create_task(start_streaming())

        def close():
            nonlocal closed
            closed = True
            task.cancel()

        return {"close": close}

    async def exec(
        self,
        process: Union[ProcessRequest, ProcessRequestWithLog, Dict[str, Any]],
    ) -> Union[ProcessResponse, ProcessResponseWithLog]:
        """Execute a process in the sandbox."""
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

        # Store original wait_for_completion setting
        should_wait_for_completion = process.wait_for_completion

        # When waiting for completion with streaming callbacks, use streaming endpoint
        if should_wait_for_completion and (on_log or on_stdout or on_stderr):
            return await self._exec_with_streaming(
                process, on_log=on_log, on_stdout=on_stdout, on_stderr=on_stderr
            )
        else:
            client = self.get_client()
            response = await client.post("/process", json=process.to_dict())
            try:
                content_bytes = await response.aread()
                self.handle_response_error(response)
                import json

                response_data = json.loads(content_bytes) if content_bytes else None
                result = ProcessResponse.from_dict(response_data)
            finally:
                await response.aclose()

            if on_log or on_stdout or on_stderr:
                stream_control = self._stream_logs(
                    result.pid, {"on_log": on_log, "on_stdout": on_stdout, "on_stderr": on_stderr}
                )
                return ProcessResponseWithLog(
                    result,
                    lambda: stream_control["close"]() if stream_control else None,
                )

            return result

    async def _exec_with_streaming(
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

        async with httpx.AsyncClient() as client_instance:
            async with client_instance.stream(
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
                    error_text = await response.aread()
                    raise Exception(f"Failed to execute process: {error_text}")

                content_type = response.headers.get("Content-Type", "")
                is_streaming = "application/x-ndjson" in content_type

                # Fallback: server doesn't support streaming, use legacy approach
                if not is_streaming:
                    content = await response.aread()
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

                async for chunk in response.aiter_text():
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

    async def wait(
        self, identifier: str, max_wait: int = 60000, interval: int = 1000
    ) -> ProcessResponse:
        """Wait for a process to complete."""
        start_time = asyncio.get_event_loop().time() * 1000  # Convert to milliseconds
        status = "running"
        data = await self.get(identifier)

        while status == "running":
            await asyncio.sleep(interval / 1000)  # Convert to seconds
            try:
                data = await self.get(identifier)
                status = data.status or "running"
            except:
                break

            if (asyncio.get_event_loop().time() * 1000) - start_time > max_wait:
                raise Exception("Process did not finish in time")

        return data

    async def get(self, identifier: str) -> ProcessResponse:
        import json

        client = self.get_client()
        response = await client.get(f"/process/{identifier}")
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            return ProcessResponse.from_dict(data)
        finally:
            await response.aclose()

    async def list(self) -> list[ProcessResponse]:
        import json

        client = self.get_client()
        response = await client.get("/process")
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            return [ProcessResponse.from_dict(item) for item in data]
        finally:
            await response.aclose()

    async def stop(self, identifier: str) -> SuccessResponse:
        import json

        client = self.get_client()
        response = await client.delete(f"/process/{identifier}")
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            return SuccessResponse.from_dict(data)
        finally:
            await response.aclose()

    async def kill(self, identifier: str) -> SuccessResponse:
        import json

        client = self.get_client()
        response = await client.delete(f"/process/{identifier}/kill")
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            return SuccessResponse.from_dict(data)
        finally:
            await response.aclose()

    async def logs(
        self,
        identifier: str,
        log_type: Literal["stdout", "stderr", "all"] = "all",
    ) -> str:
        import json

        client = self.get_client()
        response = await client.get(f"/process/{identifier}/logs")
        try:
            data = json.loads(await response.aread())
            self.handle_response_error(response)
            if log_type == "all":
                return data.get("logs", "")
            elif log_type == "stdout":
                return data.get("stdout", "")
            elif log_type == "stderr":
                return data.get("stderr", "")

            raise Exception("Unsupported log type")
        finally:
            await response.aclose()

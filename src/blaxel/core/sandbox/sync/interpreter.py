import json
import logging
from typing import Any, Callable, Dict, Optional, Union

import httpx

from ...client.models import Sandbox
from ..types import SandboxCreateConfiguration
from .sandbox import SyncSandboxInstance


class SyncCodeInterpreter(SyncSandboxInstance):
    logger = logging.getLogger(__name__)
    DEFAULT_IMAGE = "blaxel/jupyter-server"
    DEFAULT_PORTS = [
        {"name": "jupyter", "target": 8888, "protocol": "HTTP"},
    ]
    DEFAULT_LIFECYCLE = {
        "expirationPolicies": [{"type": "ttl-idle", "value": "30m", "action": "delete"}]
    }

    @classmethod
    def get(cls, sandbox_name: str) -> "SyncCodeInterpreter":
        sandbox = SyncSandboxInstance.get(sandbox_name)
        return cls(sandbox=sandbox.sandbox)

    @classmethod
    def create(
        cls,
        sandbox: Union[Sandbox, SandboxCreateConfiguration, Dict[str, Any], None] = None,
        safe: bool = True,
    ) -> "SyncCodeInterpreter":
        """
        Create a sandbox instance using the jupyter-server image.
        Constraints:
          - Image is forced to blaxel/jupyter-server
          - Ports are fixed to 8888 (non-configurable)
          - Lifecycle defaults to 30m
          - No ttl, volumes, expires, snapshot_enabled
        """
        payload: Dict[str, Any] = {
            "image": cls.DEFAULT_IMAGE,
            "ports": cls.DEFAULT_PORTS,
            "lifecycle": cls.DEFAULT_LIFECYCLE,
        }

        # Whitelist a minimal set of fields that can be propagated from input
        allowed_copy_keys = {"name", "envs", "memory", "region", "headers"}

        if isinstance(sandbox, dict):
            for k in allowed_copy_keys:
                if k in sandbox and sandbox[k] is not None:
                    payload[k] = sandbox[k]
        elif isinstance(sandbox, SandboxCreateConfiguration):
            if getattr(sandbox, "name", None):
                payload["name"] = sandbox.name
            if getattr(sandbox, "envs", None):
                payload["envs"] = sandbox.envs
            if getattr(sandbox, "memory", None):
                payload["memory"] = sandbox.memory
            if getattr(sandbox, "region", None):
                payload["region"] = sandbox.region
        elif isinstance(sandbox, Sandbox):
            # Extract a few basics if available
            if sandbox.metadata and getattr(sandbox.metadata, "name", None):
                payload["name"] = sandbox.metadata.name
            if sandbox.spec and sandbox.spec.runtime:
                if getattr(sandbox.spec.runtime, "envs", None):
                    payload["envs"] = sandbox.spec.runtime.envs
                if getattr(sandbox.spec.runtime, "memory", None):
                    payload["memory"] = sandbox.spec.runtime.memory
            if sandbox.spec and getattr(sandbox.spec, "region", None):
                payload["region"] = sandbox.spec.region

        base_instance = SyncSandboxInstance.create(payload, safe=safe)
        return cls(
            sandbox=base_instance.sandbox,
            force_url=base_instance.config.force_url,
            headers=base_instance.config.headers,
            params=base_instance.config.params,
        )

    # Minimal internal types to satisfy API surface
    class OutputMessage:
        def __init__(self, text: str, timestamp: float | None, is_stderr: bool):
            self.text = text
            self.timestamp = timestamp
            self.is_stderr = is_stderr

    class Result:
        def __init__(self, **kwargs: Any):
            for k, v in kwargs.items():
                setattr(self, k, v)

    class ExecutionError:
        def __init__(self, name: str, value: Any, traceback: Any):
            self.name = name
            self.value = value
            self.traceback = traceback

    class Logs:
        def __init__(self):
            self.stdout: list[str] = []
            self.stderr: list[str] = []

    class Execution:
        def __init__(self):
            self.results: list[SyncCodeInterpreter.Result] = []
            self.logs: SyncCodeInterpreter.Logs = SyncCodeInterpreter.Logs()
            self.error: SyncCodeInterpreter.ExecutionError | None = None
            self.execution_count: int | None = None

    class Context:
        def __init__(self, id: str):
            self.id = id

        @classmethod
        def from_json(cls, data: Dict[str, Any]) -> "SyncCodeInterpreter.Context":
            return cls(id=str(data.get("id") or data.get("context_id") or ""))

    @property
    def _jupyter_url(self) -> str:
        # Use the same base as other sync actions
        # Delegate to process helper for URL computation and headers
        return self.process.url

    def _parse_output(
        self,
        execution: "SyncCodeInterpreter.Execution",
        output: str,
        on_stdout: Callable[[Any], Any] | None = None,
        on_stderr: Callable[[Any], Any] | None = None,
        on_result: Callable[[Any], Any] | None = None,
        on_error: Callable[[Any], Any] | None = None,
    ) -> Any | None:
        data = json.loads(output)
        data_type = data.pop("type")

        if data_type == "result":
            result = SyncCodeInterpreter.Result(**data)
            execution.results.append(result)
            if on_result:
                return on_result(result)
        elif data_type == "stdout":
            execution.logs.stdout.append(data["text"])
            if on_stdout:
                return on_stdout(
                    SyncCodeInterpreter.OutputMessage(data["text"], data.get("timestamp"), False)
                )
        elif data_type == "stderr":
            execution.logs.stderr.append(data["text"])
            if on_stderr:
                return on_stderr(
                    SyncCodeInterpreter.OutputMessage(data["text"], data.get("timestamp"), True)
                )
        elif data_type == "error":
            execution.error = SyncCodeInterpreter.ExecutionError(
                data.get("name", ""), data.get("value"), data.get("traceback")
            )
            if on_error:
                return on_error(execution.error)
        elif data_type == "number_of_executions":
            execution.execution_count = data.get("execution_count")

        return None

    def _format_http_error(self, where: str, response: httpx.Response) -> str:
        try:
            body_text = response.text
        except Exception:
            body_text = "<unavailable>"
        # Limit very large bodies
        max_len = 4000
        if len(body_text) > max_len:
            body_text = body_text[:max_len] + "...<truncated>"
        req = getattr(response, "request", None)
        method = getattr(req, "method", "UNKNOWN") if req else "UNKNOWN"
        url = str(getattr(req, "url", "UNKNOWN")) if req else "UNKNOWN"
        reason = getattr(response, "reason_phrase", "")
        return (
            f"{where} failed\n"
            f"- method: {method}\n"
            f"- url: {url}\n"
            f"- status: {response.status_code} {reason}\n"
            f"- response-headers: {dict(response.headers)}\n"
            f"- body:\n{body_text}"
        )

    def run_code(
        self,
        code: str,
        language: str | None = None,
        context: Optional["SyncCodeInterpreter.Context"] = None,
        on_stdout: Callable[[Any], None] | None = None,
        on_stderr: Callable[[Any], None] | None = None,
        on_result: Callable[[Any], None] | None = None,
        on_error: Callable[[Any], None] | None = None,
        envs: Dict[str, str] | None = None,
        timeout: float | None = None,
        request_timeout: float | None = None,
    ) -> "SyncCodeInterpreter.Execution":
        # Defaults: treat 0 as no read timeout
        DEFAULT_TIMEOUT = 60.0
        if language and context:
            raise ValueError("You can provide context or language, but not both at the same time.")

        read_timeout = None if timeout == 0 else (timeout or DEFAULT_TIMEOUT)
        connect_timeout = request_timeout or 10.0
        write_timeout = request_timeout or 10.0
        pool_timeout = request_timeout or 10.0

        context_id = context.id if context else None

        body = {
            "code": code,
            "context_id": context_id,
            "language": language,
            "env_vars": envs,
        }

        execution = SyncCodeInterpreter.Execution()

        # Use the process client to inherit base_url and headers
        with self.process.get_client() as client:
            timeout_cfg = httpx.Timeout(
                connect=connect_timeout,
                read=read_timeout,
                write=write_timeout,
                pool=pool_timeout,
            )
            with client.stream(
                "POST",
                "/port/8888/execute",
                json=body,
                timeout=timeout_cfg,
            ) as response:
                if response.status_code >= 400:
                    details = self._format_http_error("Execution", response)
                    self.logger.debug(details)
                    raise RuntimeError(details)

                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        decoded = (
                            line.decode() if isinstance(line, bytes | bytearray) else str(line)
                        )
                    except Exception:
                        decoded = str(line)
                    try:
                        self._parse_output(
                            execution,
                            decoded,
                            on_stdout=on_stdout,
                            on_stderr=on_stderr,
                            on_result=on_result,
                            on_error=on_error,
                        )
                    except json.JSONDecodeError:
                        # Fallback: treat as stdout text-only message
                        execution.logs.stdout.append(decoded)
                        if on_stdout:
                            on_stdout(SyncCodeInterpreter.OutputMessage(decoded, None, False))

        return execution

    def create_code_context(
        self,
        cwd: str | None = None,
        language: str | None = None,
        request_timeout: float | None = None,
    ) -> "SyncCodeInterpreter.Context":
        data: Dict[str, Any] = {}
        if language:
            data["language"] = language
        if cwd:
            data["cwd"] = cwd

        with self.process.get_client() as client:
            response = client.post(
                "/port/8888/contexts",
                json=data,
                timeout=request_timeout or 10.0,
            )
            if response.status_code >= 400:
                details = self._format_http_error("Create context", response)
                self.logger.debug(details)
                raise RuntimeError(details)
            data = response.json()
            return SyncCodeInterpreter.Context.from_json(data)

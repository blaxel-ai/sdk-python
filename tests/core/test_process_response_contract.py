"""The process SDK preserves nullable response fields in sync and async calls."""

import json

import httpx
import pytest

from blaxel.core.client.models import Metadata, Sandbox, SandboxSpec
from blaxel.core.sandbox.client.client import Client
from blaxel.core.sandbox.client.models import ProcessResponse
from blaxel.core.sandbox.default.process import SandboxProcess
from blaxel.core.sandbox.sync.process import SyncSandboxProcess
from blaxel.core.sandbox.types import SandboxConfiguration

BASE_URL = "http://sandbox.test"
RUNNING_RESPONSE = {
    "command": "cat",
    "completedAt": None,
    "exitCode": 0,
    "logs": None,
    "name": "nullable-process",
    "pid": "1234",
    "startedAt": "Wed, 01 Jan 2025 12:00:00 GMT",
    "status": "running",
    "stderr": None,
    "stdout": None,
    "workingDir": "/workspace",
}
COMPLETED_RESPONSE = {
    "command": "cat",
    "completedAt": "Wed, 01 Jan 2025 12:00:01 GMT",
    "exitCode": 0,
    "logs": "hello\nerror\n",
    "name": "nullable-process",
    "pid": "1234",
    "startedAt": "Wed, 01 Jan 2025 12:00:00 GMT",
    "status": "completed",
    "stderr": "error\n",
    "stdout": "hello\n",
    "workingDir": "/workspace",
}
EMPTY_OUTPUT_RESPONSE = {
    **COMPLETED_RESPONSE,
    "logs": "",
    "stdout": "",
    "stderr": "",
}


@pytest.mark.parametrize("process_class", [SandboxProcess, SyncSandboxProcess])
@pytest.mark.parametrize(
    "response_body",
    [RUNNING_RESPONSE, COMPLETED_RESPONSE, EMPTY_OUTPUT_RESPONSE],
    ids=["null-output", "captured-output", "empty-output"],
)
async def test_exec_get_and_list_preserve_process_response(
    process_class, response_body, monkeypatch
):
    requests = []

    def respond(request):
        requests.append(request)
        if request.method == "GET" and request.url.path == "/process":
            return httpx.Response(200, json=[response_body])
        return httpx.Response(200, json=response_body)

    transport = httpx.MockTransport(respond)
    config = SandboxConfiguration(
        Sandbox(metadata=Metadata(name="nullable-process", url=BASE_URL), spec=SandboxSpec())
    )
    process = process_class(config)
    assert process.url == BASE_URL  # Control-plane URLs need no trailing slash.
    # Both HTTP paths use the mock transport, with no credentials required.
    monkeypatch.setattr(
        process,
        "get_api_client",
        lambda: Client(base_url=process.url, headers={}, httpx_args={"transport": transport}),
    )

    if process_class is SandboxProcess:
        async with httpx.AsyncClient(base_url=process.url, transport=transport) as client:
            monkeypatch.setattr(process, "get_client", lambda: client)
            executed = await process.exec({"command": "cat", "wait_for_completion": False})
            retrieved = await process.get("1234")
            listed = await process.list()
    else:
        monkeypatch.setattr(
            process,
            "get_client",
            lambda: httpx.Client(base_url=process.url, transport=transport),
        )
        executed = process.exec({"command": "cat", "wait_for_completion": False})
        retrieved = process.get("1234")
        listed = process.list()

    assert len(listed) == 1
    for result in [executed, retrieved, listed[0]]:
        assert isinstance(result, ProcessResponse)
        # Nulls stay null; empty strings stay empty. Required keys are not lost.
        assert result.to_dict() == response_body

    assert [(request.method, request.url.path) for request in requests] == [
        ("POST", "/process"),
        ("GET", "/process/1234"),
        ("GET", "/process"),
    ]
    assert json.loads(requests[0].content) == {"command": "cat", "waitForCompletion": False}


@pytest.mark.parametrize("field", ["logs", "stdout", "stderr", "completedAt"])
def test_nullable_fields_are_still_required(field):
    response_body = RUNNING_RESPONSE.copy()
    del response_body[field]
    with pytest.raises(KeyError):
        ProcessResponse.from_dict(response_body)

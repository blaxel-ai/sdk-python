import pytest

from blaxel.core.sandbox.default.filesystem import SandboxFileSystem
from blaxel.core.sandbox.sync.filesystem import SyncSandboxFileSystem


class _RecordingProcess:
    """Fake process manager that records the command it was asked to run."""

    def __init__(self):
        self.commands = []

    def _make_result(self):
        return type("_Proc", (), {"pid": "pid-1", "status": "completed", "logs": ""})()

    def exec(self, request):
        self.commands.append(request["command"])
        return self._make_result()

    def wait(self, pid, max_wait=180000, interval=100):
        return self._make_result()


class _AsyncRecordingProcess(_RecordingProcess):
    async def exec(self, request):
        self.commands.append(request["command"])
        return self._make_result()

    async def wait(self, pid, max_wait=180000, interval=100):
        return self._make_result()


# Payloads that would run an injected command if the paths were not quoted.
_INJECTION_PAYLOADS = [
    "/tmp/out; touch /tmp/pwned",
    "/tmp/$(touch /tmp/pwned)",
    "/tmp/`touch /tmp/pwned`",
    "/tmp/a && touch /tmp/pwned",
    "/tmp/a | touch /tmp/pwned",
    "/tmp/with space",
]


@pytest.mark.parametrize("payload", _INJECTION_PAYLOADS)
def test_sync_cp_quotes_paths_to_prevent_injection(payload):
    filesystem = object.__new__(SyncSandboxFileSystem)
    process = _RecordingProcess()
    filesystem.process = process

    filesystem.cp(payload, "/tmp/dst")
    filesystem.cp("/tmp/src", payload)

    for command in process.commands:
        # The injected payload must appear only inside a single-quoted literal,
        # never as bare shell syntax the shell would interpret.
        assert "touch /tmp/pwned" not in command.replace(f"'{payload}'", "")
        assert f"'{payload}'" in command


@pytest.mark.parametrize("payload", _INJECTION_PAYLOADS)
async def test_async_cp_quotes_paths_to_prevent_injection(payload):
    filesystem = object.__new__(SandboxFileSystem)
    process = _AsyncRecordingProcess()
    filesystem.process = process

    await filesystem.cp(payload, "/tmp/dst")
    await filesystem.cp("/tmp/src", payload)

    for command in process.commands:
        assert "touch /tmp/pwned" not in command.replace(f"'{payload}'", "")
        assert f"'{payload}'" in command


def test_sync_multipart_upload_aborts_when_part_thread_fails():
    filesystem = object.__new__(SyncSandboxFileSystem)
    uploaded_parts = []
    aborted_uploads = []
    completed_parts = []

    filesystem._initiate_multipart_upload = lambda path, permissions="0644": {
        "uploadId": "upload-1"
    }

    def upload_part(upload_id, part_number, data):
        uploaded_parts.append(part_number)
        if part_number == 2:
            raise RuntimeError("part 2 failed")
        return {"partNumber": part_number, "etag": f"etag-{part_number}"}

    filesystem._upload_part = upload_part
    filesystem._abort_multipart_upload = lambda upload_id: aborted_uploads.append(upload_id)
    filesystem._complete_multipart_upload = lambda upload_id, parts: completed_parts.append(parts)

    with pytest.raises(RuntimeError, match="part 2 failed"):
        filesystem._upload_with_multipart("/tmp/large.bin", b"0" * (11 * 1024 * 1024))

    assert 2 in uploaded_parts
    assert aborted_uploads == ["upload-1"]
    assert completed_parts == []

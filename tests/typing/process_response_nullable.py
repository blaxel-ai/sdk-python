"""Public-model usage checked by Pyright, independently of runtime parsing.

Run: uv tool run --from pyright==1.1.408 pyright -p tests/typing/pyrightconfig.json
"""

from blaxel.core.sandbox.client.models import ProcessResponse, ProcessResponseStatus

# Required keys may carry JSON null; the Python model must accept None.
response = ProcessResponse(
    command="cat",
    completed_at=None,
    exit_code=0,
    logs=None,
    name="running",
    pid="1234",
    started_at="Wed, 01 Jan 2025 12:00:00 GMT",
    status=ProcessResponseStatus.RUNNING,
    stderr=None,
    stdout=None,
    working_dir="/workspace",
)


def log_lines(process: ProcessResponse) -> list[str]:
    """Callers handle missing output before using string operations."""
    if process.logs is None:
        return []
    return process.logs.splitlines()


assert log_lines(response) == []

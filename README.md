# Blaxel Python SDK

[Blaxel](https://blaxel.ai) is a perpetual sandbox platform that achieves near instant latency by keeping infinite secure sandboxes on automatic standby, while co-hosting your agent logic to cut network overhead.

This repository contains Blaxel's Python SDK, which lets you create and manage sandboxes and other resources on Blaxel.

## Installation

```bash
pip install blaxel
```

## Authentication

The SDK authenticates with your Blaxel workspace using these sources (in priority order):

1. Blaxel CLI, when logged in
2. Environment variables in `.env` file (`BL_WORKSPACE`, `BL_API_KEY`)
3. System environment variables
4. Blaxel configuration file (`~/.blaxel/config.yaml`)

When developing locally, the recommended method is to just log in to your workspace with the Blaxel CLI:

```bash
bl login YOUR-WORKSPACE
```

This allows you to run Blaxel SDK functions that will automatically connect to your workspace without additional setup. When you deploy on Blaxel, this connection persists automatically.

When running Blaxel SDK from a remote server that is not Blaxel-hosted, we recommend using environment variables as described in the third option above.

## Usage

### Paginated list responses

Control plane list methods return one page at a time. The return value behaves like a list for the current page and also exposes pagination helpers:

```python
from blaxel.core import SandboxInstance

page = await SandboxInstance.list(limit=50)

for sandbox in page.data:
    print(sandbox.metadata.name)

if page.has_more:
    next_page = await page.next_page()
    print(next_page.next_cursor)
```

Image clients now use API version `2026-09-22`. `list_images` returns a page of
summaries (`data` and `meta`), and `get_image` returns one summary. Each summary
includes `spec.size`, `spec.tag_count`, `metadata.status`, and
`metadata.last_deployed_at`. Tags are fetched separately, one page at a time:

```python
from blaxel.core.client.client import client
from blaxel.core.client.api.images import list_images, list_image_tags

images = await list_images.asyncio(client=client, limit=50, sort="name:asc")
for image in images.data:
    print(image.metadata.name, image.spec.tag_count)

if images.meta.has_more:
    images = await list_images.asyncio(
        client=client, limit=50, sort="name:asc", cursor=images.meta.next_cursor
    )

tags = await list_image_tags.asyncio("sandbox", "my-image", client=client, limit=50)
for tag in tags.data:
    print(tag.name, tag.size)
```

For lazy pagination helpers, use `ImageInstance.list()` and
`ImageInstance.list_tags()` (or `list_async()` and `list_tags_async()`). They return
`PaginatedList` / `AsyncPaginatedList` with `next_page()` and `auto_paging_iter()`:

```python
from blaxel.core import ImageInstance

page = await ImageInstance.list_async(limit=50, q="python")
if page.has_more:
    next_page = await page.next_page()

tags = await ImageInstance.list_tags_async("sandbox", "my-image", limit=50)
```

These generated functions also expose `sync()` variants. Image responses no longer
include `spec.tags`; migrate callers to `list_image_tags` when upgrading.

Use `auto_paging_iter()` only when you explicitly want the SDK to walk every page for you:

```python
page = await SandboxInstance.list(limit=50)

async for sandbox in page.auto_paging_iter():
    print(sandbox.metadata.name)
```

The same shape is used by `DriveInstance.list()`, `VolumeInstance.list()`, job execution listing, and the sandbox-scoped `sandbox.schedules.list()` / `sandbox.schedules.executions()`. Sync APIs expose the same fields, with a synchronous `next_page()`:

```python
from blaxel.core import SyncDriveInstance

page = SyncDriveInstance.list(limit=50)

while True:
    for drive in page.data:
        print(drive.name)

    if not page.has_more:
        break

    page = page.next_page()
```

### Sandboxes

Sandboxes are secure, instant-launching compute environments that scale to zero after inactivity and resume in under 25ms.

> **Base image contents:** The default `blaxel/base-image:latest` is Alpine Linux with **Node.js 22** and **git** pre-installed. It does **not** include Python or other language runtimes. To use Python, either specify `blaxel/py-app:latest` as your image (Python 3.12) or install it in the base image with `apk add --no-cache python3 py3-pip`.

```python
import asyncio
from blaxel.core import SandboxInstance

async def main():

    # Create a new sandbox
    sandbox = await SandboxInstance.create_if_not_exists({
        "name": "my-sandbox",
        "image": "blaxel/base-image:latest",
        "memory": 4096,
        "region": "us-pdx-1",
        "ports": [{"target": 3000, "protocol": "HTTP"}],
        "labels": {"env": "dev", "project": "my-project"},
        "ttl": "24h"
    })

    # Get existing sandbox
    existing = await SandboxInstance.get("my-sandbox")

    # Delete sandbox (using class)
    await SandboxInstance.delete("my-sandbox")

    # Delete sandbox (using instance)
    await existing.delete()

if __name__ == "__main__":
    asyncio.run(main())
```

#### Preview URLs

Generate preview URLs to access services running in your sandbox:

```python
import asyncio
from blaxel.core import SandboxInstance

async def main():

    # Get existing sandbox
    sandbox = await SandboxInstance.get("my-sandbox")

    # Start a web server in the sandbox
    await sandbox.process.exec({
        "command": "python -m http.server 3000",
        "working_dir": "/app",
        "wait_for_ports": [3000]
    })

    # Create/reuse a private preview and an expiry-capped token
    preview = await sandbox.previews.create_if_not_exists({"port": 3000})
    token = await preview.tokens.create_if_expired()
    # preview.url is the base URL. Pass {"bl_preview_token": token.value}
    # as HTTP request query params; do not log this credential.
    # SyncSandboxInstance uses the same calls without await.

if __name__ == "__main__":
    asyncio.run(main())
```

Shorthand uses the per-sandbox name `preview-<port>` and defaults to private on
creation. Existing previews are returned as-is, even if public or on another port.
A URL prefix is optional; full-model inputs below remain supported.
`create_if_expired()` creates a 24-hour token or reuses the latest eligible token
with at least one hour remaining. An explicit expiry caps reuse (naive datetimes
mean UTC); concurrent callers may mint separate tokens. Delete a token with
`await preview.tokens.delete(token.name)`. No old tokens are automatically deleted.

Previews can also be private, with or without a custom prefix. When you create a private preview URL, a [token](https://docs.blaxel.ai/Sandboxes/Preview-url#private-preview-urls) is required to access the URL, passed as a request parameter or request header.

```python
# ...

# Create a private preview URL
private_preview = await sandbox.previews.create_if_not_exists({
    "metadata": {"name": "private-app-preview"},
    "spec": {
        "port": 3000,
        "public": False
    }
})

# Create a public preview URL with a custom prefix
custom_preview = await sandbox.previews.create_if_not_exists({
    "metadata": {"name": "custom-app-preview"},
    "spec": {
        "port": 3000,
        "prefix_url": "my-app",
        "public": True
    }
})
```

#### Process execution

Execute and manage processes in your sandbox:

```python
import asyncio
from blaxel.core import SandboxInstance

async def main():

    # Get existing sandbox
    sandbox = await SandboxInstance.get("my-sandbox")

    # Execute a command
    process = await sandbox.process.exec({
        "name": "build-process",
        "command": "npm run build",
        "working_dir": "/app",
        "wait_for_completion": True,
        "timeout": 60000  # 60 seconds
    })

    # Kill a running process
    await sandbox.process.kill("build-process")

if __name__ == "__main__":
    asyncio.run(main())
```

Restart a process if it fails, up to a maximum number of restart attempts:

```python
# ...

# Run with auto-restart on failure
process = await sandbox.process.exec({
    "name": "web-server",
    "command": "python -m http.server 3000 --bind 0.0.0.0",
    "restart_on_failure": True,
    "max_restarts": 5
})
```

#### Filesystem operations

Manage files and directories within your sandbox:

```python
import asyncio
from blaxel.core import SandboxInstance

async def main():

    # Get existing sandbox
    sandbox = await SandboxInstance.get("my-sandbox")

    # Write and read text files
    await sandbox.fs.write("/app/config.json", '{"key": "value"}')
    content = await sandbox.fs.read("/app/config.json")

    # Write and read binary files
    with open("./image.png", "rb") as f:
        binary_data = f.read()
    await sandbox.fs.write_binary("/app/image.png", binary_data)
    blob = await sandbox.fs.read_binary("/app/image.png")

    # Create directories
    await sandbox.fs.mkdir("/app/uploads")

    # List files
    listing = await sandbox.fs.ls("/app")
    subdirectories = listing.subdirectories
    files = listing.files

    # Search for text within files
    matches = await sandbox.fs.grep("pattern", "/app", case_sensitive=True, context_lines=2, max_results=5, file_pattern="*.py", exclude_dirs=["__pycache__"])

    # Find files and directories matching specified patterns
    results = await sandbox.fs.find("/app", type="file", patterns=["*.md", "*.html"], max_results=1000)

    # Watch for file changes
    def on_change(event):
        print(event.op, event.path)

    handle = sandbox.fs.watch("/app", on_change, {
        "with_content": True,
        "ignore": ["node_modules", ".git"]
    })

    # Close watcher
    handle["close"]()

if __name__ == "__main__":
    asyncio.run(main())
```

`read_tree` reads every file under a directory in one request and returns `{relative path: text}`.
`SyncSandboxInstance` has the same method, without `await`.

```python
import asyncio

from blaxel.core import SandboxInstance


async def main():
    sandbox = await SandboxInstance.get("my-sandbox")
    schemas = await sandbox.fs.read_tree(
        "/app/schemas", patterns=["*.json"], exclude_dirs=["node_modules"], max_files=20
    )
    # {"Blog.json": "...", "nested/About.json": "..."}
    print(schemas)


if __name__ == "__main__":
    asyncio.run(main())
```

`patterns` are globs on file names, `exclude_dirs` skips directories by name and `exclude_hidden`
skips dot-entries; nothing is excluded by default. If more than `max_files` (default 10000) files
match or they hold more than `max_bytes` (default 32 MiB), the request fails with a 422
`ResponseError` and nothing partial is returned. Only regular files (and symlinks to them) are
read, as UTF-8 text. It needs a sandbox image whose API supports recursive tree reads and raises
`RuntimeError` on older ones.

#### Volumes

Persist data by attaching and using volumes:

```python
import asyncio
from blaxel.core import VolumeInstance, SandboxInstance

async def main():

    # Create a volume
    volume = await VolumeInstance.create_if_not_exists({
        "name": "my-volume",
        "size": 1024,  # MB
        "region": "us-pdx-1",
        "labels": {"env": "test", "project": "12345"}
    })

    # Attach volume to sandbox
    sandbox = await SandboxInstance.create_if_not_exists({
        "name": "my-sandbox",
        "image": "blaxel/base-image:latest",
        "volumes": [
            {"name": "my-volume", "mount_path": "/data", "read_only": False}
        ]
    })

    # List the first page of volumes
    volumes = await VolumeInstance.list(limit=50)
    for listed_volume in volumes.data:
        print(listed_volume.name)

    # Delete volume (using class)
    await VolumeInstance.delete("my-volume")

    # Delete volume (using instance)
    await volume.delete()

if __name__ == "__main__":
    asyncio.run(main())
```

### Error handling

The SDK's typed API exceptions share a `BlaxelError` base, in both async and sync clients. `ResponseError`, `SandboxAPIError`, `SandboxCreationTimeoutError`, `DriveAPIError`, `VolumeAPIError`, `SnapshotAPIError`, `ApplicationAPIError`, and generated-client `UnexpectedStatus` / `APIStatusError` subclasses keep their existing messages, fields, and `except` behavior.

| Field | Meaning |
| --- | --- |
| `status` | HTTP status of the failing response, or `None` |
| `code` | Machine-readable code when the backend sends one, a newer string, or the numeric HTTP status in a generic `{ "error", "code" }` body; existing resource wrappers keep their legacy string `.code` (the wire code is in `.body`) |
| `message` | Existing exception message, also available through `str(err)` |
| `request_id` | Request ID to quote to Blaxel support (`X-Cf-Request-Id`, then `X-Amz-Cf-Id`, then `CF-Ray`), or `None` |
| `retryable` | Backend retry hint, or `None` when absent; generated status errors also retain their existing `Retry-After` behavior |
| `action` / `do_not` / `docs_url` | Backend guidance and related documentation, or `None` when absent |
| `origin` / `timestamp` | Backend error origin and ISO-8601 timestamp, or `None` when absent |
| `body` / `response` | Parsed response body (or non-JSON text) and response diagnostics, when available; `ResponseError` keeps its original `httpx.Response`, while other classes use request-free snapshots |

```python
from blaxel.core import BlaxelError, SandboxInstance, is_blaxel_error

try:
    sandbox = await SandboxInstance.create({"name": "my-sandbox", "region": "us-pdx-1"})
except BlaxelError as err:
    if is_blaxel_error(err, "QUOTA_EXCEEDED"):
        pass  # wait for capacity, then retry
    elif is_blaxel_error(err, ["SANDBOX_ALREADY_EXISTS", "SANDBOX_DELETION_IN_PROGRESS"]):
        pass  # the name is taken
    elif err.status in (401, 403):
        pass  # check the API key and workspace
    else:
        print(err.status, err.code, err.message, err.request_id)
    raise
```

`BlaxelErrorCode` is a `Literal` listing the same known backend codes as the TypeScript SDK. A newer backend can send a code this SDK does not list yet, so keep a fallback branch. The body shapes are exported as `BlaxelApiErrorBody`, `BlaxelActionErrorBody`, `BlaxelPlatformErrorBody`, and `BlaxelSandboxApiErrorBody` (`TypedDict` types). Network failures, cancellation, client-side validation, and missing credentials keep their original exception types.

`ResponseError.response` keeps the original `httpx.Response` object, exactly as before: its identity and existing request/URL access are unchanged. Its existing `data` object also retains its identity and mutation behavior.

Only newly retained responses—on the `BlaxelError` base for other classes, resource wrappers, generated status errors, and returned generated error models—use request-free snapshots. These retain status, response headers, decoded content, and reason/version metadata, but not the outgoing request, request headers, URL, redirect history, or transport objects. Request/URL access is unavailable only on these snapshots; use `err.request_id` for support diagnostics. The original HTTP response is not modified.

This is additive: low-level generated calls that return modeled `Error`, `SandboxError`, or `ErrorResponse` values still return them, rather than raising. Documented error branches returning `None` and generated schema-parse failures also retain their existing behavior. Likewise, `raise_on_unexpected_status=False` still suppresses undocumented-status exceptions. High-level methods that returned error values before this change still do so; this base class does not introduce a global raise-on-error policy.

### Batch jobs

Blaxel lets you support agentic workflows by offloading asynchronous batch processing tasks to its scalable infrastructure, where they can run in parallel. Jobs can run multiple times within a single execution and accept optional input parameters.

```python
import asyncio
from blaxel.core.jobs import bl_job
from blaxel.core.client.models import CreateJobExecutionRequest

async def main():
    # Create and run a job execution
    job = bl_job("job-name")

    execution_id = await job.acreate_execution(CreateJobExecutionRequest(
        tasks=[
            {"name": "John"},
            {"name": "Jane"},
            {"name": "Bob"}
        ]
    ))

    # Get execution status
    # Returns: "pending" | "running" | "completed" | "failed"
    status = await job.aget_execution_status(execution_id)

    # Get execution details
    execution = await job.aget_execution(execution_id)
    print(execution.status, execution.metadata)

    # Wait for completion
    try:
        result = await job.await_for_execution(
            execution_id,
            max_wait=300,  # 5 minutes (seconds)
            interval=2     # Poll every 2 seconds
        )
        print(f"Completed: {result.status}")
    except Exception as error:
        print(f"Timeout: {error}")

    # List one page of executions
    executions = await job.alist_executions(limit=20)
    for execution in executions.data:
        print(execution.metadata.id)

    # Delete an execution
    await job.acancel_execution(execution_id)

if __name__ == "__main__":
    asyncio.run(main())
```

Synchronous calls are [also available](https://docs.blaxel.ai/Jobs/Manage-job-execution-py).

### Framework integrations

Blaxel provides additional packages for framework-specific integrations and telemetry:

```bash
# With specific integrations
pip install "blaxel[telemetry]"
pip install "blaxel[crewai]"
pip install "blaxel[openai]"
pip install "blaxel[langgraph]"
pip install "blaxel[livekit]"
pip install "blaxel[llamaindex]"
pip install "blaxel[pydantic]"
pip install "blaxel[googleadk]"

# Everything
pip install "blaxel[all]"
```

#### Model use

Blaxel acts as a unified gateway for model APIs, centralizing access credentials, tracing and telemetry. You can integrate with any model API provider, or deploy your own custom model. When a model is deployed on Blaxel, a global API endpoint is also created to call it.

The SDK includes a helper function that creates a reference to a model deployed on Blaxel and returns a framework-specific model client that routes API calls through Blaxel's unified gateway.

```python
from blaxel.core import bl_model

# With OpenAI
from blaxel.openai import bl_model
model = await bl_model("gpt-5-mini")

# With LangChain
from blaxel.langgraph import bl_model
model = await bl_model("gpt-5-mini")

# With LlamaIndex
from blaxel.llamaindex import bl_model
model = await bl_model("gpt-5-mini")

# With Pydantic AI
from blaxel.pydantic import bl_model
model = await bl_model("gpt-5-mini")

# With CrewAI
from blaxel.crewai import bl_model
model = await bl_model("gpt-5-mini")

# With Google ADK
from blaxel.googleadk import bl_model
model = await bl_model("gpt-5-mini")

# With LiveKit
from blaxel.livekit import bl_model
model = await bl_model("gpt-5-mini")
```

#### MCP tool use

Blaxel lets you deploy and host Model Context Protocol (MCP) servers, accessible at a global endpoint over streamable HTTP.

The SDK includes a helper function that retrieves and returns tool definitions from a Blaxel-hosted MCP server in the format required by specific frameworks.

```python
# With OpenAI
from blaxel.openai import bl_tools
tools = await bl_tools(["sandbox/my-sandbox"])

# With Pydantic AI
from blaxel.pydantic import bl_tools
tools = await bl_tools(["sandbox/my-sandbox"])

# With LlamaIndex
from blaxel.llamaindex import bl_tools
tools = await bl_tools(["sandbox/my-sandbox"])

# With LangChain
from blaxel.langgraph import bl_tools
tools = await bl_tools(["sandbox/my-sandbox"])

# With CrewAI
from blaxel.crewai import bl_tools
tools = await bl_tools(["sandbox/my-sandbox"])

# With Google ADK
from blaxel.googleadk import bl_tools
tools = await bl_tools(["sandbox/my-sandbox"])

# With LiveKit
from blaxel.livekit import bl_tools
tools = await bl_tools(["sandbox/my-sandbox"])
```

Here is an example of retrieving tool definitions from a Blaxel sandbox's MCP server for use with the OpenAI SDK:

```python
import asyncio
from blaxel.core import SandboxInstance
from blaxel.openai import bl_tools

async def main():

    # Create a new sandbox
    sandbox = await SandboxInstance.create_if_not_exists({
        "name": "my-sandbox",
        "image": "blaxel/base-image:latest",
        "memory": 4096,
        "region": "us-pdx-1",
        "ports": [{"target": 3000, "protocol": "HTTP"}],
        "ttl": "24h"
    })

    # Get sandbox MCP tools
    tools = await bl_tools(["sandbox/my-sandbox"])

if __name__ == "__main__":
    asyncio.run(main())
```

### Telemetry

Instrumentation happens automatically when workloads run on Blaxel.

Enable automatic telemetry by importing the `blaxel.telemetry` package:

```python
import blaxel.telemetry
```

## Data collection

### Error tracking

The SDK includes error tracking for unhandled exceptions originating from the SDK itself (not your application code). It collects a sanitized error type and HTTP/error code, package-relative SDK stack frames, SDK version, commit, and workspace name. It does not collect application stack frames, raw exception messages, response bodies, or local filesystem paths.

Error tracking is off by default since v0.2.46. To explicitly disable it in older versions:

```bash
export DO_NOT_TRACK=1
```

Or add to `~/.blaxel/config.yaml`:

```yaml
tracking: false
```

Where both settings exist, the `DO_NOT_TRACK` variable takes precedence.

### Telemetry

Telemetry, delivered via OpenTelemetry, is controlled by the `BL_ENABLE_OPENTELEMETRY` environment variable.

When you deploy an agent to Blaxel, the platform automatically injects `BL_ENABLE_OPENTELEMETRY=true` into the environment.

When developing locally, this environment variable is not set and therefore defaults to `false`.

To explicitly disable telemetry, override the variable in your Blaxel deployment:

```bash
export BL_ENABLE_OPENTELEMETRY=false
```

For more information, refer to [our documentation](https://docs.blaxel.ai/Security/Data-collection-and-privacy).

## Requirements

- Python 3.9 or later

### Observing a process after a connection error

Give the command a name before starting it so you can reconnect using the existing API:

```python
await sandbox.process.exec({"name": "my-command", "command": "python worker.py", "wait_for_completion": False})
result = await sandbox.process.wait("my-command", max_wait=60_000)
```

`wait` retries temporary network/HTTP errors and returns only a terminal process
state. Set `max_wait=-1` to wait indefinitely, while still allowing async cancellation.
Authentication and missing-process errors propagate. Timeout or async
cancellation stops observation, not the command: call `wait` again to reconnect,
or use `kill`/`stop` explicitly. Never repeat `exec` to recover an existing command.
Sync waits apply the remaining deadline to HTTP timeouts and reject late results;
a server continuously sending bytes can exceed that deadline because sync HTTP
timeouts apply per network operation.


## Contributing

Contributions are welcome! Please feel free to [submit a pull request](https://github.com/blaxel-ai/sdk-python/pulls).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

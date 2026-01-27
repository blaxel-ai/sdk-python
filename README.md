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

### Sandboxes

Sandboxes are secure, instant-launching compute environments that scale to zero after inactivity and resume in under 25ms.

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

Generate public preview URLs to access services running in your sandbox:

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

    # Create a public preview URL
    preview = await sandbox.previews.create_if_not_exists({
        "metadata": {"name": "app-preview"},
        "spec": {
            "port": 3000,
            "public": True
        }
    })

    print(preview.spec.url)  # https://xyz.preview.bl.run

if __name__ == "__main__":
    asyncio.run(main())
```

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

    # List volumes
    volumes = await VolumeInstance.list()

    # Delete volume (using class)
    await VolumeInstance.delete("my-volume")

    # Delete volume (using instance)
    await volume.delete()

if __name__ == "__main__":
    asyncio.run(main())
```

### Batch jobs

Blaxel lets you support agentic workflows by offloading asynchronous batch processing tasks to its scalable infrastructure, where they can run in parallel. Jobs can run multiple times within a single execution and accept optional input parameters.

```python
from blaxel.core.jobs import bl_job
from blaxel.core.client.models import CreateJobExecutionRequest

# Create and run a job execution
job = bl_job("job-name")

execution_id = job.create_execution(CreateJobExecutionRequest(
    tasks=[
        {"name": "John"},
        {"name": "Jane"},
        {"name": "Bob"}
    ]
))

# Get execution status
# Returns: "pending" | "running" | "completed" | "failed"
status = job.get_execution_status(execution_id)

# Get execution details
execution = job.get_execution(execution_id)
print(execution.status, execution.metadata)

# Wait for completion
try:
    result = job.wait_for_execution(
        execution_id,
        max_wait=300,  # 5 minutes (seconds)
        interval=2     # Poll every 2 seconds
    )
    print(f"Completed: {result.status}")
except Exception as error:
    print(f"Timeout: {error}")

# List all executions
executions = job.list_executions()

# Delete an execution
job.cancel_execution(execution_id)
```

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

## Requirements

- Python 3.9 or later

## Contributing

Contributions are welcome! Please feel free to [submit a pull request](https://github.com/blaxel-ai/sdk-python/pulls).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
name: test-feature
description: Run integration tests for a feature. Covers the full cycle from verifying prerequisites to writing tests to executing them. Trigger on "test feature", "run integration tests", "test this change", or "/test-feature".
---

# Test a Feature

Run integration tests to validate a change end-to-end against the Blaxel platform.

## Prerequisites check

Before running any integration test, verify that credentials are set:

```bash
echo "BL_WORKSPACE=${BL_WORKSPACE:-NOT SET}"
echo "BL_API_KEY=${BL_API_KEY:-NOT SET}"
```

**If either is missing, stop and tell the user.** They need to set both:
```bash
export BL_WORKSPACE=<workspace>
export BL_API_KEY=<api-key>
```

Or have them in a `.env` file at the repo root (pytest loads it via `python-dotenv`).

Do NOT attempt to run integration tests without these variables -- they will fail with auth errors.

## Step 1: Install dependencies

Ensure the test dependencies are installed:

```bash
uv sync --group test
```

## Step 2: Write the integration test

Tests live in `tests/integration/core/sandbox/`. Follow the existing patterns:

### File structure
```python
import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name, wait_for_sandbox_deletion


class TestFeatureOperations:
    """Base class with cleanup tracking."""

    created_sandboxes: list[str] = []

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def cleanup(self, request):
        request.cls.created_sandboxes = []
        yield
        import asyncio
        await asyncio.gather(
            *[self._safe_delete(name) for name in request.cls.created_sandboxes],
            return_exceptions=True,
        )

    async def _safe_delete(self, name: str) -> None:
        try:
            await SandboxInstance.delete(name)
            await wait_for_sandbox_deletion(name)
        except Exception:
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestFeature(TestFeatureOperations):

    async def test_does_something(self):
        sandbox_name = unique_name("feature-test")
        sandbox = await SandboxInstance.create({
            "name": sandbox_name,
            "image": default_image,
            "memory": 2048,
            "labels": default_labels,
        })
        self.created_sandboxes.append(sandbox_name)

        # test code here
```

### Key conventions
- Use `unique_name("prefix")` to avoid name collisions across parallel runs.
- Always add `labels: default_labels` so cleanup can find leaked resources.
- Use `cleanup` fixture in `afterAll` style to delete sandboxes even if tests fail.
- Use `@pytest.mark.asyncio(loop_scope="class")` for async test classes.

### Available helpers (`tests/helpers.py`)
- `unique_name(prefix)` -- generate unique resource name
- `default_image` -- `"blaxel/prod-base-image:latest"`
- `default_labels` -- `{"env": "integration-test", "language": "python", "created-by": "pytest-integration"}`
- `default_region` -- `"us-was-1"` (prod) or `"eu-dub-1"` (dev, when `BL_ENV=dev`)
- `sleep(seconds)` / `async_sleep(seconds)` -- delay helpers
- `wait_for_sandbox_deletion(name)` -- poll until sandbox is fully gone

## Step 3: Run the tests

### Run a single test file
```bash
uv run pytest tests/integration/core/sandbox/<file>.py -v -s
```

### Run all core integration tests
```bash
make test-integration
```

### Run tests matching a pattern
```bash
uv run pytest tests/integration/core/sandbox/ -v -s -k "drive"
```

### Existing test files by area

| Area | Test file | What it covers |
|------|-----------|---------------|
| Sandbox CRUD | `test_sandbox_crud.py` | create, get, list, delete, createIfNotExists |
| Process | `test_process.py` | exec, logs, streamLogs, wait, kill |
| Filesystem | `test_filesystem.py` | write, read, binary, mkdir, ls, rm, search, find, watch |
| Previews | `test_previews.py` | create, list, get, delete, tokens |
| Sessions | `test_sessions.py` | create, list, delete, fromSession |
| Drives | `test_drives.py` | DriveInstance CRUD, mount, unmount, list, persistence |
| Volumes | `test_volumes.py` | VolumeInstance CRUD, attach to sandbox |
| Lifecycle | `test_lifecycle.py` | TTL, expiration policies |
| Interpreter | `test_interpreter.py` | CodeInterpreter.runCode |
| Codegen | `test_codegen.py` | fastapply, reranking |
| System | `test_system.py` | upgrade |
| Network/Proxy | `test_proxy.py`, `test_fetch.py` | port proxying, fetch |

## Step 4: Interpret results

- **All green**: the feature works end-to-end.
- **Auth errors (401)**: `BL_WORKSPACE` or `BL_API_KEY` is wrong or missing.
- **Timeout errors**: sandbox operations can be slow. Increase timeout if needed, but investigate if a test consistently takes >2 minutes.
- **404 on sandbox API calls**: the SDK client may be out of sync with the deployed sandbox-api. Check if a SDK regeneration is needed (see `/regenerate-sdk`).

## Quick reference

```bash
# Run one test file
uv run pytest tests/integration/core/sandbox/test_drives.py -v -s

# Run all core integration tests
make test-integration

# Run with keyword filter
uv run pytest tests/integration/core/sandbox/ -v -s -k "mount"
```

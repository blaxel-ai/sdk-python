# Migration Guide

## Control-Plane API Error Handling (Breaking Change)

### What changed

Control-plane API functions (under `blaxel.core.client.api`) now **raise exceptions** on error responses (4xx/5xx) instead of returning `Union[Model, Error]`. This aligns the control-plane client with the Go SDK and the existing Python domain wrappers (`SandboxAPIError`, `DriveAPIError`, `VolumeAPIError`).

### New exception hierarchy

```
BlaxelAPIError                  # base class (blaxel.core.errors)
├── ControlPlaneError           # control-plane 4xx/5xx (blaxel.core.client.errors)
├── SandboxAPIError             # sandbox domain errors
├── DriveAPIError               # drive domain errors
└── VolumeAPIError              # volume domain errors
```

All domain errors now inherit from `BlaxelAPIError`, so you can catch every API error with a single `except BlaxelAPIError`.

### Before (old pattern)

```python
from blaxel.core.client.api.agents.get_agent import sync as get_agent
from blaxel.core.client.models.error import Error

result = get_agent(agent_name="my-agent", client=client)
if isinstance(result, Error):
    print(f"Error {result.code}: {result.message}")
else:
    print(result.metadata.name)
```

### After (new pattern)

```python
from blaxel.core.client.api.agents.get_agent import sync as get_agent
from blaxel.core import ControlPlaneError

try:
    result = get_agent(agent_name="my-agent", client=client)
    print(result.metadata.name)
except ControlPlaneError as e:
    print(f"Error {e.status_code}: {e}")
    # e.error_model contains the original Error data model if needed
```

### Opting out

If you prefer the old union-return behaviour, set `raise_on_error=False` on the client:

```python
from blaxel.core.client.client import Client

client = Client(base_url="...", raise_on_error=False)
```

With this flag, the functions continue to return `Union[Model, Error]` as before.

### Catching all Blaxel errors

```python
from blaxel.core import BlaxelAPIError

try:
    # any SDK operation
    ...
except BlaxelAPIError as e:
    print(f"Blaxel API error ({e.status_code}): {e}")
```

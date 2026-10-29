"""SandboxInstance.create sends docker_config as spec.runtime.dockerConfig (a JSON string)."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from blaxel.core import SandboxInstance, SyncSandboxInstance
from blaxel.core.client.models import Metadata, Sandbox, SandboxRuntime, SandboxSpec

AUTHS = {"auths": {"ghcr.io": {"auth": "dXNlcjpwYXNz"}}}
RESPONSE = Sandbox(
    metadata=Metadata(name="sbx"),
    spec=SandboxSpec(region="us-was-1", runtime=SandboxRuntime(image="ghcr.io/org/img:tag")),
)


async def _runtime_sent(kind: str, config: dict, flat: bool = True) -> dict:
    """Run create against a stubbed control plane; return spec.runtime of the body sent."""
    if flat:
        config = {"name": "sbx", "image": "ghcr.io/org/img:tag", "region": "us-was-1", **config}
    if kind == "async":
        with patch(
            "blaxel.core.sandbox.default.sandbox.create_sandbox",
            new_callable=AsyncMock,
            return_value=RESPONSE,
        ) as create:
            await SandboxInstance.create(config)
    else:
        with patch(
            "blaxel.core.sandbox.sync.sandbox.create_sandbox",
            new_callable=MagicMock,
            return_value=RESPONSE,
        ) as create:
            SyncSandboxInstance.create(config)
    body = create.call_args.kwargs["body"]
    return (body if isinstance(body, dict) else body.to_dict())["spec"]["runtime"]


kinds = pytest.mark.parametrize("kind", ["async", "sync"])


@kinds
async def test_dict_is_serialized_to_json(kind):
    runtime = await _runtime_sent(kind, {"docker_config": AUTHS})
    assert json.loads(runtime["dockerConfig"]) == AUTHS


@kinds
async def test_string_is_sent_as_is(kind):
    raw = json.dumps(AUTHS)
    runtime = await _runtime_sent(kind, {"docker_config": raw})
    assert runtime["dockerConfig"] == raw


@kinds
async def test_absent_when_not_set(kind):
    runtime = await _runtime_sent(kind, {})
    assert "dockerConfig" not in runtime


@kinds
async def test_full_sandbox_dict_keeps_its_runtime(kind):
    raw = json.dumps(AUTHS)
    full = {
        "metadata": {"name": "private-box"},
        "spec": {"runtime": {"image": "ghcr.io/org/private:v1", "dockerConfig": raw}},
        "docker_config": raw,
    }
    runtime = await _runtime_sent(kind, full, flat=False)
    assert runtime["image"] == "ghcr.io/org/private:v1"
    assert runtime["dockerConfig"] == raw

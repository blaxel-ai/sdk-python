"""Unit tests for the warning create_if_not_exists logs when the sandbox it returns differs.

create_if_not_exists returns the sandbox already holding the name, whatever it was
created with. When that sandbox is not what the call asked for, the SDK warns once
naming the fields that differ; what the call returns does not change and nothing is
raised. Only fields the caller set are compared, and env values are never logged.
"""

import warnings
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from blaxel.core import SandboxInstance, SyncSandboxInstance
from blaxel.core.client.models import Env, Metadata, Sandbox, SandboxRuntime, SandboxSpec
from blaxel.core.sandbox.drift import RequestedSandbox, describe_drift

ASYNC_CREATE = "blaxel.core.sandbox.default.sandbox.create_sandbox"
SYNC_CREATE = "blaxel.core.sandbox.sync.sandbox.create_sandbox"


def _existing(runtime: SandboxRuntime | None = None, region: str = "us-was-1") -> Sandbox:
    # The control plane masks every env value it reads back, createIfNotExist included.
    runtime = runtime or SandboxRuntime(
        image="sandbox/app:v1",
        memory=2048,
        envs=[Env(name="KEEP", value="****"), Env(name="TOKEN", value="****", secret=True)],
    )
    return Sandbox(metadata=Metadata(name="sbx"), spec=SandboxSpec(region=region, runtime=runtime))


async def _run(kind: str, existing: Sandbox, config):
    """Run create_if_not_exists against a stubbed control plane; return (instance, drift warnings)."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        if kind == "async":
            with patch(ASYNC_CREATE, new_callable=AsyncMock, return_value=existing):
                instance = await SandboxInstance.create_if_not_exists(config)
        else:
            with patch(SYNC_CREATE, new_callable=MagicMock, return_value=existing):
                instance = SyncSandboxInstance.create_if_not_exists(config)
    return instance, [w for w in caught if "already exists" in str(w.message)]


async def _create_if_not_exists(kind: str, existing: Sandbox, config):
    instance, records = await _run(kind, existing, config)
    return instance, [str(w.message) for w in records]


kinds = pytest.mark.parametrize("kind", ["async", "sync"])


@kinds
async def test_warns_once_naming_every_field_that_differs_and_returns_the_existing_sandbox(kind):
    instance, drift = await _create_if_not_exists(
        kind,
        _existing(),
        {
            "name": "sbx",
            "image": "sandbox/app:v2",
            "memory": 8192,
            "region": "us-pdx-1",
            "envs": [{"name": "KEEP", "value": "same"}, {"name": "ADDED", "value": "never-logged"}],
        },
    )

    assert len(drift) == 1
    message = drift[0]
    assert 'sandbox "sbx" already exists' in message
    assert "image (requested sandbox/app:v2, existing sandbox/app:v1)" in message
    assert "memory (requested 8192 MB, existing 2048 MB)" in message
    assert "region (requested us-pdx-1, existing us-was-1)" in message
    assert "envs (not set on the existing sandbox: ADDED)" in message
    assert "never-logged" not in message
    assert "Delete the sandbox and create it again" in message
    # Nothing about the call changed: the existing record is handed back as is.
    assert instance.spec.runtime.image == "sandbox/app:v1"
    assert instance.spec.runtime.memory == 2048


@kinds
async def test_the_warning_points_at_the_calling_code_not_at_the_sdk(kind):
    _, [record] = await _run(
        kind, _existing(), {"name": "sbx", "image": "sandbox/app:v2", "region": "us-was-1"}
    )
    assert record.filename == __file__


@kinds
async def test_stays_quiet_when_the_sandbox_matches_the_request(kind):
    _, drift = await _create_if_not_exists(
        kind,
        _existing(),
        {
            "name": "sbx",
            "image": "sandbox/app:v1",
            "memory": 2048,
            "region": "us-was-1",
            "envs": [{"name": "KEEP", "value": "anything"}],
        },
    )
    assert drift == []


@kinds
async def test_compares_only_what_the_caller_set_never_the_sdk_defaults(kind):
    # No image and no memory: the SDK sends base-image and 4096 MB, which the caller never asked for.
    _, drift = await _create_if_not_exists(kind, _existing(), {"name": "sbx", "region": "us-was-1"})
    assert drift == []


@kinds
async def test_treats_an_untagged_image_as_latest(kind):
    runtime = SandboxRuntime(image="blaxel/base-image:latest")
    _, drift = await _create_if_not_exists(
        kind,
        _existing(runtime),
        {"name": "sbx", "image": "blaxel/base-image", "region": "us-was-1"},
    )
    assert drift == []
    runtime = SandboxRuntime(image="blaxel/base-image")
    _, drift = await _create_if_not_exists(
        kind,
        _existing(runtime),
        {"name": "sbx", "image": "blaxel/base-image:latest", "region": "us-was-1"},
    )
    assert drift == []


@kinds
async def test_reads_the_model_form_of_the_request_too(kind):
    requested = Sandbox(
        metadata=Metadata(name="sbx"),
        spec=SandboxSpec(
            region="us-was-1", runtime=SandboxRuntime(image="sandbox/app:v3", memory=2048)
        ),
    )
    _, drift = await _create_if_not_exists(kind, _existing(), requested)
    assert len(drift) == 1
    assert "image (requested sandbox/app:v3, existing sandbox/app:v1)" in drift[0]
    assert "memory" not in drift[0] and "region" not in drift[0]


@kinds
async def test_does_not_warn_about_a_field_the_existing_sandbox_did_not_report(kind):
    existing = Sandbox(metadata=Metadata(name="sbx"), spec=SandboxSpec(runtime=SandboxRuntime()))
    _, drift = await _create_if_not_exists(
        kind,
        existing,
        {
            "name": "sbx",
            "image": "sandbox/app:v2",
            "memory": 8192,
            "region": "us-pdx-1",
            "envs": [{"name": "A", "value": "1"}],
        },
    )
    assert drift == []


@kinds
async def test_never_lets_the_comparison_fail_the_create(kind):
    # envs is not a list of Env: the comparison raises inside, the create must not.
    existing = _existing(SandboxRuntime(image="sandbox/app:v1", envs="oops"))  # type: ignore[arg-type]
    instance, drift = await _create_if_not_exists(
        kind,
        existing,
        {"name": "sbx", "image": "sandbox/app:v2", "envs": [{"name": "A", "value": "1"}]},
    )
    assert instance.metadata.name == "sbx"
    assert drift == []


async def test_a_plain_create_does_not_warn():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with patch(ASYNC_CREATE, new_callable=AsyncMock, return_value=_existing()):
            await SandboxInstance.create(
                {"name": "sbx", "image": "sandbox/app:v2", "memory": 8192, "region": "us-was-1"}
            )
    assert [w for w in caught if "already exists" in str(w.message)] == []


def test_describe_drift_reports_env_names_never_env_values():
    drift = describe_drift(
        RequestedSandbox(
            envs=[Env(name="API_KEY", value="super-secret"), Env(name="MODE", value="new")]
        ),
        Sandbox(
            metadata=Metadata(name="sbx"),
            spec=SandboxSpec(runtime=SandboxRuntime(envs=[Env(name="MODE", value="old")])),
        ),
    )
    assert drift == ["envs (not set on the existing sandbox: API_KEY; different value: MODE)"]
    assert not any(secret in " ".join(drift) for secret in ("super-secret", "new", "old"))


def test_describe_drift_cannot_see_a_changed_env_value_while_the_control_plane_masks_it():
    drift = describe_drift(
        RequestedSandbox(envs=[Env(name="MODE", value="new")]),
        _existing(SandboxRuntime(envs=[Env(name="MODE", value="****")])),
    )
    assert drift == []


@pytest.mark.parametrize(
    "requested,existing,drifts",
    [
        ("app", "app:latest", False),
        ("registry.io:5000/app", "registry.io:5000/app:latest", False),
        ("app@sha256:abc", "app@sha256:abc", False),
        ("app:v2", "app:v1", True),
        ("registry.io:5000/app:v2", "registry.io:5000/app:v1", True),
    ],
)
def test_describe_drift_normalizes_image_references_before_comparing(requested, existing, drifts):
    drift = describe_drift(
        RequestedSandbox(image=requested), _existing(SandboxRuntime(image=existing))
    )
    assert bool(drift) is drifts

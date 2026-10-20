"""Regression tests for SDK-PYTHON-12D (``ValueError: Unhandled SDK exception``).

The control plane legitimately sends empty (default) or newer values for
optional, defaulted enum fields -- most notably ``generation`` on every
``*Runtime`` spec, whose docstring states that an empty value selects the
classic deployment path. The generated ``from_dict`` used a bare
``Enum(value)`` for optional enums, so an empty/unknown value raised
``ValueError`` and crashed the *entire* ``from_dict`` (e.g. deep inside
``Model.from_dict`` on the model-resolution path). Uncaught, that surfaced in
Sentry as a scrubbed ``ValueError: Unhandled SDK exception``.

Optional enums must now degrade an unparseable value to ``UNSET`` while
required enums stay strict.
"""

import pytest

from blaxel.core.client.models.agent_runtime import AgentRuntime
from blaxel.core.client.models.function_runtime import FunctionRuntime
from blaxel.core.client.models.job_runtime import JobRuntime
from blaxel.core.client.models.model import Model
from blaxel.core.client.models.model_runtime import ModelRuntime
from blaxel.core.client.models.model_runtime_generation import ModelRuntimeGeneration
from blaxel.core.client.models.sandbox_snapshot_spec import SandboxSnapshotSpec
from blaxel.core.client.types import UNSET

# All optional ``generation`` enums share the documented "empty == default" semantics.
GENERATION_MODELS = [
    ModelRuntime,
    FunctionRuntime,
    JobRuntime,
    AgentRuntime,
    SandboxSnapshotSpec,
]


@pytest.mark.parametrize("model_cls", GENERATION_MODELS)
def test_empty_generation_degrades_to_unset(model_cls):
    """The exact Sentry case: the documented empty ``generation`` value."""
    obj = model_cls.from_dict({"generation": ""})
    assert obj is not None
    assert obj.generation is UNSET


@pytest.mark.parametrize("model_cls", GENERATION_MODELS)
def test_unknown_generation_degrades_to_unset(model_cls):
    """Forward compatibility: a newer value an old SDK does not know about."""
    obj = model_cls.from_dict({"generation": "mk99"})
    assert obj is not None
    assert obj.generation is UNSET


def test_valid_generation_is_preserved():
    obj = ModelRuntime.from_dict({"generation": "mk3"})
    assert obj.generation == ModelRuntimeGeneration.MK3


@pytest.mark.parametrize("model_cls", GENERATION_MODELS)
def test_absent_generation_is_unset(model_cls):
    obj = model_cls.from_dict({"model": "whatever"})
    assert obj.generation is UNSET


def test_other_optional_enums_in_same_files_degrade():
    """Same-file optional enums patched alongside ``generation`` also degrade."""
    runtime = ModelRuntime.from_dict({"type": "", "model": "gpt-4.1"})
    assert runtime.type_ is UNSET
    # ``type_`` still backs the ``type_ or "openai"`` default used by model resolution.
    assert (runtime.type_ or "openai") == "openai"

    unknown_type = ModelRuntime.from_dict({"type": "brand-new-provider"})
    assert unknown_type.type_ is UNSET

    fn = FunctionRuntime.from_dict({"transport": ""})
    assert fn.transport is UNSET


def test_full_model_from_dict_chain_does_not_crash():
    """``Model.from_dict`` is the model-resolution / metadata-cache parse path."""
    model = Model.from_dict(
        {
            "metadata": {"name": "sandbox-openai"},
            "spec": {"runtime": {"type": "openai", "model": "gpt-4.1", "generation": ""}},
        }
    )
    assert model is not None
    assert model.spec.runtime.generation is UNSET
    assert model.spec.runtime.model == "gpt-4.1"


def test_degraded_generation_is_omitted_on_round_trip():
    """A degraded value is omitted by ``to_dict`` so the server applies its default."""
    runtime = ModelRuntime.from_dict({"model": "gpt-4.1", "generation": ""})
    assert "generation" not in runtime.to_dict()


def test_required_enum_still_raises():
    """Required enums must stay strict -- only optional enums degrade."""
    base = {
        "command": "ls",
        "completedAt": "",
        "exitCode": 0,
        "logs": "",
        "name": "p",
        "pid": "1",
        "startedAt": "",
        "status": "running",
        "stderr": "",
        "stdout": "",
        "workingDir": "/",
    }
    # Import here so a sandbox-client import failure does not affect the controlplane
    # enum tests above.
    from blaxel.core.sandbox.client.models.process_response import ProcessResponse

    ok = ProcessResponse.from_dict(dict(base))
    assert ok.status.value == "running"

    with pytest.raises(ValueError):
        ProcessResponse.from_dict({**base, "status": "not-a-real-status"})


@pytest.mark.asyncio
async def test_get_parameters_cache_path_survives_empty_generation(monkeypatch):
    """The concrete uncaught Sentry path: ``BLModel.get_parameters`` cache parse.

    ``_get_model_metadata`` parses the metadata cache via ``Model.from_dict``
    *outside* any try/except, so before the fix an empty ``generation`` here
    raised ``ValueError`` straight out to the caller's app (and Sentry).
    """
    import blaxel.core.models as models_module
    from blaxel.core.models import BLModel, bl_model

    async def fake_cache(_kind, _name):
        return {
            "metadata": {"name": "sandbox-openai"},
            "spec": {"runtime": {"type": "openai", "model": "gpt-4.1", "generation": ""}},
        }

    monkeypatch.setattr(models_module, "find_from_cache", fake_cache)
    BLModel.models.clear()
    try:
        url, model_type, model_name = await bl_model("sandbox-openai").get_parameters()
        assert model_type == "openai"
        assert model_name == "gpt-4.1"
    finally:
        BLModel.models.clear()

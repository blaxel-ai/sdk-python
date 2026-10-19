"""Regression tests for tolerant optional-enum deserialization in generated models.

The control plane sends an empty string ("") for a defaulted enum field such as
`ModelRuntime.generation` ("" means the classic deployment path). The generated
`from_dict` used to call `ModelRuntimeGeneration("")` directly, which raised
`ValueError: '' is not a valid ModelRuntimeGeneration` and blew up the entire
model parse (Sentry SDK-PYTHON-12C). An optional enum must degrade an empty or
unrecognized value to UNSET instead of raising. Required enums stay strict.
"""

import pytest

from blaxel.core.client.models.agent_runtime import AgentRuntime
from blaxel.core.client.models.function_runtime import FunctionRuntime
from blaxel.core.client.models.job_runtime import JobRuntime
from blaxel.core.client.models.model import Model
from blaxel.core.client.models.model_runtime import ModelRuntime
from blaxel.core.client.models.model_runtime_generation import ModelRuntimeGeneration
from blaxel.core.client.models.model_runtime_type import ModelRuntimeType
from blaxel.core.client.models.sandbox_snapshot_spec import SandboxSnapshotSpec
from blaxel.core.client.types import UNSET
from blaxel.core.sandbox.client.models.process_response import ProcessResponse


def test_empty_generation_degrades_to_unset():
    # The exact failure signature from Sentry: "" is a valid server value.
    runtime = ModelRuntime.from_dict({"generation": "", "type": "openai", "model": "gpt-4.1"})

    assert runtime.generation is UNSET
    assert runtime.type_ == ModelRuntimeType.OPENAI
    assert runtime.model == "gpt-4.1"


def test_unknown_generation_degrades_to_unset():
    # A newer server enum member must not crash an older client build.
    runtime = ModelRuntime.from_dict({"generation": "mk99"})

    assert runtime.generation is UNSET


def test_valid_generation_is_preserved():
    runtime = ModelRuntime.from_dict({"generation": "mk3"})

    assert runtime.generation == ModelRuntimeGeneration.MK3


def test_absent_generation_stays_unset():
    runtime = ModelRuntime.from_dict({"model": "gpt-4.1"})

    assert runtime.generation is UNSET


def test_empty_optional_type_enum_degrades_to_unset():
    runtime = ModelRuntime.from_dict({"type": ""})

    assert runtime.type_ is UNSET


def test_degraded_generation_is_omitted_on_roundtrip():
    # UNSET is not serialized, so a degraded empty value round-trips to the
    # same server default (omitted == classic deployment path).
    runtime = ModelRuntime.from_dict({"generation": "", "model": "gpt-4.1"})

    assert "generation" not in runtime.to_dict()


def test_nested_model_tolerates_empty_generation():
    # The real-world path: parsing a whole Model whose spec.runtime.generation
    # is "" (e.g. from get_model or the metadata cache).
    model = Model.from_dict(
        {
            "metadata": {"name": "gpt-4.1"},
            "spec": {"runtime": {"generation": "", "type": "openai", "model": "gpt-4.1"}},
        }
    )

    assert model.spec.runtime.generation is UNSET
    assert model.spec.runtime.model == "gpt-4.1"


@pytest.mark.parametrize(
    "model_cls", [AgentRuntime, FunctionRuntime, JobRuntime, SandboxSnapshotSpec]
)
def test_sibling_generation_fields_tolerate_empty(model_cls):
    # Every *Runtime/*Spec "generation" field shares the "empty == default"
    # semantics and the same latent crash.
    parsed = model_cls.from_dict({"generation": ""})

    assert parsed.generation is UNSET


def test_required_enum_still_raises_on_invalid_value():
    # The fix is intentionally narrow: required enums remain strict, so a
    # genuinely malformed required field is still surfaced rather than silently
    # dropped.
    body = {
        "command": "echo hi",
        "completedAt": "",
        "exitCode": 0,
        "logs": "",
        "name": "proc",
        "pid": "1",
        "startedAt": "",
        "status": "not-a-real-status",
        "stderr": "",
        "stdout": "",
        "workingDir": "/",
    }

    with pytest.raises(ValueError):
        ProcessResponse.from_dict(body)

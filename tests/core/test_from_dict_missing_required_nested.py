"""Regression tests for SDK-PYTHON-13B (and the earlier SDK-PYTHON-11V).

A generated model's ``from_dict`` is run on every API response body. A required
*nested object* (e.g. ``metadata``/``spec``) that is absent from a non-empty
response — a partial or version-skewed payload — used to pop without a default
and raise a raw ``KeyError`` deep inside the SDK. Because that ``KeyError`` has a
frame inside the installed package, the SDK's last-chance Sentry hook reports it
(scrubbed) as ``KeyError: Unhandled SDK exception``.

The fix makes required nested-object pops default to ``UNSET`` so a missing block
deserializes to ``None`` (mirroring the empty-input guard) instead of crashing.
Required scalars/enums/datetimes intentionally keep raising.
"""

import pytest

from blaxel.core.client.models.drive import Drive
from blaxel.core.client.models.job import Job
from blaxel.core.client.models.metadata import Metadata
from blaxel.core.client.models.model import Model
from blaxel.core.client.models.preview import Preview
from blaxel.core.client.models.sandbox import Sandbox
from blaxel.core.client.models.volume import Volume
from blaxel.core.sandbox.client.models.export_result import ExportResult

# Top-level resource models: each requires the nested ``metadata`` + ``spec``.
RESOURCE_MODELS = [Sandbox, Volume, Drive, Model, Job, Preview]


@pytest.mark.parametrize("model_cls", RESOURCE_MODELS)
def test_missing_required_nested_object_does_not_raise(model_cls):
    # A non-empty body missing the required nested ``metadata`` block must
    # deserialize to None rather than raising a raw KeyError.
    result = model_cls.from_dict({"spec": {}})

    assert result is not None
    assert result.metadata is None


@pytest.mark.parametrize("model_cls", RESOURCE_MODELS)
def test_empty_body_still_returns_none(model_cls):
    assert model_cls.from_dict({}) is None


def test_valid_body_still_parses_nested_metadata():
    result = Sandbox.from_dict({"metadata": {"name": "sb-1"}, "spec": {}})

    assert result is not None
    assert isinstance(result.metadata, Metadata)
    assert result.metadata.name == "sb-1"


def test_sandbox_client_export_result_missing_manifest_does_not_raise():
    # The same required-nested-object fix applies to the sandbox API client.
    result = ExportResult.from_dict({"size": 1024})

    assert result is not None
    assert result.manifest is None

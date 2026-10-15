"""Regression tests for generated-model ``from_dict`` robustness.

Covers SDK-PYTHON-11V: a 200 response whose body is a non-empty object missing a
required nested field (e.g. ``metadata``) used to raise a raw ``KeyError`` deep inside
the generated ``Sandbox.from_dict``. The SDK now tolerates a missing required nested
object instead of crashing with an opaque ``KeyError``.
"""

import pytest

from blaxel.core.client.models.preview_token import PreviewToken
from blaxel.core.client.models.sandbox import Sandbox
from blaxel.core.sandbox.client.models.process_request import ProcessRequest


def test_missing_required_metadata_does_not_raise_key_error():
    """A non-empty body missing ``metadata`` parses instead of raising KeyError."""
    sandbox = Sandbox.from_dict({"spec": {"runtime": {"image": "img"}}})

    assert sandbox is not None
    # The missing required nested object degrades to None rather than crashing.
    assert sandbox.metadata is None
    assert sandbox.spec is not None


def test_missing_required_spec_does_not_raise_key_error():
    """A non-empty body missing ``spec`` parses instead of raising KeyError."""
    sandbox = Sandbox.from_dict({"metadata": {"name": "n"}})

    assert sandbox is not None
    assert sandbox.metadata is not None
    assert sandbox.metadata.name == "n"
    assert sandbox.spec is None


def test_empty_body_still_returns_none():
    """The pre-existing empty-input guard is preserved."""
    assert Sandbox.from_dict({}) is None


def test_valid_body_is_unchanged():
    """Well-formed responses parse exactly as before (no behavior change)."""
    sandbox = Sandbox.from_dict({"metadata": {"name": "ok"}, "spec": {"runtime": {"image": "img"}}})

    assert sandbox is not None
    assert sandbox.metadata.name == "ok"
    assert sandbox.spec.runtime.image == "img"


def test_fix_applies_to_other_models_with_required_nested_objects():
    """The template-level fix is not a one-off: any required nested object degrades."""
    token = PreviewToken.from_dict({"spec": {}})

    assert token is not None
    assert token.metadata is None


def test_missing_required_scalar_still_raises():
    """Scope is intentionally narrow: required scalars keep raising (unchanged)."""
    with pytest.raises(KeyError):
        ProcessRequest.from_dict({"env": {"PORT": "3000"}})

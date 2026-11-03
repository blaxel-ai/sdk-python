"""Behavior the generated clients must keep across openapi-python-client upgrades."""

from blaxel.core.client.api.agents.get_agent import _get_kwargs as get_agent_kwargs
from blaxel.core.client.models import SandboxRuntime
from blaxel.core.sandbox.client.models.archive_export_state import ArchiveExportState


def test_optional_list_missing_or_null_reads_as_empty_list():
    # The API sends "envs": null; callers iterate the list directly.
    assert SandboxRuntime.from_dict({"envs": None, "image": "x"}).envs == []
    assert SandboxRuntime.from_dict({"image": "x"}).envs == []


def test_enum_keeps_value_derived_member_names():
    # 0.26+ names members from x-enum-varnames; the old names stay as aliases.
    assert ArchiveExportState.FAILED is ArchiveExportState.EXPORT_FAILED
    assert ArchiveExportState("FAILED") is ArchiveExportState.EXPORT_FAILED


def test_path_params_are_url_encoded():
    assert get_agent_kwargs("a/../b")["url"] == "/agents/a%2F..%2Fb"

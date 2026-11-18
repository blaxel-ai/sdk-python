"""Regression tests for the required dual-key ``from_dict`` fallback.

A generated model reads a field that has both a camelCase wire name and a
snake_case python name with::

    d.pop("wireName") if "wireName" in d else d.pop("snake_name")

When the server omits BOTH keys (e.g. an ``omitempty`` field), the ``else``
branch raised a raw ``KeyError`` on the snake_case name deep inside the SDK —
e.g. ``KeyError: 'egress_gateway_name'`` out of ``SandboxNetwork.from_dict``.
That crashed the caller for the common case of a response that simply did not
carry the optional field.

A required field whose construct can accept UNSET (a scalar read as-is, or a
nested model whose ``from_dict`` returns ``None`` for UNSET) now degrades to
UNSET instead of raising. Enums and other constructs that cannot accept UNSET
intentionally keep raising.
"""

import pytest

from blaxel.core.client.models.job_volume import JobVolume
from blaxel.core.client.models.sandbox_fork_request import SandboxForkRequest
from blaxel.core.client.models.sandbox_snapshot import SandboxSnapshot
from blaxel.core.client.models.share_custom_domain_body import ShareCustomDomainBody
from blaxel.core.client.types import UNSET as CP_UNSET
from blaxel.core.sandbox.client.models.find_match import FindMatch
from blaxel.core.sandbox.client.models.health_response import HealthResponse
from blaxel.core.sandbox.client.models.process_response import ProcessResponse
from blaxel.core.sandbox.client.types import UNSET as SB_UNSET


def test_missing_required_scalar_degrades_to_unset_controlplane():
    # createdAt omitted (server omitempty) must NOT raise KeyError('created_at').
    snap = SandboxSnapshot.from_dict(
        {"id": "x", "name": "n", "status": "ready", "workspace": "ws"}
    )
    assert snap is not None
    assert snap.created_at is CP_UNSET


def test_missing_required_scalars_degrade_to_unset_sandbox():
    # exitCode / completedAt / startedAt / workingDir all omitted.
    proc = ProcessResponse.from_dict(
        {
            "command": "ls",
            "logs": "",
            "name": "p",
            "pid": 1,
            "status": "completed",
            "stderr": "",
            "stdout": "",
        }
    )
    assert proc is not None
    assert proc.exit_code is SB_UNSET
    assert proc.completed_at is SB_UNSET
    assert proc.started_at is SB_UNSET
    assert proc.working_dir is SB_UNSET


def test_missing_required_scalar_in_request_body_degrades_to_unset():
    # Mirrors the reported egress_gateway_name signature: a request/response
    # model with a required dual-key scalar, body missing both keys.
    body = ShareCustomDomainBody.from_dict({})
    # Empty dict short-circuits to None via the `if not src_dict` guard...
    assert body is None
    # ...but a non-empty body missing the field must degrade, not KeyError.
    body = ShareCustomDomainBody.from_dict({"other": "value"})
    assert body is not None
    assert body.target_workspace is CP_UNSET


def test_missing_required_nested_model_degrades_to_none():
    # lastUpgrade (a nested model) omitted -> UpgradeStatus.from_dict(UNSET) -> None.
    health = HealthResponse.from_dict(
        {
            "arch": "amd64",
            "os": "linux",
            "status": "ok",
            "uptime": "1s",
            "version": "1.0",
        }
    )
    assert health is not None
    assert health.last_upgrade is None
    # sibling required scalars also degrade instead of raising.
    assert health.build_time is SB_UNSET
    assert health.git_commit is SB_UNSET


def test_camelcase_wire_name_still_parsed():
    snap = SandboxSnapshot.from_dict(
        {
            "id": "x",
            "name": "n",
            "status": "ready",
            "workspace": "ws",
            "createdAt": "2024-01-01T00:00:00Z",
        }
    )
    assert snap.created_at == "2024-01-01T00:00:00Z"


def test_snake_case_fallback_key_still_parsed():
    # The Blaxel dual-key support (accept snake_case input) is preserved.
    snap = SandboxSnapshot.from_dict(
        {
            "id": "x",
            "name": "n",
            "status": "ready",
            "workspace": "ws",
            "created_at": "2024-02-02T00:00:00Z",
        }
    )
    assert snap.created_at == "2024-02-02T00:00:00Z"


def test_bare_scalar_type_field_degrades_to_unset():
    # FindMatch.type is a plain string dual-key field (NOT an enum).
    match = FindMatch.from_dict({"path": "/a"})
    assert match is not None
    assert match.type_ is SB_UNSET


def test_dual_key_scalars_in_fork_request_degrade():
    fork = SandboxForkRequest.from_dict({"foo": "bar"})
    assert fork is not None
    assert fork.target_name is CP_UNSET
    assert fork.target_type is CP_UNSET


def test_enum_required_field_still_raises_when_missing():
    # type_ is wrapped in JobVolumeType(...): UNSET cannot construct an enum,
    # so this required field intentionally keeps raising rather than silently
    # degrading to an invalid enum value.
    with pytest.raises(KeyError):
        JobVolume.from_dict({"mountPath": "/m", "name": "n", "sizeMb": 1})


def test_valid_enum_body_still_parses():
    vol = JobVolume.from_dict(
        {"mountPath": "/m", "name": "n", "sizeMb": 1, "type": "ephemeral"}
    )
    assert vol is not None
    assert vol.mount_path == "/m"
    assert vol.size_mb == 1

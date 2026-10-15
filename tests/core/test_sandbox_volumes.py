"""Tests for sandbox volume normalization, including ephemeral volumes."""

import pytest

from blaxel.core.client.models import VolumeAttachmentType
from blaxel.core.client.types import UNSET
from blaxel.core.sandbox import SandboxCreateConfiguration, VolumeBinding


def _normalize(volumes):
    return SandboxCreateConfiguration(volumes=volumes)._normalize_volumes()


def test_persistent_dict_without_type_is_backward_compatible():
    result = _normalize([{"name": "data", "mount_path": "/data"}])
    assert len(result) == 1
    assert result[0].name == "data"
    assert result[0].mount_path == "/data"
    # No type means persistent: the generated field stays unset so the payload is unchanged.
    assert result[0].type_ is UNSET
    assert result[0].size_mb is UNSET


def test_explicit_persistent_type_dict():
    result = _normalize([{"name": "data", "mount_path": "/data", "type": "persistent"}])
    assert result[0].type_ == VolumeAttachmentType.PERSISTENT
    assert result[0].size_mb is UNSET


def test_ephemeral_dict_sets_type_and_size():
    result = _normalize(
        [{"name": "scratch", "mount_path": "/scratch", "type": "ephemeral", "size_mb": 1024}]
    )
    assert result[0].type_ == VolumeAttachmentType.EPHEMERAL
    assert result[0].size_mb == 1024


def test_ephemeral_volume_binding_sets_type_and_size():
    result = _normalize(
        [VolumeBinding(name="scratch", mount_path="/scratch", type="ephemeral", size_mb=512)]
    )
    assert result[0].type_ == VolumeAttachmentType.EPHEMERAL
    assert result[0].size_mb == 512


def test_ephemeral_requires_size():
    with pytest.raises(ValueError, match="positive 'size_mb'"):
        _normalize([{"name": "scratch", "mount_path": "/scratch", "type": "ephemeral"}])


@pytest.mark.parametrize("bad_size", [0, -1, True])
def test_ephemeral_rejects_non_positive_size(bad_size):
    with pytest.raises(ValueError, match="positive 'size_mb'"):
        _normalize(
            [
                {
                    "name": "scratch",
                    "mount_path": "/scratch",
                    "type": "ephemeral",
                    "size_mb": bad_size,
                }
            ]
        )

"""Unit tests for ApplicationInstance config → spec conversion and update merge.

These cover the wrapper logic that turns a simplified
``ApplicationCreateConfiguration`` (or a full ``Application`` model) into an
``ApplicationSpec``, and the merge that must preserve existing spec-level
compute fields on update (image / memory / port / envs / urls / proxy / region)
instead of silently dropping them.
"""

from blaxel.core.application.application import (
    ApplicationCreateConfiguration,
    _merge_application_spec,
)
from blaxel.core.client.models import ApplicationSpec, Env
from blaxel.core.client.types import UNSET


def test_to_spec_sets_only_provided_compute_fields():
    cfg = ApplicationCreateConfiguration(
        name="my-app",
        image="reg/img:1",
        memory=2048,
        port=3000,
        envs=[Env(name="NODE_ENV", value="production")],
    )
    spec = cfg.to_spec()
    assert spec.image == "reg/img:1"
    assert spec.memory == 2048
    assert spec.port == 3000
    assert [(e.name, e.value) for e in spec.envs] == [("NODE_ENV", "production")]
    assert spec.enabled is True


def test_to_spec_leaves_unset_compute_fields_unset():
    spec = ApplicationCreateConfiguration(name="my-app", region="us-pdx-1").to_spec()
    assert spec.image is UNSET
    assert spec.memory is UNSET
    assert spec.port is UNSET
    assert spec.envs is UNSET


def test_to_update_spec_omits_defaults():
    spec = ApplicationCreateConfiguration(image="reg/img:2").to_update_spec()
    assert spec.image == "reg/img:2"
    # enabled/region must not be forced when the caller did not provide them
    assert spec.region is UNSET
    assert spec.memory is UNSET


def test_merge_preserves_current_compute_when_not_overridden():
    current = ApplicationSpec(
        region="us-pdx-1",
        image="reg/img:1",
        memory=4096,
        port=8080,
        envs=[Env(name="K", value="v")],
        proxy=True,
        enabled=True,
    )
    new = ApplicationCreateConfiguration(image="reg/img:2").to_update_spec()
    merged = _merge_application_spec(new, current, enabled=current.enabled, proxy=current.proxy)
    assert merged.image == "reg/img:2"  # overridden
    assert merged.memory == 4096  # preserved
    assert merged.port == 8080  # preserved
    assert merged.region == "us-pdx-1"  # preserved
    assert merged.proxy is True  # preserved
    assert [(e.name, e.value) for e in merged.envs] == [("K", "v")]  # preserved


def test_merge_overrides_when_new_value_provided():
    current = ApplicationSpec(image="reg/img:1", memory=2048)
    new = ApplicationCreateConfiguration(memory=8192).to_update_spec()
    merged = _merge_application_spec(new, current, enabled=True, proxy=None)
    assert merged.memory == 8192
    assert merged.image == "reg/img:1"


def test_from_dict_converts_raw_env_dicts_to_env_and_serializes():
    cfg = ApplicationCreateConfiguration.from_dict(
        {
            "name": "my-app",
            "image": "reg/img:1",
            "envs": [
                {"name": "NODE_ENV", "value": "production"},
                {"name": "API_KEY", "value": "secret", "secret": True},
            ],
        }
    )
    assert all(isinstance(e, Env) for e in cfg.envs)
    # to_dict() must not raise: raw dicts would fail because they lack .to_dict()
    spec_dict = cfg.to_spec().to_dict()
    assert spec_dict["envs"] == [
        {"name": "NODE_ENV", "value": "production"},
        {"name": "API_KEY", "value": "secret", "secret": True},
    ]


def test_merge_respects_explicit_disabled():
    current = ApplicationSpec(image="reg/img:1", enabled=True)
    new = ApplicationCreateConfiguration(enabled=False).to_update_spec()
    merged = _merge_application_spec(new, current, enabled=False, proxy=None)
    assert merged.enabled is False
    assert merged.image == "reg/img:1"

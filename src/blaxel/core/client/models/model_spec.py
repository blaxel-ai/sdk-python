from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flavor import Flavor
    from ..models.model_runtime import ModelRuntime


T = TypeVar("T", bound="ModelSpec")


@_attrs_define
class ModelSpec:
    """Configuration for a model gateway endpoint including provider type, credentials, and access policies

    Attributes:
        enabled (bool | Unset): When false, the model endpoint is disabled and will not accept inference requests
            Default: True. Example: True.
        flavors (list[Flavor] | Unset): Types of hardware available for deployments
        integration_connections (list[str] | Unset):
        policies (list[str] | Unset):
        runtime (ModelRuntime | Unset): Configuration identifying which external LLM provider and model this gateway
            endpoint proxies to
        sandbox (bool | Unset): When true, uses sandbox/test credentials from the integration connection Example: False.
    """

    enabled: bool | Unset = True
    flavors: list[Flavor] | Unset = UNSET
    integration_connections: list[str] | Unset = UNSET
    policies: list[str] | Unset = UNSET
    runtime: ModelRuntime | Unset = UNSET
    sandbox: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        flavors: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.flavors, Unset):
            flavors = []
            for componentsschemas_flavors_item_data in self.flavors:
                if type(componentsschemas_flavors_item_data) is dict:
                    componentsschemas_flavors_item = componentsschemas_flavors_item_data
                else:
                    componentsschemas_flavors_item = componentsschemas_flavors_item_data.to_dict()
                flavors.append(componentsschemas_flavors_item)

        integration_connections: list[str] | Unset = UNSET
        if not isinstance(self.integration_connections, Unset):
            integration_connections = self.integration_connections

        policies: list[str] | Unset = UNSET
        if not isinstance(self.policies, Unset):
            policies = self.policies

        runtime: dict[str, Any] | Unset = UNSET
        if (
            self.runtime
            and not isinstance(self.runtime, Unset)
            and not isinstance(self.runtime, dict)
        ):
            runtime = self.runtime.to_dict()
        elif self.runtime and isinstance(self.runtime, dict):
            runtime = self.runtime

        sandbox = self.sandbox

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if flavors is not UNSET:
            field_dict["flavors"] = flavors
        if integration_connections is not UNSET:
            field_dict["integrationConnections"] = integration_connections
        if policies is not UNSET:
            field_dict["policies"] = policies
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if sandbox is not UNSET:
            field_dict["sandbox"] = sandbox

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.flavor import Flavor  # noqa: PLC0415
        from ..models.model_runtime import ModelRuntime  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        flavors = []
        _flavors = d.pop("flavors", UNSET)
        for componentsschemas_flavors_item_data in _flavors or []:
            componentsschemas_flavors_item = Flavor.from_dict(componentsschemas_flavors_item_data)

            flavors.append(componentsschemas_flavors_item)

        integration_connections = cast(
            list[str], d.pop("integrationConnections", d.pop("integration_connections", UNSET))
        )

        policies = cast(list[str], d.pop("policies", UNSET))

        _runtime = d.pop("runtime", UNSET)
        runtime: ModelRuntime | Unset
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = ModelRuntime.from_dict(_runtime)

        sandbox = d.pop("sandbox", UNSET)

        model_spec = cls(
            enabled=enabled,
            flavors=flavors,
            integration_connections=integration_connections,
            policies=policies,
            runtime=runtime,
            sandbox=sandbox,
        )

        model_spec.additional_properties = d
        return model_spec

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

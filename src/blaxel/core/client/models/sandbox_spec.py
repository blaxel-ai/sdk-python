from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_lifecycle import SandboxLifecycle
    from ..models.sandbox_network import SandboxNetwork
    from ..models.sandbox_runtime import SandboxRuntime
    from ..models.volume_attachment import VolumeAttachment


T = TypeVar("T", bound="SandboxSpec")


@_attrs_define
class SandboxSpec:
    """Configuration for a sandbox including its image, memory, ports, region, and lifecycle policies

    Attributes:
        enabled (bool | Unset): When false, the sandbox is disabled and will not accept connections Default: True.
            Example: True.
        lifecycle (SandboxLifecycle | Unset): Lifecycle configuration controlling automatic sandbox deletion based on
            idle time, max age, or specific dates
        network (SandboxNetwork | Unset): Network configuration for a sandbox including subnet, firewall rulesets,
            domain filtering, egress IP binding, and proxy settings
        region (str | Unset): Region where the sandbox should be created (e.g. us-pdx-1, eu-lon-1). If not specified,
            defaults to the region closest to the user. Example: us-pdx-1.
        runtime (SandboxRuntime | Unset): Runtime configuration defining how the sandbox VM is provisioned and its
            resource limits
        volumes (list[VolumeAttachment] | Unset):
        vpc (str | Unset): VPC name for the sandbox. Defaults to "default" when absent. Example: default.
    """

    enabled: bool | Unset = True
    lifecycle: SandboxLifecycle | Unset = UNSET
    network: SandboxNetwork | Unset = UNSET
    region: str | Unset = UNSET
    runtime: SandboxRuntime | Unset = UNSET
    volumes: list[VolumeAttachment] | Unset = UNSET
    vpc: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        lifecycle: dict[str, Any] | Unset = UNSET
        if (
            self.lifecycle
            and not isinstance(self.lifecycle, Unset)
            and not isinstance(self.lifecycle, dict)
        ):
            lifecycle = self.lifecycle.to_dict()
        elif self.lifecycle and isinstance(self.lifecycle, dict):
            lifecycle = self.lifecycle

        network: dict[str, Any] | Unset = UNSET
        if (
            self.network
            and not isinstance(self.network, Unset)
            and not isinstance(self.network, dict)
        ):
            network = self.network.to_dict()
        elif self.network and isinstance(self.network, dict):
            network = self.network

        region = self.region

        runtime: dict[str, Any] | Unset = UNSET
        if (
            self.runtime
            and not isinstance(self.runtime, Unset)
            and not isinstance(self.runtime, dict)
        ):
            runtime = self.runtime.to_dict()
        elif self.runtime and isinstance(self.runtime, dict):
            runtime = self.runtime

        volumes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.volumes, Unset):
            volumes = []
            for componentsschemas_volume_attachments_item_data in self.volumes:
                if type(componentsschemas_volume_attachments_item_data) is dict:
                    componentsschemas_volume_attachments_item = (
                        componentsschemas_volume_attachments_item_data
                    )
                else:
                    componentsschemas_volume_attachments_item = (
                        componentsschemas_volume_attachments_item_data.to_dict()
                    )
                volumes.append(componentsschemas_volume_attachments_item)

        vpc = self.vpc

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if lifecycle is not UNSET:
            field_dict["lifecycle"] = lifecycle
        if network is not UNSET:
            field_dict["network"] = network
        if region is not UNSET:
            field_dict["region"] = region
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if volumes is not UNSET:
            field_dict["volumes"] = volumes
        if vpc is not UNSET:
            field_dict["vpc"] = vpc

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.sandbox_lifecycle import SandboxLifecycle  # noqa: PLC0415
        from ..models.sandbox_network import SandboxNetwork  # noqa: PLC0415
        from ..models.sandbox_runtime import SandboxRuntime  # noqa: PLC0415
        from ..models.volume_attachment import VolumeAttachment  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        _lifecycle = d.pop("lifecycle", UNSET)
        lifecycle: SandboxLifecycle | Unset
        if isinstance(_lifecycle, Unset):
            lifecycle = UNSET
        else:
            lifecycle = SandboxLifecycle.from_dict(_lifecycle)

        _network = d.pop("network", UNSET)
        network: SandboxNetwork | Unset
        if isinstance(_network, Unset):
            network = UNSET
        else:
            network = SandboxNetwork.from_dict(_network)

        region = d.pop("region", UNSET)

        _runtime = d.pop("runtime", UNSET)
        runtime: SandboxRuntime | Unset
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = SandboxRuntime.from_dict(_runtime)

        volumes = []
        _volumes = d.pop("volumes", UNSET)
        for componentsschemas_volume_attachments_item_data in _volumes or []:
            componentsschemas_volume_attachments_item = VolumeAttachment.from_dict(
                componentsschemas_volume_attachments_item_data
            )

            volumes.append(componentsschemas_volume_attachments_item)

        vpc = d.pop("vpc", UNSET)

        sandbox_spec = cls(
            enabled=enabled,
            lifecycle=lifecycle,
            network=network,
            region=region,
            runtime=runtime,
            volumes=volumes,
            vpc=vpc,
        )

        sandbox_spec.additional_properties = d
        return sandbox_spec

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

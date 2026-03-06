from typing import TYPE_CHECKING, Any, TypeVar, Union

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
        enabled (Union[Unset, bool]): When false, the sandbox is disabled and will not accept connections Default: True.
            Example: True.
        lifecycle (Union[Unset, SandboxLifecycle]): Lifecycle configuration controlling automatic sandbox deletion based
            on idle time, max age, or specific dates
        network (Union[Unset, SandboxNetwork]): Network configuration for a sandbox including egress IP binding. All
            three fields (vpcName, egressGatewayName, egressIpName) must be specified together to assign a dedicated IP.
        region (Union[Unset, str]): Region where the sandbox should be created (e.g. us-pdx-1, eu-lon-1). If not
            specified, defaults to the region closest to the user. Example: us-pdx-1.
        runtime (Union[Unset, SandboxRuntime]): Runtime configuration defining how the sandbox VM is provisioned and its
            resource limits
        volumes (Union[Unset, list['VolumeAttachment']]):
    """

    enabled: Union[Unset, bool] = True
    lifecycle: Union[Unset, "SandboxLifecycle"] = UNSET
    network: Union[Unset, "SandboxNetwork"] = UNSET
    region: Union[Unset, str] = UNSET
    runtime: Union[Unset, "SandboxRuntime"] = UNSET
    volumes: Union[Unset, list["VolumeAttachment"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        lifecycle: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.lifecycle
            and not isinstance(self.lifecycle, Unset)
            and not isinstance(self.lifecycle, dict)
        ):
            lifecycle = self.lifecycle.to_dict()
        elif self.lifecycle and isinstance(self.lifecycle, dict):
            lifecycle = self.lifecycle

        network: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.network
            and not isinstance(self.network, Unset)
            and not isinstance(self.network, dict)
        ):
            network = self.network.to_dict()
        elif self.network and isinstance(self.network, dict):
            network = self.network

        region = self.region

        runtime: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.runtime
            and not isinstance(self.runtime, Unset)
            and not isinstance(self.runtime, dict)
        ):
            runtime = self.runtime.to_dict()
        elif self.runtime and isinstance(self.runtime, dict):
            runtime = self.runtime

        volumes: Union[Unset, list[dict[str, Any]]] = UNSET
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.sandbox_lifecycle import SandboxLifecycle
        from ..models.sandbox_network import SandboxNetwork
        from ..models.sandbox_runtime import SandboxRuntime
        from ..models.volume_attachment import VolumeAttachment

        if not src_dict:
            return None
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        _lifecycle = d.pop("lifecycle", UNSET)
        lifecycle: Union[Unset, SandboxLifecycle]
        if isinstance(_lifecycle, Unset):
            lifecycle = UNSET
        else:
            lifecycle = SandboxLifecycle.from_dict(_lifecycle)

        _network = d.pop("network", UNSET)
        network: Union[Unset, SandboxNetwork]
        if isinstance(_network, Unset):
            network = UNSET
        else:
            network = SandboxNetwork.from_dict(_network)

        region = d.pop("region", UNSET)

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, SandboxRuntime]
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

        sandbox_spec = cls(
            enabled=enabled,
            lifecycle=lifecycle,
            network=network,
            region=region,
            runtime=runtime,
            volumes=volumes,
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

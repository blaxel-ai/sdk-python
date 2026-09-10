from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_snapshot_spec_generation import SandboxSnapshotSpecGeneration
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.port import Port
    from ..models.volume_attachment import VolumeAttachment


T = TypeVar("T", bound="SandboxSnapshotSpec")


@_attrs_define
class SandboxSnapshotSpec:
    """The configuration a snapshot carries, so a sandbox or an application can be created from it once its source object
    is gone.

        Attributes:
            generation (Union[Unset, SandboxSnapshotSpecGeneration]): Infrastructure generation the snapshot was captured
                on. A snapshot only restores on the generation it came from.
            image (Union[Unset, str]): Image the source object ran
            memory (Union[Unset, int]): Memory in MB the source object ran with
            ports (Union[Unset, list['Port']]): Set of ports for a resource
            region (Union[Unset, str]): Region holding the snapshot. Restores and forks land in it.
            volumes (Union[Unset, list['VolumeAttachment']]):
    """

    generation: Union[Unset, SandboxSnapshotSpecGeneration] = UNSET
    image: Union[Unset, str] = UNSET
    memory: Union[Unset, int] = UNSET
    ports: Union[Unset, list["Port"]] = UNSET
    region: Union[Unset, str] = UNSET
    volumes: Union[Unset, list["VolumeAttachment"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        generation: Union[Unset, str] = UNSET
        if not isinstance(self.generation, Unset):
            generation = self.generation.value

        image = self.image

        memory = self.memory

        ports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = []
            for componentsschemas_ports_item_data in self.ports:
                if type(componentsschemas_ports_item_data) is dict:
                    componentsschemas_ports_item = componentsschemas_ports_item_data
                else:
                    componentsschemas_ports_item = componentsschemas_ports_item_data.to_dict()
                ports.append(componentsschemas_ports_item)

        region = self.region

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
        if generation is not UNSET:
            field_dict["generation"] = generation
        if image is not UNSET:
            field_dict["image"] = image
        if memory is not UNSET:
            field_dict["memory"] = memory
        if ports is not UNSET:
            field_dict["ports"] = ports
        if region is not UNSET:
            field_dict["region"] = region
        if volumes is not UNSET:
            field_dict["volumes"] = volumes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.port import Port
        from ..models.volume_attachment import VolumeAttachment

        if not src_dict:
            return None
        d = src_dict.copy()
        _generation = d.pop("generation", UNSET)
        generation: Union[Unset, SandboxSnapshotSpecGeneration]
        if isinstance(_generation, Unset):
            generation = UNSET
        else:
            generation = SandboxSnapshotSpecGeneration(_generation)

        image = d.pop("image", UNSET)

        memory = d.pop("memory", UNSET)

        ports = []
        _ports = d.pop("ports", UNSET)
        for componentsschemas_ports_item_data in _ports or []:
            componentsschemas_ports_item = Port.from_dict(componentsschemas_ports_item_data)

            ports.append(componentsschemas_ports_item)

        region = d.pop("region", UNSET)

        volumes = []
        _volumes = d.pop("volumes", UNSET)
        for componentsschemas_volume_attachments_item_data in _volumes or []:
            componentsschemas_volume_attachments_item = VolumeAttachment.from_dict(
                componentsschemas_volume_attachments_item_data
            )

            volumes.append(componentsschemas_volume_attachments_item)

        sandbox_snapshot_spec = cls(
            generation=generation,
            image=image,
            memory=memory,
            ports=ports,
            region=region,
            volumes=volumes,
        )

        sandbox_snapshot_spec.additional_properties = d
        return sandbox_snapshot_spec

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

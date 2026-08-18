from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.volume_attachment_type import VolumeAttachmentType
from ..types import UNSET, Unset

T = TypeVar("T", bound="VolumeAttachment")


@_attrs_define
class VolumeAttachment:
    """Configuration for attaching a volume to a sandbox at a specific filesystem path. Defaults to a persistent volume;
    set type to "ephemeral" for disk-backed scratch space created with the sandbox and destroyed when it stops.

        Attributes:
            mount_path (Union[Unset, str]): Absolute filesystem path where the volume will be mounted inside the sandbox
                Example: /mnt/data.
            name (Union[Unset, str]): For persistent volumes, the name of the volume resource to attach (must exist in the
                same workspace and region). For ephemeral volumes, an identifier used to reference the volume internally.
                Example: my-volume.
            read_only (Union[Unset, bool]): If true, the volume is mounted read-only and cannot be modified by the sandbox
            size_mb (Union[Unset, int]): Storage capacity in megabytes. Required for ephemeral volumes, ignored for
                persistent volumes. Example: 102400.
            type_ (Union[Unset, VolumeAttachmentType]): Type of volume. Defaults to "persistent" (an existing volume
                resource). Use "ephemeral" for temporary disk-backed storage created with the sandbox. Example: persistent.
    """

    mount_path: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    read_only: Union[Unset, bool] = UNSET
    size_mb: Union[Unset, int] = UNSET
    type_: Union[Unset, VolumeAttachmentType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mount_path = self.mount_path

        name = self.name

        read_only = self.read_only

        size_mb = self.size_mb

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mount_path is not UNSET:
            field_dict["mountPath"] = mount_path
        if name is not UNSET:
            field_dict["name"] = name
        if read_only is not UNSET:
            field_dict["readOnly"] = read_only
        if size_mb is not UNSET:
            field_dict["sizeMb"] = size_mb
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        mount_path = d.pop("mountPath", d.pop("mount_path", UNSET))

        name = d.pop("name", UNSET)

        read_only = d.pop("readOnly", d.pop("read_only", UNSET))

        size_mb = d.pop("sizeMb", d.pop("size_mb", UNSET))

        _type_ = d.pop("type", d.pop("type_", UNSET))
        type_: Union[Unset, VolumeAttachmentType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = VolumeAttachmentType(_type_)

        volume_attachment = cls(
            mount_path=mount_path,
            name=name,
            read_only=read_only,
            size_mb=size_mb,
            type_=type_,
        )

        volume_attachment.additional_properties = d
        return volume_attachment

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

from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VolumeAttachment")


@_attrs_define
class VolumeAttachment:
    """Volume attachment configuration for sandbox

    Attributes:
        mount_path (Union[Unset, str]): Mount path in the container
        name (Union[Unset, str]): Name of the volume to attach
        read_only (Union[Unset, bool]): Whether the volume is mounted as read-only
    """

    mount_path: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    read_only: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mount_path = self.mount_path

        name = self.name

        read_only = self.read_only

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mount_path is not UNSET:
            field_dict["mountPath"] = mount_path
        if name is not UNSET:
            field_dict["name"] = name
        if read_only is not UNSET:
            field_dict["readOnly"] = read_only

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        mount_path = d.pop("mountPath", UNSET)

        name = d.pop("name", UNSET)

        read_only = d.pop("readOnly", UNSET)

        volume_attachment = cls(
            mount_path=mount_path,
            name=name,
            read_only=read_only,
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

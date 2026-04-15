from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DriveMountInfo")


@_attrs_define
class DriveMountInfo:
    """
    Attributes:
        drive_name (Union[Unset, str]):
        drive_path (Union[Unset, str]):
        mount_path (Union[Unset, str]):
    """

    drive_name: Union[Unset, str] = UNSET
    drive_path: Union[Unset, str] = UNSET
    mount_path: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        drive_name = self.drive_name

        drive_path = self.drive_path

        mount_path = self.mount_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if drive_name is not UNSET:
            field_dict["driveName"] = drive_name
        if drive_path is not UNSET:
            field_dict["drivePath"] = drive_path
        if mount_path is not UNSET:
            field_dict["mountPath"] = mount_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        drive_name = d.pop("driveName", d.pop("drive_name", UNSET))

        drive_path = d.pop("drivePath", d.pop("drive_path", UNSET))

        mount_path = d.pop("mountPath", d.pop("mount_path", UNSET))

        drive_mount_info = cls(
            drive_name=drive_name,
            drive_path=drive_path,
            mount_path=mount_path,
        )

        drive_mount_info.additional_properties = d
        return drive_mount_info

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

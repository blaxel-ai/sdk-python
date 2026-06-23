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
        gid_map (Union[Unset, str]): The local GID used for this mount
        mount_path (Union[Unset, str]):
        read_only (Union[Unset, bool]):
        uid_map (Union[Unset, str]): The local UID used for this mount
    """

    drive_name: Union[Unset, str] = UNSET
    drive_path: Union[Unset, str] = UNSET
    gid_map: Union[Unset, str] = UNSET
    mount_path: Union[Unset, str] = UNSET
    read_only: Union[Unset, bool] = UNSET
    uid_map: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        drive_name = self.drive_name

        drive_path = self.drive_path

        gid_map = self.gid_map

        mount_path = self.mount_path

        read_only = self.read_only

        uid_map = self.uid_map

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if drive_name is not UNSET:
            field_dict["driveName"] = drive_name
        if drive_path is not UNSET:
            field_dict["drivePath"] = drive_path
        if gid_map is not UNSET:
            field_dict["gidMap"] = gid_map
        if mount_path is not UNSET:
            field_dict["mountPath"] = mount_path
        if read_only is not UNSET:
            field_dict["readOnly"] = read_only
        if uid_map is not UNSET:
            field_dict["uidMap"] = uid_map

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        drive_name = d.pop("driveName", d.pop("drive_name", UNSET))

        drive_path = d.pop("drivePath", d.pop("drive_path", UNSET))

        gid_map = d.pop("gidMap", d.pop("gid_map", UNSET))

        mount_path = d.pop("mountPath", d.pop("mount_path", UNSET))

        read_only = d.pop("readOnly", d.pop("read_only", UNSET))

        uid_map = d.pop("uidMap", d.pop("uid_map", UNSET))

        drive_mount_info = cls(
            drive_name=drive_name,
            drive_path=drive_path,
            gid_map=gid_map,
            mount_path=mount_path,
            read_only=read_only,
            uid_map=uid_map,
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

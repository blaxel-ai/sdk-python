from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DriveUnmountResponse")


@_attrs_define
class DriveUnmountResponse:
    """
    Attributes:
        message (Union[Unset, str]):
        mount_path (Union[Unset, str]):
        success (Union[Unset, bool]):
    """

    message: Union[Unset, str] = UNSET
    mount_path: Union[Unset, str] = UNSET
    success: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        mount_path = self.mount_path

        success = self.success

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if mount_path is not UNSET:
            field_dict["mountPath"] = mount_path
        if success is not UNSET:
            field_dict["success"] = success

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        message = d.pop("message", UNSET)

        mount_path = d.pop("mountPath", d.pop("mount_path", UNSET))

        success = d.pop("success", UNSET)

        drive_unmount_response = cls(
            message=message,
            mount_path=mount_path,
            success=success,
        )

        drive_unmount_response.additional_properties = d
        return drive_unmount_response

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

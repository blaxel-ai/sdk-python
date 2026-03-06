from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DriveState")


@_attrs_define
class DriveState:
    """Current runtime state of the drive

    Attributes:
        s_3_url (Union[Unset, str]): S3-compatible endpoint URL for accessing drive contents
    """

    s_3_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        s_3_url = self.s_3_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if s_3_url is not UNSET:
            field_dict["s3Url"] = s_3_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        s_3_url = d.pop("s3Url", d.pop("s_3_url", UNSET))

        drive_state = cls(
            s_3_url=s_3_url,
        )

        drive_state.additional_properties = d
        return drive_state

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

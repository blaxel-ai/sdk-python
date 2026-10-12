from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.drive_mount_info import DriveMountInfo


T = TypeVar("T", bound="DriveListResponse")


@_attrs_define
class DriveListResponse:
    """
    Attributes:
        mounts (Union[Unset, list['DriveMountInfo']]):
    """

    mounts: Union[Unset, list["DriveMountInfo"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mounts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.mounts, Unset):
            mounts = []
            for mounts_item_data in self.mounts:
                if type(mounts_item_data) is dict:
                    mounts_item = mounts_item_data
                else:
                    mounts_item = mounts_item_data.to_dict()
                mounts.append(mounts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mounts is not UNSET:
            field_dict["mounts"] = mounts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.drive_mount_info import DriveMountInfo

        if not src_dict:
            return None
        d = src_dict.copy()
        mounts = []
        _mounts = d.pop("mounts", UNSET)
        for mounts_item_data in _mounts or []:
            mounts_item = DriveMountInfo.from_dict(mounts_item_data)

            mounts.append(mounts_item)

        drive_list_response = cls(
            mounts=mounts,
        )

        drive_list_response.additional_properties = d
        return drive_list_response

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

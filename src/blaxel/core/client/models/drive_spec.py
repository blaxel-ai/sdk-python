from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.drive_permission import DrivePermission


T = TypeVar("T", bound="DriveSpec")


@_attrs_define
class DriveSpec:
    """Immutable drive configuration set at creation time

    Attributes:
        permissions (Union[Unset, list['DrivePermission']]): Permissions controlling which workloads can access this
            drive. Empty means all workloads in the workspace can access the drive. Maximum 3 permissions.
        region (Union[Unset, str]): Deployment region for the drive (e.g., us-pdx-1, eu-lon-1). Must match the region of
            resources it attaches to. Example: us-pdx-1.
    """

    permissions: Union[Unset, list["DrivePermission"]] = UNSET
    region: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        permissions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                if type(permissions_item_data) is dict:
                    permissions_item = permissions_item_data
                else:
                    permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        region = self.region

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.drive_permission import DrivePermission

        if not src_dict:
            return None
        d = src_dict.copy()
        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = DrivePermission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        region = d.pop("region", UNSET)

        drive_spec = cls(
            permissions=permissions,
            region=region,
        )

        drive_spec.additional_properties = d
        return drive_spec

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

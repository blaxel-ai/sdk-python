from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.drive_permission_mode import DrivePermissionMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.drive_permission_labels import DrivePermissionLabels


T = TypeVar("T", bound="DrivePermission")


@_attrs_define
class DrivePermission:
    """Permission that controls which workloads can access a drive. A workload must have ALL specified labels (AND logic).
    Permissions are evaluated with OR logic — the first matching permission grants access.

        Attributes:
            labels (Union[Unset, DrivePermissionLabels]): Labels that the workload must have. All labels must match (AND
                logic). Empty labels match all workloads.
            mode (Union[Unset, DrivePermissionMode]): Access mode granted by this permission
            path (Union[Unset, str]): Subfolder path to restrict access to. Defaults to / (full drive). Example: /data.
    """

    labels: Union[Unset, "DrivePermissionLabels"] = UNSET
    mode: Union[Unset, DrivePermissionMode] = UNSET
    path: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        labels: Union[Unset, dict[str, Any]] = UNSET
        if self.labels and not isinstance(self.labels, Unset) and not isinstance(self.labels, dict):
            labels = self.labels.to_dict()
        elif self.labels and isinstance(self.labels, dict):
            labels = self.labels

        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        path = self.path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if labels is not UNSET:
            field_dict["labels"] = labels
        if mode is not UNSET:
            field_dict["mode"] = mode
        if path is not UNSET:
            field_dict["path"] = path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.drive_permission_labels import DrivePermissionLabels

        if not src_dict:
            return None
        d = src_dict.copy()
        _labels = d.pop("labels", UNSET)
        labels: Union[Unset, DrivePermissionLabels]
        if isinstance(_labels, Unset):
            labels = UNSET
        else:
            labels = DrivePermissionLabels.from_dict(_labels)

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, DrivePermissionMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = DrivePermissionMode(_mode)

        path = d.pop("path", UNSET)

        drive_permission = cls(
            labels=labels,
            mode=mode,
            path=path,
        )

        drive_permission.additional_properties = d
        return drive_permission

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

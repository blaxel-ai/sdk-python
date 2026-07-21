from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceHipaaUnsafe")


@_attrs_define
class WorkspaceHipaaUnsafe:
    """Per-workspace HIPAA opt-out record. Toggled from workspace settings; the backend stamps `updatedBy` and `updatedAt`.

    Attributes:
        enabled (Union[Unset, bool]): True marks this workspace as HIPAA-unsafe (NOT compliant), overriding the account-
            level addon. False marks the workspace as HIPAA compliant.
        updated_at (Union[Unset, str]): RFC3339 timestamp when the opt-out was last toggled. Stamped server-side.
        updated_by (Union[Unset, str]): User id (sub) of the actor that last toggled this opt-out. Stamped server-side.
    """

    enabled: Union[Unset, bool] = UNSET
    updated_at: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        updated_at = self.updated_at

        updated_by = self.updated_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if updated_by is not UNSET:
            field_dict["updatedBy"] = updated_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        updated_by = d.pop("updatedBy", d.pop("updated_by", UNSET))

        workspace_hipaa_unsafe = cls(
            enabled=enabled,
            updated_at=updated_at,
            updated_by=updated_by,
        )

        workspace_hipaa_unsafe.additional_properties = d
        return workspace_hipaa_unsafe

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

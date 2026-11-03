from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.group_workspace_mapping_role import GroupWorkspaceMappingRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupWorkspaceMapping")


@_attrs_define
class GroupWorkspaceMapping:
    """Mapping between an IdP group and a workspace role for directory sync

    Attributes:
        group_name (str | Unset): Name of the IdP group (e.g. "Engineering", "Platform") Example: Engineering.
        role (GroupWorkspaceMappingRole | Unset): Role to assign in this workspace (admin, member or viewer) Example:
            admin.
    """

    group_name: str | Unset = UNSET
    role: GroupWorkspaceMappingRole | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group_name = self.group_name

        role: str | Unset = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if group_name is not UNSET:
            field_dict["groupName"] = group_name
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        group_name = d.pop("groupName", d.pop("group_name", UNSET))

        _role = d.pop("role", UNSET)
        role: GroupWorkspaceMappingRole | Unset
        if isinstance(_role, Unset) or _role == "":
            role = UNSET
        else:
            role = GroupWorkspaceMappingRole(_role)

        group_workspace_mapping = cls(
            group_name=group_name,
            role=role,
        )

        group_workspace_mapping.additional_properties = d
        return group_workspace_mapping

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

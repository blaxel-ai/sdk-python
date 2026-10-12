from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_workspace_service_account_body_role import (
    UpdateWorkspaceServiceAccountBodyRole,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateWorkspaceServiceAccountBody")


@_attrs_define
class UpdateWorkspaceServiceAccountBody:
    """
    Attributes:
        description (Union[Unset, str]): Service account description
        name (Union[Unset, str]): Service account name
        role (Union[Unset, UpdateWorkspaceServiceAccountBodyRole]): Role of the service account in the workspace.
            Defaults to admin on creation; unchanged on update when omitted.
    """

    description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    role: Union[Unset, UpdateWorkspaceServiceAccountBodyRole] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        _role = d.pop("role", UNSET)
        role: Union[Unset, UpdateWorkspaceServiceAccountBodyRole]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = UpdateWorkspaceServiceAccountBodyRole(_role)

        update_workspace_service_account_body = cls(
            description=description,
            name=name,
            role=role,
        )

        update_workspace_service_account_body.additional_properties = d
        return update_workspace_service_account_body

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

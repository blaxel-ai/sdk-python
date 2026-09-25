from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomDomainShareTarget")


@_attrs_define
class CustomDomainShareTarget:
    """A workspace (or the whole account) a custom domain is shared with

    Attributes:
        status (str): Share status; always "active" for same-account custom domain shares.
        workspace (str): The workspace the domain is shared with, or "account" for an account-wide share.
        workspace_display_name (Union[Unset, str]): Display name of the target workspace (empty for an account-wide
            share).
    """

    status: str
    workspace: str
    workspace_display_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        workspace = self.workspace

        workspace_display_name = self.workspace_display_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "workspace": workspace,
            }
        )
        if workspace_display_name is not UNSET:
            field_dict["workspaceDisplayName"] = workspace_display_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        status = d.pop("status")

        workspace = d.pop("workspace")

        workspace_display_name = d.pop(
            "workspaceDisplayName", d.pop("workspace_display_name", UNSET)
        )

        custom_domain_share_target = cls(
            status=status,
            workspace=workspace,
            workspace_display_name=workspace_display_name,
        )

        custom_domain_share_target.additional_properties = d
        return custom_domain_share_target

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

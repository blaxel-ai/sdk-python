from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PendingInvitationRenderAccount")


@_attrs_define
class PendingInvitationRenderAccount:
    """Account info in pending invitation render (for account_admin type)

    Attributes:
        display_name (Union[Unset, str]): Account display name or owner email
        id (Union[Unset, str]): Account ID
    """

    display_name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        display_name = d.pop("displayName", d.pop("display_name", UNSET))

        id = d.pop("id", UNSET)

        pending_invitation_render_account = cls(
            display_name=display_name,
            id=id,
        )

        pending_invitation_render_account.additional_properties = d
        return pending_invitation_render_account

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

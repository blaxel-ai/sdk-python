from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PendingInvitationWorkspaceDetails")


@_attrs_define
class PendingInvitationWorkspaceDetails:
    """Workspace details

    Attributes:
        emails (Union[Unset, list[Any]]): List of user emails in the workspace
        user_number (Union[Unset, float]): Number of users in the workspace
    """

    emails: Union[Unset, list[Any]] = UNSET
    user_number: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        emails: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.emails, Unset):
            emails = self.emails

        user_number = self.user_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if emails is not UNSET:
            field_dict["emails"] = emails
        if user_number is not UNSET:
            field_dict["user_number"] = user_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        emails = cast(list[Any], d.pop("emails", UNSET))

        user_number = d.pop("user_number", UNSET)

        pending_invitation_workspace_details = cls(
            emails=emails,
            user_number=user_number,
        )

        pending_invitation_workspace_details.additional_properties = d
        return pending_invitation_workspace_details

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

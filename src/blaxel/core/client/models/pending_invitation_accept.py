from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace import Workspace


T = TypeVar("T", bound="PendingInvitationAccept")


@_attrs_define
class PendingInvitationAccept:
    """Pending invitation accept

    Attributes:
        email (Union[Unset, str]): User email
        workspace (Union[Unset, Workspace]): Workspace
    """

    email: Union[Unset, str] = UNSET
    workspace: Union[Unset, "Workspace"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        workspace: Union[Unset, dict[str, Any]] = UNSET
        if self.workspace and not isinstance(self.workspace, Unset) and not isinstance(self.workspace, dict):
            workspace = self.workspace.to_dict()
        elif self.workspace and isinstance(self.workspace, dict):
            workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.workspace import Workspace

        if not src_dict:
            return None
        d = src_dict.copy()
        email = d.pop("email", UNSET)

        _workspace = d.pop("workspace", UNSET)
        workspace: Union[Unset, Workspace]
        if isinstance(_workspace, Unset):
            workspace = UNSET
        else:
            workspace = Workspace.from_dict(_workspace)

        pending_invitation_accept = cls(
            email=email,
            workspace=workspace,
        )

        pending_invitation_accept.additional_properties = d
        return pending_invitation_accept

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

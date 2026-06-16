from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_hipaa_unsafe import WorkspaceHipaaUnsafe


T = TypeVar("T", bound="WorkspaceHipaaInfo")


@_attrs_define
class WorkspaceHipaaInfo:
    """HIPAA compliance state for a workspace. `accountEnabled` mirrors the account-level `hipaa_compliance` addon (set
    server-side from operator tooling and Stripe billing events). `unsafe` records a per-workspace opt-out toggled from
    workspace settings; absent when the account does not have the addon.

        Attributes:
            account_enabled (Union[Unset, bool]): True when the parent account has the HIPAA compliance addon active. Set
                server-side from operator tooling and Stripe billing events; cannot be changed from workspace settings.
            unsafe (Union[Unset, WorkspaceHipaaUnsafe]): Per-workspace HIPAA opt-out record. Toggled from workspace
                settings; the backend stamps `updatedBy` and `updatedAt`.
    """

    account_enabled: Union[Unset, bool] = UNSET
    unsafe: Union[Unset, "WorkspaceHipaaUnsafe"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        account_enabled = self.account_enabled

        unsafe: Union[Unset, dict[str, Any]] = UNSET
        if self.unsafe and not isinstance(self.unsafe, Unset) and not isinstance(self.unsafe, dict):
            unsafe = self.unsafe.to_dict()
        elif self.unsafe and isinstance(self.unsafe, dict):
            unsafe = self.unsafe

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account_enabled is not UNSET:
            field_dict["accountEnabled"] = account_enabled
        if unsafe is not UNSET:
            field_dict["unsafe"] = unsafe

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.workspace_hipaa_unsafe import WorkspaceHipaaUnsafe

        if not src_dict:
            return None
        d = src_dict.copy()
        account_enabled = d.pop("accountEnabled", d.pop("account_enabled", UNSET))

        _unsafe = d.pop("unsafe", UNSET)
        unsafe: Union[Unset, WorkspaceHipaaUnsafe]
        if isinstance(_unsafe, Unset):
            unsafe = UNSET
        else:
            unsafe = WorkspaceHipaaUnsafe.from_dict(_unsafe)

        workspace_hipaa_info = cls(
            account_enabled=account_enabled,
            unsafe=unsafe,
        )

        workspace_hipaa_info.additional_properties = d
        return workspace_hipaa_info

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

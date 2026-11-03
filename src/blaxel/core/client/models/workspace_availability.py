from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.workspace_availability_reason import WorkspaceAvailabilityReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceAvailability")


@_attrs_define
class WorkspaceAvailability:
    """Result of a workspace-name availability check.

    Attributes:
        available (bool | Unset): Whether the requested workspace name is available.
        message (str | Unset): Human-readable explanation suitable for display in the UI. Empty when available.
        reason (WorkspaceAvailabilityReason | Unset): Machine-readable reason explaining why the name is unavailable.
            Empty when available.
    """

    available: bool | Unset = UNSET
    message: str | Unset = UNSET
    reason: WorkspaceAvailabilityReason | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available = self.available

        message = self.message

        reason: str | Unset = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if available is not UNSET:
            field_dict["available"] = available
        if message is not UNSET:
            field_dict["message"] = message
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        available = d.pop("available", UNSET)

        message = d.pop("message", UNSET)

        _reason = d.pop("reason", UNSET)
        reason: WorkspaceAvailabilityReason | Unset
        if isinstance(_reason, Unset) or _reason == "":
            reason = UNSET
        else:
            reason = WorkspaceAvailabilityReason(_reason)

        workspace_availability = cls(
            available=available,
            message=message,
            reason=reason,
        )

        workspace_availability.additional_properties = d
        return workspace_availability

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

from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceSandboxSettings")


@_attrs_define
class WorkspaceSandboxSettings:
    """Workspace-wide sandbox configuration that applies to all sandbox deployments in the workspace.

    Attributes:
        disable_process_logging (Union[Unset, bool]): When true, sandbox deployments in this workspace set
            SANDBOX_DISABLE_PROCESS_LOGGING=true to disable per-process stdout/stderr logging. Requires sandbox-api
            v0.2.28+.
    """

    disable_process_logging: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disable_process_logging = self.disable_process_logging

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if disable_process_logging is not UNSET:
            field_dict["disableProcessLogging"] = disable_process_logging

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        disable_process_logging = d.pop(
            "disableProcessLogging", d.pop("disable_process_logging", UNSET)
        )

        workspace_sandbox_settings = cls(
            disable_process_logging=disable_process_logging,
        )

        workspace_sandbox_settings.additional_properties = d
        return workspace_sandbox_settings

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

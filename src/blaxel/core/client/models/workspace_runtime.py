from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_sandbox_settings import WorkspaceSandboxSettings


T = TypeVar("T", bound="WorkspaceRuntime")


@_attrs_define
class WorkspaceRuntime:
    """Runtime configuration for the workspace infrastructure

    Attributes:
        generation (Union[Unset, str]): Infrastructure generation version for the workspace (affects available features
            and deployment behavior) Example: mk3.
        sandbox (Union[Unset, WorkspaceSandboxSettings]): Workspace-wide sandbox configuration that applies to all
            sandbox deployments in the workspace.
    """

    generation: Union[Unset, str] = UNSET
    sandbox: Union[Unset, "WorkspaceSandboxSettings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        generation = self.generation

        sandbox: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.sandbox
            and not isinstance(self.sandbox, Unset)
            and not isinstance(self.sandbox, dict)
        ):
            sandbox = self.sandbox.to_dict()
        elif self.sandbox and isinstance(self.sandbox, dict):
            sandbox = self.sandbox

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if generation is not UNSET:
            field_dict["generation"] = generation
        if sandbox is not UNSET:
            field_dict["sandbox"] = sandbox

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.workspace_sandbox_settings import WorkspaceSandboxSettings

        if not src_dict:
            return None
        d = src_dict.copy()
        generation = d.pop("generation", UNSET)

        _sandbox = d.pop("sandbox", UNSET)
        sandbox: Union[Unset, WorkspaceSandboxSettings]
        if isinstance(_sandbox, Unset):
            sandbox = UNSET
        else:
            sandbox = WorkspaceSandboxSettings.from_dict(_sandbox)

        workspace_runtime = cls(
            generation=generation,
            sandbox=sandbox,
        )

        workspace_runtime.additional_properties = d
        return workspace_runtime

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

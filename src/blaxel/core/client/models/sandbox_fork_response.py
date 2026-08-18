from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_fork_response_type import SandboxForkResponseType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxForkResponse")


@_attrs_define
class SandboxForkResponse:
    """Response returned after forking a sandbox. Contains either the new sandbox or application depending on the fork
    type.

        Attributes:
            name (Union[Unset, str]): Name of the created or updated resource
            snapshot_id (Union[Unset, str]): The snapshot ID the fork was created from
            type_ (Union[Unset, SandboxForkResponseType]): Type of resource that was created (sandbox or application)
    """

    name: Union[Unset, str] = UNSET
    snapshot_id: Union[Unset, str] = UNSET
    type_: Union[Unset, SandboxForkResponseType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        snapshot_id = self.snapshot_id

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if snapshot_id is not UNSET:
            field_dict["snapshotId"] = snapshot_id
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        snapshot_id = d.pop("snapshotId", d.pop("snapshot_id", UNSET))

        _type_ = d.pop("type", d.pop("type_", UNSET))
        type_: Union[Unset, SandboxForkResponseType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = SandboxForkResponseType(_type_)

        sandbox_fork_response = cls(
            name=name,
            snapshot_id=snapshot_id,
            type_=type_,
        )

        sandbox_fork_response.additional_properties = d
        return sandbox_fork_response

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

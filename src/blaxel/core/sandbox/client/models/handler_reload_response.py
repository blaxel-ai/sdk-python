from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HandlerReloadResponse")


@_attrs_define
class HandlerReloadResponse:
    """
    Attributes:
        applied (Union[Unset, int]):
        generation (Union[Unset, int]):
        removed (Union[Unset, int]):
    """

    applied: Union[Unset, int] = UNSET
    generation: Union[Unset, int] = UNSET
    removed: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        applied = self.applied

        generation = self.generation

        removed = self.removed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if applied is not UNSET:
            field_dict["applied"] = applied
        if generation is not UNSET:
            field_dict["generation"] = generation
        if removed is not UNSET:
            field_dict["removed"] = removed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        applied = d.pop("applied", UNSET)

        generation = d.pop("generation", UNSET)

        removed = d.pop("removed", UNSET)

        handler_reload_response = cls(
            applied=applied,
            generation=generation,
            removed=removed,
        )

        handler_reload_response.additional_properties = d
        return handler_reload_response

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

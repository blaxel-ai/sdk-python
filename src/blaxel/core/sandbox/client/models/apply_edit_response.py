from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplyEditResponse")


@_attrs_define
class ApplyEditResponse:
    """
    Attributes:
        message (str | Unset):  Example: Code edit applied successfully.
        original_content (str | Unset):  Example: function hello() {
              console.log('Hello');
            }.
        path (str | Unset):  Example: src/main.js.
        provider (str | Unset):  Example: Relace.
        success (bool | Unset):  Example: True.
        updated_content (str | Unset):  Example: function hello(world) {
              console.log('Hello', world);
            }.
    """

    message: str | Unset = UNSET
    original_content: str | Unset = UNSET
    path: str | Unset = UNSET
    provider: str | Unset = UNSET
    success: bool | Unset = UNSET
    updated_content: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        original_content = self.original_content

        path = self.path

        provider = self.provider

        success = self.success

        updated_content = self.updated_content

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if original_content is not UNSET:
            field_dict["originalContent"] = original_content
        if path is not UNSET:
            field_dict["path"] = path
        if provider is not UNSET:
            field_dict["provider"] = provider
        if success is not UNSET:
            field_dict["success"] = success
        if updated_content is not UNSET:
            field_dict["updatedContent"] = updated_content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        message = d.pop("message", UNSET)

        original_content = d.pop("originalContent", d.pop("original_content", UNSET))

        path = d.pop("path", UNSET)

        provider = d.pop("provider", UNSET)

        success = d.pop("success", UNSET)

        updated_content = d.pop("updatedContent", d.pop("updated_content", UNSET))

        apply_edit_response = cls(
            message=message,
            original_content=original_content,
            path=path,
            provider=provider,
            success=success,
            updated_content=updated_content,
        )

        apply_edit_response.additional_properties = d
        return apply_edit_response

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

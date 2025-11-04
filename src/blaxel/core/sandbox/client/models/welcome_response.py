from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WelcomeResponse")


@_attrs_define
class WelcomeResponse:
    """
    Attributes:
        description (Union[Unset, str]):  Example: This sandbox provides a full-featured environment for running code
            securely.
        documentation (Union[Unset, str]):  Example: https://docs.blaxel.ai/Sandboxes/Overview.
        message (Union[Unset, str]):  Example: Welcome to your Blaxel Sandbox.
    """

    description: Union[Unset, str] = UNSET
    documentation: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        documentation = self.documentation

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if documentation is not UNSET:
            field_dict["documentation"] = documentation
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        documentation = d.pop("documentation", UNSET)

        message = d.pop("message", UNSET)

        welcome_response = cls(
            description=description,
            documentation=documentation,
            message=message,
        )

        welcome_response.additional_properties = d
        return welcome_response

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

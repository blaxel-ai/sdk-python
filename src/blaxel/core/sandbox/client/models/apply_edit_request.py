from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplyEditRequest")


@_attrs_define
class ApplyEditRequest:
    """
    Attributes:
        code_edit (str):  Example: // Add world parameter
            function hello(world) {
              console.log('Hello', world);
            }.
        model (Union[Unset, str]):  Example: auto.
    """

    code_edit: str
    model: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code_edit = self.code_edit

        model = self.model

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "codeEdit": code_edit,
            }
        )
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        code_edit = d.pop("codeEdit") if "codeEdit" in d else d.pop("code_edit")

        model = d.pop("model", UNSET)

        apply_edit_request = cls(
            code_edit=code_edit,
            model=model,
        )

        apply_edit_request.additional_properties = d
        return apply_edit_request

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

from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplicationExtension")


@_attrs_define
class ApplicationExtension:
    """Configuration for a single application extension. The fields used depend on the extension key; for
    ai.blaxel.experimental/bind-to-sandbox only "sandbox" is used.

        Attributes:
            sandbox (Union[Unset, str]): Name of the sandbox this application binds to (used by the
                ai.blaxel.experimental/bind-to-sandbox extension). Example: my-sandbox.
    """

    sandbox: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sandbox = self.sandbox

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sandbox is not UNSET:
            field_dict["sandbox"] = sandbox

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        sandbox = d.pop("sandbox", UNSET)

        application_extension = cls(
            sandbox=sandbox,
        )

        application_extension.additional_properties = d
        return application_extension

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

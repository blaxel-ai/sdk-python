from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.application_extension import ApplicationExtension


T = TypeVar("T", bound="ApplicationExtensions")


@_attrs_define
class ApplicationExtensions:
    """Map of experimental, opt-in application extensions keyed by fully-qualified extension name (e.g.
    "ai.blaxel.experimental/bind-to-sandbox").

    """

    additional_properties: dict[str, "ApplicationExtension"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if type(prop) is dict:
                field_dict[prop_name] = prop
            else:
                field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.application_extension import ApplicationExtension

        if not src_dict:
            return None
        d = src_dict.copy()
        application_extensions = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ApplicationExtension.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        application_extensions.additional_properties = additional_properties
        return application_extensions

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "ApplicationExtension":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "ApplicationExtension") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

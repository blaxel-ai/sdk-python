from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VolumeTemplateSpec")


@_attrs_define
class VolumeTemplateSpec:
    """Volume template specification

    Attributes:
        default_size (Union[Unset, int]): Default size of the volume in MB
        description (Union[Unset, str]): Description of the volume template
    """

    default_size: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default_size = self.default_size

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default_size is not UNSET:
            field_dict["defaultSize"] = default_size
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        default_size = d.pop("defaultSize", d.pop("default_size", UNSET))

        description = d.pop("description", UNSET)

        volume_template_spec = cls(
            default_size=default_size,
            description=description,
        )

        volume_template_spec.additional_properties = d
        return volume_template_spec

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

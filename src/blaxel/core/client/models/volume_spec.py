from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VolumeSpec")


@_attrs_define
class VolumeSpec:
    """Volume specification

    Attributes:
        attached_to (Union[Unset, str]): Resource this volume is attached to (e.g. "sandbox:my-sandbox", "model:my-
            model")
        region (Union[Unset, str]): AWS region where the volume should be created (e.g. us-west-2, eu-west-1)
        size (Union[Unset, int]): Size of the volume in MB
    """

    attached_to: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attached_to = self.attached_to

        region = self.region

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attached_to is not UNSET:
            field_dict["attachedTo"] = attached_to
        if region is not UNSET:
            field_dict["region"] = region
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        attached_to = d.pop("attachedTo", UNSET)

        region = d.pop("region", UNSET)

        size = d.pop("size", UNSET)

        volume_spec = cls(
            attached_to=attached_to,
            region=region,
            size=size,
        )

        volume_spec.additional_properties = d
        return volume_spec

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

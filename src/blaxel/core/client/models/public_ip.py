from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PublicIp")


@_attrs_define
class PublicIp:
    """
    Attributes:
        description (Union[Unset, str]): Description of the region/location
        ipv_4_cidrs (Union[Unset, list[str]]): List of public ipv4 addresses
        ipv_6_cidrs (Union[Unset, list[str]]): List of public ipv6 addresses
    """

    description: Union[Unset, str] = UNSET
    ipv_4_cidrs: Union[Unset, list[str]] = UNSET
    ipv_6_cidrs: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        ipv_4_cidrs: Union[Unset, list[str]] = UNSET
        if not isinstance(self.ipv_4_cidrs, Unset):
            ipv_4_cidrs = self.ipv_4_cidrs

        ipv_6_cidrs: Union[Unset, list[str]] = UNSET
        if not isinstance(self.ipv_6_cidrs, Unset):
            ipv_6_cidrs = self.ipv_6_cidrs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if ipv_4_cidrs is not UNSET:
            field_dict["ipv4Cidrs"] = ipv_4_cidrs
        if ipv_6_cidrs is not UNSET:
            field_dict["ipv6Cidrs"] = ipv_6_cidrs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        ipv_4_cidrs = cast(list[str], d.pop("ipv4Cidrs", UNSET))

        ipv_6_cidrs = cast(list[str], d.pop("ipv6Cidrs", UNSET))

        public_ip = cls(
            description=description,
            ipv_4_cidrs=ipv_4_cidrs,
            ipv_6_cidrs=ipv_6_cidrs,
        )

        public_ip.additional_properties = d
        return public_ip

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

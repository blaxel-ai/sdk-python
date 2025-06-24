from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Port")


@_attrs_define
class Port:
    """A port for a resource

    Attributes:
        name (Union[Unset, str]): The name of the port
        protocol (Union[Unset, str]): The protocol of the port
        target (Union[Unset, int]): The target port of the port
    """

    name: Union[Unset, str] = UNSET
    protocol: Union[Unset, str] = UNSET
    target: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        protocol = self.protocol

        target = self.target

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if protocol is not UNSET:
            field_dict["protocol"] = protocol
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        protocol = d.pop("protocol", UNSET)

        target = d.pop("target", UNSET)

        port = cls(
            name=name,
            protocol=protocol,
            target=target,
        )

        port.additional_properties = d
        return port

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

from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.port_protocol import PortProtocol
from ..types import UNSET, Unset

T = TypeVar("T", bound="Port")


@_attrs_define
class Port:
    """A port for a resource

    Attributes:
        target (int): The target port of the port Example: 8080.
        name (Union[Unset, str]): The name of the port Example: http.
        protocol (Union[Unset, PortProtocol]): The protocol of the port Example: HTTP.
    """

    target: int
    name: Union[Unset, str] = UNSET
    protocol: Union[Unset, PortProtocol] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        name = self.name

        protocol: Union[Unset, str] = UNSET
        if not isinstance(self.protocol, Unset):
            protocol = self.protocol.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target": target,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if protocol is not UNSET:
            field_dict["protocol"] = protocol

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        target = d.pop("target")

        name = d.pop("name", UNSET)

        _protocol = d.pop("protocol", UNSET)
        protocol: Union[Unset, PortProtocol]
        if isinstance(_protocol, Unset):
            protocol = UNSET
        else:
            protocol = PortProtocol(_protocol)

        port = cls(
            target=target,
            name=name,
            protocol=protocol,
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

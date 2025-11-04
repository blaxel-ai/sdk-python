from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MemoryAllocationByName")


@_attrs_define
class MemoryAllocationByName:
    """Memory allocation by service name

    Attributes:
        allocation (Union[Unset, float]): Memory allocation value
        name (Union[Unset, str]): Name
    """

    allocation: Union[Unset, float] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allocation = self.allocation

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allocation is not UNSET:
            field_dict["allocation"] = allocation
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        allocation = d.pop("allocation", UNSET)

        name = d.pop("name", UNSET)

        memory_allocation_by_name = cls(
            allocation=allocation,
            name=name,
        )

        memory_allocation_by_name.additional_properties = d
        return memory_allocation_by_name

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

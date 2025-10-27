from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MemoryAllocationMetric")


@_attrs_define
class MemoryAllocationMetric:
    """Metrics for memory allocation

    Attributes:
        total_allocation (Union[Unset, float]): Total memory allocation in GB-seconds
    """

    total_allocation: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_allocation = self.total_allocation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total_allocation is not UNSET:
            field_dict["totalAllocation"] = total_allocation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        total_allocation = d.pop("totalAllocation", UNSET)

        memory_allocation_metric = cls(
            total_allocation=total_allocation,
        )

        memory_allocation_metric.additional_properties = d
        return memory_allocation_metric

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

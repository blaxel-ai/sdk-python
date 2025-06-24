from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BillableTimeMetric")


@_attrs_define
class BillableTimeMetric:
    """Billable time metric

    Attributes:
        billable_time (Union[Unset, float]): Billable time
        total_allocation (Union[Unset, float]): Total memory allocation in GB-seconds
    """

    billable_time: Union[Unset, float] = UNSET
    total_allocation: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        billable_time = self.billable_time

        total_allocation = self.total_allocation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if billable_time is not UNSET:
            field_dict["billableTime"] = billable_time
        if total_allocation is not UNSET:
            field_dict["totalAllocation"] = total_allocation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        billable_time = d.pop("billableTime", UNSET)

        total_allocation = d.pop("totalAllocation", UNSET)

        billable_time_metric = cls(
            billable_time=billable_time,
            total_allocation=total_allocation,
        )

        billable_time_metric.additional_properties = d
        return billable_time_metric

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

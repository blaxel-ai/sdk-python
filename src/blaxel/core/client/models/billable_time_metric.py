from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.jobs_chart_value import JobsChartValue


T = TypeVar("T", bound="BillableTimeMetric")


@_attrs_define
class BillableTimeMetric:
    """Billable time metric

    Attributes:
        billable_time (Union[Unset, list['JobsChartValue']]): Billable time
        total_allocation (Union[Unset, float]): Total memory allocation in GB-seconds
    """

    billable_time: Union[Unset, list["JobsChartValue"]] = UNSET
    total_allocation: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        billable_time: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.billable_time, Unset):
            billable_time = []
            for billable_time_item_data in self.billable_time:
                if type(billable_time_item_data) is dict:
                    billable_time_item = billable_time_item_data
                else:
                    billable_time_item = billable_time_item_data.to_dict()
                billable_time.append(billable_time_item)

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
        from ..models.jobs_chart_value import JobsChartValue

        if not src_dict:
            return None
        d = src_dict.copy()
        billable_time = []
        _billable_time = d.pop("billableTime", UNSET)
        for billable_time_item_data in _billable_time or []:
            billable_time_item = JobsChartValue.from_dict(billable_time_item_data)

            billable_time.append(billable_time_item)

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

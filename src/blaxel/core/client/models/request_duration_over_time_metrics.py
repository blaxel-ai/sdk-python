from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.request_duration_over_time_metric import RequestDurationOverTimeMetric


T = TypeVar("T", bound="RequestDurationOverTimeMetrics")


@_attrs_define
class RequestDurationOverTimeMetrics:
    """Request duration over time metrics

    Attributes:
        request_duration_over_time (Union[Unset, list['RequestDurationOverTimeMetric']]): Request duration over time
    """

    request_duration_over_time: Union[Unset, list["RequestDurationOverTimeMetric"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request_duration_over_time: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.request_duration_over_time, Unset):
            request_duration_over_time = []
            for request_duration_over_time_item_data in self.request_duration_over_time:
                if type(request_duration_over_time_item_data) is dict:
                    request_duration_over_time_item = request_duration_over_time_item_data
                else:
                    request_duration_over_time_item = request_duration_over_time_item_data.to_dict()
                request_duration_over_time.append(request_duration_over_time_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if request_duration_over_time is not UNSET:
            field_dict["requestDurationOverTime"] = request_duration_over_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.request_duration_over_time_metric import RequestDurationOverTimeMetric

        if not src_dict:
            return None
        d = src_dict.copy()
        request_duration_over_time = []
        _request_duration_over_time = d.pop("requestDurationOverTime", UNSET)
        for request_duration_over_time_item_data in _request_duration_over_time or []:
            request_duration_over_time_item = RequestDurationOverTimeMetric.from_dict(
                request_duration_over_time_item_data
            )

            request_duration_over_time.append(request_duration_over_time_item)

        request_duration_over_time_metrics = cls(
            request_duration_over_time=request_duration_over_time,
        )

        request_duration_over_time_metrics.additional_properties = d
        return request_duration_over_time_metrics

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

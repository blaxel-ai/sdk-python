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
        request_duration_over_time (Union[Unset, RequestDurationOverTimeMetric]): Request duration over time metric
    """

    request_duration_over_time: Union[Unset, "RequestDurationOverTimeMetric"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request_duration_over_time: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.request_duration_over_time
            and not isinstance(self.request_duration_over_time, Unset)
            and not isinstance(self.request_duration_over_time, dict)
        ):
            request_duration_over_time = self.request_duration_over_time.to_dict()
        elif self.request_duration_over_time and isinstance(self.request_duration_over_time, dict):
            request_duration_over_time = self.request_duration_over_time

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
        _request_duration_over_time = d.pop("requestDurationOverTime", UNSET)
        request_duration_over_time: Union[Unset, RequestDurationOverTimeMetric]
        if isinstance(_request_duration_over_time, Unset):
            request_duration_over_time = UNSET
        else:
            request_duration_over_time = RequestDurationOverTimeMetric.from_dict(_request_duration_over_time)

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

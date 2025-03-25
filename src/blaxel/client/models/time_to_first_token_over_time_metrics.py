from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.request_duration_over_time_metric import RequestDurationOverTimeMetric


T = TypeVar("T", bound="TimeToFirstTokenOverTimeMetrics")


@_attrs_define
class TimeToFirstTokenOverTimeMetrics:
    """Time to first token over time metrics

    Attributes:
        time_to_first_token_over_time (Union[Unset, RequestDurationOverTimeMetric]): Request duration over time metric
    """

    time_to_first_token_over_time: Union[Unset, "RequestDurationOverTimeMetric"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        time_to_first_token_over_time: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.time_to_first_token_over_time
            and not isinstance(self.time_to_first_token_over_time, Unset)
            and not isinstance(self.time_to_first_token_over_time, dict)
        ):
            time_to_first_token_over_time = self.time_to_first_token_over_time.to_dict()
        elif self.time_to_first_token_over_time and isinstance(self.time_to_first_token_over_time, dict):
            time_to_first_token_over_time = self.time_to_first_token_over_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if time_to_first_token_over_time is not UNSET:
            field_dict["timeToFirstTokenOverTime"] = time_to_first_token_over_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.request_duration_over_time_metric import RequestDurationOverTimeMetric

        if not src_dict:
            return None
        d = src_dict.copy()
        _time_to_first_token_over_time = d.pop("timeToFirstTokenOverTime", UNSET)
        time_to_first_token_over_time: Union[Unset, RequestDurationOverTimeMetric]
        if isinstance(_time_to_first_token_over_time, Unset):
            time_to_first_token_over_time = UNSET
        else:
            time_to_first_token_over_time = RequestDurationOverTimeMetric.from_dict(_time_to_first_token_over_time)

        time_to_first_token_over_time_metrics = cls(
            time_to_first_token_over_time=time_to_first_token_over_time,
        )

        time_to_first_token_over_time_metrics.additional_properties = d
        return time_to_first_token_over_time_metrics

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

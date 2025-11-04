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
        time_to_first_token_over_time (Union[Unset, list['RequestDurationOverTimeMetric']]): Time to first token over
            time
    """

    time_to_first_token_over_time: Union[Unset, list["RequestDurationOverTimeMetric"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        time_to_first_token_over_time: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.time_to_first_token_over_time, Unset):
            time_to_first_token_over_time = []
            for time_to_first_token_over_time_item_data in self.time_to_first_token_over_time:
                if type(time_to_first_token_over_time_item_data) is dict:
                    time_to_first_token_over_time_item = time_to_first_token_over_time_item_data
                else:
                    time_to_first_token_over_time_item = time_to_first_token_over_time_item_data.to_dict()
                time_to_first_token_over_time.append(time_to_first_token_over_time_item)

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
        time_to_first_token_over_time = []
        _time_to_first_token_over_time = d.pop("timeToFirstTokenOverTime", UNSET)
        for time_to_first_token_over_time_item_data in _time_to_first_token_over_time or []:
            time_to_first_token_over_time_item = RequestDurationOverTimeMetric.from_dict(
                time_to_first_token_over_time_item_data
            )

            time_to_first_token_over_time.append(time_to_first_token_over_time_item)

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

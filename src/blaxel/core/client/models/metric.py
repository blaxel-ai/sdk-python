from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Metric")


@_attrs_define
class Metric:
    """Metric

    Attributes:
        rate (Union[Unset, int]): Metric value
        request_total (Union[Unset, int]): Metric value
        timestamp (Union[Unset, str]): Metric timestamp
    """

    rate: Union[Unset, int] = UNSET
    request_total: Union[Unset, int] = UNSET
    timestamp: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rate = self.rate

        request_total = self.request_total

        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rate is not UNSET:
            field_dict["rate"] = rate
        if request_total is not UNSET:
            field_dict["requestTotal"] = request_total
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        rate = d.pop("rate", UNSET)

        request_total = d.pop("requestTotal", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        metric = cls(
            rate=rate,
            request_total=request_total,
            timestamp=timestamp,
        )

        metric.additional_properties = d
        return metric

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

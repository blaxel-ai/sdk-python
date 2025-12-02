from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxMetrics")


@_attrs_define
class SandboxMetrics:
    """Enhanced sandbox metrics with memory, value, and percent data

    Attributes:
        memory (Union[Unset, float]): Memory limit in bytes (from query A)
        percent (Union[Unset, float]): Memory usage percentage (from formula F1)
        timestamp (Union[Unset, str]): Metric timestamp
        value (Union[Unset, float]): Memory usage in bytes (from query B)
    """

    memory: Union[Unset, float] = UNSET
    percent: Union[Unset, float] = UNSET
    timestamp: Union[Unset, str] = UNSET
    value: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        memory = self.memory

        percent = self.percent

        timestamp = self.timestamp

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if memory is not UNSET:
            field_dict["memory"] = memory
        if percent is not UNSET:
            field_dict["percent"] = percent
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        memory = d.pop("memory", UNSET)

        percent = d.pop("percent", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        value = d.pop("value", UNSET)

        sandbox_metrics = cls(
            memory=memory,
            percent=percent,
            timestamp=timestamp,
            value=value,
        )

        sandbox_metrics.additional_properties = d
        return sandbox_metrics

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

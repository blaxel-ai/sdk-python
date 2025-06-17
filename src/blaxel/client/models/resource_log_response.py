from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceLogResponse")


@_attrs_define
class ResourceLogResponse:
    """Response for a resource log

    Attributes:
        chart (Union[Unset, list[Any]]): Chart
        logs (Union[Unset, list[Any]]): Logs
        total_count (Union[Unset, int]): Total count of logs
    """

    chart: Union[Unset, list[Any]] = UNSET
    logs: Union[Unset, list[Any]] = UNSET
    total_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        chart: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.chart, Unset):
            chart = self.chart

        logs: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.logs, Unset):
            logs = self.logs

        total_count = self.total_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if chart is not UNSET:
            field_dict["chart"] = chart
        if logs is not UNSET:
            field_dict["logs"] = logs
        if total_count is not UNSET:
            field_dict["totalCount"] = total_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        chart = cast(list[Any], d.pop("chart", UNSET))

        logs = cast(list[Any], d.pop("logs", UNSET))

        total_count = d.pop("totalCount", UNSET)

        resource_log_response = cls(
            chart=chart,
            logs=logs,
            total_count=total_count,
        )

        resource_log_response.additional_properties = d
        return resource_log_response

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

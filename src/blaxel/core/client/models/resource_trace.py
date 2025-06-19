from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceTrace")


@_attrs_define
class ResourceTrace:
    """Log for a resource deployment (eg. model deployment, function deployment)

    Attributes:
        duration (Union[Unset, int]): Duration in nanoseconds
        has_error (Union[Unset, bool]): Has error
        start_time (Union[Unset, str]): The timestamp of the log
        status_code (Union[Unset, int]): Status code
        trace_id (Union[Unset, str]): Trace ID of the log
    """

    duration: Union[Unset, int] = UNSET
    has_error: Union[Unset, bool] = UNSET
    start_time: Union[Unset, str] = UNSET
    status_code: Union[Unset, int] = UNSET
    trace_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration = self.duration

        has_error = self.has_error

        start_time = self.start_time

        status_code = self.status_code

        trace_id = self.trace_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if duration is not UNSET:
            field_dict["duration"] = duration
        if has_error is not UNSET:
            field_dict["hasError"] = has_error
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if status_code is not UNSET:
            field_dict["statusCode"] = status_code
        if trace_id is not UNSET:
            field_dict["traceID"] = trace_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        duration = d.pop("duration", UNSET)

        has_error = d.pop("hasError", UNSET)

        start_time = d.pop("startTime", UNSET)

        status_code = d.pop("statusCode", UNSET)

        trace_id = d.pop("traceID", UNSET)

        resource_trace = cls(
            duration=duration,
            has_error=has_error,
            start_time=start_time,
            status_code=status_code,
            trace_id=trace_id,
        )

        resource_trace.additional_properties = d
        return resource_trace

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

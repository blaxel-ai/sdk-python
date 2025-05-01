from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceLog")


@_attrs_define
class ResourceLog:
    """Log for a resource deployment (eg. model deployment, function deployment)

    Attributes:
        message (Union[Unset, str]): Content of the log
        severity (Union[Unset, int]): Severity of the log
        timestamp (Union[Unset, str]): The timestamp of the log
        trace_id (Union[Unset, str]): Trace ID of the log
    """

    message: Union[Unset, str] = UNSET
    severity: Union[Unset, int] = UNSET
    timestamp: Union[Unset, str] = UNSET
    trace_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        severity = self.severity

        timestamp = self.timestamp

        trace_id = self.trace_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if severity is not UNSET:
            field_dict["severity"] = severity
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if trace_id is not UNSET:
            field_dict["trace_id"] = trace_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        message = d.pop("message", UNSET)

        severity = d.pop("severity", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        trace_id = d.pop("trace_id", UNSET)

        resource_log = cls(
            message=message,
            severity=severity,
            timestamp=timestamp,
            trace_id=trace_id,
        )

        resource_log.additional_properties = d
        return resource_log

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

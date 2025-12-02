from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogsResponseData")


@_attrs_define
class LogsResponseData:
    """Response data for logs

    Attributes:
        body (Union[Unset, str]): Body of the log
        log_attributes (Union[Unset, list[Any]]): Log attributes
        severity_number (Union[Unset, int]): Severity number of the log
        timestamp (Union[Unset, str]): Timestamp of the log
        trace_id (Union[Unset, str]): Trace ID of the log
    """

    body: Union[Unset, str] = UNSET
    log_attributes: Union[Unset, list[Any]] = UNSET
    severity_number: Union[Unset, int] = UNSET
    timestamp: Union[Unset, str] = UNSET
    trace_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body = self.body

        log_attributes: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.log_attributes, Unset):
            log_attributes = self.log_attributes

        severity_number = self.severity_number

        timestamp = self.timestamp

        trace_id = self.trace_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if body is not UNSET:
            field_dict["body"] = body
        if log_attributes is not UNSET:
            field_dict["logAttributes"] = log_attributes
        if severity_number is not UNSET:
            field_dict["severityNumber"] = severity_number
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if trace_id is not UNSET:
            field_dict["traceId"] = trace_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        body = d.pop("body", UNSET)

        log_attributes = cast(list[Any], d.pop("logAttributes", UNSET))

        severity_number = d.pop("severityNumber", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        trace_id = d.pop("traceId", UNSET)

        logs_response_data = cls(
            body=body,
            log_attributes=log_attributes,
            severity_number=severity_number,
            timestamp=timestamp,
            trace_id=trace_id,
        )

        logs_response_data.additional_properties = d
        return logs_response_data

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

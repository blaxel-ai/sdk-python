from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceLogChart")


@_attrs_define
class ResourceLogChart:
    """Chart for a resource log

    Attributes:
        count (Union[Unset, int]): Count of the log
        debug (Union[Unset, int]): Debug count of the log
        error (Union[Unset, int]): Error count of the log
        fatal (Union[Unset, int]): Fatal count of the log
        info (Union[Unset, int]): Info count of the log
        timestamp (Union[Unset, str]): Timestamp of the log
        trace (Union[Unset, int]): Trace count of the log
        unknown (Union[Unset, int]): Unknown count of the log
        warning (Union[Unset, int]): Warning count of the log
    """

    count: Union[Unset, int] = UNSET
    debug: Union[Unset, int] = UNSET
    error: Union[Unset, int] = UNSET
    fatal: Union[Unset, int] = UNSET
    info: Union[Unset, int] = UNSET
    timestamp: Union[Unset, str] = UNSET
    trace: Union[Unset, int] = UNSET
    unknown: Union[Unset, int] = UNSET
    warning: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        debug = self.debug

        error = self.error

        fatal = self.fatal

        info = self.info

        timestamp = self.timestamp

        trace = self.trace

        unknown = self.unknown

        warning = self.warning

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if debug is not UNSET:
            field_dict["debug"] = debug
        if error is not UNSET:
            field_dict["error"] = error
        if fatal is not UNSET:
            field_dict["fatal"] = fatal
        if info is not UNSET:
            field_dict["info"] = info
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if trace is not UNSET:
            field_dict["trace"] = trace
        if unknown is not UNSET:
            field_dict["unknown"] = unknown
        if warning is not UNSET:
            field_dict["warning"] = warning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        count = d.pop("count", UNSET)

        debug = d.pop("debug", UNSET)

        error = d.pop("error", UNSET)

        fatal = d.pop("fatal", UNSET)

        info = d.pop("info", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        trace = d.pop("trace", UNSET)

        unknown = d.pop("unknown", UNSET)

        warning = d.pop("warning", UNSET)

        resource_log_chart = cls(
            count=count,
            debug=debug,
            error=error,
            fatal=fatal,
            info=info,
            timestamp=timestamp,
            trace=trace,
            unknown=unknown,
            warning=warning,
        )

        resource_log_chart.additional_properties = d
        return resource_log_chart

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

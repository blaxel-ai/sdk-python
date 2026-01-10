from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobExecutionStats")


@_attrs_define
class JobExecutionStats:
    """Job execution statistics

    Attributes:
        cancelled (Union[Unset, int]): Number of cancelled tasks
        failure (Union[Unset, int]): Number of failed tasks Example: 1.
        retried (Union[Unset, int]): Number of retried tasks Example: 2.
        running (Union[Unset, int]): Number of running tasks Example: 1.
        success (Union[Unset, int]): Number of successful tasks Example: 8.
        total (Union[Unset, int]): Total number of tasks Example: 10.
    """

    cancelled: Union[Unset, int] = UNSET
    failure: Union[Unset, int] = UNSET
    retried: Union[Unset, int] = UNSET
    running: Union[Unset, int] = UNSET
    success: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cancelled = self.cancelled

        failure = self.failure

        retried = self.retried

        running = self.running

        success = self.success

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cancelled is not UNSET:
            field_dict["cancelled"] = cancelled
        if failure is not UNSET:
            field_dict["failure"] = failure
        if retried is not UNSET:
            field_dict["retried"] = retried
        if running is not UNSET:
            field_dict["running"] = running
        if success is not UNSET:
            field_dict["success"] = success
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        cancelled = d.pop("cancelled", UNSET)

        failure = d.pop("failure", UNSET)

        retried = d.pop("retried", UNSET)

        running = d.pop("running", UNSET)

        success = d.pop("success", UNSET)

        total = d.pop("total", UNSET)

        job_execution_stats = cls(
            cancelled=cancelled,
            failure=failure,
            retried=retried,
            running=running,
            success=success,
            total=total,
        )

        job_execution_stats.additional_properties = d
        return job_execution_stats

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

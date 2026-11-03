from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobExecutionStats")


@_attrs_define
class JobExecutionStats:
    """Job execution statistics

    Attributes:
        cancelled (int | Unset): Number of cancelled tasks Example: 0.
        failure (int | Unset): Number of failed tasks Example: 1.
        retried (int | Unset): Number of retried tasks Example: 2.
        running (int | Unset): Number of running tasks Example: 1.
        success (int | Unset): Number of successful tasks Example: 8.
        total (int | Unset): Total number of tasks Example: 10.
    """

    cancelled: int | Unset = UNSET
    failure: int | Unset = UNSET
    retried: int | Unset = UNSET
    running: int | Unset = UNSET
    success: int | Unset = UNSET
    total: int | Unset = UNSET
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
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

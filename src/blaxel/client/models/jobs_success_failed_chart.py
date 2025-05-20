from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.jobs_chart_value import JobsChartValue


T = TypeVar("T", bound="JobsSuccessFailedChart")


@_attrs_define
class JobsSuccessFailedChart:
    """Jobs chart

    Attributes:
        failed (Union[Unset, JobsChartValue]): Jobs CPU usage
        retried (Union[Unset, JobsChartValue]): Jobs CPU usage
        success (Union[Unset, JobsChartValue]): Jobs CPU usage
        timestamp (Union[Unset, str]): Metric timestamp
        total (Union[Unset, JobsChartValue]): Jobs CPU usage
    """

    failed: Union[Unset, "JobsChartValue"] = UNSET
    retried: Union[Unset, "JobsChartValue"] = UNSET
    success: Union[Unset, "JobsChartValue"] = UNSET
    timestamp: Union[Unset, str] = UNSET
    total: Union[Unset, "JobsChartValue"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        failed: Union[Unset, dict[str, Any]] = UNSET
        if self.failed and not isinstance(self.failed, Unset) and not isinstance(self.failed, dict):
            failed = self.failed.to_dict()
        elif self.failed and isinstance(self.failed, dict):
            failed = self.failed

        retried: Union[Unset, dict[str, Any]] = UNSET
        if self.retried and not isinstance(self.retried, Unset) and not isinstance(self.retried, dict):
            retried = self.retried.to_dict()
        elif self.retried and isinstance(self.retried, dict):
            retried = self.retried

        success: Union[Unset, dict[str, Any]] = UNSET
        if self.success and not isinstance(self.success, Unset) and not isinstance(self.success, dict):
            success = self.success.to_dict()
        elif self.success and isinstance(self.success, dict):
            success = self.success

        timestamp = self.timestamp

        total: Union[Unset, dict[str, Any]] = UNSET
        if self.total and not isinstance(self.total, Unset) and not isinstance(self.total, dict):
            total = self.total.to_dict()
        elif self.total and isinstance(self.total, dict):
            total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if failed is not UNSET:
            field_dict["failed"] = failed
        if retried is not UNSET:
            field_dict["retried"] = retried
        if success is not UNSET:
            field_dict["success"] = success
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.jobs_chart_value import JobsChartValue

        if not src_dict:
            return None
        d = src_dict.copy()
        _failed = d.pop("failed", UNSET)
        failed: Union[Unset, JobsChartValue]
        if isinstance(_failed, Unset):
            failed = UNSET
        else:
            failed = JobsChartValue.from_dict(_failed)

        _retried = d.pop("retried", UNSET)
        retried: Union[Unset, JobsChartValue]
        if isinstance(_retried, Unset):
            retried = UNSET
        else:
            retried = JobsChartValue.from_dict(_retried)

        _success = d.pop("success", UNSET)
        success: Union[Unset, JobsChartValue]
        if isinstance(_success, Unset):
            success = UNSET
        else:
            success = JobsChartValue.from_dict(_success)

        timestamp = d.pop("timestamp", UNSET)

        _total = d.pop("total", UNSET)
        total: Union[Unset, JobsChartValue]
        if isinstance(_total, Unset):
            total = UNSET
        else:
            total = JobsChartValue.from_dict(_total)

        jobs_success_failed_chart = cls(
            failed=failed,
            retried=retried,
            success=success,
            timestamp=timestamp,
            total=total,
        )

        jobs_success_failed_chart.additional_properties = d
        return jobs_success_failed_chart

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

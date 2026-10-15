from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxScheduleExecutionStatusMetrics")


@_attrs_define
class SandboxScheduleExecutionStatusMetrics:
    """Schedule execution counts grouped by submission acceptance status.

    Attributes:
        failed (Union[Unset, int]): Number of process submissions that were not accepted.
        succeeded (Union[Unset, int]): Number of process submissions accepted by the sandbox.
    """

    failed: Union[Unset, int] = UNSET
    succeeded: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        failed = self.failed

        succeeded = self.succeeded

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if failed is not UNSET:
            field_dict["failed"] = failed
        if succeeded is not UNSET:
            field_dict["succeeded"] = succeeded

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        failed = d.pop("failed", UNSET)

        succeeded = d.pop("succeeded", UNSET)

        sandbox_schedule_execution_status_metrics = cls(
            failed=failed,
            succeeded=succeeded,
        )

        sandbox_schedule_execution_status_metrics.additional_properties = d
        return sandbox_schedule_execution_status_metrics

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

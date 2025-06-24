from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobsTotal")


@_attrs_define
class JobsTotal:
    """Jobs executions

    Attributes:
        failed (Union[Unset, int]): Failed executions
        retried (Union[Unset, int]): Retried executions
        running (Union[Unset, int]): Running executions
        success (Union[Unset, int]): Success executions
        total (Union[Unset, int]): Total executions
    """

    failed: Union[Unset, int] = UNSET
    retried: Union[Unset, int] = UNSET
    running: Union[Unset, int] = UNSET
    success: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        failed = self.failed

        retried = self.retried

        running = self.running

        success = self.success

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if failed is not UNSET:
            field_dict["failed"] = failed
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        failed = d.pop("failed", UNSET)

        retried = d.pop("retried", UNSET)

        running = d.pop("running", UNSET)

        success = d.pop("success", UNSET)

        total = d.pop("total", UNSET)

        jobs_total = cls(
            failed=failed,
            retried=retried,
            running=running,
            success=success,
            total=total,
        )

        jobs_total.additional_properties = d
        return jobs_total

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

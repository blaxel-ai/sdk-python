from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_schedule_execution_status_metrics import (
        SandboxScheduleExecutionStatusMetrics,
    )


T = TypeVar("T", bound="SandboxScheduleMetrics")


@_attrs_define
class SandboxScheduleMetrics:
    """Workspace sandbox scheduling metrics for a UTC minute window. since is inclusive and until is exclusive.

    Attributes:
        executions (Union[Unset, int]): Number of schedule execution submissions in the selected window.
        executions_by_status (Union[Unset, SandboxScheduleExecutionStatusMetrics]): Schedule execution counts grouped by
            submission acceptance status.
        sandboxes (Union[Unset, int]): Number of active sandboxes in the workspace.
        schedules (Union[Unset, int]): Number of schedules in the workspace.
        since (Union[Unset, str]): Inclusive beginning of the metrics window, normalized to a UTC minute.
        until (Union[Unset, str]): Exclusive end of the metrics window, normalized to a UTC minute.
    """

    executions: Union[Unset, int] = UNSET
    executions_by_status: Union[Unset, "SandboxScheduleExecutionStatusMetrics"] = UNSET
    sandboxes: Union[Unset, int] = UNSET
    schedules: Union[Unset, int] = UNSET
    since: Union[Unset, str] = UNSET
    until: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        executions = self.executions

        executions_by_status: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.executions_by_status
            and not isinstance(self.executions_by_status, Unset)
            and not isinstance(self.executions_by_status, dict)
        ):
            executions_by_status = self.executions_by_status.to_dict()
        elif self.executions_by_status and isinstance(self.executions_by_status, dict):
            executions_by_status = self.executions_by_status

        sandboxes = self.sandboxes

        schedules = self.schedules

        since = self.since

        until = self.until

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if executions is not UNSET:
            field_dict["executions"] = executions
        if executions_by_status is not UNSET:
            field_dict["executionsByStatus"] = executions_by_status
        if sandboxes is not UNSET:
            field_dict["sandboxes"] = sandboxes
        if schedules is not UNSET:
            field_dict["schedules"] = schedules
        if since is not UNSET:
            field_dict["since"] = since
        if until is not UNSET:
            field_dict["until"] = until

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.sandbox_schedule_execution_status_metrics import (
            SandboxScheduleExecutionStatusMetrics,
        )

        if not src_dict:
            return None
        d = src_dict.copy()
        executions = d.pop("executions", UNSET)

        _executions_by_status = d.pop("executionsByStatus", d.pop("executions_by_status", UNSET))
        executions_by_status: Union[Unset, SandboxScheduleExecutionStatusMetrics]
        if isinstance(_executions_by_status, Unset):
            executions_by_status = UNSET
        else:
            executions_by_status = SandboxScheduleExecutionStatusMetrics.from_dict(
                _executions_by_status
            )

        sandboxes = d.pop("sandboxes", UNSET)

        schedules = d.pop("schedules", UNSET)

        since = d.pop("since", UNSET)

        until = d.pop("until", UNSET)

        sandbox_schedule_metrics = cls(
            executions=executions,
            executions_by_status=executions_by_status,
            sandboxes=sandboxes,
            schedules=schedules,
            since=since,
            until=until,
        )

        sandbox_schedule_metrics.additional_properties = d
        return sandbox_schedule_metrics

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

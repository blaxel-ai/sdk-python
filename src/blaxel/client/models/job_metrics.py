from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_metrics_executions_chart import JobMetricsExecutionsChart
    from ..models.job_metrics_executions_total import JobMetricsExecutionsTotal
    from ..models.job_metrics_tasks_chart import JobMetricsTasksChart
    from ..models.job_metrics_tasks_total import JobMetricsTasksTotal


T = TypeVar("T", bound="JobMetrics")


@_attrs_define
class JobMetrics:
    """Metrics for job

    Attributes:
        billable_time (Union[Unset, list[Any]]): Billable time
        cpu_usage (Union[Unset, list[Any]]): CPU usage
        executions_chart (Union[Unset, JobMetricsExecutionsChart]): Executions chart
        executions_running (Union[Unset, list[Any]]): Executions running
        executions_total (Union[Unset, JobMetricsExecutionsTotal]): Total executions
        ram_usage (Union[Unset, list[Any]]): RAM usage
        tasks_chart (Union[Unset, JobMetricsTasksChart]): Tasks chart
        tasks_running (Union[Unset, list[Any]]): Tasks running
        tasks_total (Union[Unset, JobMetricsTasksTotal]): Total tasks
    """

    billable_time: Union[Unset, list[Any]] = UNSET
    cpu_usage: Union[Unset, list[Any]] = UNSET
    executions_chart: Union[Unset, "JobMetricsExecutionsChart"] = UNSET
    executions_running: Union[Unset, list[Any]] = UNSET
    executions_total: Union[Unset, "JobMetricsExecutionsTotal"] = UNSET
    ram_usage: Union[Unset, list[Any]] = UNSET
    tasks_chart: Union[Unset, "JobMetricsTasksChart"] = UNSET
    tasks_running: Union[Unset, list[Any]] = UNSET
    tasks_total: Union[Unset, "JobMetricsTasksTotal"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        billable_time: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.billable_time, Unset):
            billable_time = self.billable_time

        cpu_usage: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.cpu_usage, Unset):
            cpu_usage = self.cpu_usage

        executions_chart: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.executions_chart
            and not isinstance(self.executions_chart, Unset)
            and not isinstance(self.executions_chart, dict)
        ):
            executions_chart = self.executions_chart.to_dict()
        elif self.executions_chart and isinstance(self.executions_chart, dict):
            executions_chart = self.executions_chart

        executions_running: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.executions_running, Unset):
            executions_running = self.executions_running

        executions_total: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.executions_total
            and not isinstance(self.executions_total, Unset)
            and not isinstance(self.executions_total, dict)
        ):
            executions_total = self.executions_total.to_dict()
        elif self.executions_total and isinstance(self.executions_total, dict):
            executions_total = self.executions_total

        ram_usage: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.ram_usage, Unset):
            ram_usage = self.ram_usage

        tasks_chart: Union[Unset, dict[str, Any]] = UNSET
        if self.tasks_chart and not isinstance(self.tasks_chart, Unset) and not isinstance(self.tasks_chart, dict):
            tasks_chart = self.tasks_chart.to_dict()
        elif self.tasks_chart and isinstance(self.tasks_chart, dict):
            tasks_chart = self.tasks_chart

        tasks_running: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.tasks_running, Unset):
            tasks_running = self.tasks_running

        tasks_total: Union[Unset, dict[str, Any]] = UNSET
        if self.tasks_total and not isinstance(self.tasks_total, Unset) and not isinstance(self.tasks_total, dict):
            tasks_total = self.tasks_total.to_dict()
        elif self.tasks_total and isinstance(self.tasks_total, dict):
            tasks_total = self.tasks_total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if billable_time is not UNSET:
            field_dict["billableTime"] = billable_time
        if cpu_usage is not UNSET:
            field_dict["cpuUsage"] = cpu_usage
        if executions_chart is not UNSET:
            field_dict["executionsChart"] = executions_chart
        if executions_running is not UNSET:
            field_dict["executionsRunning"] = executions_running
        if executions_total is not UNSET:
            field_dict["executionsTotal"] = executions_total
        if ram_usage is not UNSET:
            field_dict["ramUsage"] = ram_usage
        if tasks_chart is not UNSET:
            field_dict["tasksChart"] = tasks_chart
        if tasks_running is not UNSET:
            field_dict["tasksRunning"] = tasks_running
        if tasks_total is not UNSET:
            field_dict["tasksTotal"] = tasks_total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.job_metrics_executions_chart import JobMetricsExecutionsChart
        from ..models.job_metrics_executions_total import JobMetricsExecutionsTotal
        from ..models.job_metrics_tasks_chart import JobMetricsTasksChart
        from ..models.job_metrics_tasks_total import JobMetricsTasksTotal

        if not src_dict:
            return None
        d = src_dict.copy()
        billable_time = cast(list[Any], d.pop("billableTime", UNSET))

        cpu_usage = cast(list[Any], d.pop("cpuUsage", UNSET))

        _executions_chart = d.pop("executionsChart", UNSET)
        executions_chart: Union[Unset, JobMetricsExecutionsChart]
        if isinstance(_executions_chart, Unset):
            executions_chart = UNSET
        else:
            executions_chart = JobMetricsExecutionsChart.from_dict(_executions_chart)

        executions_running = cast(list[Any], d.pop("executionsRunning", UNSET))

        _executions_total = d.pop("executionsTotal", UNSET)
        executions_total: Union[Unset, JobMetricsExecutionsTotal]
        if isinstance(_executions_total, Unset):
            executions_total = UNSET
        else:
            executions_total = JobMetricsExecutionsTotal.from_dict(_executions_total)

        ram_usage = cast(list[Any], d.pop("ramUsage", UNSET))

        _tasks_chart = d.pop("tasksChart", UNSET)
        tasks_chart: Union[Unset, JobMetricsTasksChart]
        if isinstance(_tasks_chart, Unset):
            tasks_chart = UNSET
        else:
            tasks_chart = JobMetricsTasksChart.from_dict(_tasks_chart)

        tasks_running = cast(list[Any], d.pop("tasksRunning", UNSET))

        _tasks_total = d.pop("tasksTotal", UNSET)
        tasks_total: Union[Unset, JobMetricsTasksTotal]
        if isinstance(_tasks_total, Unset):
            tasks_total = UNSET
        else:
            tasks_total = JobMetricsTasksTotal.from_dict(_tasks_total)

        job_metrics = cls(
            billable_time=billable_time,
            cpu_usage=cpu_usage,
            executions_chart=executions_chart,
            executions_running=executions_running,
            executions_total=executions_total,
            ram_usage=ram_usage,
            tasks_chart=tasks_chart,
            tasks_running=tasks_running,
            tasks_total=tasks_total,
        )

        job_metrics.additional_properties = d
        return job_metrics

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

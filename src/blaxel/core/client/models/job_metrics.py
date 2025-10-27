from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_metrics_executions_total import JobMetricsExecutionsTotal
    from ..models.job_metrics_tasks_total import JobMetricsTasksTotal
    from ..models.jobs_chart_value import JobsChartValue
    from ..models.jobs_success_failed_chart import JobsSuccessFailedChart


T = TypeVar("T", bound="JobMetrics")


@_attrs_define
class JobMetrics:
    """Metrics for job

    Attributes:
        billable_time (Union[Unset, list['JobsChartValue']]): Billable time
        cpu_usage (Union[Unset, list['JobsChartValue']]): CPU usage
        executions_chart (Union[Unset, list['JobsSuccessFailedChart']]): Executions chart
        executions_running (Union[Unset, list['JobsChartValue']]): Executions running
        executions_total (Union[Unset, JobMetricsExecutionsTotal]): Total executions
        ram_usage (Union[Unset, list['JobsChartValue']]): RAM usage
        tasks_chart (Union[Unset, list['JobsSuccessFailedChart']]): Tasks chart
        tasks_running (Union[Unset, list['JobsChartValue']]): Tasks running
        tasks_total (Union[Unset, JobMetricsTasksTotal]): Total tasks
    """

    billable_time: Union[Unset, list["JobsChartValue"]] = UNSET
    cpu_usage: Union[Unset, list["JobsChartValue"]] = UNSET
    executions_chart: Union[Unset, list["JobsSuccessFailedChart"]] = UNSET
    executions_running: Union[Unset, list["JobsChartValue"]] = UNSET
    executions_total: Union[Unset, "JobMetricsExecutionsTotal"] = UNSET
    ram_usage: Union[Unset, list["JobsChartValue"]] = UNSET
    tasks_chart: Union[Unset, list["JobsSuccessFailedChart"]] = UNSET
    tasks_running: Union[Unset, list["JobsChartValue"]] = UNSET
    tasks_total: Union[Unset, "JobMetricsTasksTotal"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        billable_time: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.billable_time, Unset):
            billable_time = []
            for billable_time_item_data in self.billable_time:
                if type(billable_time_item_data) is dict:
                    billable_time_item = billable_time_item_data
                else:
                    billable_time_item = billable_time_item_data.to_dict()
                billable_time.append(billable_time_item)

        cpu_usage: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.cpu_usage, Unset):
            cpu_usage = []
            for cpu_usage_item_data in self.cpu_usage:
                if type(cpu_usage_item_data) is dict:
                    cpu_usage_item = cpu_usage_item_data
                else:
                    cpu_usage_item = cpu_usage_item_data.to_dict()
                cpu_usage.append(cpu_usage_item)

        executions_chart: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.executions_chart, Unset):
            executions_chart = []
            for executions_chart_item_data in self.executions_chart:
                if type(executions_chart_item_data) is dict:
                    executions_chart_item = executions_chart_item_data
                else:
                    executions_chart_item = executions_chart_item_data.to_dict()
                executions_chart.append(executions_chart_item)

        executions_running: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.executions_running, Unset):
            executions_running = []
            for executions_running_item_data in self.executions_running:
                if type(executions_running_item_data) is dict:
                    executions_running_item = executions_running_item_data
                else:
                    executions_running_item = executions_running_item_data.to_dict()
                executions_running.append(executions_running_item)

        executions_total: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.executions_total
            and not isinstance(self.executions_total, Unset)
            and not isinstance(self.executions_total, dict)
        ):
            executions_total = self.executions_total.to_dict()
        elif self.executions_total and isinstance(self.executions_total, dict):
            executions_total = self.executions_total

        ram_usage: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ram_usage, Unset):
            ram_usage = []
            for ram_usage_item_data in self.ram_usage:
                if type(ram_usage_item_data) is dict:
                    ram_usage_item = ram_usage_item_data
                else:
                    ram_usage_item = ram_usage_item_data.to_dict()
                ram_usage.append(ram_usage_item)

        tasks_chart: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tasks_chart, Unset):
            tasks_chart = []
            for tasks_chart_item_data in self.tasks_chart:
                if type(tasks_chart_item_data) is dict:
                    tasks_chart_item = tasks_chart_item_data
                else:
                    tasks_chart_item = tasks_chart_item_data.to_dict()
                tasks_chart.append(tasks_chart_item)

        tasks_running: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tasks_running, Unset):
            tasks_running = []
            for tasks_running_item_data in self.tasks_running:
                if type(tasks_running_item_data) is dict:
                    tasks_running_item = tasks_running_item_data
                else:
                    tasks_running_item = tasks_running_item_data.to_dict()
                tasks_running.append(tasks_running_item)

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
        from ..models.job_metrics_executions_total import JobMetricsExecutionsTotal
        from ..models.job_metrics_tasks_total import JobMetricsTasksTotal
        from ..models.jobs_chart_value import JobsChartValue
        from ..models.jobs_success_failed_chart import JobsSuccessFailedChart

        if not src_dict:
            return None
        d = src_dict.copy()
        billable_time = []
        _billable_time = d.pop("billableTime", UNSET)
        for billable_time_item_data in _billable_time or []:
            billable_time_item = JobsChartValue.from_dict(billable_time_item_data)

            billable_time.append(billable_time_item)

        cpu_usage = []
        _cpu_usage = d.pop("cpuUsage", UNSET)
        for cpu_usage_item_data in _cpu_usage or []:
            cpu_usage_item = JobsChartValue.from_dict(cpu_usage_item_data)

            cpu_usage.append(cpu_usage_item)

        executions_chart = []
        _executions_chart = d.pop("executionsChart", UNSET)
        for executions_chart_item_data in _executions_chart or []:
            executions_chart_item = JobsSuccessFailedChart.from_dict(executions_chart_item_data)

            executions_chart.append(executions_chart_item)

        executions_running = []
        _executions_running = d.pop("executionsRunning", UNSET)
        for executions_running_item_data in _executions_running or []:
            executions_running_item = JobsChartValue.from_dict(executions_running_item_data)

            executions_running.append(executions_running_item)

        _executions_total = d.pop("executionsTotal", UNSET)
        executions_total: Union[Unset, JobMetricsExecutionsTotal]
        if isinstance(_executions_total, Unset):
            executions_total = UNSET
        else:
            executions_total = JobMetricsExecutionsTotal.from_dict(_executions_total)

        ram_usage = []
        _ram_usage = d.pop("ramUsage", UNSET)
        for ram_usage_item_data in _ram_usage or []:
            ram_usage_item = JobsChartValue.from_dict(ram_usage_item_data)

            ram_usage.append(ram_usage_item)

        tasks_chart = []
        _tasks_chart = d.pop("tasksChart", UNSET)
        for tasks_chart_item_data in _tasks_chart or []:
            tasks_chart_item = JobsSuccessFailedChart.from_dict(tasks_chart_item_data)

            tasks_chart.append(tasks_chart_item)

        tasks_running = []
        _tasks_running = d.pop("tasksRunning", UNSET)
        for tasks_running_item_data in _tasks_running or []:
            tasks_running_item = JobsChartValue.from_dict(tasks_running_item_data)

            tasks_running.append(tasks_running_item)

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

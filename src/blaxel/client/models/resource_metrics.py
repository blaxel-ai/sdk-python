from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.latency_metric import LatencyMetric
    from ..models.memory_allocation_metric import MemoryAllocationMetric
    from ..models.metric import Metric
    from ..models.request_duration_over_time_metrics import RequestDurationOverTimeMetrics
    from ..models.request_total_by_origin_metric import RequestTotalByOriginMetric
    from ..models.resource_metrics_request_total_per_code import ResourceMetricsRequestTotalPerCode
    from ..models.resource_metrics_rps_per_code import ResourceMetricsRpsPerCode
    from ..models.time_to_first_token_over_time_metrics import TimeToFirstTokenOverTimeMetrics
    from ..models.token_rate_metrics import TokenRateMetrics
    from ..models.token_total_metric import TokenTotalMetric


T = TypeVar("T", bound="ResourceMetrics")


@_attrs_define
class ResourceMetrics:
    """Metrics for a single resource deployment (eg. model deployment, function deployment)

    Attributes:
        inference_global (Union[Unset, list['Metric']]): Array of metrics
        last_n_requests (Union[Unset, list['Metric']]): Array of metrics
        latency (Union[Unset, LatencyMetric]): Latency metrics
        memory_allocation (Union[Unset, MemoryAllocationMetric]): Metrics for memory allocation
        model_ttft (Union[Unset, LatencyMetric]): Latency metrics
        model_ttft_over_time (Union[Unset, TimeToFirstTokenOverTimeMetrics]): Time to first token over time metrics
        request_duration_over_time (Union[Unset, RequestDurationOverTimeMetrics]): Request duration over time metrics
        request_total (Union[Unset, float]): Number of requests for the resource globally
        request_total_by_origin (Union[Unset, RequestTotalByOriginMetric]): Request total by origin metric
        request_total_per_code (Union[Unset, ResourceMetricsRequestTotalPerCode]): Number of requests for the resource
            globally per code
        rps (Union[Unset, float]): Number of requests per second for the resource globally
        rps_per_code (Union[Unset, ResourceMetricsRpsPerCode]): Number of requests per second for the resource globally
            per code
        token_rate (Union[Unset, TokenRateMetrics]): Token rate metrics
        token_total (Union[Unset, TokenTotalMetric]): Token total metric
    """

    inference_global: Union[Unset, list["Metric"]] = UNSET
    last_n_requests: Union[Unset, list["Metric"]] = UNSET
    latency: Union[Unset, "LatencyMetric"] = UNSET
    memory_allocation: Union[Unset, "MemoryAllocationMetric"] = UNSET
    model_ttft: Union[Unset, "LatencyMetric"] = UNSET
    model_ttft_over_time: Union[Unset, "TimeToFirstTokenOverTimeMetrics"] = UNSET
    request_duration_over_time: Union[Unset, "RequestDurationOverTimeMetrics"] = UNSET
    request_total: Union[Unset, float] = UNSET
    request_total_by_origin: Union[Unset, "RequestTotalByOriginMetric"] = UNSET
    request_total_per_code: Union[Unset, "ResourceMetricsRequestTotalPerCode"] = UNSET
    rps: Union[Unset, float] = UNSET
    rps_per_code: Union[Unset, "ResourceMetricsRpsPerCode"] = UNSET
    token_rate: Union[Unset, "TokenRateMetrics"] = UNSET
    token_total: Union[Unset, "TokenTotalMetric"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inference_global: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.inference_global, Unset):
            inference_global = []
            for componentsschemas_array_metric_item_data in self.inference_global:
                if type(componentsschemas_array_metric_item_data) == dict:
                    componentsschemas_array_metric_item = componentsschemas_array_metric_item_data
                else:
                    componentsschemas_array_metric_item = componentsschemas_array_metric_item_data.to_dict()
                inference_global.append(componentsschemas_array_metric_item)

        last_n_requests: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.last_n_requests, Unset):
            last_n_requests = []
            for componentsschemas_array_metric_item_data in self.last_n_requests:
                if type(componentsschemas_array_metric_item_data) == dict:
                    componentsschemas_array_metric_item = componentsschemas_array_metric_item_data
                else:
                    componentsschemas_array_metric_item = componentsschemas_array_metric_item_data.to_dict()
                last_n_requests.append(componentsschemas_array_metric_item)

        latency: Union[Unset, dict[str, Any]] = UNSET
        if self.latency and not isinstance(self.latency, Unset) and not isinstance(self.latency, dict):
            latency = self.latency.to_dict()
        elif self.latency and isinstance(self.latency, dict):
            latency = self.latency

        memory_allocation: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.memory_allocation
            and not isinstance(self.memory_allocation, Unset)
            and not isinstance(self.memory_allocation, dict)
        ):
            memory_allocation = self.memory_allocation.to_dict()
        elif self.memory_allocation and isinstance(self.memory_allocation, dict):
            memory_allocation = self.memory_allocation

        model_ttft: Union[Unset, dict[str, Any]] = UNSET
        if self.model_ttft and not isinstance(self.model_ttft, Unset) and not isinstance(self.model_ttft, dict):
            model_ttft = self.model_ttft.to_dict()
        elif self.model_ttft and isinstance(self.model_ttft, dict):
            model_ttft = self.model_ttft

        model_ttft_over_time: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.model_ttft_over_time
            and not isinstance(self.model_ttft_over_time, Unset)
            and not isinstance(self.model_ttft_over_time, dict)
        ):
            model_ttft_over_time = self.model_ttft_over_time.to_dict()
        elif self.model_ttft_over_time and isinstance(self.model_ttft_over_time, dict):
            model_ttft_over_time = self.model_ttft_over_time

        request_duration_over_time: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.request_duration_over_time
            and not isinstance(self.request_duration_over_time, Unset)
            and not isinstance(self.request_duration_over_time, dict)
        ):
            request_duration_over_time = self.request_duration_over_time.to_dict()
        elif self.request_duration_over_time and isinstance(self.request_duration_over_time, dict):
            request_duration_over_time = self.request_duration_over_time

        request_total = self.request_total

        request_total_by_origin: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.request_total_by_origin
            and not isinstance(self.request_total_by_origin, Unset)
            and not isinstance(self.request_total_by_origin, dict)
        ):
            request_total_by_origin = self.request_total_by_origin.to_dict()
        elif self.request_total_by_origin and isinstance(self.request_total_by_origin, dict):
            request_total_by_origin = self.request_total_by_origin

        request_total_per_code: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.request_total_per_code
            and not isinstance(self.request_total_per_code, Unset)
            and not isinstance(self.request_total_per_code, dict)
        ):
            request_total_per_code = self.request_total_per_code.to_dict()
        elif self.request_total_per_code and isinstance(self.request_total_per_code, dict):
            request_total_per_code = self.request_total_per_code

        rps = self.rps

        rps_per_code: Union[Unset, dict[str, Any]] = UNSET
        if self.rps_per_code and not isinstance(self.rps_per_code, Unset) and not isinstance(self.rps_per_code, dict):
            rps_per_code = self.rps_per_code.to_dict()
        elif self.rps_per_code and isinstance(self.rps_per_code, dict):
            rps_per_code = self.rps_per_code

        token_rate: Union[Unset, dict[str, Any]] = UNSET
        if self.token_rate and not isinstance(self.token_rate, Unset) and not isinstance(self.token_rate, dict):
            token_rate = self.token_rate.to_dict()
        elif self.token_rate and isinstance(self.token_rate, dict):
            token_rate = self.token_rate

        token_total: Union[Unset, dict[str, Any]] = UNSET
        if self.token_total and not isinstance(self.token_total, Unset) and not isinstance(self.token_total, dict):
            token_total = self.token_total.to_dict()
        elif self.token_total and isinstance(self.token_total, dict):
            token_total = self.token_total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if inference_global is not UNSET:
            field_dict["inferenceGlobal"] = inference_global
        if last_n_requests is not UNSET:
            field_dict["lastNRequests"] = last_n_requests
        if latency is not UNSET:
            field_dict["latency"] = latency
        if memory_allocation is not UNSET:
            field_dict["memoryAllocation"] = memory_allocation
        if model_ttft is not UNSET:
            field_dict["modelTtft"] = model_ttft
        if model_ttft_over_time is not UNSET:
            field_dict["modelTtftOverTime"] = model_ttft_over_time
        if request_duration_over_time is not UNSET:
            field_dict["requestDurationOverTime"] = request_duration_over_time
        if request_total is not UNSET:
            field_dict["requestTotal"] = request_total
        if request_total_by_origin is not UNSET:
            field_dict["requestTotalByOrigin"] = request_total_by_origin
        if request_total_per_code is not UNSET:
            field_dict["requestTotalPerCode"] = request_total_per_code
        if rps is not UNSET:
            field_dict["rps"] = rps
        if rps_per_code is not UNSET:
            field_dict["rpsPerCode"] = rps_per_code
        if token_rate is not UNSET:
            field_dict["tokenRate"] = token_rate
        if token_total is not UNSET:
            field_dict["tokenTotal"] = token_total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.latency_metric import LatencyMetric
        from ..models.memory_allocation_metric import MemoryAllocationMetric
        from ..models.metric import Metric
        from ..models.request_duration_over_time_metrics import RequestDurationOverTimeMetrics
        from ..models.request_total_by_origin_metric import RequestTotalByOriginMetric
        from ..models.resource_metrics_request_total_per_code import (
            ResourceMetricsRequestTotalPerCode,
        )
        from ..models.resource_metrics_rps_per_code import ResourceMetricsRpsPerCode
        from ..models.time_to_first_token_over_time_metrics import TimeToFirstTokenOverTimeMetrics
        from ..models.token_rate_metrics import TokenRateMetrics
        from ..models.token_total_metric import TokenTotalMetric

        if not src_dict:
            return None
        d = src_dict.copy()
        inference_global = []
        _inference_global = d.pop("inferenceGlobal", UNSET)
        for componentsschemas_array_metric_item_data in _inference_global or []:
            componentsschemas_array_metric_item = Metric.from_dict(componentsschemas_array_metric_item_data)

            inference_global.append(componentsschemas_array_metric_item)

        last_n_requests = []
        _last_n_requests = d.pop("lastNRequests", UNSET)
        for componentsschemas_array_metric_item_data in _last_n_requests or []:
            componentsschemas_array_metric_item = Metric.from_dict(componentsschemas_array_metric_item_data)

            last_n_requests.append(componentsschemas_array_metric_item)

        _latency = d.pop("latency", UNSET)
        latency: Union[Unset, LatencyMetric]
        if isinstance(_latency, Unset):
            latency = UNSET
        else:
            latency = LatencyMetric.from_dict(_latency)

        _memory_allocation = d.pop("memoryAllocation", UNSET)
        memory_allocation: Union[Unset, MemoryAllocationMetric]
        if isinstance(_memory_allocation, Unset):
            memory_allocation = UNSET
        else:
            memory_allocation = MemoryAllocationMetric.from_dict(_memory_allocation)

        _model_ttft = d.pop("modelTtft", UNSET)
        model_ttft: Union[Unset, LatencyMetric]
        if isinstance(_model_ttft, Unset):
            model_ttft = UNSET
        else:
            model_ttft = LatencyMetric.from_dict(_model_ttft)

        _model_ttft_over_time = d.pop("modelTtftOverTime", UNSET)
        model_ttft_over_time: Union[Unset, TimeToFirstTokenOverTimeMetrics]
        if isinstance(_model_ttft_over_time, Unset):
            model_ttft_over_time = UNSET
        else:
            model_ttft_over_time = TimeToFirstTokenOverTimeMetrics.from_dict(_model_ttft_over_time)

        _request_duration_over_time = d.pop("requestDurationOverTime", UNSET)
        request_duration_over_time: Union[Unset, RequestDurationOverTimeMetrics]
        if isinstance(_request_duration_over_time, Unset):
            request_duration_over_time = UNSET
        else:
            request_duration_over_time = RequestDurationOverTimeMetrics.from_dict(_request_duration_over_time)

        request_total = d.pop("requestTotal", UNSET)

        _request_total_by_origin = d.pop("requestTotalByOrigin", UNSET)
        request_total_by_origin: Union[Unset, RequestTotalByOriginMetric]
        if isinstance(_request_total_by_origin, Unset):
            request_total_by_origin = UNSET
        else:
            request_total_by_origin = RequestTotalByOriginMetric.from_dict(_request_total_by_origin)

        _request_total_per_code = d.pop("requestTotalPerCode", UNSET)
        request_total_per_code: Union[Unset, ResourceMetricsRequestTotalPerCode]
        if isinstance(_request_total_per_code, Unset):
            request_total_per_code = UNSET
        else:
            request_total_per_code = ResourceMetricsRequestTotalPerCode.from_dict(_request_total_per_code)

        rps = d.pop("rps", UNSET)

        _rps_per_code = d.pop("rpsPerCode", UNSET)
        rps_per_code: Union[Unset, ResourceMetricsRpsPerCode]
        if isinstance(_rps_per_code, Unset):
            rps_per_code = UNSET
        else:
            rps_per_code = ResourceMetricsRpsPerCode.from_dict(_rps_per_code)

        _token_rate = d.pop("tokenRate", UNSET)
        token_rate: Union[Unset, TokenRateMetrics]
        if isinstance(_token_rate, Unset):
            token_rate = UNSET
        else:
            token_rate = TokenRateMetrics.from_dict(_token_rate)

        _token_total = d.pop("tokenTotal", UNSET)
        token_total: Union[Unset, TokenTotalMetric]
        if isinstance(_token_total, Unset):
            token_total = UNSET
        else:
            token_total = TokenTotalMetric.from_dict(_token_total)

        resource_metrics = cls(
            inference_global=inference_global,
            last_n_requests=last_n_requests,
            latency=latency,
            memory_allocation=memory_allocation,
            model_ttft=model_ttft,
            model_ttft_over_time=model_ttft_over_time,
            request_duration_over_time=request_duration_over_time,
            request_total=request_total,
            request_total_by_origin=request_total_by_origin,
            request_total_per_code=request_total_per_code,
            rps=rps,
            rps_per_code=rps_per_code,
            token_rate=token_rate,
            token_total=token_total,
        )

        resource_metrics.additional_properties = d
        return resource_metrics

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

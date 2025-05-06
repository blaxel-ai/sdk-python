from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metrics_models import MetricsModels
    from ..models.metrics_request_total_per_code import MetricsRequestTotalPerCode
    from ..models.metrics_rps_per_code import MetricsRpsPerCode


T = TypeVar("T", bound="Metrics")


@_attrs_define
class Metrics:
    """Metrics for resources

    Attributes:
        agents (Union[Unset, Any]): Metrics for agents
        functions (Union[Unset, Any]): Metrics for functions
        inference_global (Union[Unset, list[Any]]): Historical requests for all resources globally
        items (Union[Unset, list[Any]]): Historical requests for all resources globally
        last_n_requests (Union[Unset, int]): Metric value
        models (Union[Unset, MetricsModels]): Metrics for models
        request_total (Union[Unset, float]): Number of requests for all resources globally
        request_total_per_code (Union[Unset, MetricsRequestTotalPerCode]): Number of requests for all resources globally
            per code
        rps (Union[Unset, float]): Number of requests per second for all resources globally
        rps_per_code (Union[Unset, MetricsRpsPerCode]): Number of requests per second for all resources globally per
            code
        sandboxes (Union[Unset, Any]): Metrics for sandboxes
    """

    agents: Union[Unset, Any] = UNSET
    functions: Union[Unset, Any] = UNSET
    inference_global: Union[Unset, list[Any]] = UNSET
    items: Union[Unset, list[Any]] = UNSET
    last_n_requests: Union[Unset, int] = UNSET
    models: Union[Unset, "MetricsModels"] = UNSET
    request_total: Union[Unset, float] = UNSET
    request_total_per_code: Union[Unset, "MetricsRequestTotalPerCode"] = UNSET
    rps: Union[Unset, float] = UNSET
    rps_per_code: Union[Unset, "MetricsRpsPerCode"] = UNSET
    sandboxes: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agents = self.agents

        functions = self.functions

        inference_global: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.inference_global, Unset):
            inference_global = self.inference_global

        items: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.items, Unset):
            items = self.items

        last_n_requests = self.last_n_requests

        models: Union[Unset, dict[str, Any]] = UNSET
        if self.models and not isinstance(self.models, Unset) and not isinstance(self.models, dict):
            models = self.models.to_dict()
        elif self.models and isinstance(self.models, dict):
            models = self.models

        request_total = self.request_total

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

        sandboxes = self.sandboxes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agents is not UNSET:
            field_dict["agents"] = agents
        if functions is not UNSET:
            field_dict["functions"] = functions
        if inference_global is not UNSET:
            field_dict["inferenceGlobal"] = inference_global
        if items is not UNSET:
            field_dict["items"] = items
        if last_n_requests is not UNSET:
            field_dict["lastNRequests"] = last_n_requests
        if models is not UNSET:
            field_dict["models"] = models
        if request_total is not UNSET:
            field_dict["requestTotal"] = request_total
        if request_total_per_code is not UNSET:
            field_dict["requestTotalPerCode"] = request_total_per_code
        if rps is not UNSET:
            field_dict["rps"] = rps
        if rps_per_code is not UNSET:
            field_dict["rpsPerCode"] = rps_per_code
        if sandboxes is not UNSET:
            field_dict["sandboxes"] = sandboxes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metrics_models import MetricsModels
        from ..models.metrics_request_total_per_code import MetricsRequestTotalPerCode
        from ..models.metrics_rps_per_code import MetricsRpsPerCode

        if not src_dict:
            return None
        d = src_dict.copy()
        agents = d.pop("agents", UNSET)

        functions = d.pop("functions", UNSET)

        inference_global = cast(list[Any], d.pop("inferenceGlobal", UNSET))

        items = cast(list[Any], d.pop("items", UNSET))

        last_n_requests = d.pop("lastNRequests", UNSET)

        _models = d.pop("models", UNSET)
        models: Union[Unset, MetricsModels]
        if isinstance(_models, Unset):
            models = UNSET
        else:
            models = MetricsModels.from_dict(_models)

        request_total = d.pop("requestTotal", UNSET)

        _request_total_per_code = d.pop("requestTotalPerCode", UNSET)
        request_total_per_code: Union[Unset, MetricsRequestTotalPerCode]
        if isinstance(_request_total_per_code, Unset):
            request_total_per_code = UNSET
        else:
            request_total_per_code = MetricsRequestTotalPerCode.from_dict(_request_total_per_code)

        rps = d.pop("rps", UNSET)

        _rps_per_code = d.pop("rpsPerCode", UNSET)
        rps_per_code: Union[Unset, MetricsRpsPerCode]
        if isinstance(_rps_per_code, Unset):
            rps_per_code = UNSET
        else:
            rps_per_code = MetricsRpsPerCode.from_dict(_rps_per_code)

        sandboxes = d.pop("sandboxes", UNSET)

        metrics = cls(
            agents=agents,
            functions=functions,
            inference_global=inference_global,
            items=items,
            last_n_requests=last_n_requests,
            models=models,
            request_total=request_total,
            request_total_per_code=request_total_per_code,
            rps=rps,
            rps_per_code=rps_per_code,
            sandboxes=sandboxes,
        )

        metrics.additional_properties = d
        return metrics

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

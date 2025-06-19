from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenRateMetric")


@_attrs_define
class TokenRateMetric:
    """Token rate metric

    Attributes:
        model (Union[Unset, str]): Model ID
        provider (Union[Unset, str]): Provider name
        provider_name (Union[Unset, str]): Provider integration name
        timestamp (Union[Unset, str]): Timestamp
        token_total (Union[Unset, float]): Total tokens
        trend (Union[Unset, float]): Trend
    """

    model: Union[Unset, str] = UNSET
    provider: Union[Unset, str] = UNSET
    provider_name: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    token_total: Union[Unset, float] = UNSET
    trend: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model = self.model

        provider = self.provider

        provider_name = self.provider_name

        timestamp = self.timestamp

        token_total = self.token_total

        trend = self.trend

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if model is not UNSET:
            field_dict["model"] = model
        if provider is not UNSET:
            field_dict["provider"] = provider
        if provider_name is not UNSET:
            field_dict["providerName"] = provider_name
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if token_total is not UNSET:
            field_dict["tokenTotal"] = token_total
        if trend is not UNSET:
            field_dict["trend"] = trend

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        model = d.pop("model", UNSET)

        provider = d.pop("provider", UNSET)

        provider_name = d.pop("providerName", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        token_total = d.pop("tokenTotal", UNSET)

        trend = d.pop("trend", UNSET)

        token_rate_metric = cls(
            model=model,
            provider=provider,
            provider_name=provider_name,
            timestamp=timestamp,
            token_total=token_total,
            trend=trend,
        )

        token_rate_metric.additional_properties = d
        return token_rate_metric

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

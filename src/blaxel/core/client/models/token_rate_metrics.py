from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.token_rate_metric import TokenRateMetric


T = TypeVar("T", bound="TokenRateMetrics")


@_attrs_define
class TokenRateMetrics:
    """Token rate metrics

    Attributes:
        token_rate (Union[Unset, TokenRateMetric]): Token rate metric
        token_rate_input (Union[Unset, TokenRateMetric]): Token rate metric
        token_rate_output (Union[Unset, TokenRateMetric]): Token rate metric
    """

    token_rate: Union[Unset, "TokenRateMetric"] = UNSET
    token_rate_input: Union[Unset, "TokenRateMetric"] = UNSET
    token_rate_output: Union[Unset, "TokenRateMetric"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token_rate: Union[Unset, dict[str, Any]] = UNSET
        if self.token_rate and not isinstance(self.token_rate, Unset) and not isinstance(self.token_rate, dict):
            token_rate = self.token_rate.to_dict()
        elif self.token_rate and isinstance(self.token_rate, dict):
            token_rate = self.token_rate

        token_rate_input: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.token_rate_input
            and not isinstance(self.token_rate_input, Unset)
            and not isinstance(self.token_rate_input, dict)
        ):
            token_rate_input = self.token_rate_input.to_dict()
        elif self.token_rate_input and isinstance(self.token_rate_input, dict):
            token_rate_input = self.token_rate_input

        token_rate_output: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.token_rate_output
            and not isinstance(self.token_rate_output, Unset)
            and not isinstance(self.token_rate_output, dict)
        ):
            token_rate_output = self.token_rate_output.to_dict()
        elif self.token_rate_output and isinstance(self.token_rate_output, dict):
            token_rate_output = self.token_rate_output

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if token_rate is not UNSET:
            field_dict["tokenRate"] = token_rate
        if token_rate_input is not UNSET:
            field_dict["tokenRateInput"] = token_rate_input
        if token_rate_output is not UNSET:
            field_dict["tokenRateOutput"] = token_rate_output

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.token_rate_metric import TokenRateMetric

        if not src_dict:
            return None
        d = src_dict.copy()
        _token_rate = d.pop("tokenRate", UNSET)
        token_rate: Union[Unset, TokenRateMetric]
        if isinstance(_token_rate, Unset):
            token_rate = UNSET
        else:
            token_rate = TokenRateMetric.from_dict(_token_rate)

        _token_rate_input = d.pop("tokenRateInput", UNSET)
        token_rate_input: Union[Unset, TokenRateMetric]
        if isinstance(_token_rate_input, Unset):
            token_rate_input = UNSET
        else:
            token_rate_input = TokenRateMetric.from_dict(_token_rate_input)

        _token_rate_output = d.pop("tokenRateOutput", UNSET)
        token_rate_output: Union[Unset, TokenRateMetric]
        if isinstance(_token_rate_output, Unset):
            token_rate_output = UNSET
        else:
            token_rate_output = TokenRateMetric.from_dict(_token_rate_output)

        token_rate_metrics = cls(
            token_rate=token_rate,
            token_rate_input=token_rate_input,
            token_rate_output=token_rate_output,
        )

        token_rate_metrics.additional_properties = d
        return token_rate_metrics

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

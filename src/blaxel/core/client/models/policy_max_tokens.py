from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PolicyMaxTokens")


@_attrs_define
class PolicyMaxTokens:
    """PolicyMaxTokens is a local type that wraps a slice of PolicyMaxTokens

    Attributes:
        granularity (Union[Unset, str]): Granularity
        input_ (Union[Unset, int]): Input
        output (Union[Unset, int]): Output
        ratio_input_over_output (Union[Unset, int]): RatioInputOverOutput
        step (Union[Unset, int]): Step
        total (Union[Unset, int]): Total
    """

    granularity: Union[Unset, str] = UNSET
    input_: Union[Unset, int] = UNSET
    output: Union[Unset, int] = UNSET
    ratio_input_over_output: Union[Unset, int] = UNSET
    step: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        granularity = self.granularity

        input_ = self.input_

        output = self.output

        ratio_input_over_output = self.ratio_input_over_output

        step = self.step

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if granularity is not UNSET:
            field_dict["granularity"] = granularity
        if input_ is not UNSET:
            field_dict["input"] = input_
        if output is not UNSET:
            field_dict["output"] = output
        if ratio_input_over_output is not UNSET:
            field_dict["ratioInputOverOutput"] = ratio_input_over_output
        if step is not UNSET:
            field_dict["step"] = step
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        granularity = d.pop("granularity", UNSET)

        input_ = d.pop("input", UNSET)

        output = d.pop("output", UNSET)

        ratio_input_over_output = d.pop("ratioInputOverOutput", UNSET)

        step = d.pop("step", UNSET)

        total = d.pop("total", UNSET)

        policy_max_tokens = cls(
            granularity=granularity,
            input_=input_,
            output=output,
            ratio_input_over_output=ratio_input_over_output,
            step=step,
            total=total,
        )

        policy_max_tokens.additional_properties = d
        return policy_max_tokens

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

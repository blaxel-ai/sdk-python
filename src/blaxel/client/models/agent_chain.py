from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentChain")


@_attrs_define
class AgentChain:
    """Agent chain configuration

    Attributes:
        description (Union[Unset, str]): Description of the agent in case you want to override the default one
        enabled (Union[Unset, bool]): Whether the agent chain is enabled
        name (Union[Unset, str]): The name of the agent to chain to
        prompt (Union[Unset, str]): Prompt of the agent in case you want to override the default one
    """

    description: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    prompt: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        enabled = self.enabled

        name = self.name

        prompt = self.prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if name is not UNSET:
            field_dict["name"] = name
        if prompt is not UNSET:
            field_dict["prompt"] = prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        enabled = d.pop("enabled", UNSET)

        name = d.pop("name", UNSET)

        prompt = d.pop("prompt", UNSET)

        agent_chain = cls(
            description=description,
            enabled=enabled,
            name=name,
            prompt=prompt,
        )

        agent_chain.additional_properties = d
        return agent_chain

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

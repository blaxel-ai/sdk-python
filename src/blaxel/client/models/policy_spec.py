from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flavor import Flavor
    from ..models.policy_location import PolicyLocation
    from ..models.policy_max_tokens import PolicyMaxTokens


T = TypeVar("T", bound="PolicySpec")


@_attrs_define
class PolicySpec:
    """Policy specification

    Attributes:
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        locations (Union[Unset, list['PolicyLocation']]): PolicyLocations is a local type that wraps a slice of Location
        max_tokens (Union[Unset, PolicyMaxTokens]): PolicyMaxTokens is a local type that wraps a slice of
            PolicyMaxTokens
        resource_types (Union[Unset, list[str]]): PolicyResourceTypes is a local type that wraps a slice of
            PolicyResourceType
        sandbox (Union[Unset, bool]): Sandbox mode
        type_ (Union[Unset, str]): Policy type, can be location or flavor
    """

    flavors: Union[Unset, list["Flavor"]] = UNSET
    locations: Union[Unset, list["PolicyLocation"]] = UNSET
    max_tokens: Union[Unset, "PolicyMaxTokens"] = UNSET
    resource_types: Union[Unset, list[str]] = UNSET
    sandbox: Union[Unset, bool] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flavors: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.flavors, Unset):
            flavors = []
            for componentsschemas_flavors_item_data in self.flavors:
                if type(componentsschemas_flavors_item_data) == dict:
                    componentsschemas_flavors_item = componentsschemas_flavors_item_data
                else:
                    componentsschemas_flavors_item = componentsschemas_flavors_item_data.to_dict()
                flavors.append(componentsschemas_flavors_item)

        locations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.locations, Unset):
            locations = []
            for componentsschemas_policy_locations_item_data in self.locations:
                if type(componentsschemas_policy_locations_item_data) == dict:
                    componentsschemas_policy_locations_item = componentsschemas_policy_locations_item_data
                else:
                    componentsschemas_policy_locations_item = componentsschemas_policy_locations_item_data.to_dict()
                locations.append(componentsschemas_policy_locations_item)

        max_tokens: Union[Unset, dict[str, Any]] = UNSET
        if self.max_tokens and not isinstance(self.max_tokens, Unset) and not isinstance(self.max_tokens, dict):
            max_tokens = self.max_tokens.to_dict()
        elif self.max_tokens and isinstance(self.max_tokens, dict):
            max_tokens = self.max_tokens

        resource_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.resource_types, Unset):
            resource_types = self.resource_types

        sandbox = self.sandbox

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if flavors is not UNSET:
            field_dict["flavors"] = flavors
        if locations is not UNSET:
            field_dict["locations"] = locations
        if max_tokens is not UNSET:
            field_dict["maxTokens"] = max_tokens
        if resource_types is not UNSET:
            field_dict["resourceTypes"] = resource_types
        if sandbox is not UNSET:
            field_dict["sandbox"] = sandbox
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.flavor import Flavor
        from ..models.policy_location import PolicyLocation
        from ..models.policy_max_tokens import PolicyMaxTokens

        if not src_dict:
            return None
        d = src_dict.copy()
        flavors = []
        _flavors = d.pop("flavors", UNSET)
        for componentsschemas_flavors_item_data in _flavors or []:
            componentsschemas_flavors_item = Flavor.from_dict(componentsschemas_flavors_item_data)

            flavors.append(componentsschemas_flavors_item)

        locations = []
        _locations = d.pop("locations", UNSET)
        for componentsschemas_policy_locations_item_data in _locations or []:
            componentsschemas_policy_locations_item = PolicyLocation.from_dict(
                componentsschemas_policy_locations_item_data
            )

            locations.append(componentsschemas_policy_locations_item)

        _max_tokens = d.pop("maxTokens", UNSET)
        max_tokens: Union[Unset, PolicyMaxTokens]
        if isinstance(_max_tokens, Unset):
            max_tokens = UNSET
        else:
            max_tokens = PolicyMaxTokens.from_dict(_max_tokens)

        resource_types = cast(list[str], d.pop("resourceTypes", UNSET))

        sandbox = d.pop("sandbox", UNSET)

        type_ = d.pop("type", UNSET)

        policy_spec = cls(
            flavors=flavors,
            locations=locations,
            max_tokens=max_tokens,
            resource_types=resource_types,
            sandbox=sandbox,
            type_=type_,
        )

        policy_spec.additional_properties = d
        return policy_spec

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

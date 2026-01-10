from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.expiration_policy import ExpirationPolicy


T = TypeVar("T", bound="SandboxLifecycle")


@_attrs_define
class SandboxLifecycle:
    """Lifecycle configuration controlling automatic sandbox deletion based on idle time, max age, or specific dates

    Attributes:
        expiration_policies (Union[Unset, list['ExpirationPolicy']]): List of expiration policies. Multiple policies can
            be combined; whichever condition is met first triggers the action.
    """

    expiration_policies: Union[Unset, list["ExpirationPolicy"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expiration_policies: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.expiration_policies, Unset):
            expiration_policies = []
            for expiration_policies_item_data in self.expiration_policies:
                if type(expiration_policies_item_data) is dict:
                    expiration_policies_item = expiration_policies_item_data
                else:
                    expiration_policies_item = expiration_policies_item_data.to_dict()
                expiration_policies.append(expiration_policies_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expiration_policies is not UNSET:
            field_dict["expirationPolicies"] = expiration_policies

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.expiration_policy import ExpirationPolicy

        if not src_dict:
            return None
        d = src_dict.copy()
        expiration_policies = []
        _expiration_policies = d.pop("expirationPolicies", d.pop("expiration_policies", UNSET))
        for expiration_policies_item_data in _expiration_policies or []:
            expiration_policies_item = ExpirationPolicy.from_dict(expiration_policies_item_data)

            expiration_policies.append(expiration_policies_item)

        sandbox_lifecycle = cls(
            expiration_policies=expiration_policies,
        )

        sandbox_lifecycle.additional_properties = d
        return sandbox_lifecycle

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

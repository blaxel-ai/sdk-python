from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.policy_spec import PolicySpec


T = TypeVar("T", bound="Policy")


@_attrs_define
class Policy:
    """Rule that controls how a deployment is made and served (e.g. location restrictions)

    Attributes:
        metadata (Metadata): Common metadata fields shared by all Blaxel resources including name, labels, timestamps,
            and ownership information
        spec (PolicySpec): Policy specification
    """

    metadata: "Metadata"
    spec: "PolicySpec"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        if type(self.metadata) is dict:
            metadata = self.metadata
        else:
            metadata = self.metadata.to_dict()

        if type(self.spec) is dict:
            spec = self.spec
        else:
            spec = self.spec.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata": metadata,
                "spec": spec,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.metadata import Metadata
        from ..models.policy_spec import PolicySpec

        if not src_dict:
            return None
        d = src_dict.copy()
        metadata = Metadata.from_dict(d.pop("metadata"))

        spec = PolicySpec.from_dict(d.pop("spec"))

        policy = cls(
            metadata=metadata,
            spec=spec,
        )

        policy.additional_properties = d
        return policy

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

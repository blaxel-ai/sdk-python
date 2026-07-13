from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.policy_spec import PolicySpec
    from ..models.policy_usage_counts import PolicyUsageCounts


T = TypeVar("T", bound="Policy")


@_attrs_define
class Policy:
    """Rule that controls how a deployment is made and served (e.g. location restrictions)

    Attributes:
        metadata (Metadata): Common metadata fields shared by all Blaxel resources including name, labels, timestamps,
            and ownership information
        spec (PolicySpec): Policy specification
        usage (Union[Unset, PolicyUsageCounts]): Per-resource counts of how many resources reference a policy. Computed
            by the policies listing endpoint to avoid client-side fan-out across the agents/models/functions/sandboxes/jobs
            listings.
    """

    metadata: "Metadata"
    spec: "PolicySpec"
    usage: Union[Unset, "PolicyUsageCounts"] = UNSET
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

        usage: Union[Unset, dict[str, Any]] = UNSET
        if self.usage and not isinstance(self.usage, Unset) and not isinstance(self.usage, dict):
            usage = self.usage.to_dict()
        elif self.usage and isinstance(self.usage, dict):
            usage = self.usage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata": metadata,
                "spec": spec,
            }
        )
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.metadata import Metadata
        from ..models.policy_spec import PolicySpec
        from ..models.policy_usage_counts import PolicyUsageCounts

        if not src_dict:
            return None
        d = src_dict.copy()
        metadata = Metadata.from_dict(d.pop("metadata"))

        spec = PolicySpec.from_dict(d.pop("spec"))

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, PolicyUsageCounts]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = PolicyUsageCounts.from_dict(_usage)

        policy = cls(
            metadata=metadata,
            spec=spec,
            usage=usage,
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

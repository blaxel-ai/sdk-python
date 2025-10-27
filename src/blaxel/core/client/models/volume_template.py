from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.volume_template_spec import VolumeTemplateSpec
    from ..models.volume_template_state import VolumeTemplateState
    from ..models.volume_template_version import VolumeTemplateVersion


T = TypeVar("T", bound="VolumeTemplate")


@_attrs_define
class VolumeTemplate:
    """Volume template for creating pre-configured volumes

    Attributes:
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, VolumeTemplateSpec]): Volume template specification
        state (Union[Unset, VolumeTemplateState]): Volume template state
        versions (Union[Unset, list['VolumeTemplateVersion']]): List of versions for this template
    """

    metadata: Union[Unset, "Metadata"] = UNSET
    spec: Union[Unset, "VolumeTemplateSpec"] = UNSET
    state: Union[Unset, "VolumeTemplateState"] = UNSET
    versions: Union[Unset, list["VolumeTemplateVersion"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata: Union[Unset, dict[str, Any]] = UNSET
        if self.metadata and not isinstance(self.metadata, Unset) and not isinstance(self.metadata, dict):
            metadata = self.metadata.to_dict()
        elif self.metadata and isinstance(self.metadata, dict):
            metadata = self.metadata

        spec: Union[Unset, dict[str, Any]] = UNSET
        if self.spec and not isinstance(self.spec, Unset) and not isinstance(self.spec, dict):
            spec = self.spec.to_dict()
        elif self.spec and isinstance(self.spec, dict):
            spec = self.spec

        state: Union[Unset, dict[str, Any]] = UNSET
        if self.state and not isinstance(self.state, Unset) and not isinstance(self.state, dict):
            state = self.state.to_dict()
        elif self.state and isinstance(self.state, dict):
            state = self.state

        versions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.versions, Unset):
            versions = []
            for versions_item_data in self.versions:
                if type(versions_item_data) is dict:
                    versions_item = versions_item_data
                else:
                    versions_item = versions_item_data.to_dict()
                versions.append(versions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if spec is not UNSET:
            field_dict["spec"] = spec
        if state is not UNSET:
            field_dict["state"] = state
        if versions is not UNSET:
            field_dict["versions"] = versions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metadata import Metadata
        from ..models.volume_template_spec import VolumeTemplateSpec
        from ..models.volume_template_state import VolumeTemplateState
        from ..models.volume_template_version import VolumeTemplateVersion

        if not src_dict:
            return None
        d = src_dict.copy()
        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, Metadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        _spec = d.pop("spec", UNSET)
        spec: Union[Unset, VolumeTemplateSpec]
        if isinstance(_spec, Unset):
            spec = UNSET
        else:
            spec = VolumeTemplateSpec.from_dict(_spec)

        _state = d.pop("state", UNSET)
        state: Union[Unset, VolumeTemplateState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = VolumeTemplateState.from_dict(_state)

        versions = []
        _versions = d.pop("versions", UNSET)
        for versions_item_data in _versions or []:
            versions_item = VolumeTemplateVersion.from_dict(versions_item_data)

            versions.append(versions_item)

        volume_template = cls(
            metadata=metadata,
            spec=spec,
            state=state,
            versions=versions,
        )

        volume_template.additional_properties = d
        return volume_template

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

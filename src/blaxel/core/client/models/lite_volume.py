from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.lite_volume_metadata import LiteVolumeMetadata
    from ..models.lite_volume_spec import LiteVolumeSpec
    from ..models.volume_state import VolumeState


T = TypeVar("T", bound="LiteVolume")


@_attrs_define
class LiteVolume:
    """LiteVolume is the listing-shape projection of a Volume. Drops events to keep page payloads small.

    Attributes:
        metadata (LiteVolumeMetadata | Unset): Compact metadata for a Volume, returned in listing responses.
        spec (LiteVolumeSpec | Unset): Compact spec for a Volume, returned in listing responses.
        state (VolumeState | Unset): Current runtime state of the volume including attachment status
        status (str | Unset): Computed status of the volume.
        terminated_at (str | Unset): Termination timestamp for soft-deleted volumes.
    """

    metadata: LiteVolumeMetadata | Unset = UNSET
    spec: LiteVolumeSpec | Unset = UNSET
    state: VolumeState | Unset = UNSET
    status: str | Unset = UNSET
    terminated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata: dict[str, Any] | Unset = UNSET
        if (
            self.metadata
            and not isinstance(self.metadata, Unset)
            and not isinstance(self.metadata, dict)
        ):
            metadata = self.metadata.to_dict()
        elif self.metadata and isinstance(self.metadata, dict):
            metadata = self.metadata

        spec: dict[str, Any] | Unset = UNSET
        if self.spec and not isinstance(self.spec, Unset) and not isinstance(self.spec, dict):
            spec = self.spec.to_dict()
        elif self.spec and isinstance(self.spec, dict):
            spec = self.spec

        state: dict[str, Any] | Unset = UNSET
        if self.state and not isinstance(self.state, Unset) and not isinstance(self.state, dict):
            state = self.state.to_dict()
        elif self.state and isinstance(self.state, dict):
            state = self.state

        status = self.status

        terminated_at = self.terminated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if spec is not UNSET:
            field_dict["spec"] = spec
        if state is not UNSET:
            field_dict["state"] = state
        if status is not UNSET:
            field_dict["status"] = status
        if terminated_at is not UNSET:
            field_dict["terminatedAt"] = terminated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.lite_volume_metadata import LiteVolumeMetadata  # noqa: PLC0415
        from ..models.lite_volume_spec import LiteVolumeSpec  # noqa: PLC0415
        from ..models.volume_state import VolumeState  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        _metadata = d.pop("metadata", UNSET)
        metadata: LiteVolumeMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = LiteVolumeMetadata.from_dict(_metadata)

        _spec = d.pop("spec", UNSET)
        spec: LiteVolumeSpec | Unset
        if isinstance(_spec, Unset):
            spec = UNSET
        else:
            spec = LiteVolumeSpec.from_dict(_spec)

        _state = d.pop("state", UNSET)
        state: VolumeState | Unset
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = VolumeState.from_dict(_state)

        status = d.pop("status", UNSET)

        terminated_at = d.pop("terminatedAt", d.pop("terminated_at", UNSET))

        lite_volume = cls(
            metadata=metadata,
            spec=spec,
            state=state,
            status=status,
            terminated_at=terminated_at,
        )

        lite_volume.additional_properties = d
        return lite_volume

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

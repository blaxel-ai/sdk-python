from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_creation_options_extra_args import SandboxCreationOptionsExtraArgs
    from ..models.volume_attachment import VolumeAttachment


T = TypeVar("T", bound="SandboxCreationOptions")


@_attrs_define
class SandboxCreationOptions:
    """Optional Hub template settings applied by the console without additional sandbox creation lookups.

    Attributes:
        extra_args (Union[Unset, SandboxCreationOptionsExtraArgs]): Kernel selection arguments copied into
            runtime.extraArgs. At most 8 entries.
        volumes (Union[Unset, list['VolumeAttachment']]): Volume attachments included in the creation request. At most 5
            attachments per template.
    """

    extra_args: Union[Unset, "SandboxCreationOptionsExtraArgs"] = UNSET
    volumes: Union[Unset, list["VolumeAttachment"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        extra_args: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.extra_args
            and not isinstance(self.extra_args, Unset)
            and not isinstance(self.extra_args, dict)
        ):
            extra_args = self.extra_args.to_dict()
        elif self.extra_args and isinstance(self.extra_args, dict):
            extra_args = self.extra_args

        volumes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.volumes, Unset):
            volumes = []
            for volumes_item_data in self.volumes:
                if type(volumes_item_data) is dict:
                    volumes_item = volumes_item_data
                else:
                    volumes_item = volumes_item_data.to_dict()
                volumes.append(volumes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if extra_args is not UNSET:
            field_dict["extraArgs"] = extra_args
        if volumes is not UNSET:
            field_dict["volumes"] = volumes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.sandbox_creation_options_extra_args import SandboxCreationOptionsExtraArgs
        from ..models.volume_attachment import VolumeAttachment

        if not src_dict:
            return None
        d = src_dict.copy()
        _extra_args = d.pop("extraArgs", d.pop("extra_args", UNSET))
        extra_args: Union[Unset, SandboxCreationOptionsExtraArgs]
        if isinstance(_extra_args, Unset):
            extra_args = UNSET
        else:
            extra_args = SandboxCreationOptionsExtraArgs.from_dict(_extra_args)

        volumes = []
        _volumes = d.pop("volumes", UNSET)
        for volumes_item_data in _volumes or []:
            volumes_item = VolumeAttachment.from_dict(volumes_item_data)

            volumes.append(volumes_item)

        sandbox_creation_options = cls(
            extra_args=extra_args,
            volumes=volumes,
        )

        sandbox_creation_options.additional_properties = d
        return sandbox_creation_options

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

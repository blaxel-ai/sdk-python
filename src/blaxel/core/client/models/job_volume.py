from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_volume_type import JobVolumeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="JobVolume")


@_attrs_define
class JobVolume:
    """Ephemeral volume for a job. Temporary disk-backed storage that is created when the job starts and destroyed when it
    completes.

        Attributes:
            mount_path (str): Absolute filesystem path where the volume will be mounted inside the container Example:
                /mnt/data.
            name (str): Identifier for the volume, used to reference it internally Example: scratch.
            size_mb (int): Storage capacity in megabytes Example: 102400.
            type_ (JobVolumeType): Type of volume. Currently only "ephemeral" is supported. Example: ephemeral.
            read_only (Union[Unset, bool]): If true, the volume is mounted read-only
    """

    mount_path: str
    name: str
    size_mb: int
    type_: JobVolumeType
    read_only: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mount_path = self.mount_path

        name = self.name

        size_mb = self.size_mb

        type_ = self.type_.value

        read_only = self.read_only

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mountPath": mount_path,
                "name": name,
                "sizeMb": size_mb,
                "type": type_,
            }
        )
        if read_only is not UNSET:
            field_dict["readOnly"] = read_only

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        mount_path = d.pop("mountPath") if "mountPath" in d else d.pop("mount_path")

        name = d.pop("name")

        size_mb = d.pop("sizeMb") if "sizeMb" in d else d.pop("size_mb")

        type_ = JobVolumeType(d.pop("type") if "type" in d else d.pop("type_"))

        read_only = d.pop("readOnly", d.pop("read_only", UNSET))

        job_volume = cls(
            mount_path=mount_path,
            name=name,
            size_mb=size_mb,
            type_=type_,
            read_only=read_only,
        )

        job_volume.additional_properties = d
        return job_volume

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

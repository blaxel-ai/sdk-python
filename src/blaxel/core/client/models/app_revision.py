from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.env import Env


T = TypeVar("T", bound="AppRevision")


@_attrs_define
class AppRevision:
    """A single application revision containing the deployed image and configuration

    Attributes:
        image (str): Container image for this revision (mandatory)
        created_at (str | Unset): When this revision was created
        created_by (str | Unset): Who created this revision
        envs (list[Env] | Unset): Environment variables for this revision
        id (str | Unset): Unique revision identifier
        memory (int | Unset): Memory allocation in megabytes. Determines CPU allocation (CPU = memory / 2048). Example:
            2048.
        port (int | Unset): Port the application listens on for this revision (default uses spec-level port or 8080)
            Example: 8080.
        snapshot (str | Unset): Snapshot ID this revision was forked from (optional, only set when created via fork)
    """

    image: str
    created_at: str | Unset = UNSET
    created_by: str | Unset = UNSET
    envs: list[Env] | Unset = UNSET
    id: str | Unset = UNSET
    memory: int | Unset = UNSET
    port: int | Unset = UNSET
    snapshot: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image = self.image

        created_at = self.created_at

        created_by = self.created_by

        envs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.envs, Unset):
            envs = []
            for envs_item_data in self.envs:
                if type(envs_item_data) is dict:
                    envs_item = envs_item_data
                else:
                    envs_item = envs_item_data.to_dict()
                envs.append(envs_item)

        id = self.id

        memory = self.memory

        port = self.port

        snapshot = self.snapshot

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
            }
        )
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if envs is not UNSET:
            field_dict["envs"] = envs
        if id is not UNSET:
            field_dict["id"] = id
        if memory is not UNSET:
            field_dict["memory"] = memory
        if port is not UNSET:
            field_dict["port"] = port
        if snapshot is not UNSET:
            field_dict["snapshot"] = snapshot

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.env import Env  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        image = d.pop("image")

        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        created_by = d.pop("createdBy", d.pop("created_by", UNSET))

        envs = []
        _envs = d.pop("envs", UNSET)
        for envs_item_data in _envs or []:
            envs_item = Env.from_dict(envs_item_data)

            envs.append(envs_item)

        id = d.pop("id", UNSET)

        memory = d.pop("memory", UNSET)

        port = d.pop("port", UNSET)

        snapshot = d.pop("snapshot", UNSET)

        app_revision = cls(
            image=image,
            created_at=created_at,
            created_by=created_by,
            envs=envs,
            id=id,
            memory=memory,
            port=port,
            snapshot=snapshot,
        )

        app_revision.additional_properties = d
        return app_revision

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

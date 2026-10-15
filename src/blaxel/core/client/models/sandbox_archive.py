from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sandbox_archive_restore import SandboxArchiveRestore


T = TypeVar("T", bound="SandboxArchive")


@_attrs_define
class SandboxArchive:
    """State of the filesystem archive of a sandbox. An archive holds the writable filesystem changes and the process
    configurations of the sandbox, not its memory, so restoring it produces a sandbox with the same disk state and
    freshly started processes.

        Attributes:
            created_at (Union[Unset, str]): When the archive was created (read-only)
            generation (Union[Unset, str]): Infrastructure generation the archive was taken from (read-only) Example: mk3.0.
            key (Union[Unset, str]): Storage key of the archive (read-only) Example: my-workspace/my-sandbox.tar.
            restore (Union[Unset, SandboxArchiveRestore]): Progress of the restore of a sandbox archive. A restore writes
                the archived filesystem over the image the sandbox booted from, which takes as long as the archive is big; the
                sandbox answers and its terminal is reachable throughout, but nothing may write to its filesystem until the
                restore is done.
            restore_started_at (Union[Unset, str]): When the restore of the archive started, while the sandbox is being
                unarchived (read-only)
            size (Union[Unset, int]): Size of the archive in bytes (read-only)
            started_at (Union[Unset, str]): When the archive was started, while the filesystem of the sandbox is still being
                uploaded (read-only)
    """

    created_at: Union[Unset, str] = UNSET
    generation: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    restore: Union[Unset, "SandboxArchiveRestore"] = UNSET
    restore_started_at: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    started_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        created_at = self.created_at

        generation = self.generation

        key = self.key

        restore: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.restore
            and not isinstance(self.restore, Unset)
            and not isinstance(self.restore, dict)
        ):
            restore = self.restore.to_dict()
        elif self.restore and isinstance(self.restore, dict):
            restore = self.restore

        restore_started_at = self.restore_started_at

        size = self.size

        started_at = self.started_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if generation is not UNSET:
            field_dict["generation"] = generation
        if key is not UNSET:
            field_dict["key"] = key
        if restore is not UNSET:
            field_dict["restore"] = restore
        if restore_started_at is not UNSET:
            field_dict["restoreStartedAt"] = restore_started_at
        if size is not UNSET:
            field_dict["size"] = size
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.sandbox_archive_restore import SandboxArchiveRestore

        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        generation = d.pop("generation", UNSET)

        key = d.pop("key", UNSET)

        _restore = d.pop("restore", UNSET)
        restore: Union[Unset, SandboxArchiveRestore]
        if isinstance(_restore, Unset):
            restore = UNSET
        else:
            restore = SandboxArchiveRestore.from_dict(_restore)

        restore_started_at = d.pop("restoreStartedAt", d.pop("restore_started_at", UNSET))

        size = d.pop("size", UNSET)

        started_at = d.pop("startedAt", d.pop("started_at", UNSET))

        sandbox_archive = cls(
            created_at=created_at,
            generation=generation,
            key=key,
            restore=restore,
            restore_started_at=restore_started_at,
            size=size,
            started_at=started_at,
        )

        sandbox_archive.additional_properties = d
        return sandbox_archive

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

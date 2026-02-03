from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.upgrade_status import UpgradeStatus


T = TypeVar("T", bound="HealthResponse")


@_attrs_define
class HealthResponse:
    """
    Attributes:
        arch (str):  Example: amd64.
        build_time (str):  Example: 2026-01-29 17:36:52+00:00.
        git_commit (str):  Example: abc123.
        go_version (str):  Example: go1.25.0.
        last_upgrade (UpgradeStatus):
        os (str):  Example: linux.
        started_at (str):  Example: 2026-01-29 18:45:49+00:00.
        status (str):  Example: ok.
        upgrade_count (int):
        uptime (str):  Example: 1h30m.
        uptime_seconds (float):  Example: 5400.5.
        version (str):  Example: v0.1.0.
    """

    arch: str
    build_time: str
    git_commit: str
    go_version: str
    last_upgrade: "UpgradeStatus"
    os: str
    started_at: str
    status: str
    upgrade_count: int
    uptime: str
    uptime_seconds: float
    version: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        arch = self.arch

        build_time = self.build_time

        git_commit = self.git_commit

        go_version = self.go_version

        if type(self.last_upgrade) is dict:
            last_upgrade = self.last_upgrade
        else:
            last_upgrade = self.last_upgrade.to_dict()

        os = self.os

        started_at = self.started_at

        status = self.status

        upgrade_count = self.upgrade_count

        uptime = self.uptime

        uptime_seconds = self.uptime_seconds

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "arch": arch,
                "buildTime": build_time,
                "gitCommit": git_commit,
                "goVersion": go_version,
                "lastUpgrade": last_upgrade,
                "os": os,
                "startedAt": started_at,
                "status": status,
                "upgradeCount": upgrade_count,
                "uptime": uptime,
                "uptimeSeconds": uptime_seconds,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.upgrade_status import UpgradeStatus

        if not src_dict:
            return None
        d = src_dict.copy()
        arch = d.pop("arch")

        build_time = d.pop("buildTime") if "buildTime" in d else d.pop("build_time")

        git_commit = d.pop("gitCommit") if "gitCommit" in d else d.pop("git_commit")

        go_version = d.pop("goVersion") if "goVersion" in d else d.pop("go_version")

        last_upgrade = UpgradeStatus.from_dict(
            d.pop("lastUpgrade") if "lastUpgrade" in d else d.pop("last_upgrade")
        )

        os = d.pop("os")

        started_at = d.pop("startedAt") if "startedAt" in d else d.pop("started_at")

        status = d.pop("status")

        upgrade_count = d.pop("upgradeCount") if "upgradeCount" in d else d.pop("upgrade_count")

        uptime = d.pop("uptime")

        uptime_seconds = d.pop("uptimeSeconds") if "uptimeSeconds" in d else d.pop("uptime_seconds")

        version = d.pop("version")

        health_response = cls(
            arch=arch,
            build_time=build_time,
            git_commit=git_commit,
            go_version=go_version,
            last_upgrade=last_upgrade,
            os=os,
            started_at=started_at,
            status=status,
            upgrade_count=upgrade_count,
            uptime=uptime,
            uptime_seconds=uptime_seconds,
            version=version,
        )

        health_response.additional_properties = d
        return health_response

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

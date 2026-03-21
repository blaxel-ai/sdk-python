from enum import Enum


class WorkspaceUserSource(str, Enum):
    DIRECTORY_SYNC = "directory_sync"
    DOMAIN_CAPTURE = "domain_capture"
    INVITATION = "invitation"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "WorkspaceUserSource | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

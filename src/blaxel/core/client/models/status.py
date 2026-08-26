from enum import Enum


class Status(str, Enum):
    ARCHIVED = "ARCHIVED"
    ARCHIVING = "ARCHIVING"
    BUILDING = "BUILDING"
    BUILT = "BUILT"
    DEACTIVATED = "DEACTIVATED"
    DEACTIVATING = "DEACTIVATING"
    DELETING = "DELETING"
    DEPLOYED = "DEPLOYED"
    DEPLOYING = "DEPLOYING"
    FAILED = "FAILED"
    TERMINATED = "TERMINATED"
    UNARCHIVING = "UNARCHIVING"
    UPLOADING = "UPLOADING"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "Status | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

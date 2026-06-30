from enum import Enum


class DrivePermissionMode(str, Enum):
    READ = "read"
    READ_WRITE = "read-write"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "DrivePermissionMode | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

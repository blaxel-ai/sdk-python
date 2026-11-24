from enum import Enum


class SecretStatus(str, Enum):
    DEGRADED = "DEGRADED"
    DELETING = "DELETING"
    PENDING = "PENDING"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "SecretStatus | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

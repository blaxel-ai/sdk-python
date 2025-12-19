from enum import Enum


class VolumeTemplateStateStatus(str, Enum):
    CREATED = "created"
    ERROR = "error"
    READY = "ready"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "VolumeTemplateStateStatus | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

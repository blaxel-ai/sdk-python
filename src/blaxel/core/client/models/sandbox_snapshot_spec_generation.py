from enum import Enum


class SandboxSnapshotSpecGeneration(str, Enum):
    MK2 = "mk2"
    MK3 = "mk3"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "SandboxSnapshotSpecGeneration | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

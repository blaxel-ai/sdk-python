from enum import Enum


class ArchiveQuiesceState(str, Enum):
    ACTIVE = "active"
    QUIESCED = "quiesced"
    QUIESCING = "quiescing"
    RESTORING = "restoring"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "ArchiveQuiesceState | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

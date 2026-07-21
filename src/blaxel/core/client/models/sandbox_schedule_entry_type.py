from enum import Enum


class SandboxScheduleEntryType(str, Enum):
    AT = "at"
    CRON = "cron"
    SLEEP = "sleep"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "SandboxScheduleEntryType | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

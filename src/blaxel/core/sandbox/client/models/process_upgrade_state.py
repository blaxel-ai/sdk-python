from enum import Enum


class ProcessUpgradeState(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    IDLE = "idle"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "ProcessUpgradeState | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

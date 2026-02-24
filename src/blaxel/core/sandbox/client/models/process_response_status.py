from enum import Enum


class ProcessResponseStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    KILLED = "killed"
    RUNNING = "running"
    STOPPED = "stopped"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "ProcessResponseStatus | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

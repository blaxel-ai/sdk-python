from enum import Enum


class JobExecutionTaskStatus(str, Enum):
    CANCELLED = "cancelled"
    FAILED = "failed"
    PENDING = "pending"
    RECONCILING = "reconciling"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    UNSPECIFIED = "unspecified"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "JobExecutionTaskStatus | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

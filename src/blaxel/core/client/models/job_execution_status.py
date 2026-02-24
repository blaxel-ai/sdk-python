from enum import Enum


class JobExecutionStatus(str, Enum):
    CANCELLED = "cancelled"
    CANCELLING = "cancelling"
    FAILED = "failed"
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    TIMEOUT = "timeout"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "JobExecutionStatus | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

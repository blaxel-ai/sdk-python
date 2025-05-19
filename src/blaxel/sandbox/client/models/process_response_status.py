from enum import Enum


class ProcessResponseStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    KILLED = "killed"
    RUNNING = "running"
    STOPPED = "stopped"

    def __str__(self) -> str:
        return str(self.value)

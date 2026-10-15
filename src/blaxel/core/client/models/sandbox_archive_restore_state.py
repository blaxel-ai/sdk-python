from enum import Enum


class SandboxArchiveRestoreState(str, Enum):
    DOWNLOADING = "downloading"
    EXTRACTING = "extracting"
    FAILED = "failed"
    RELAUNCHING = "relaunching"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "SandboxArchiveRestoreState | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

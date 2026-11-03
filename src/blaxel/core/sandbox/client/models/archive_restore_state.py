from enum import Enum


class ArchiveRestoreState(str, Enum):
    RESTORE_DOWNLOADING = "downloading"
    RESTORE_EXTRACTING = "extracting"
    RESTORE_FAILED = "failed"
    RESTORE_RELAUNCHING = "relaunching"
    RESTORE_SUCCEEDED = "succeeded"
    DOWNLOADING = "downloading"
    EXTRACTING = "extracting"
    FAILED = "failed"
    RELAUNCHING = "relaunching"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "ArchiveRestoreState | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

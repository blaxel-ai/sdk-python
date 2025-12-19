from enum import Enum


class WorkspaceStatus(str, Enum):
    ACCOUNT_BINDED = "account_binded"
    ACCOUNT_CONFIGURED = "account_configured"
    CREATED = "created"
    ERROR = "error"
    READY = "ready"
    WORKSPACE_CONFIGURED = "workspace_configured"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "WorkspaceStatus | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

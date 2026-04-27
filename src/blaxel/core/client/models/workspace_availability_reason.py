from enum import Enum


class WorkspaceAvailabilityReason(str, Enum):
    FORBIDDEN_BLAXEL = "forbidden_blaxel"
    FORBIDDEN_RESERVED = "forbidden_reserved"
    FORBIDDEN_V_PREFIX = "forbidden_v_prefix"
    TAKEN = "taken"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "WorkspaceAvailabilityReason | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

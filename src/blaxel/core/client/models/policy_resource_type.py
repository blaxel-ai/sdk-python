from enum import Enum


class PolicyResourceType(str, Enum):
    AGENT = "agent"
    FUNCTION = "function"
    MODEL = "model"
    SANDBOX = "sandbox"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "PolicyResourceType | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

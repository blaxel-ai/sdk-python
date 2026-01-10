from enum import Enum


class ExpirationPolicyAction(str, Enum):
    DELETE = "delete"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "ExpirationPolicyAction | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

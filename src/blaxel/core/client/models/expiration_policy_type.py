from enum import Enum


class ExpirationPolicyType(str, Enum):
    DATE = "date"
    TTL_IDLE = "ttl-idle"
    TTL_MAX_AGE = "ttl-max-age"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "ExpirationPolicyType | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

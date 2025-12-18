from enum import Enum


class PolicySpecType(str, Enum):
    FLAVOR = "flavor"
    LOCATION = "location"
    MAXTOKEN = "maxToken"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "PolicySpecType | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

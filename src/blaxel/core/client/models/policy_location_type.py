from enum import Enum


class PolicyLocationType(str, Enum):
    CONTINENT = "continent"
    COUNTRY = "country"
    LOCATION = "location"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "PolicyLocationType | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

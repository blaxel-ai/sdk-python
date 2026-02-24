from enum import Enum


class EgressIPSpecIpFamily(str, Enum):
    IPV4 = "IPv4"
    IPV6 = "IPv6"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "EgressIPSpecIpFamily | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

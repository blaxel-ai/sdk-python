from enum import Enum


class PortProtocol(str, Enum):
    HTTP = "HTTP"
    TCP = "TCP"
    UDP = "UDP"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "PortProtocol | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

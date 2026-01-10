from enum import Enum


class FunctionSpecTransport(str, Enum):
    HTTP_STREAM = "http-stream"
    WEBSOCKET = "websocket"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "FunctionSpecTransport | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

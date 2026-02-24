from enum import Enum


class FunctionRuntimeTransport(str, Enum):
    HTTP_STREAM = "http-stream"
    WEBSOCKET = "websocket"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "FunctionRuntimeTransport | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

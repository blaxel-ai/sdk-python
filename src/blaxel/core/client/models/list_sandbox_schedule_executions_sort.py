from enum import Enum


class ListSandboxScheduleExecutionsSort(str, Enum):
    CREATEDATASC = "createdAt:asc"
    CREATEDATDESC = "createdAt:desc"
    NAMEASC = "name:asc"
    NAMEDESC = "name:desc"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "ListSandboxScheduleExecutionsSort | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

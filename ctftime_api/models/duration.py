from dataclasses import dataclass

from dataclasses_json import Undefined, dataclass_json

__all__ = ["Duration"]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class Duration:
    hours: int
    days: int

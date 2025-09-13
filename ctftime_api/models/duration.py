from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin, Undefined, dataclass_json

__all__ = ["Duration"]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class Duration(DataClassJsonMixin):
    hours: int
    days: int

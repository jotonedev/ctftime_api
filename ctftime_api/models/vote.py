from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import DataClassJsonMixin, Undefined, dataclass_json

__all__ = ["Vote"]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class Vote(DataClassJsonMixin):
    event_id: int
    user_id: int
    user_teams: list[int]  # list of team IDs
    weight: str
    creation_date: datetime

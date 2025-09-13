from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import DataClassJsonMixin, Undefined, dataclass_json
from yarl import URL

from .duration import Duration
from .team import BaseTeam, TeamResult

__all__ = ["Event", "EventResult"]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class Event(DataClassJsonMixin):
    """Represents a CTF event."""

    organizers: list[BaseTeam]
    ctftime_url: URL
    ctf_id: int
    weight: float
    duration: Duration
    live_feed: str
    logo: URL | str
    id: int
    title: str
    participants: int
    location: str
    description: str
    format: str
    is_votable_now: bool
    prizes: str
    restrictions: str
    url: URL | str
    public_votable: bool
    start: datetime | str
    finish: datetime | str

    def __post_init__(self):
        if isinstance(self.start, str):
            object.__setattr__(self, "start", datetime.fromisoformat(self.start))
        if isinstance(self.finish, str):
            object.__setattr__(self, "finish", datetime.fromisoformat(self.finish))


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class EventResult(DataClassJsonMixin):
    """Represents a CTF event result."""

    title: str
    time: datetime
    scores: list[TeamResult]

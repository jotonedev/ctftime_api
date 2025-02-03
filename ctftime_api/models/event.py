from pydantic import BaseModel, HttpUrl
from datetime import datetime


from .duration import Duration
from .team import BaseTeam, TeamResult

__all__ = ["Event", "EventResult"]


class Event(BaseModel):
    """Represents a CTF event."""

    organizers: list[BaseTeam]
    ctftime_url: HttpUrl
    ctf_id: int
    weight: float
    duration: Duration
    live_feed: str
    logo: HttpUrl | str
    id: int
    title: str
    start: datetime
    participants: int
    location: str
    finish: datetime
    description: str
    format: str
    is_votable_now: bool
    prizes: str
    restrictions: str
    url: HttpUrl | str
    public_votable: bool


class EventResult(BaseModel):
    """Represents a CTF event result."""

    ctf_id: int
    title: str
    time: datetime
    scores: list[TeamResult]

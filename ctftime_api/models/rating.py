from dataclasses import dataclass

from dataclasses_json import Undefined, dataclass_json

__all__ = ["Rating"]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class Rating:
    """Represents a CTF team rating."""

    rating_place: int | None = None
    organizer_points: float | None = None
    rating_points: float | None = None
    country_place: int | None = None

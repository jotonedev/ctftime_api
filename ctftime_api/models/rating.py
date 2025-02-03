from pydantic import BaseModel

__all__ = ["Rating"]


class Rating(BaseModel):
    """Represents a CTF team rating."""

    rating_place: int | None = None
    organizer_points: float | None = None
    rating_points: float | None = None
    country_place: int | None = None

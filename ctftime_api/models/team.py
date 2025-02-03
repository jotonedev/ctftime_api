from dataclasses import field

from pydantic import Field, BaseModel, HttpUrl, AliasChoices
from pydantic_extra_types.country import CountryAlpha2

from .rating import Rating


__all__ = ["BaseTeam", "Team", "TeamRank", "TeamComplete", "TeamResult"]


class BaseTeam(BaseModel):
    """Represents a CTF team. Contains only the minimal information."""

    id: int = Field(validation_alias=AliasChoices("team_id", "id"))
    name: str = Field(validation_alias=AliasChoices("team_name", "name"))


class Team(BaseTeam):
    """Represents a CTF team"""

    country: CountryAlpha2 | None = Field(None, validation_alias="team_country")
    academic: bool = False
    aliases: list[str] = Field(default_factory=list)


class TeamRank(BaseTeam):
    """Represents a CTF team in the leaderboard"""

    points: float
    country_place: int | None = None
    place: int | None = None
    events: int | None = None


class TeamResult(BaseModel):
    """Represents a CTF team result"""

    team_id: int
    points: float
    place: int


class TeamComplete(Team):
    """Represents a CTF team with complete information"""

    primary_alias: str
    logo: HttpUrl | str | None = None
    university: str | None = None
    university_website: HttpUrl | str | None = None
    rating: dict[int, Rating | None] = field(default_factory=dict)

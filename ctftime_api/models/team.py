from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, Undefined, config, dataclass_json
from yarl import URL

from .country import CountryCode
from .rating import Rating

__all__ = ["BaseTeam", "Team", "TeamRank", "TeamComplete", "TeamResult"]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class BaseTeam(DataClassJsonMixin):
    """Represents a CTF team. Contains only the minimal information."""

    team_id: int = field(metadata=config(field_name="id"))
    team_name: str = field(metadata=config(field_name="name"))


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class Team(BaseTeam):
    """Represents a CTF team"""

    team_country: CountryCode | None = None
    academic: bool = False
    aliases: list[str] = field(default_factory=list)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class TeamRank(BaseTeam):
    """Represents a CTF team in the leaderboard"""

    points: float
    country_place: int | None = None
    place: int | None = None
    events: int | None = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class TeamResult(DataClassJsonMixin):
    """Represents a CTF team result"""

    team_id: int
    points: float
    place: int


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class TeamComplete(Team):
    """Represents a CTF team with complete information"""

    primary_alias: str | None = None
    logo: URL | str | None = None
    university: str | None = None
    university_website: URL | str | None = None
    rating: dict[int, Rating | None] = field(default_factory=dict)

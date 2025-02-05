from datetime import datetime

from pydantic import BaseModel


__all__ = ["Vote"]


class Vote(BaseModel):
    event_id: int
    user_id: int
    user_teams: list[int]  # list of team IDs
    weight: str
    creation_date: datetime

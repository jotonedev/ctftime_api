from pydantic import BaseModel


__all__ = ["Duration"]


class Duration(BaseModel):
    hours: int
    days: int

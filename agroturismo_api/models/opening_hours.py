import enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Weekday(int, enum.Enum):
    sunday: int = 0
    monday: int = 1
    tuesday: int = 2
    wednesday: int = 3
    thursday: int = 4
    friday: int = 5
    saturday: int = 6


class OpeningHoursBase(SQLModel):
    local_id: int = Field(default=None, foreign_key="local.id")
    weekday: int = Field(default=None)  # TODO: try to use the Weekday enum
    is_closed: bool = Field(default=False)
    start_time: Optional[str] = Field(default=None)
    end_time: Optional[str] = Field(default=None)
    start_pause_time: Optional[str] = Field(default=None)
    end_pause_time: Optional[str] = Field(default=None)


class OpeningHours(OpeningHoursBase, table=True):
    __tablename__ = "opening_hours"

    id: Optional[int] = Field(default=None, primary_key=True)


class OpeningHoursCreate(OpeningHoursBase):
    pass

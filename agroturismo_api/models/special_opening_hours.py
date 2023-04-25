from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class SpecialOpeningHoursBase(SQLModel):
    local_id: int = Field(default=None, foreign_key="local.id")
    opening_date: date = Field(default=None)
    description: str = Field(default=None)
    is_closed: bool = Field(default=False)
    start_time: Optional[str] = Field(default=None)
    end_time: Optional[str] = Field(default=None)
    start_pause_time: Optional[str] = Field(default=None)
    end_pause_time: Optional[str] = Field(default=None)


class SpecialOpeningHours(SpecialOpeningHoursBase, table=True):
    __tablename__ = "special_opening_hours"

    id: Optional[int] = Field(default=None, primary_key=True)


class SpecialOpeningHoursCreate(SpecialOpeningHoursBase):
    pass

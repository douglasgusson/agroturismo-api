from typing import Optional

from sqlmodel import Field, SQLModel


class TouristBase(SQLModel):
    name: str
    email: str


class Tourist(TouristBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str


class TouristCreate(TouristBase):
    pass


class TouristRead(TouristBase):
    id: int

from typing import Optional

from sqlmodel import Field, SQLModel


class CostBase(SQLModel):
    local_origin_id: Optional[int] = Field(
        default=None, foreign_key="local.id", primary_key=True
    )
    local_destination_id: Optional[int] = Field(
        default=None, foreign_key="local.id", primary_key=True
    )
    distance: float = Field(default=None)  # in km
    duration: int = Field(default=None)  # in minutes


class Cost(CostBase, table=True):
    __tablename__ = "cost"


class CostRead(CostBase):
    pass

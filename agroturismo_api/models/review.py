from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ReviewBase(SQLModel):
    content: str = Field(default=None)
    rating: int = Field(default=None)
    local_id: int = Field(default=None, foreign_key="local.id")
    created_at: datetime = Field(default_factory=datetime.now)


class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tourist_id: int = Field(default=None, foreign_key="tourist.id")


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    pass

from typing import Optional

from sqlmodel import Field, SQLModel


class TagBase(SQLModel):
    content: str


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int

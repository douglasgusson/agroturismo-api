from typing import Optional

from sqlmodel import Field, SQLModel


class TagLocal(SQLModel, table=True):
    __tablename__ = "tag_local"

    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    local_id: Optional[int] = Field(
        default=None, foreign_key="local.id", primary_key=True
    )

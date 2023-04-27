from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .local import Local


class CategoryBase(SQLModel):
    name: str
    slug: str = Field(unique=True, index=True)


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    locals: Optional["Local"] = Relationship(back_populates="main_category")


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int

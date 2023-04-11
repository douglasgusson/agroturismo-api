from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .category import Category, CategoryRead
    from .gallery_local import GalleryLocal


class LocalBase(SQLModel):
    name: str
    slug: str
    latitude: float
    longitude: float
    description: str
    main_category_id: Optional[int] = Field(default=None, foreign_key="category.id")


class Local(LocalBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    main_category: Optional["Category"] = Relationship(back_populates="locals")
    images: Optional["GalleryLocal"] = Relationship(back_populates="local")


class LocalCreate(LocalBase):
    pass


class LocalRead(LocalBase):
    id: int
